# full_node_injection_and_statistics_gnn_ranks.py
# 两阶段故障注入与统计脚本
# 阶段1：对网表所有节点进行故障注入，保存测试结果
# 阶段2：根据保存的结果，对不同gnn_rank文件的覆盖率进行统计
# 使用 gnn_ranks 目录（文件名格式：gnn_rank_{topk}.txt）

import os
import re
import csv
import time
import json
import subprocess
from typing import List, Tuple, Set, Dict
import glob
from collections import defaultdict

## ===== 基本配置 =====
VERILOG_SRC = 'pe.synth_dct.v'    # 网表
TB_FILE     = 'tb_1.v'              # testbench
CELL_LIB    = 'cells.v'           # 工艺库
RANK_DIR    = 'gnn_ranks_1'          # 存放多个 gnn_rank_xxx.txt 的目录

# 日志&临时文件目录
LOGDIR = 'sim_logs_full_injection'
os.makedirs(LOGDIR, exist_ok=True)

# 全节点注入结果保存目录
RESULTS_DIR = 'full_injection_results'
os.makedirs(RESULTS_DIR, exist_ok=True)

# 注入时序配置
INJECT_DELAY_CYCLES = 5
MAX_VVP_SECONDS     = 60

# 输出匹配模式
OSUM_HEX_RE = re.compile(r'^o_sum=([0-9a-fA-FxzXZ]+)')

# 允许的未知比例
MAX_UNKNOWN_RATIO = 0.2


# ========== 工具函数 ==========

def run_cmd(cmd: List[str], capture=False, timeout=None) -> Tuple[int, str]:
    """执行命令，在 Windows 下用 UTF-8 并忽略不能解码的字符"""
    if capture:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, encoding='utf-8', errors='ignore')
        try:
            out, _ = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            return -1, 'TIMEOUT'
        return proc.returncode, out
    else:
        try:
            rc = subprocess.call(cmd)
            return rc, ''
        except Exception as e:
            return -1, str(e)


def strip_comments(text: str) -> str:
    """去除 Verilog 注释"""
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    text = re.sub(r'//.*', '', text)
    return text


def extract_module(text: str, modname: str) -> str:
    """提取模块定义"""
    m = re.search(rf'\bmodule\s+{re.escape(modname)}\b.*?\bendmodule\b', text, flags=re.DOTALL)
    return m.group(0) if m else ''


def split_decl_names(decl_body: str) -> List[str]:
    """拆分声明中的信号名"""
    out = []
    decl_body = re.sub(r'\[[^]\n]*:[^]\n]*\]', '', decl_body)
    for chunk in decl_body.split(','):
        token = chunk.strip()
        if not token:
            continue
        m = re.match(r'^([A-Za-z_][A-Za-z0-9_$]*)(\[\d+\])?$', token)
        if m:
            out.append(m.group(0))
    return out


def parse_ports(module_text: str) -> Tuple[Set[str], Set[str], Set[str]]:
    """解析模块的输入、输出、双向端口"""
    inputs, outputs, inouts = set(), set(), set()
    for stmt in module_text.split(';'):
        s = stmt.strip()
        if not s: continue
        if re.match(r'^\binput\b', s):
            body = re.sub(r'^\binput\b\s+((?:wire|reg|logic|signed|unsigned)\s+)*', '', s)
            inputs.update(split_decl_names(body))
        elif re.match(r'^\boutput\b', s):
            body = re.sub(r'^\boutput\b\s+((?:wire|reg|logic|signed|unsigned)\s+)*', '', s)
            outputs.update(split_decl_names(body))
        elif re.match(r'^\binout\b', s):
            body = re.sub(r'^\binout\b\s+((?:wire|reg|logic|signed|unsigned)\s+)*', '', s)
            inouts.update(split_decl_names(body))
    return inputs, outputs, inouts


