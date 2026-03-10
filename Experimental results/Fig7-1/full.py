# fault_injection_validation.py
import os
import re
import csv
import time
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

# ---------- 主流程 ----------
def main():
    t0 = time.time()
    RESULT_CSV = 'fault_injection_results.csv'

    print('🔧 Step 1: Running golden simulation...')
    golden_log = os.path.join(LOGDIR, 'golden.log')
    golden_exe = os.path.join(LOGDIR, 'golden.out')
    golden_vcd = os.path.join(LOGDIR, 'golden.vcd')

    ok = compile_and_run([CELL_LIB, VERILOG_SRC, TB_FILE],
                         golden_exe, golden_vcd, golden_log,
                         timeout=MAX_VVP_SECONDS)
    if not ok:
        print('❌ Golden 仿真失败')
        with open(golden_log, 'r', encoding='utf-8', errors='ignore') as f:
            print(f.read())
        return

    golden_vals, golden_unk = parse_osum_as_ints(golden_log)
    if not golden_vals:
        print('❌ golden.log 没有有效的 o_sum 样本')
        with open(golden_log, 'r', encoding='utf-8', errors='ignore') as f:
            print(f.read())
        return

    print(f'✅ golden 样本 {len(golden_vals)}，unknown_ratio={golden_unk:.2%}')

    # 解析注入目标
    with open(VERILOG_SRC, 'r', encoding='utf-8', errors='ignore') as f:
        targets = parse_targets_from_netlist(f.read(), 'pe')
    print(f'🎯 Found {len(targets)} fault targets.')

    tb_src = open(TB_FILE, 'r', encoding='utf-8', errors='ignore').read()

    # 初始化 CSV
    with open(RESULT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['node_index', 'node_name', 'node_detected', 'node_coverage(%)',
                         'fault_detected', 'fault_coverage(%)', 'total_time(s)'])

    detected_nodes = 0      # 节点检测到至少一个 fault
    total_faults = 0        # 总注入 fault
    detected_faults = 0     # 检测到的 fault 数

    for i, net in enumerate(targets, 1):
        node_detected = False
        for val in [0, 1]:
            total_faults += 1
            tb_inj = make_injected_tb(tb_src, net, val)
            tb_tmp = os.path.join(LOGDIR, f'tb_inj_{net}_sa{val}.v')
            with open(tb_tmp, 'w', encoding='utf-8', errors='ignore') as w:
                w.write(tb_inj)

            exe = os.path.join(LOGDIR, f'{net}_sa{val}.out')
            vcd = os.path.join(LOGDIR, f'{net}_sa{val}.vcd')
            log = os.path.join(LOGDIR, f'{net}_sa{val}.log')

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

        node_coverage = detected_nodes / i * 100
        fault_coverage = detected_faults / total_faults * 100
        elapsed = time.time() - t0

        print(f'节点 {i}/{len(targets)}: {"DETECTED" if node_detected else "NO"} | '
              f'Node Coverage={node_coverage:.2f}%, Fault Coverage={fault_coverage:.2f}%')

        with open(RESULT_CSV, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([i, net, int(node_detected), f'{node_coverage:.2f}',
                             detected_faults, f'{fault_coverage:.2f}', f'{elapsed:.1f}'])

    print(f'\n✅ Final Node Coverage = {node_coverage:.2f}% ({detected_nodes}/{len(targets)})')
    print(f'✅ Final Fault Coverage = {fault_coverage:.2f}% ({detected_faults}/{total_faults})')
    print(f'⏱️ Total Runtime: {time.time() - t0:.2f}s')


if __name__ == '__main__':
    main()
