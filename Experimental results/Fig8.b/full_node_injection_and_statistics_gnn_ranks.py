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
import math

## ===== 基本配置 =====
VERILOG_SRC = 'pe.synth_dct.v'    # 网表
TB_FILE     = 'tb_1.v'              # testbench
CELL_LIB    = 'cells.v'           # 工艺库
RANK_DIR    = 'gnn_ranks'          # 存放多个 gnn_rank_xxx.txt 的目录

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


def calculate_rmse(golden_vals: List[int], faulty_vals: List[int]) -> Tuple[float, int]:
    """
    计算 RMSE (Root Mean Square Error) between golden and faulty outputs
    
    Args:
        golden_vals: Golden reference values
        faulty_vals: Faulty simulation values
    
    Returns:
        - RMSE value (float)
        - Number of valid comparison points
    """
    if not golden_vals or not faulty_vals:
        return float('nan'), 0
    
    # Use minimum length to ensure valid comparison
    n = min(len(golden_vals), len(faulty_vals))
    
    if n == 0:
        return float('nan'), 0
    
    # Calculate squared differences
    squared_diffs = [(float(g) - float(f)) ** 2 for g, f in zip(golden_vals[:n], faulty_vals[:n])]
    
    # Calculate mean squared error
    mse = sum(squared_diffs) / n
    
    # Calculate RMSE
    rmse = math.sqrt(mse)
    
    return rmse, n


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