def parse_internal_nets(module_text: str) -> Set[str]:
    """解析模块内部的 wire/reg 信号"""
    nets = set()
    for stmt in module_text.split(';'):
        s = stmt.strip()
        if not s: continue
        if re.match(r'^(wire|reg|logic)\b', s):
            body = re.sub(r'^(wire|reg|logic)\b\s+((?:signed|unsigned)\s+)?', '', s)
            nets.update(split_decl_names(body))
    return nets


def parse_targets_from_netlist(netlist_text: str, dut_module: str = 'pe') -> List[str]:
    """
    解析可注入目标：输出端口 ∪ 内部 nets − 输入端口
    仅保留可 force 的合法名字（ID 或 ID[NUM]）
    """
    text = strip_comments(netlist_text)
    mod = extract_module(text, dut_module)
    if not mod:
        mod = text
    inputs, outputs, _ = parse_ports(mod)
    internals = parse_internal_nets(mod)
    targets = (outputs | internals) - inputs

    good = []
    for n in sorted(targets):
        if re.match(r'^[A-Za-z_][A-Za-z0-9_$]*$', n) or re.match(r'^[A-Za-z_][A-Za-z0-9_$]*\[\d+\]$', n):
            good.append(n)
    return good


def make_injected_tb(tb_text: str, target_net: str, stuck: int) -> str:
    """生成带故障注入的 testbench"""
    inj_block = f"""
// --- fault injection block (auto) ---
initial begin : __fi_block
    wait (reset == 0);
    repeat({INJECT_DELAY_CYCLES}) @(posedge clock);
    force uut.{target_net} = 1'b{stuck};
    $display("FAULT_INJECTED: {target_net} sa{stuck}");
end
// --- end injection block ---
"""
    idx = tb_text.rfind('endmodule')
    if idx == -1:
        return tb_text + '\n' + inj_block
    else:
        return tb_text[:idx] + inj_block + tb_text[idx:]


