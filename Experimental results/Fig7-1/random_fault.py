# fault_injection_validation.py
import os
import re
import csv
import time
import random
import subprocess
from typing import List, Tuple, Set

# ===== 配置 =====
VERILOG_SRC = 'pe.synth_dct.v'
TB_FILE = 'tb_1.v'
CELL_LIB = 'cells.v'

LOGDIR = 'sim_logs'
os.makedirs(LOGDIR, exist_ok=True)

INJECT_DELAY_CYCLES = 5
MAX_VVP_SECONDS = 60
MAX_UNKNOWN_RATIO = 0.2

OSUM_HEX_RE = re.compile(r'o_sum\s*=\s*([0-9a-fA-FxzXZ]+)')

# ---------- 工具函数 ----------
def run_cmd(cmd: List[str], capture=False, timeout=None) -> Tuple[int, str]:
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
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    text = re.sub(r'//.*', '', text)
    return text

def extract_module(text: str, modname: str) -> str:
    m = re.search(rf'\bmodule\s+{re.escape(modname)}\b.*?\bendmodule\b', text, flags=re.DOTALL)
    return m.group(0) if m else ''

def split_decl_names(decl_body: str) -> List[str]:
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
    inputs, outputs, inouts = set(), set(), set()
    for stmt in module_text.split(';'):
        s = stmt.strip()
        if not s:
            continue
        if s.startswith('input'):
            body = re.sub(r'^\binput\b\s+((?:wire|reg|logic|signed|unsigned)\s+)*', '', s)
            inputs.update(split_decl_names(body))
        elif s.startswith('output'):
            body = re.sub(r'^\boutput\b\s+((?:wire|reg|logic|signed|unsigned)\s+)*', '', s)
            outputs.update(split_decl_names(body))
        elif s.startswith('inout'):
            body = re.sub(r'^\binout\b\s+((?:wire|reg|logic|signed|unsigned)\s+)*', '', s)
            inouts.update(split_decl_names(body))
    return inputs, outputs, inouts

def parse_internal_nets(module_text: str) -> Set[str]:
    nets = set()
    for stmt in module_text.split(';'):
        s = stmt.strip()
        if not s:
            continue
        if re.match(r'^(wire|reg|logic)\b', s):
            body = re.sub(r'^(wire|reg|logic)\b\s+((?:signed|unsigned)\s+)?', '', s)
            nets.update(split_decl_names(body))
    return nets

def parse_targets_from_netlist(netlist_text: str, dut_module: str = 'pe') -> List[str]:
    """
    注入目标 = 输出 ∪ 内部信号 - 输入
    排序规则：
        1. 节点名末尾有数字，按数字排序
        2. 没数字的按字典序排在后面
    """
    text = strip_comments(netlist_text)
    mod = extract_module(text, dut_module)
    if not mod:
        mod = text

    inputs, outputs, _ = parse_ports(mod)
    internals = parse_internal_nets(mod)
    targets = (outputs | internals) - inputs

    valid = []
    for n in targets:
        if re.match(r'^[A-Za-z_][A-Za-z0-9_$]*$', n) or re.match(r'^[A-Za-z_][A-Za-z0-9_$]*\[\d+\]$', n):
            valid.append(n)

    # 自然数排序 + 字典排序
    def nat_key(s: str):
        m = re.search(r'(\d+)$', s)  # 尾部数字
        if m:
            return (0, int(m.group(1)), s)  # 有数字 → 数字优先
        else:
            return (1, 0, s)               # 没数字 → 排在后面，按字典序

    valid = sorted(valid, key=nat_key)
    return valid

def make_injected_tb(tb_text: str, target_net: str, stuck: int) -> str:
    """
    在 testbench 中自动注入 force 语句
    """
    inj_block = f"""
// --- fault injection (auto) ---
initial begin : __fi_block
    wait (reset == 0);
    repeat({INJECT_DELAY_CYCLES}) @(posedge clock);
    force uut.{target_net} = 1'b{stuck};
    $display("FAULT_INJECTED: {target_net} sa{stuck}");
end
// --- end fault injection ---
"""
    idx = tb_text.rfind('endmodule')
    if idx == -1:
        return tb_text + inj_block
    else:
        return tb_text[:idx] + inj_block + tb_text[idx:]