def extract_topk(filename: str):
    """从文件名提取 TopK 数字，例如 gnn_rank_50.txt -> 50
    如果文件名是 gnn_rank.txt（没有下划线），返回 None
    """
    # 提取纯文件名（不含路径）
    basename = os.path.basename(filename)
    
    # 支持格式：gnn_rank_50.txt
    m = re.search(r'gnn_rank_(\d+)\.txt', basename)
    if m:
        return int(m.group(1))
    # 支持 gnn_rank_all.txt 格式
    m2 = re.search(r'gnn_rank_all\.txt', basename)
    if m2:
        return float('inf')  # 表示全部节点
    # 支持 gnn_rank.txt 格式（没有下划线）
    if basename == 'gnn_rank.txt':
        return None  # 表示普通排名文件，节点数未知
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
            
            # 计算 RMSE
            rmse, valid_points = calculate_rmse(golden_vals, vals)
            
            node_results[net][fault_type] = {
                'status': 'success',
                'detected': detected,
                'diff_count': diff_count,
                'sample_count': L,
                'values': vals,
                'unknown_ratio': unk,
                'rmse': rmse,
                'rmse_valid_points': valid_points
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
        # 由于结果可能很大，不保存具体的 values，只保存检测状态和RMSE
        simplified_results = {}
        for node, faults in node_results.items():
            simplified_results[node] = {
                'sa0': {k: v for k, v in faults['sa0'].items() if k != 'values'} if faults['sa0'] else None,
                'sa1': {k: v for k, v in faults['sa1'].items() if k != 'values'} if faults['sa1'] else None
            }
        json.dump(simplified_results, f, indent=2)
    
    # 保存 RMSE 专门的 CSV 文件
    rmse_csv_file = os.path.join(RESULTS_DIR, 'rmse_results.csv')
    print(f'保存 RMSE 结果到: {rmse_csv_file}')
    
    rmse_data = []
    for node, faults in node_results.items():
        for fault_type in ['sa0', 'sa1']:
            fault_result = faults.get(fault_type)
            if fault_result and fault_result.get('status') == 'success':
                rmse_value = fault_result.get('rmse', float('nan'))
                rmse_data.append({
                    'node_name': node,
                    'stuck_at': fault_type.replace('sa', ''),
                    'rmse': rmse_value,
                    'valid_points': fault_result.get('rmse_valid_points', 0),
                    'diff_count': fault_result.get('diff_count', 0),
                    'detected': 'Yes' if fault_result.get('detected', False) else 'No'
                })
    
    # 按 RMSE 降序排序
    rmse_data_sorted = sorted(rmse_data, 
                              key=lambda x: x['rmse'] if not math.isnan(x['rmse']) else -1, 
                              reverse=True)
    
    with open(rmse_csv_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['node_name', 'stuck_at', 'rmse', 'valid_points', 'diff_count', 'detected']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for data in rmse_data_sorted:
            writer.writerow({
                'node_name': data['node_name'],
                'stuck_at': data['stuck_at'],
                'rmse': f"{data['rmse']:.4f}" if not math.isnan(data['rmse']) else 'N/A',
                'valid_points': data['valid_points'],
                'diff_count': data['diff_count'],
                'detected': data['detected']
            })
    
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
    
    # RMSE 统计
    valid_rmse_values = [data['rmse'] for data in rmse_data if not math.isnan(data['rmse'])]
    
    elapsed_phase1 = time.time() - t0_phase1
    
    print('\n' + '='*70)
    print('阶段1 完成 - 全节点注入测试统计')
    print('='*70)
    print(f'总测试节点数: {total_nodes}')
    print(f'总测试故障数: {total_faults}')
    print(f'检测到的节点数: {detected_nodes} ({detected_nodes/total_nodes*100:.2f}%)')
    print(f'检测到的故障数: {detected_faults} ({detected_faults/total_faults*100:.2f}%)')
    
    if valid_rmse_values:
        print(f'\n📊 RMSE 统计:')
        print(f'   有效 RMSE 计算数: {len(valid_rmse_values)}')
        print(f'   最大 RMSE: {max(valid_rmse_values):.4f}')
        print(f'   最小 RMSE: {min(valid_rmse_values):.4f}')
        print(f'   平均 RMSE: {sum(valid_rmse_values)/len(valid_rmse_values):.4f}')
        
        # 计算临界故障数（RMSE > 1000）
        RMSE_THRESHOLD = 1000.0
        critical_count = sum(1 for r in valid_rmse_values if r > RMSE_THRESHOLD)
        print(f'   临界故障 (RMSE > {RMSE_THRESHOLD}): {critical_count} ({critical_count/len(valid_rmse_values)*100:.2f}%)')
    
    print(f'\n阶段1总用时: {elapsed_phase1:.2f}s')
    print('='*70)
    
    return golden_vals, node_results


# ========== 阶段2：基于保存结果的覆盖率统计 ==========

def phase2_coverage_statistics(golden_vals: List[int], node_results: Dict):
    """
    阶段2：根据保存的全节点测试结果，对不同 gnn_rank 文件的覆盖率进行统计
    gnn_ranks 目录下的文件格式：gnn_rank_{topk}.txt（没有 run 后缀）
    如果只有一个文件，按节点数递增输出累积覆盖率
    """
    print('\n' + '='*70)
    print('阶段2：基于全节点结果的覆盖率统计')
    print('='*70)
    
    t0_phase2 = time.time()
    
    # 1) 查找所有 gnn_rank 文件
    print('\n[1/2] 查找 gnn_rank 文件...')
    # 查找 gnn_rank_*.txt 格式的文件
    rank_files = glob.glob(os.path.join(RANK_DIR, "gnn_rank_*.txt"))
    # 也查找 gnn_rank.txt 格式的文件（没有下划线）
    rank_file_plain = os.path.join(RANK_DIR, "gnn_rank.txt")
    if os.path.exists(rank_file_plain) and rank_file_plain not in rank_files:
        rank_files.append(rank_file_plain)
    
    if not rank_files:
        print(f'❌ {RANK_DIR} 下没有找到 gnn_rank 文件（支持 gnn_rank.txt 或 gnn_rank_*.txt）')
        return
    
    # 如果只有一个文件，使用累积统计模式
    if len(rank_files) == 1:
        rank_file = rank_files[0]
        filename = os.path.basename(rank_file)
        print(f'✅ 找到 1 个 gnn_rank 文件: {filename}')
        print('\n[2/2] 按节点数递增统计累积覆盖率...')
        
        # 读取所有节点
        gnn_nodes = load_gnn_topk(rank_file, topk=10**9)
        
        # 过滤：只保留在 node_results 中的节点
        filtered_nodes = [n for n in gnn_nodes if n in node_results]
        
        if not filtered_nodes:
            print(f'❌ 没有匹配的节点')
            return
        
        print(f'✅ 有效节点数: {len(filtered_nodes)}')
        print('\n开始递增统计（从1个节点开始，逐步增加到所有节点）...\n')
        
        results = []  # 列表，每个元素为累积统计结果
        
        # 从1个节点开始，逐步增加到所有节点
        for num_nodes in range(1, len(filtered_nodes) + 1):
            # 取前 num_nodes 个节点（累积）
            current_nodes = filtered_nodes[:num_nodes]
            
            # 统计累积覆盖率和RMSE
            detected_nodes = 0
            detected_faults = 0
            rmse_values = []
            
            for node in current_nodes:
                node_detected = False
                for fault_type in ['sa0', 'sa1']:
                    fault_result = node_results[node].get(fault_type)
                    if fault_result and fault_result.get('detected', False):
                        detected_faults += 1
                        node_detected = True
                    # 收集 RMSE 值
                    if fault_result and fault_result.get('status') == 'success':
                        rmse_val = fault_result.get('rmse', float('nan'))
                        if not math.isnan(rmse_val):
                            rmse_values.append(rmse_val)
                if node_detected:
                    detected_nodes += 1
            
            # 计算累积覆盖率
            total_faults = len(current_nodes) * 2
            node_cov = detected_nodes / len(current_nodes) * 100.0 if current_nodes else 0
            fault_cov = detected_faults / total_faults * 100.0 if total_faults else 0
            
            # 计算平均RMSE
            avg_rmse = sum(rmse_values) / len(rmse_values) if rmse_values else 0.0
            max_rmse = max(rmse_values) if rmse_values else 0.0
            
            results.append({
                'num_nodes': num_nodes,
                'fault_cov': fault_cov,
                'node_cov': node_cov,
                'tested_nodes': len(current_nodes),
                'detected_nodes': detected_nodes,
                'detected_faults': detected_faults,
                'avg_rmse': avg_rmse,
                'max_rmse': max_rmse,
                'rmse_count': len(rmse_values)
            })
            
            # 实时输出当前结果
            escaped_nodes = len(current_nodes) - detected_nodes
            escaped_faults = total_faults - detected_faults
            print(f'节点数={num_nodes:4d}: 节点覆盖率={node_cov:6.2f}%, 故障覆盖率={fault_cov:6.2f}%, '
                  f'检测节点={detected_nodes:4d}, 检测故障={detected_faults:4d}, '
                  f'逃逸节点={escaped_nodes:4d}, 逃逸故障={escaped_faults:4d}, '
                  f'平均RMSE={avg_rmse:.4f}')
        
        # 保存统计结果到 CSV
        RESULT_CSV = os.path.join(RESULTS_DIR, 'coverage_statistics.csv')
        print(f'\n保存统计结果到: {RESULT_CSV}')
        
        with open(RESULT_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # 写入列标题
            header = ['num_nodes', 'tested_nodes', 'fault_coverage(%)', 'node_coverage(%)', 
                     'avg_rmse', 'max_rmse', 'detected_nodes', 'detected_faults', 
                     'escaped_nodes', 'escaped_faults']
            writer.writerow(header)
            
            # 写入每个节点数的累积数据
            for result in results:
                tested_nodes = result['tested_nodes']
                detected_nodes = result['detected_nodes']
                detected_faults = result['detected_faults']
                
                # 计算逃逸节点和逃逸故障
                escaped_nodes = tested_nodes - detected_nodes
                injected_faults = tested_nodes * 2
                escaped_faults = injected_faults - detected_faults
                
                row = [
                    result['num_nodes'],
                    tested_nodes,
                    f"{result['fault_cov']:.2f}",
                    f"{result['node_cov']:.2f}",
                    f"{result['avg_rmse']:.4f}",
                    f"{result['max_rmse']:.4f}",
                    str(detected_nodes),
                    str(detected_faults),
                    str(escaped_nodes),
                    str(escaped_faults)
                ]
                writer.writerow(row)
        
        elapsed_phase2 = time.time() - t0_phase2
        
        # 输出最终统计
        final_result = results[-1]
        print('\n' + '='*70)
        print('阶段2 完成 - 累积覆盖率统计')
        print('='*70)
        print(f'总节点数: {len(filtered_nodes)}')
        print(f'最终节点覆盖率: {final_result["node_cov"]:.2f}%')
        print(f'最终故障覆盖率: {final_result["fault_cov"]:.2f}%')
        print(f'最终检测节点数: {final_result["detected_nodes"]}')
        print(f'最终检测故障数: {final_result["detected_faults"]}')
        print(f'结果文件: {RESULT_CSV}')
        print(f'\n阶段2用时: {elapsed_phase2:.2f}s')
        print('='*70)
        
        return
    
    # 多个文件的情况：按 topk 分组处理（原有逻辑）
    # 按 topk 分组
    files_by_topk = {}  # {topk: [filepath]}
    plain_files = []  # 存储 gnn_rank.txt 格式的文件
    for filepath in rank_files:
        filename = os.path.basename(filepath)
        topk = extract_topk(filename)
        if topk is None:
            # gnn_rank.txt 格式的文件
            plain_files.append(filepath)
        elif topk != float('inf'):
            if topk not in files_by_topk:
                files_by_topk[topk] = []
            files_by_topk[topk].append(filepath)
    
    # 如果有 gnn_rank.txt 格式的文件，也添加到处理列表
    if plain_files:
        # 使用 None 作为 key 表示普通排名文件
        if None not in files_by_topk:
            files_by_topk[None] = []
        files_by_topk[None].extend(plain_files)
    
    # 输出统计信息
    # 自定义排序：None 放在最后，其他按数字排序
    def sort_key(item):
        topk = item[0] if isinstance(item, tuple) else item
        if topk is None:
            return (1, 0)  # None 放在最后
        elif isinstance(topk, (int, float)):
            return (0, topk)  # 数字正常排序
        else:
            return (2, 0)  # 其他类型放在最后
    
    for topk, files in sorted(files_by_topk.items(), key=sort_key):
        topk_display = 'all' if topk == float('inf') else (topk if topk is not None else 'plain')
        print(f'  TopK={topk_display}: 找到 {len(files)} 个排名文件')
    
    if not files_by_topk:
        print('❌ 没有找到有效的排名文件')
        return
    
    # 使用 files_by_topk 的 key 确保一致性，进行排序
    topk_list = sorted([k for k in files_by_topk.keys()], 
                       key=lambda x: (1, 0) if x is None else ((0, x) if isinstance(x, (int, float)) else (2, 0)))
    print(f'✅ 找到 {len(topk_list)} 个 topk 值: {[str(x) if x is not None else "plain" for x in topk_list]}')
    
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
            
            if topk is None:
                rank_tag = 'gnn_rank'
            elif topk == float('inf'):
                rank_tag = 'topk_all'
            else:
                rank_tag = f'topk{topk}'
            
            # 读取 gnn_rank 文件中的节点列表
            # 由于文件本身已经包含 topk 个节点，直接读取全部
            gnn_nodes = load_gnn_topk(rank_file, topk=10**9)
            
            # 过滤：只保留在 node_results 中的节点
            filtered_nodes = [n for n in gnn_nodes if n in node_results]
            
            if not filtered_nodes:
                print(f'⚠️ [{current_file}/{total_files}] {rank_tag}: 没有匹配的节点，跳过')
                continue
            
            # 统计覆盖率和RMSE
            detected_nodes = 0
            detected_faults = 0
            rmse_values = []
            
            for node in filtered_nodes:
                node_detected = False
                for fault_type in ['sa0', 'sa1']:
                    fault_result = node_results[node].get(fault_type)
                    if fault_result and fault_result.get('detected', False):
                        detected_faults += 1
                        node_detected = True
                    # 收集 RMSE 值
                    if fault_result and fault_result.get('status') == 'success':
                        rmse_val = fault_result.get('rmse', float('nan'))
                        if not math.isnan(rmse_val):
                            rmse_values.append(rmse_val)
                if node_detected:
                    detected_nodes += 1
            
            # 计算覆盖率
            total_faults = len(filtered_nodes) * 2
            node_cov = detected_nodes / len(filtered_nodes) * 100.0 if filtered_nodes else 0
            fault_cov = detected_faults / total_faults * 100.0 if total_faults else 0
            
            # 计算平均RMSE
            avg_rmse = sum(rmse_values) / len(rmse_values) if rmse_values else 0.0
            max_rmse = max(rmse_values) if rmse_values else 0.0
            
            results.append({
                'topk': topk,
                'fault_cov': fault_cov,
                'node_cov': node_cov,
                'tested_nodes': len(filtered_nodes),
                'detected_nodes': detected_nodes,
                'detected_faults': detected_faults,
                'avg_rmse': avg_rmse,
                'max_rmse': max_rmse,
                'rmse_count': len(rmse_values)
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
        header = ['topk', 'tested_nodes', 'fault_coverage(%)', 'node_coverage(%)', 'avg_rmse', 'max_rmse', 'escaped_nodes', 'escaped_faults']
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
            
            # 处理 topk 显示
            topk_display = result['topk']
            if topk_display is None:
                topk_display = 'plain'
            elif topk_display == float('inf'):
                topk_display = 'all'
            
            row = [
                topk_display,
                tested_nodes,
                f"{result['fault_cov']:.2f}",
                f"{result['node_cov']:.2f}",
                f"{result['avg_rmse']:.4f}",
                f"{result['max_rmse']:.4f}",
                str(escaped_nodes),
                str(escaped_faults)
            ]
            writer.writerow(row)
    
    elapsed_phase2 = time.time() - t0_phase2
    
    # 计算整体RMSE统计
    all_avg_rmse = [res['avg_rmse'] for res in results if res['avg_rmse'] > 0]
    all_max_rmse = [res['max_rmse'] for res in results if res['max_rmse'] > 0]
    
    print('\n' + '='*70)
    print('阶段2 完成 - 覆盖率统计')
    print('='*70)
    print(f'统计的 topk 数量: {len(topk_list)}')
    print(f'TopK 范围: {min(topk_list)} - {max(topk_list)}')
    print(f'总文件数: {len(results)}')
    print(f'结果文件: {RESULT_CSV}')
    
    if all_avg_rmse:
        print(f'\n📊 RMSE 整体统计 (跨所有 topk):')
        print(f'   平均 RMSE 范围: {min(all_avg_rmse):.4f} - {max(all_avg_rmse):.4f}')
        print(f'   最大 RMSE 范围: {min(all_max_rmse):.4f} - {max(all_max_rmse):.4f}')
        print(f'   总体平均 RMSE: {sum(all_avg_rmse)/len(all_avg_rmse):.4f}')
    
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