def compile_and_run(sources: List[str], exe_path: str, vcd_path: str, log_path: str,
                    timeout: int = MAX_VVP_SECONDS) -> bool:
    """
    Icarus Verilog 编译和运行流程
    返回 True/False 表示成功/失败
    """
    # 编译
    cmd_compile = ['iverilog', '-g2012', '-o', exe_path] + [os.path.abspath(s) for s in sources]
    rc, out = run_cmd(cmd_compile, capture=True)
    if rc != 0:
        with open(log_path, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(out)
        return False

    # 运行
    cmd_run = ['vvp', exe_path, f'+DUMPFILE={vcd_path}']
    with open(log_path, 'w', encoding='utf-8', errors='ignore') as f:
        try:
            proc = subprocess.Popen(cmd_run, stdout=f, stderr=subprocess.STDOUT,
                                    text=True, encoding='utf-8', errors='ignore')
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            f.write('\n[ERROR] vvp TIMEOUT\n')
            return False

    return True


def parse_osum_as_ints(logfile: str) -> Tuple[List[int], float]:
    """从日志文件中解析 o_sum 输出值"""
    vals, total, unknown = [], 0, 0
    try:
        with open(logfile, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                m = OSUM_HEX_RE.match(line.strip())
                if not m:
                    continue
                total += 1
                s = m.group(1).lower()
                if 'x' in s or 'z' in s:
                    unknown += 1
                    continue
                try:
                    vals.append(int(s, 16))
                except ValueError:
                    unknown += 1
    except Exception as e:
        print(f'⚠️ 读取 {logfile} 失败: {e}')
    unk_ratio = (unknown / total) if total > 0 else 1.0
    return vals, unk_ratio


def load_gnn_topk(path: str, topk: int) -> List[str]:
    """从 gnn_rank 文件中读取前 topk 个节点"""
    if not os.path.exists(path):
        print(f'❌ 未找到 {path}')
        return []
    nodes = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            parts = line.split()
            if len(parts) >= 1:
                nodes.append(parts[0])
    return nodes[:topk]


def extract_topk(filename: str) -> int:
    """从文件名提取 TopK 数字，例如 gnn_rank_50.txt -> 50"""
    # 支持格式：gnn_rank_50.txt
    m = re.search(r'gnn_rank_(\d+)\.txt', filename)
    if m:
        return int(m.group(1))
    # 也支持 gnn_rank_all.txt 格式
    m2 = re.search(r'gnn_rank_all\.txt', filename)
    if m2:
        return float('inf')  # 表示全部节点
    return float('inf')


# ========== 阶段1：全节点注入 ==========

def phase1_full_node_injection():
    """
    阶段1：对网表所有节点进行故障注入测试，并保存每个节点的测试结果
    返回：golden 值列表和全节点测试结果字典
    """
    print('\n' + '='*70)
    print('阶段1：全节点故障注入测试')
    print('='*70)
    
    t0_phase1 = time.time()
    
    # 1) 生成 golden 基准
    print('\n[1/3] 运行 golden 仿真（无故障基准）...')
    golden_exe = os.path.join(LOGDIR, 'golden.out')
    golden_vcd = os.path.join(LOGDIR, 'golden.vcd')
    golden_log = os.path.join(LOGDIR, 'golden.log')
    ok = compile_and_run([CELL_LIB, VERILOG_SRC, TB_FILE],
                         golden_exe, golden_vcd, golden_log,
                         timeout=MAX_VVP_SECONDS)
    if not ok:
        print('❌ Golden 仿真失败')
        with open(golden_log, 'r', encoding='utf-8', errors='ignore') as f:
            print(f.read())
        return None, None
    
    golden_vals, golden_unk = parse_osum_as_ints(golden_log)
    if not golden_vals:
        print('❌ golden.log 没有有效的 o_sum 样本')
        return None, None
    print(f'✅ Golden 样本数: {len(golden_vals)}, Unknown比例: {golden_unk:.2%}')
    
    # 保存 golden 结果
    golden_result_file = os.path.join(RESULTS_DIR, 'golden_result.json')
    with open(golden_result_file, 'w', encoding='utf-8') as f:
        json.dump({
            'values': golden_vals,
            'unknown_ratio': golden_unk,
            'sample_count': len(golden_vals)
        }, f, indent=2)
    print(f'✅ Golden 结果已保存: {golden_result_file}')
    
    # 2) 解析所有可注入的合法节点
    print('\n[2/3] 解析网表中的可注入节点...')
    with open(VERILOG_SRC, 'r', encoding='utf-8', errors='ignore') as f:
        net_text = f.read()
    all_targets = parse_targets_from_netlist(net_text, dut_module='pe')
    
    # 过滤掉时钟和复位信号
    legal_targets = [n for n in all_targets 
                     if not re.match(r'^(clk|clock|rst|reset)', n, flags=re.IGNORECASE)]
    
    print(f'✅ 共找到 {len(legal_targets)} 个可注入节点（已过滤时钟和复位信号）')
    
    # 保存节点列表
    nodes_list_file = os.path.join(RESULTS_DIR, 'all_nodes.txt')
    with open(nodes_list_file, 'w', encoding='utf-8') as f:
        for node in legal_targets:
            f.write(f'{node}\n')
    print(f'✅ 节点列表已保存: {nodes_list_file}')
    
    # 3) 对每个节点进行 SA0 和 SA1 注入
    print('\n[3/3] 开始全节点注入测试...')
    print(f'总共需要测试: {len(legal_targets)} 个节点 × 2 种故障类型 = {len(legal_targets)*2} 次仿真')
    
    tb_src = open(TB_FILE, 'r', encoding='utf-8', errors='ignore').read()
    
    # 存储每个节点的测试结果
    node_results = {}  # {node_name: {'sa0': {...}, 'sa1': {...}}}
    
    total_tests = len(legal_targets) * 2
    current_test = 0
    
    for i, net in enumerate(legal_targets, 1):
        node_results[net] = {'sa0': None, 'sa1': None}
        
        for val in [0, 1]:
            current_test += 1
            fault_type = f'sa{val}'
            
            # 显示进度
            if current_test % 100 == 0 or current_test == total_tests:
                elapsed = time.time() - t0_phase1
                progress = current_test / total_tests * 100
                print(f'  进度: [{current_test}/{total_tests}] ({progress:.1f}%) '
                      f'当前节点: {net} {fault_type} - 已用时: {elapsed:.1f}s')
            
            # 生成注入 testbench
            tb_inj = make_injected_tb(tb_src, net, val)
            tb_tmp = os.path.join(LOGDIR, f'tb_inj_{i}_{fault_type}.v')
            with open(tb_tmp, 'w', encoding='utf-8', errors='ignore') as w:
                w.write(tb_inj)
            
            # 编译和运行
            exe = os.path.join(LOGDIR, f'sim_{i}_{fault_type}.out')
            vcd = os.path.join(LOGDIR, f'sim_{i}_{fault_type}.vcd')
            log = os.path.join(LOGDIR, f'sim_{i}_{fault_type}.log')
            
            ok = compile_and_run([CELL_LIB, VERILOG_SRC, tb_tmp], 
                                exe, vcd, log, timeout=MAX_VVP_SECONDS)
            
            if not ok:
                node_results[net][fault_type] = {
                    'status': 'compile_fail',
                    'detected': False,
                    'values': [],
                    'unknown_ratio': 1.0
                }
                continue
            
            # 解析结果
            vals, unk = parse_osum_as_ints(log)
            
            if not vals or unk > MAX_UNKNOWN_RATIO:
                node_results[net][fault_type] = {
                    'status': 'invalid_output',
                    'detected': False,
                    'values': vals,
                    'unknown_ratio': unk
                }
                continue
            
            # 对比 golden 值判断是否检测到故障
            L = min(len(golden_vals), len(vals))
            diff_count = sum(1 for a, b in zip(golden_vals[:L], vals[:L]) if a != b)
            detected = diff_count > 0
            
            node_results[net][fault_type] = {
                'status': 'success',
                'detected': detected,
                'diff_count': diff_count,
                'sample_count': L,
                'values': vals,
                'unknown_ratio': unk
            }
            
            # 清理临时文件（保留 log，删除 exe 和 vcd）
            try:
                if os.path.exists(tb_tmp):
                    os.remove(tb_tmp)
                if os.path.exists(exe):
                    os.remove(exe)
                if os.path.exists(vcd):
                    os.remove(vcd)
            except Exception as e:
                pass
    
    # 保存完整测试结果
    results_file = os.path.join(RESULTS_DIR, 'full_injection_results.json')
    print(f'\n保存测试结果到: {results_file}')
    with open(results_file, 'w', encoding='utf-8') as f:
        # 由于结果可能很大，不保存具体的 values，只保存检测状态
        simplified_results = {}
        for node, faults in node_results.items():
            simplified_results[node] = {
                'sa0': {k: v for k, v in faults['sa0'].items() if k != 'values'} if faults['sa0'] else None,
                'sa1': {k: v for k, v in faults['sa1'].items() if k != 'values'} if faults['sa1'] else None
            }
        json.dump(simplified_results, f, indent=2)
    
    # 统计汇总
    total_nodes = len(legal_targets)
    total_faults = total_nodes * 2
    detected_nodes = 0
    detected_faults = 0
    
    for node, faults in node_results.items():
        node_detected = False
        for fault_type in ['sa0', 'sa1']:
            if faults[fault_type] and faults[fault_type].get('detected', False):
                detected_faults += 1
                node_detected = True
        if node_detected:
            detected_nodes += 1
    
    elapsed_phase1 = time.time() - t0_phase1
    
    print('\n' + '='*70)
    print('阶段1 完成 - 全节点注入测试统计')
    print('='*70)
    print(f'总测试节点数: {total_nodes}')
    print(f'总测试故障数: {total_faults}')
    print(f'检测到的节点数: {detected_nodes} ({detected_nodes/total_nodes*100:.2f}%)')
    print(f'检测到的故障数: {detected_faults} ({detected_faults/total_faults*100:.2f}%)')
    print(f'\n阶段1总用时: {elapsed_phase1:.2f}s')
    print('='*70)
    
    return golden_vals, node_results


# ========== 阶段2：基于保存结果的覆盖率统计 ==========

def phase2_coverage_statistics(golden_vals: List[int], node_results: Dict):
    """
    阶段2：根据保存的全节点测试结果，对不同 gnn_rank 文件的覆盖率进行统计
    gnn_ranks 目录下的文件格式：gnn_rank_{topk}.txt（没有 run 后缀）
    """
    print('\n' + '='*70)
    print('阶段2：基于全节点结果的覆盖率统计')
    print('='*70)
    
    t0_phase2 = time.time()
    
    # 1) 查找所有 gnn_rank 文件
    print('\n[1/2] 查找 gnn_rank 文件...')
    rank_files = glob.glob(os.path.join(RANK_DIR, "gnn_rank_*.txt"))
    if not rank_files:
        print(f'❌ {RANK_DIR} 下没有 gnn_rank_*.txt 文件')
        return
    
    # 按 topk 分组
    files_by_topk = {}  # {topk: [filepath]}
    for filepath in rank_files:
        filename = os.path.basename(filepath)
        topk = extract_topk(filename)
        if topk != float('inf'):
            if topk not in files_by_topk:
                files_by_topk[topk] = []
            files_by_topk[topk].append(filepath)
    
    # 输出统计信息
    for topk, files in sorted(files_by_topk.items()):
        print(f'  TopK={topk}: 找到 {len(files)} 个排名文件')
    
    if not files_by_topk:
        print('❌ 没有找到有效的排名文件')
        return
    
    # 使用 files_by_topk 的 key 确保一致性
    topk_list = sorted(files_by_topk.keys())
    print(f'✅ 找到 {len(topk_list)} 个 topk 值: {topk_list}')
    
    # 2) 对每个 gnn_rank 文件统计覆盖率
    print('\n[2/2] 统计各 gnn_rank 文件的覆盖率...')
    
    results = []  # 列表，每个元素为 {'topk': x, ...} 的字典
    
    total_files = sum(len(files) for files in files_by_topk.values())
    current_file = 0
    
    for i, topk in enumerate(topk_list, 1):
        # 确保 topk 在 files_by_topk 中（应该总是在，但为了安全）
        if topk not in files_by_topk:
            print(f'⚠️ TopK={topk} 不在文件列表中，跳过')
            continue
        
        rank_files = files_by_topk[topk]
        
        for rank_file in sorted(rank_files):  # 对每个文件都统计
            current_file += 1
            filename = os.path.basename(rank_file)
            
            rank_tag = f'topk{topk}'
            
            # 读取 gnn_rank 文件中的节点列表
            # 由于文件本身已经包含 topk 个节点，直接读取全部
            gnn_nodes = load_gnn_topk(rank_file, topk=10**9)
            
            # 过滤：只保留在 node_results 中的节点
            filtered_nodes = [n for n in gnn_nodes if n in node_results]
            
            if not filtered_nodes:
                print(f'⚠️ [{current_file}/{total_files}] {rank_tag}: 没有匹配的节点，跳过')
                continue
            
            # 统计覆盖率
            detected_nodes = 0
            detected_faults = 0
            
            for node in filtered_nodes:
                node_detected = False
                for fault_type in ['sa0', 'sa1']:
                    fault_result = node_results[node].get(fault_type)
                    if fault_result and fault_result.get('detected', False):
                        detected_faults += 1
                        node_detected = True
                if node_detected:
                    detected_nodes += 1
            
            # 计算覆盖率
            total_faults = len(filtered_nodes) * 2
            node_cov = detected_nodes / len(filtered_nodes) * 100.0 if filtered_nodes else 0
            fault_cov = detected_faults / total_faults * 100.0 if total_faults else 0
            
            results.append({
                'topk': topk,
                'fault_cov': fault_cov,
                'node_cov': node_cov,
                'tested_nodes': len(filtered_nodes),
                'detected_nodes': detected_nodes,
                'detected_faults': detected_faults
            })
            
            if current_file % 50 == 0 or current_file == total_files:
                print(f'  [{current_file}/{total_files}] {rank_tag}: 节点={len(filtered_nodes)}, '
                      f'节点覆盖率={node_cov:.2f}%, 故障覆盖率={fault_cov:.2f}%')
    
    # 3) 保存统计结果到 CSV
    RESULT_CSV = os.path.join(RESULTS_DIR, 'coverage_statistics.csv')
    print(f'\n保存统计结果到: {RESULT_CSV}')
    
    with open(RESULT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # 写入列标题（去掉 run 列，因为 gnn_ranks 目录下的文件没有 run）
        header = ['topk', 'tested_nodes', 'fault_coverage(%)', 'node_coverage(%)', 'escaped_nodes', 'escaped_faults']
        writer.writerow(header)
        
        # 写入每个文件的数据（每行代表一个 topk 的文件）
        for result in results:
            tested_nodes = result['tested_nodes']
            detected_nodes = result['detected_nodes']
            detected_faults = result['detected_faults']
            
            # 计算逃逸节点和逃逸故障
            escaped_nodes = tested_nodes - detected_nodes
            injected_faults = tested_nodes * 2
            escaped_faults = injected_faults - detected_faults
            
            row = [
                result['topk'],
                tested_nodes,
                f"{result['fault_cov']:.2f}",
                f"{result['node_cov']:.2f}",
                str(escaped_nodes),
                str(escaped_faults)
            ]
            writer.writerow(row)
    
    elapsed_phase2 = time.time() - t0_phase2
    
    print('\n' + '='*70)
    print('阶段2 完成 - 覆盖率统计')
    print('='*70)
    print(f'统计的 topk 数量: {len(topk_list)}')
    print(f'TopK 范围: {min(topk_list)} - {max(topk_list)}')
    print(f'总文件数: {len(results)}')
    print(f'结果文件: {RESULT_CSV}')
    print(f'\n阶段2用时: {elapsed_phase2:.2f}s')
    print('='*70)


# ========== 主函数 ==========

def main():
    print('='*70)
    print('全节点故障注入与覆盖率统计工具 (使用 gnn_ranks 目录)')
    print('='*70)
    print(f'网表文件: {VERILOG_SRC}')
    print(f'Testbench: {TB_FILE}')
    print(f'工艺库: {CELL_LIB}')
    print(f'Rank 目录: {RANK_DIR}')
    print(f'结果目录: {RESULTS_DIR}')
    print('='*70)
    
    t0_total = time.time()
    
    # 检查结果文件是否已存在
    results_file = os.path.join(RESULTS_DIR, 'full_injection_results.json')
    golden_file = os.path.join(RESULTS_DIR, 'golden_result.json')
    
    if os.path.exists(results_file) and os.path.exists(golden_file):
        print('\n⚠️ 检测到已存在的全节点注入结果')
        user_input = input('是否跳过阶段1，直接使用现有结果进行统计？(y/n): ')
        if user_input.lower() == 'y':
            print('加载现有结果...')
            with open(golden_file, 'r', encoding='utf-8') as f:
                golden_data = json.load(f)
                golden_vals = golden_data['values']
            
            with open(results_file, 'r', encoding='utf-8') as f:
                node_results = json.load(f)
            
            print(f'✅ 已加载 {len(node_results)} 个节点的测试结果')
            
            # 直接进入阶段2
            phase2_coverage_statistics(golden_vals, node_results)
            
            elapsed_total = time.time() - t0_total
            print(f'\n⏱️ 总运行时间: {elapsed_total:.2f}s')
            return
    
    # 阶段1：全节点注入
    golden_vals, node_results = phase1_full_node_injection()
    
    if golden_vals is None or node_results is None:
        print('\n❌ 阶段1失败，程序终止')
        return
    
    # 阶段2：覆盖率统计
    phase2_coverage_statistics(golden_vals, node_results)
    
    elapsed_total = time.time() - t0_total
    
    print('\n' + '='*70)
    print('全部完成！')
    print('='*70)
    print(f'⏱️ 总运行时间: {elapsed_total:.2f}s')
    print(f'📁 结果保存在: {RESULTS_DIR}/')
    print('='*70)


if __name__ == '__main__':
    main()