def compile_and_run(sources: List[str], exe_path: str, vcd_path: str, log_path: str,
                    timeout: int = MAX_VVP_SECONDS) -> bool:
    """
    编译 + 运行仿真
    """
    cmd_compile = ['iverilog', '-g2012', '-o', exe_path] + sources
    rc, out = run_cmd(cmd_compile, capture=True)
    if rc != 0:
        with open(log_path, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(out)
        return False

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
    vals, total, unknown = [], 0, 0
    try:
        with open(logfile, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                m = OSUM_HEX_RE.search(line)
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
        print(f'⚠️ 无法读取 {logfile}: {e}')
    unk_ratio = (unknown / total) if total > 0 else 1.0
    return vals, unk_ratio

TOPK_FILE = 'topk.csv'  # 假设 CSV，每列是一组 topk 节点

def read_topk(topk_file: str) -> List[List[str]]:
    """
    读取 topk 文件，每列一组节点
    返回 List[List[str]]，每个子列表对应一列 topk 节点
    """
    import csv
    columns = []
    with open(topk_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
        if not rows:
            return []
        num_cols = len(rows[0])
        columns = [[] for _ in range(num_cols)]
        for row in rows:
            for i, val in enumerate(row):
                if val.strip():
                    columns[i].append(val.strip())
    return columns


def main():
    import csv
    import random
    import time
    import glob

    t0_total = time.time()
    TOPK_FILE = 'topk.csv'  
    RESULT_DIR = 'topk_results'
    os.makedirs(RESULT_DIR, exist_ok=True)

    # 读取 TopK CSV 文件
    topk_numbers = []
    with open(TOPK_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            val = row[0].strip()
            if val.isdigit():
                topk_numbers.append(int(val))
    if not topk_numbers:
        print(f'❌ TopK 文件 {TOPK_FILE} 为空或格式错误')
        return

    tb_src = open(TB_FILE, 'r', encoding='utf-8', errors='ignore').read()

    # CSV 汇总文件
    summary_csv = os.path.join(RESULT_DIR, 'topk_summary.csv')
    file_exists = os.path.exists(summary_csv)
    with open(summary_csv, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['topk', 'selected_nodes', 'avg_node_coverage(%)',
                             'avg_fault_coverage(%)', 'avg_runtime(s)'])

    # 每行 TopK 独立仿真
    NUM_TRIALS = 20  # 每个 TopK 做 1 次随机试验
    for idx, k in enumerate(topk_numbers, 1):
        print(f'\n🔧 TopK row {idx}: topk={k} | Starting simulation...')
        node_cov_list = []
        fault_cov_list = []
        runtime_list = []
        selected_nodes_list = []

        # Step 1: golden 仿真
        golden_log = os.path.join(LOGDIR, f'golden_row{idx}.log')
        golden_exe = os.path.join(LOGDIR, f'golden_row{idx}.out')
        golden_vcd = os.path.join(LOGDIR, f'golden_row{idx}.vcd')

        ok = compile_and_run([CELL_LIB, VERILOG_SRC, TB_FILE],
                             golden_exe, golden_vcd, golden_log,
                             timeout=MAX_VVP_SECONDS)
        if not ok:
            print(f'❌ TopK row {idx} golden 仿真失败')
            continue

        golden_vals, golden_unk = parse_osum_as_ints(golden_log)
        if not golden_vals:
            print(f'❌ TopK row {idx} golden.log 没有有效 o_sum 样本')
            continue

        # Step 2: 解析 netlist得到所有可注入节点
        with open(VERILOG_SRC, 'r', encoding='utf-8', errors='ignore') as f:
            all_targets = parse_targets_from_netlist(f.read(), 'pe')
        if not all_targets:
            print(f'❌ TopK row {idx} 未找到可注入节点')
            continue
        print(f'🎯 TopK row {idx}: total {len(all_targets)} fault-injectable nodes found.')

        # Step 3: 多次随机抽样仿真
        for trial in range(1, NUM_TRIALS + 1):
            t0 = time.time()

            # 随机选取五分之一节点注入
            num_inject = max(1, k // 5)
            if num_inject >= len(all_targets):
                selected_nodes = all_targets[:]
            else:
                selected_nodes = random.sample(all_targets, num_inject)

            detected_nodes = 0
            detected_faults = 0
            total_faults = 0

            for net in selected_nodes:
                node_detected = False
                for val in [0, 1]:
                    total_faults += 1
                    tb_inj = make_injected_tb(tb_src, net, val)
                    tb_tmp = os.path.join(LOGDIR, f'tb_inj_row{idx}_{net}_sa{val}.v')
                    with open(tb_tmp, 'w', encoding='utf-8', errors='ignore') as w:
                        w.write(tb_inj)

                    exe = os.path.join(LOGDIR, f'{net}_sa{val}_row{idx}.out')
                    vcd = os.path.join(LOGDIR, f'{net}_sa{val}_row{idx}.vcd')
                    log = os.path.join(LOGDIR, f'{net}_sa{val}_row{idx}.log')

                    ok = compile_and_run([CELL_LIB, VERILOG_SRC, tb_tmp],
                                         exe, vcd, log, timeout=MAX_VVP_SECONDS)
                    if not ok:
                        continue

                    vals, unk = parse_osum_as_ints(log)
                    if not vals or unk > MAX_UNKNOWN_RATIO:
                        continue

                    L = min(len(golden_vals), len(vals))
                    diff = sum(1 for a, b in zip(golden_vals[:L], vals[:L]) if a != b)
                    if diff > 0:
                        node_detected = True
                        detected_faults += 1

                if node_detected:
                    detected_nodes += 1

            node_cov = detected_nodes / len(selected_nodes) * 100
            fault_cov = detected_faults / total_faults * 100
            elapsed = time.time() - t0

            node_cov_list.append(node_cov)
            fault_cov_list.append(fault_cov)
            runtime_list.append(elapsed)
            selected_nodes_list.append(len(selected_nodes))

            # ✅ 清理临时日志
            try:
                for file in glob.glob(os.path.join(LOGDIR, '*')):
                    if os.path.isfile(file):
                        os.remove(file)
            except Exception as e:
                print(f'⚠️ Trial {trial}: 清理日志目录失败 - {e}')

        # Step 4: 汇总平均结果
        avg_node_cov = sum(node_cov_list) / NUM_TRIALS
        avg_fault_cov = sum(fault_cov_list) / NUM_TRIALS
        avg_runtime = sum(runtime_list) / NUM_TRIALS
        avg_selected_nodes = sum(selected_nodes_list) / NUM_TRIALS

        print(f'\n✅ TopK row {idx} Summary (avg over {NUM_TRIALS} trials):')
        print(f'  Avg Node Coverage = {avg_node_cov:.2f}%')
        print(f'  Avg Fault Coverage = {avg_fault_cov:.2f}%')
        print(f'  Avg Runtime = {avg_runtime:.2f}s')
        print(f'  TopK nodes = {k}, Avg selected nodes = {avg_selected_nodes:.0f}')

        # 写入 CSV
        with open(summary_csv, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([k, avg_selected_nodes, f'{avg_node_cov:.2f}',
                             f'{avg_fault_cov:.2f}', f'{avg_runtime:.1f}'])

        # ✅ 每个 TopK 循环结束后再清理一次
        try:
            for file in glob.glob(os.path.join(LOGDIR, '*')):
                if os.path.isfile(file):
                    os.remove(file)
        except Exception as e:
            print(f'⚠️ TopK row {idx}: 清理日志目录失败 - {e}')

    print(f'\n⏱️ Total Runtime for all TopK rows: {time.time() - t0_total:.2f}s')


if __name__ == '__main__':
    main()
