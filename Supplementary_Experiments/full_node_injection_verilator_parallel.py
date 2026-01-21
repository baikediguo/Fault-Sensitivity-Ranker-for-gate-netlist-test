"""
超快速故障注入测试器 V2 - Verilator 版本
============================================
核心优化: 使用 Verilator 编译仿真，运行速度比 Icarus Verilog 快 10-100 倍

重要差异:
- Verilator 不支持 force/release，因此使用 网表修改 方式注入故障
- 在网表中为每个目标信号添加故障注入 MUX
- 通过 plusargs (+FAULT_ID=N +FAULT_VAL=X) 在运行时选择故障
"""

import os
import re
import csv
import time
import json
import shutil
import subprocess
import glob
import concurrent.futures
import multiprocessing
from typing import List, Tuple, Set, Dict

# ===== 基本配置 =====
INPUT_NETLIST_DIR = './netlists'
RANK_DIR          = './gnn_ranks'
BASE_RESULTS_DIR  = 'full_injection_results_verilator'
CELL_LIB          = 'cells.v'
TIMING_REPORT_PATH = './gnn_ranks/timing_report.csv'

# Verilator Configuration (WSL2)
# We assume 'wsl' command is available and default distro is configured
# Clang will be used via --compiler clang flag in Verilator

# 注入配置
MAX_UNKNOWN_RATIO = 0.2

# 并行配置
CPU_COUNT = os.cpu_count() or 4
WORKER_COUNT = max(1, CPU_COUNT - 2)

# 预编译正则表达式 - 支持多种输出格式
# 匹配: o_sum=xxx, OUT=xxx, OUTPUT=xxx, out=xxx, 或者裸十六进制行
OSUM_HEX_RE = re.compile(r'^(?:o_sum|OUT|OUTPUT|out|o)\s*[=:]\s*([0-9a-fA-FxzXZ]+)', re.MULTILINE | re.IGNORECASE)
# 备用正则: 匹配 $display 常见格式如 "value: xxx" 或纯十六进制输出
ALT_HEX_RE = re.compile(r'^(?:value|result|data|output)?\s*[=:]?\s*([0-9a-fA-F]{2,})[\s$]', re.MULTILINE | re.IGNORECASE)


def run_cmd_fast(cmd: List[str], capture=False, timeout=None) -> Tuple[int, str]:
    """优化的命令执行"""
    try:
        if capture:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout,
                encoding='utf-8', errors='ignore'
            )
            return result.returncode, result.stdout + result.stderr
        else:
            result = subprocess.run(
                cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=timeout
            )
            return result.returncode, ''
    except subprocess.TimeoutExpired:
        return -1, 'TIMEOUT'
    except Exception as e:
        return -1, str(e)


def to_wsl_path(win_path: str) -> str:
    """
    Convert Windows path to WSL path - 改进版
    优先使用手动转换以避免 wslpath 命令的编码问题
    """
    # 先规范化路径，统一使用正斜杠
    win_path = os.path.abspath(win_path)
    # 直接手动转换，避免 wslpath 命令的编码/特殊字符问题
    drive, rest = os.path.splitdrive(win_path)
    if not drive:
        # 没有盘符，可能已经是 WSL 路径
        return win_path.replace('\\', '/')
    drive_letter = drive[0].lower()
    # 将所有反斜杠转换为正斜杠，并确保没有连续的斜杠
    rest = rest.replace('\\', '/').replace('//', '/')
    wsl_path = f'/mnt/{drive_letter}{rest}'
    # 清理可能的路径问题
    wsl_path = re.sub(r'/+', '/', wsl_path)
    return wsl_path


def run_wsl_cmd(cmd_str: str, capture=False, timeout=None, max_retries=3) -> Tuple[int, str]:
    """
    Execute command in WSL environment - 带重试机制
    自动重试 WSL 服务临时错误
    """
    for attempt in range(max_retries):
        try:
            full_cmd = ['wsl', 'bash', '-c', cmd_str]
            
            if capture:
                # 使用 bytes 模式避免编码问题
                result = subprocess.run(
                    full_cmd, capture_output=True, timeout=timeout
                )
                # 手动解码，尝试多种编码
                output = b''
                if result.stdout:
                    output += result.stdout
                if result.stderr:
                    output += result.stderr
                try:
                    text_output = output.decode('utf-8', errors='ignore')
                except:
                    try:
                        text_output = output.decode('gbk', errors='ignore')
                    except:
                        text_output = output.decode('latin-1', errors='ignore')
                
                # 检查是否是 WSL 服务错误，如果是则重试
                if 'E_UNEXPECTED' in text_output or 'Wsl/Service' in text_output:
                    if attempt < max_retries - 1:
                        print(f'    [WSL] 服务错误，等待重试 ({attempt+1}/{max_retries})...')
                        time.sleep(2)  # 等待 2 秒后重试
                        continue
                
                return result.returncode, text_output
            else:
                result = subprocess.run(
                    full_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=timeout
                )
                return result.returncode, ''
        except subprocess.TimeoutExpired:
            return -1, 'TIMEOUT'
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            return -1, str(e)
    return -1, 'MAX_RETRIES_EXCEEDED'


def strip_comments(text: str) -> str:
    return re.sub(r'/\*.*?\*/|//.*?$', '', text, flags=re.DOTALL | re.MULTILINE)


def extract_module(text: str, modname: str) -> str:
    m = re.search(rf'\bmodule\s+{re.escape(modname)}\b.*?\bendmodule\b', text, flags=re.DOTALL)
    return m.group(0) if m else text


def split_decl_names(decl_body: str) -> List[str]:
    out = []
    decl_body = re.sub(r'\[[^\]\n]*:[^\]\n]*\]', '', decl_body)
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
    nets = set()
    for stmt in module_text.split(';'):
        s = stmt.strip()
        if not s:
            continue
        if re.match(r'^(wire|reg|logic)\b', s):
            body = re.sub(r'^(wire|reg|logic)\b\s+((?:signed|unsigned)\s+)?', '', s)
            nets.update(split_decl_names(body))
    return nets


def preprocess_netlist_for_verilator(netlist_text: str, max_line_length: int = 10000) -> str:
    """
    预处理网表，将超长的 wire/reg 声明拆分成多行
    Verilator 默认限制每行 40000 个 token，这里将长行拆分
    """
    lines = netlist_text.split('\n')
    new_lines = []
    
    for line in lines:
        # 检查是否是超长的 wire/reg/input/output 声明
        if len(line) > max_line_length:
            stripped = line.strip()
            # 检查是否是 wire/reg/input/output 声明 (以逗号分隔的信号列表)
            m = re.match(r'^(\s*)(wire|reg|input|output)\s+(.+?)(;?)(\s*)$', stripped)
            if m:
                indent = m.group(1) or '  '
                keyword = m.group(2)
                signals = m.group(3)
                semicolon = m.group(4)
                
                # 将信号列表拆分成多行
                signal_list = [s.strip() for s in signals.split(',') if s.strip()]
                
                # 每行最多放 20 个信号
                chunk_size = 20
                for i in range(0, len(signal_list), chunk_size):
                    chunk = signal_list[i:i+chunk_size]
                    chunk_str = ', '.join(chunk)
                    if i == 0:
                        # 第一行带关键字
                        if i + chunk_size < len(signal_list):
                            new_lines.append(f'{indent}{keyword} {chunk_str},')
                        else:
                            new_lines.append(f'{indent}{keyword} {chunk_str}{semicolon}')
                    elif i + chunk_size >= len(signal_list):
                        # 最后一行带分号
                        new_lines.append(f'{indent}       {chunk_str}{semicolon}')
                    else:
                        # 中间行带逗号
                        new_lines.append(f'{indent}       {chunk_str},')
                continue
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)


def parse_targets_from_netlist(netlist_text: str, dut_module_name: str) -> List[str]:
    """解析网表，找出所有可注入的目标信号"""
    text = strip_comments(netlist_text)
    mod = extract_module(text, dut_module_name)
    if not mod:
        mod = text
    inputs, outputs, _ = parse_ports(mod)
    internals = parse_internal_nets(mod)
    targets = (outputs | internals) - inputs
    good = []
    for n in sorted(targets):
        # 只保留有效的标识符
        if re.match(r'^[A-Za-z_][A-Za-z0-9_$]*$', n):
            good.append(n)
        elif re.match(r'^[A-Za-z_][A-Za-z0-9_$]*\[\d+\]$', n):
            good.append(n)
    return good


def generate_fault_injection_netlist(netlist_text: str, dut_module_name: str, 
                                      legal_targets: List[str]) -> str:
    """
    生成支持故障注入的修改版网表 - 真正的网表级 MUX 插入
    
    方法: 
    1. 为每个目标信号创建 xxx_orig 版本
    2. 将门实例的输出从 .Y(xxx) 改为 .Y(xxx_orig)
    3. 添加 MUX: assign xxx = (FI条件) ? FI值 : xxx_orig;
    
    示例:
    原始: 
        wire n123;
        AND2 g1 (.A(a), .B(b), .Y(n123));
    修改后: 
        wire n123_orig, n123;
        AND2 g1 (.A(a), .B(b), .Y(n123_orig));
        assign n123 = (__FAULT_ID == 0) ? 1'b0 : 
                      (__FAULT_ID == 1) ? 1'b1 : n123_orig;
    """
    # 找到 module 声明的结尾 (第一个分号之后的位置)
    module_match = re.search(rf'\bmodule\s+{re.escape(dut_module_name)}\b[^;]*;', netlist_text)
    if not module_match:
        print(f"  [警告] 无法找到模块 {dut_module_name}")
        return netlist_text
    
    insert_pos = module_match.end()
    
    # 构建目标信号集合 (用于快速查找)
    target_set = set(legal_targets)
    
    # ===== Step 1: 生成故障注入控制信号声明 =====
    fault_control = """
  // ===== Verilator 故障注入控制信号 (自动生成) =====
  integer __FAULT_ID;
  initial begin
    if (!$value$plusargs("FAULT_ID=%d", __FAULT_ID)) __FAULT_ID = -1;  // 默认无故障
  end
"""
    
    # ===== Step 2: 为目标信号生成 _orig wire 声明和 MUX =====
    orig_wire_decls = []
    mux_assigns = []
    
    for fid, target in enumerate(legal_targets):
        fid_sa0 = fid * 2
        fid_sa1 = fid * 2 + 1
        orig_name = f"{target}_fi_orig"
        
        # 声明 _orig wire
        orig_wire_decls.append(f"  wire {orig_name};")
        
        # 生成 MUX assign
        mux_assigns.append(
            f"  assign {target} = (__FAULT_ID == {fid_sa0}) ? 1'b0 :\n"
            f"                    (__FAULT_ID == {fid_sa1}) ? 1'b1 : {orig_name};"
        )
    
    # ===== Step 3: 替换门实例的输出端口连接 (优化: 单次扫描) =====
    # 构建替换映射表
    target_to_orig = {target: f"{target}_fi_orig" for target in legal_targets}
    target_set = set(legal_targets)
    
    # 使用正则表达式回调函数进行单次替换
    port_pattern = re.compile(r'\.(Y|Z|Q|X|O)\s*\(\s*(\w+)\s*\)')
    
    def replace_port(match):
        port_name = match.group(1)
        signal_name = match.group(2)
        if signal_name in target_set:
            return f'.{port_name}({target_to_orig[signal_name]})'
        return match.group(0)
    
    modified_netlist = port_pattern.sub(replace_port, netlist_text)
    
    # ===== Step 4: 移除目标信号的原始 wire 声明 (它们会被 MUX 驱动) =====
    # 注意: 不能直接删除 wire 声明，因为 MUX 的 assign 隐式声明了 wire
    # 实际上我们需要保留 wire 声明，但确保 assign 在后面
    
    # ===== Step 5: 组装修改后的网表 =====
    injection_block = "\n".join([
        "",
        "  // ===== 故障注入 _orig wire 声明 =====",
        "\n".join(orig_wire_decls),
        "",
        "  // ===== 故障注入 MUX =====", 
        "\n".join(mux_assigns),
        ""
    ])
    
    # 在 module 声明后插入控制信号和注入逻辑
    modified_netlist = (
        modified_netlist[:insert_pos] + 
        fault_control + 
        injection_block +
        modified_netlist[insert_pos:]
    )
    
    return modified_netlist


def generate_fault_injection_testbench(tb_text: str, legal_targets: List[str], 
                                        dut_module_name: str) -> Tuple[str, List[Tuple[str, int]]]:
    """
    生成 Verilator 兼容的故障注入 Testbench
    
    故障注入现在通过网表中的 MUX 实现:
    - 网表中已插入 __FAULT_ID 控制信号和 MUX
    - TB 只需要通过 hierarchical reference 设置 uut.__FAULT_ID
    - 然后运行 stimulus 并观察输出
    
    新增: 自动检测并注入输出观测语句
    """
    endmod_idx = tb_text.rfind('endmodule')
    if endmod_idx == -1:
        return tb_text, []
    
    # 构建故障映射表: (target_name, stuck_value)
    fault_map = []
    for net in legal_targets:
        fault_map.append((net, 0))  # SA0
        fault_map.append((net, 1))  # SA1
    
    total_faults = len(fault_map)
    
    # ====== 检检测是否已有 o_sum= 格式输出 ======
    has_osum_output = bool(re.search(r'\$display\s*\([^)]*o_sum\s*=', tb_text, re.IGNORECASE))
    
    # ====== 检测 DUT 实例和输出信号 ======
    dut_outputs = []
    if not has_osum_output:
        # 查找 DUT 实例化 (常见模式: top uut (.port(signal), ...))
        dut_inst_match = re.search(r'\b(top|' + re.escape(dut_module_name) + r')\s+(\w+)\s*\(([^;]+)\);', tb_text, re.DOTALL)
        if dut_inst_match:
            inst_name = dut_inst_match.group(2)
            port_str = dut_inst_match.group(3)
            # 提取输出端口 (常见输出端口名)
            output_port_patterns = [
                r'\.(?:o_|out|O_|OUT|result|sum|data_out|dout|q|y|z)\w*\s*\(\s*(\w+)\s*\)',
            ]
            for pattern in output_port_patterns:
                for match in re.finditer(pattern, port_str, re.IGNORECASE):
                    sig = match.group(1)
                    if sig and sig not in dut_outputs:
                        dut_outputs.append(sig)
            
            # 如果没找到明确的输出端口，尝试找任何看起来像输出的信号
            if not dut_outputs:
                # 查找所有端口连接
                all_ports = re.findall(r'\.(\w+)\s*\(\s*(\w+)\s*\)', port_str)
                for port_name, sig_name in all_ports:
                    port_lower = port_name.lower()
                    # 排除时钟、复位、输入
                    if not re.match(r'^(clk|clock|rst|reset|in_|input|a_|b_|din|data_in|wen|ren|en_|enable)', port_lower):
                        if port_lower.startswith(('o_', 'out', 'q', 'y', 'z', 'sum', 'result', 'data')):
                            if sig_name not in dut_outputs:
                                dut_outputs.append(sig_name)
        
        # 如果还是没找到，尝试查找 wire/reg 声明中的输出信号
        if not dut_outputs:
            for match in re.finditer(r'\b(wire|reg)\s+(?:\[\d+:\d+\])?\s*(\w+)', tb_text):
                sig = match.group(2)
                sig_lower = sig.lower()
                if sig_lower.startswith(('o_', 'out', 'result', 'sum', 'dout')):
                    if sig not in dut_outputs:
                        dut_outputs.append(sig)
    
    # ====== 转换主 initial block 为 task ======
    lines = tb_text.split('\n')
    new_lines = []
    
    in_main_initial = False
    brace_count = 0
    converted_main_block = False
    
    # 用于在时钟边沿后插入 $display
    clock_pattern = re.compile(r'#\s*\d+|@\s*\(\s*posedge\s+\w+\s*\)|@\s*\(\s*negedge\s+\w+\s*\)')
    display_inserted_count = 0
    max_display_inserts = 1000  # 限制插入数量避免输出过多
    
    # --- 单次遍历模式: 只转换第一个合适的 block ---
    main_converted = False
    in_block = False
    brace_depth = 0
    final_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # 处理 initial begin
        if not main_converted and not in_block and stripped == "initial begin":
            # 标记开始并转换
            final_lines.append("  task run_stimulus_pass;")
            final_lines.append("  begin")
            in_block = True
            brace_depth = 1
            i += 1
            continue
            
        if in_block:
            # 在块内处理
            if "$finish;" in stripped:
                final_lines.append(line.replace("$finish;", "// $finish; // disabled"))
            else:
                final_lines.append(line)
            
            brace_depth += stripped.count("begin")
            brace_depth -= stripped.count("end")
            
            if brace_depth <= 0:
                # 块结束
                final_lines.append("  endtask")
                final_lines.append("")
                in_block = False
                main_converted = True
            
            # 块内自动插入观测点
            if not has_osum_output and clock_pattern.search(stripped) and not stripped.startswith("//"):
                if display_inserted_count < max_display_inserts:
                    if len(dut_outputs) == 1:
                        final_lines.append(f'    $display("o_sum=%h", {dut_outputs[0]});')
                    else:
                        fmt = '_'.join(['%h'] * len(dut_outputs))
                        sigs = ', '.join(dut_outputs)
                        final_lines.append(f'    $display("o_sum={fmt}", {sigs});')
                    display_inserted_count += 1
            i += 1
            continue
            
        # 块外处理
        if "$finish;" in stripped:
            final_lines.append(line.replace("$finish;", "// $finish; // disabled"))
        else:
            final_lines.append(line)
        i += 1

    patched_tb = '\n'.join(final_lines)
    endmod_idx = patched_tb.rfind('endmodule')
    
    # 打印调试信息
    if not has_osum_output:
        if dut_outputs:
            print(f"  [TB修补] 自动检测到输出信号: {dut_outputs}, 已注入 {display_inserted_count} 个 $display 语句")
        else:
            print(f"  [TB修补] 警告: 未检测到输出信号，可能需要手动修改 testbench")
    
    # ====== 生成简化的故障注入控制逻辑 ======
    # 故障注入 MUX 已在网表中，TB 只需控制 uut.__FAULT_ID
    inject_code_lines = []
    inject_code_lines.append("\n  // ===== Verilator 故障注入控制 (简化版) =====")
    inject_code_lines.append("  // 故障注入 MUX 已在网表中插入，TB 只需设置 uut.__FAULT_ID")
    inject_code_lines.append("")
    inject_code_lines.append("  // 故障注入控制器")
    inject_code_lines.append("  integer __batch_fid;")
    inject_code_lines.append("  integer __BATCH_START, __BATCH_END;")
    inject_code_lines.append("")
    inject_code_lines.append("  initial begin")
    inject_code_lines.append("    if (!$value$plusargs(\"BATCH_START=%d\", __BATCH_START)) __BATCH_START = 0;")
    inject_code_lines.append(f"    if (!$value$plusargs(\"BATCH_END=%d\", __BATCH_END)) __BATCH_END = {total_faults};")
    inject_code_lines.append("")
    inject_code_lines.append("    $display(\"[BATCH] Start=%0d End=%0d\", __BATCH_START, __BATCH_END);")
    inject_code_lines.append("")
    inject_code_lines.append("    // 批量故障注入循环")
    inject_code_lines.append("    for (__batch_fid = __BATCH_START; __batch_fid < __BATCH_END; __batch_fid = __batch_fid + 1) begin")
    inject_code_lines.append("      // 通过 hierarchical reference 设置 DUT 内部的 __FAULT_ID")
    inject_code_lines.append("      uut.__FAULT_ID = __batch_fid;")
    inject_code_lines.append("      $display(\"[FID:%0d]\", __batch_fid);")
    inject_code_lines.append("      run_stimulus_pass();")
    inject_code_lines.append("    end")
    inject_code_lines.append("")
    inject_code_lines.append("    $finish;")
    inject_code_lines.append("  end")
    
    injection_code = "\n".join(inject_code_lines)
    final_tb = patched_tb[:endmod_idx] + injection_code + "\n\n" + patched_tb[endmod_idx:]
    
    return final_tb, fault_map


def parse_batched_output(log_output: str, golden_vals: List[int], 
                          fault_map: List[Tuple[str, int]]) -> Dict[str, Dict]:
    """解析批量运行输出"""
    results = {}
    
    lines = log_output.splitlines()
    current_fid = -1
    current_vals = []
    
    for line in lines:
        if line.startswith('[FID:'):
            # 保存上一个故障的结果
            if current_fid != -1 and 0 <= current_fid < len(fault_map):
                net, stuck = fault_map[current_fid]
                if net not in results:
                    results[net] = {'sa0': None, 'sa1': None}
                results[net][f'sa{stuck}'] = analyze_vals(current_vals, golden_vals)
            
            # 开始新故障
            try:
                # 格式: [FID:123]
                fid_str = line[5:].rstrip(']').strip()
                current_fid = int(fid_str)
            except:
                current_fid = -1
            current_vals = []
            
        elif 'o_sum=' in line.lower() or 'out' in line.lower() or re.match(r'^\s*[0-9a-fA-F]+\s*$', line):
            # 尝试多种匹配模式
            m = OSUM_HEX_RE.search(line)
            if not m:
                m = ALT_HEX_RE.search(line)
            if m:
                s = m.group(1).lower()
                if 'x' in s or 'z' in s:
                    current_vals.append(-1)
                else:
                    try:
                        current_vals.append(int(s, 16))
                    except:
                        current_vals.append(-1)
    
    # 保存最后一个故障的结果
    if current_fid != -1 and 0 <= current_fid < len(fault_map):
        net, stuck = fault_map[current_fid]
        if net not in results:
            results[net] = {'sa0': None, 'sa1': None}
        results[net][f'sa{stuck}'] = analyze_vals(current_vals, golden_vals)
    
    return results


def analyze_vals(vals: List[int], golden: List[int]) -> Dict:
    """分析单个故障结果"""
    if not vals:
        return {'status': 'no_output', 'detected': False}
    
    L = min(len(vals), len(golden))
    diff_count = sum(1 for i in range(L) if vals[i] != golden[i])
    
    return {
        'status': 'success',
        'detected': diff_count > 0,
        'diff_count': diff_count
    }


def run_batch_worker(args) -> Dict:
    """并行批量工作器 - 运行一个批次的故障 (WSL)"""
    wsl_exe_path, start_idx, end_idx, golden_vals, fault_map = args
    
    # Run in WSL
    # Note: wsl_exe_path must be a WSL path
    cmd_str = f'"{wsl_exe_path}" +BATCH_START={start_idx} +BATCH_END={end_idx}'
    
    # Run via WSL
    # We shouldn't use run_cmd_fast directly as it spawns subprocess on Windows without wsl prefix
    # unless we pass the full wsl command
    wsl_cmd = ['wsl', 'bash', '-c', cmd_str]
    
    try:
        result = subprocess.run(
            wsl_cmd, capture_output=True, text=True,
            encoding='utf-8', errors='ignore'
        )
        output = result.stdout + result.stderr
        rc = result.returncode
    except Exception as e:
        output = str(e)
        rc = -1

    return parse_batched_output(output, golden_vals, fault_map)


def run_circuit_injection_batched(circuit_name: str, verilog_path: str, 
                                   tb_path: str, output_dir: str):
    """Verilator 批量故障注入"""
    os.makedirs(output_dir, exist_ok=True)
    
    print(f'\n{"="*60}')
    print(f'Verilator 故障注入: {circuit_name}')
    print(f'{"="*60}')
    t0 = time.time()
    
    # 1. 读取源文件
    with open(tb_path, 'r', encoding='utf-8') as f:
        tb_src = f.read()
    with open(verilog_path, 'r', encoding='utf-8') as f:
        net_text = f.read()
    
    # 1.2 检测网表中的真实模块名 (可能与文件名不同)
    module_match = re.search(r'\bmodule\s+(\w+)\s*[\(;]', net_text)
    dut_module_name = module_match.group(1) if module_match else circuit_name
    if dut_module_name != circuit_name:
        print(f'  [模块] 网表模块名: {dut_module_name} (文件名: {circuit_name})')
    
    # 1.5 解析注入目标 (使用检测到的模块名)
    all_targets = parse_targets_from_netlist(net_text, dut_module_name=dut_module_name)
    # 过滤时钟/复位信号
    legal_targets = [n for n in all_targets if not re.match(r'^(clk|clock|rst|reset)', n, re.I)]
    
    print(f'  [目标] 找到 {len(legal_targets)} 个可注入节点')
    total_faults = len(legal_targets) * 2
    print(f'  [故障] 总计 {total_faults} 个故障 (SA0+SA1)')
    
    # 2. 生成故障注入版网表 (插入 MUX)
    print(f'  [网表] 插入故障注入 MUX...')
    fi_netlist = generate_fault_injection_netlist(net_text, dut_module_name, legal_targets)
    
    # 2.5 预处理网表 (拆分超长行，解决 Verilator token 限制)
    fi_netlist_processed = preprocess_netlist_for_verilator(fi_netlist)
    fi_netlist_path = os.path.join(output_dir, f'{circuit_name}_fi.v')
    with open(fi_netlist_path, 'w', encoding='utf-8') as f:
        f.write(fi_netlist_processed)
    print(f'  [网表] 故障注入网表: {fi_netlist_path}')
    
    # 检查缓存
    res_json = os.path.join(output_dir, 'full_injection_results.json')
    golden_json = os.path.join(output_dir, 'golden_result.json')
    if os.path.exists(res_json) and os.path.exists(golden_json):
        print(f'  [跳过] 发现已有结果')
        try:
            with open(golden_json, 'r', encoding='utf-8') as gf:
                golden_data = json.load(gf)
            with open(res_json, 'r', encoding='utf-8') as rf:
                return golden_data['values'], json.load(rf)
        except:
            pass
    
    # 3. 生成带故障注入的 Testbench
    print(f'  [生成] 创建故障注入 Testbench...')
    batched_tb, fault_map = generate_fault_injection_testbench(tb_src, legal_targets, circuit_name)
    batched_tb_path = os.path.join(output_dir, 'tb_fault_inject.v')
    with open(batched_tb_path, 'w', encoding='utf-8') as f:
        f.write(batched_tb)
    
    # 4. Verilator 编译 (WSL + Clang)
    print(f'  [编译] Verilator 编译中 (WSL + Clang)...')
    obj_dir = os.path.join(output_dir, 'obj_dir')
    # Linux binary has no extension
    exe_name = 'Vtb' 
    # But for Windows path checks we might need to know where it lands. 
    # It will be in obj_dir/Vtb
    win_exe_path = os.path.join(obj_dir, exe_name)
    
    # Convert paths to WSL
    wsl_cell_lib = to_wsl_path(CELL_LIB)
    wsl_fi_netlist = to_wsl_path(fi_netlist_path)
    wsl_tb = to_wsl_path(batched_tb_path)
    wsl_obj_dir = to_wsl_path(obj_dir)
    
    # Calculate jobs
    compile_jobs = max(1, (os.cpu_count() or 4) - 2)
    
    # Verilator command with Clang
    # --binary: Build binary directly
    # --compiler clang: Use clang
    # -j: Parallel jobs
    verilator_cmd = (
        f'verilator --binary --timing -j {compile_jobs} '
        f'--compiler clang ' 
        f'--top-module tb '
        f'-Wno-fatal -Wno-WIDTHTRUNC -Wno-WIDTHEXPAND '
        f'-Wno-ASSIGNDLY -Wno-STMTDLY -Wno-MULTIDRIVEN '
        f'--error-limit 100 '
        f'-o {exe_name} --Mdir "{wsl_obj_dir}" '
        f'"{wsl_cell_lib}" "{wsl_fi_netlist}" "{wsl_tb}"'
    )
    
    print(f'  [Verilator] Generating and compiling C++ code (Clang, j={compile_jobs})...')
    rc, out = run_wsl_cmd(verilator_cmd, capture=True, timeout=600)
    if rc != 0:
        print(f'  [错误] Verilator 编译失败:')
        error_lines = out.split('\n')[:30]
        for line in error_lines:
            print(f'    {line}')
        return None, None
    
    compile_time = time.time() - t0
    print(f'  [编译完成] 耗时: {compile_time:.2f}s')
    
    # 5. Golden Run (No fault)
    print(f'  [Golden] 运行无故障仿真...')
    
    golden_obj_dir = os.path.join(output_dir, 'obj_dir_golden')
    
    # Golden paths
    wsl_orig_netlist = to_wsl_path(verilog_path)
    wsl_tb_orig = to_wsl_path(tb_path)
    wsl_golden_dir = to_wsl_path(golden_obj_dir)
    
    golden_verilator_cmd = (
        f'verilator --binary --timing -j {compile_jobs} '
        f'--compiler clang '
        f'--top-module tb '
        f'-Wno-fatal -Wno-WIDTHTRUNC -Wno-WIDTHEXPAND '
        f'-o Vtb_golden --Mdir "{wsl_golden_dir}" '
        f'"{wsl_cell_lib}" "{wsl_orig_netlist}" "{wsl_tb_orig}"'
    )
    
    rc, out = run_wsl_cmd(golden_verilator_cmd, capture=True, timeout=600)
    golden_compiled = (rc == 0)
    
    wsl_exe_path = f"{wsl_obj_dir}/{exe_name}"
    
    if not golden_compiled:
         print(f'  [警告] Golden 编译失败，尝试从注入版获取基准')
         gold_out = ""
         # Fallback to FI version with no fault
         cmd_str = f'"{wsl_exe_path}" +FAULT_ID=-1 +BATCH_START=0 +BATCH_END=1'
         rc, gold_out = run_wsl_cmd(cmd_str, capture=True, timeout=120)
    else:
        wsl_golden_exe = f"{wsl_golden_dir}/Vtb_golden"
        rc, gold_out = run_wsl_cmd(f'"{wsl_golden_exe}"', capture=True, timeout=120)
    
    golden_vals = []
    for line in gold_out.splitlines():
        # 尝试多种匹配模式
        m = OSUM_HEX_RE.search(line)
        if not m:
            m = ALT_HEX_RE.search(line)
        if m:
            s = m.group(1).lower()
            if 'x' in s or 'z' in s:
                golden_vals.append(-1)
            else:
                try:
                    golden_vals.append(int(s, 16))
                except:
                    golden_vals.append(-1)
    
    if not golden_vals:
        print('  [错误] 未找到 Golden 输出')
        print(f'  调试信息 (前10行): {gold_out.splitlines()[:10]}')
        return None, None
    
    print(f'  [Golden] 获取到 {len(golden_vals)} 个输出值')
    
    with open(golden_json, 'w', encoding='utf-8') as f:
        json.dump({'values': golden_vals}, f)
    
    # 6. 批量故障注入
    num_batches = min(WORKER_COUNT, total_faults)
    faults_per_batch = (total_faults + num_batches - 1) // num_batches
    
    jobs = []
    for i in range(num_batches):
        start = i * faults_per_batch
        end = min(start + faults_per_batch, total_faults)
        if start < total_faults:
            # Pass WSL path to worker
            jobs.append((wsl_exe_path, start, end, golden_vals, fault_map))
    
    print(f'  [运行] {total_faults} 故障, 分 {len(jobs)} 批, 每批约 {faults_per_batch} 故障')
    
    # 7. 并行运行
    node_results = {net: {'sa0': None, 'sa1': None} for net in legal_targets}
    run_start = time.time()
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=WORKER_COUNT) as executor:
        futures = {executor.submit(run_batch_worker, job): job for job in jobs}
        
        done_cnt = 0
        for future in concurrent.futures.as_completed(futures):
            done_cnt += 1
            batch_results = future.result()
            
            for net, res_dict in batch_results.items():
                if net in node_results:
                    if res_dict.get('sa0'):
                        node_results[net]['sa0'] = res_dict['sa0']
                    if res_dict.get('sa1'):
                        node_results[net]['sa1'] = res_dict['sa1']
            
            elapsed = time.time() - run_start
            progress_pct = 100 * done_cnt / len(jobs)
            eta = elapsed / done_cnt * (len(jobs) - done_cnt) if done_cnt > 0 else 0
            print(f"    批次: {done_cnt}/{len(jobs)} ({progress_pct:.0f}%) | "
                  f"耗时: {elapsed:.1f}s | 剩余: {eta:.0f}s", end='\r')
    
    print("")
    
    # 8. 保存结果
    with open(res_json, 'w', encoding='utf-8') as f:
        json.dump(node_results, f, indent=2)
    
    total_time = time.time() - t0
    run_time = time.time() - run_start
    
    success_count = sum(1 for net in node_results.values() 
                        for fault in [net['sa0'], net['sa1']] 
                        if fault and fault.get('status') == 'success')
    
    print(f'  [完成] 总时间: {total_time:.1f}s (编译: {compile_time:.1f}s, 运行: {run_time:.1f}s)')
    print(f'  [速率] {total_faults/max(total_time, 0.1):.1f} 故障/秒')
    print(f'  [成功] {success_count}/{total_faults} 故障测试成功')
    
    return golden_vals, node_results


def analyze_ranking_versioned(circuit_name: str, rank_file: str, node_results: Dict, 
                               output_dir: str, version: str):
    """
    分析排名覆盖率 - 流式处理版本
    
    优化: 不再将所有累积数据保存在内存中，而是逐行写入 CSV
    只保留关键节点(10%/20%/最终)的统计快照用于返回值
    """
    ranked_nodes = []
    if os.path.exists(rank_file):
        with open(rank_file, "r", encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if parts:
                    ranked_nodes.append(parts[0])
    
    valid_ranked_nodes = [n for n in ranked_nodes if n in node_results]
    
    if not valid_ranked_nodes:
        print(f"    [错误] 排名文件中没有有效节点: {rank_file}")
        return None

    total_nodes = len(valid_ranked_nodes)
    
    # 预计算关键检查点索引 (10%, 20%, 最终)
    idx_10pct = max(1, int(total_nodes * 0.10))
    idx_20pct = max(1, int(total_nodes * 0.20))
    
    # 只保存关键检查点的快照，不再累积全部数据
    snapshot_10pct = None
    snapshot_20pct = None
    snapshot_final = None
    
    csv_path = os.path.join(output_dir, f"cumulative_coverage_{version}.csv")
    fieldnames = ['topk', 'node', 'tested_nodes', 'detected_nodes', 'escaped_nodes', 
                  'detected_faults', 'escaped_faults', 'node_cov_pct', 'fault_cov_pct']
    
    # 流式写入: 打开文件后逐行写入，内存中不保留历史数据
    with open(csv_path, "w", newline="", encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        tested_nodes = 0
        detected_nodes = 0
        detected_faults = 0

        for k, node in enumerate(valid_ranked_nodes, start=1):
            tested_nodes += 1
            node_detected = False
            res = node_results.get(node, {'sa0': None, 'sa1': None})
            
            if res['sa0'] and res['sa0'].get('detected', False):
                detected_faults += 1
                node_detected = True
            if res['sa1'] and res['sa1'].get('detected', False):
                detected_faults += 1
                node_detected = True
            if node_detected:
                detected_nodes += 1

            fault_cov = (detected_faults / (tested_nodes * 2) * 100) if tested_nodes > 0 else 0
            node_cov = (detected_nodes / tested_nodes * 100) if tested_nodes > 0 else 0

            row = {
                'topk': k,
                'node': node,
                'tested_nodes': tested_nodes,
                'detected_nodes': detected_nodes,
                'escaped_nodes': tested_nodes - detected_nodes,
                'detected_faults': detected_faults,
                'escaped_faults': (tested_nodes * 2) - detected_faults,
                'node_cov_pct': f"{node_cov:.2f}",
                'fault_cov_pct': f"{fault_cov:.2f}"
            }
            
            # 立即写入磁盘，释放内存
            writer.writerow(row)
            
            # 只在关键检查点保存快照
            if k == idx_10pct:
                snapshot_10pct = (row['node_cov_pct'], row['fault_cov_pct'])
            if k == idx_20pct:
                snapshot_20pct = (row['node_cov_pct'], row['fault_cov_pct'])
            
            # 最后一行总是更新 final 快照
            snapshot_final = (row['node_cov_pct'], row['fault_cov_pct'])

    return {
        'total_nodes': total_nodes,
        'node_cov_10pct': snapshot_10pct[0] if snapshot_10pct else '0.00',
        'fault_cov_10pct': snapshot_10pct[1] if snapshot_10pct else '0.00',
        'node_cov_20pct': snapshot_20pct[0] if snapshot_20pct else '0.00',
        'fault_cov_20pct': snapshot_20pct[1] if snapshot_20pct else '0.00',
        'node_cov_final': snapshot_final[0] if snapshot_final else '0.00',
        'fault_cov_final': snapshot_final[1] if snapshot_final else '0.00'
    }


def load_timing_data() -> Dict[str, Dict]:
    """加载时间报告"""
    timing_data = {}
    if not os.path.exists(TIMING_REPORT_PATH):
        return timing_data
    try:
        with open(TIMING_REPORT_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                filename = row.get('filename', '')
                circuit_name = os.path.splitext(filename)[0]
                if circuit_name:
                    timing_data[circuit_name] = {
                        'nodes': row.get('nodes', ''),
                        'v1_total_time': row.get('v1_total_time', ''),
                        'v2_total_time': row.get('v2_total_time', ''),
                    }
    except Exception as e:
        print(f"[警告] 加载时间报告失败: {e}")
    return timing_data


def generate_summary_csv(circuit_coverage_data: Dict[str, Dict], output_path: str, 
                          injection_times: Dict[str, float] = None):
    """
    生成汇总 CSV - 增强版
    
    新增:
    - 前10%/20%与最终覆盖率的差值比较
    - 故障注入运行时间
    - 动态列：根据实际存在的版本生成列
    """
    timing_data = load_timing_data()
    injection_times = injection_times or {}
    
    # 扫描所有出现的版本键
    all_versions = set()
    for c_data in circuit_coverage_data.values():
        all_versions.update(c_data.keys())
    
    # 排序版本: v1 < v1_no_embed < v1_with_embed < v2 ...
    sorted_versions = sorted(list(all_versions))
    
    # 检测是否有 v1/v2 版本
    has_v1 = any(v.startswith('v1') for v in sorted_versions)
    has_v2 = any(v.startswith('v2') for v in sorted_versions)
    
    # 基础字段 - 动态生成 GNN 时间列
    fieldnames = ['circuit_name', 'nodes']
    if has_v1:
        fieldnames.append('gnn_time_v1')
    if has_v2:
        fieldnames.append('gnn_time_v2')
    fieldnames.append('injection_time')
    
    # 为每个版本添加覆盖率字段 + 差值字段 (节点覆盖率 + 故障覆盖率)
    for v in sorted_versions:
        fieldnames.extend([
            f'{v}_node_cov_10pct',   # 前10%节点覆盖率
            f'{v}_node_cov_20pct',   # 前20%节点覆盖率  
            f'{v}_node_cov_final',   # 最终节点覆盖率
            f'{v}_fault_cov_10pct',  # 前10%故障覆盖率
            f'{v}_fault_cov_20pct',  # 前20%故障覆盖率
            f'{v}_fault_cov_final',  # 最终故障覆盖率
            f'{v}_gap_10_final',     # 前10%与最终故障覆盖率的差值
            f'{v}_gap_20_final',     # 前20%与最终故障覆盖率的差值
        ])
    
    rows = []
    for circuit_name, versions_data in sorted(circuit_coverage_data.items()):
        timing = timing_data.get(circuit_name, {})
        row = {
            'circuit_name': circuit_name,
            'nodes': timing.get('nodes', ''),
            'injection_time': f"{injection_times.get(circuit_name, 0):.2f}" if circuit_name in injection_times else '',
        }
        # 动态添加 GNN 时间列
        if has_v1:
            row['gnn_time_v1'] = timing.get('v1_total_time', '')
        if has_v2:
            row['gnn_time_v2'] = timing.get('v2_total_time', '')
        
        for v in sorted_versions:
            vdata = versions_data.get(v, {})
            
            # 提取节点覆盖率
            node_cov_10 = vdata.get('node_cov_10pct', '0.00')
            node_cov_20 = vdata.get('node_cov_20pct', '0.00')
            node_cov_final = vdata.get('node_cov_final', '0.00')
            
            # 提取故障覆盖率
            fault_cov_10 = vdata.get('fault_cov_10pct', '0.00')
            fault_cov_20 = vdata.get('fault_cov_20pct', '0.00')
            fault_cov_final = vdata.get('fault_cov_final', '0.00')
            
            row[f'{v}_node_cov_10pct'] = node_cov_10
            row[f'{v}_node_cov_20pct'] = node_cov_20
            row[f'{v}_node_cov_final'] = node_cov_final
            row[f'{v}_fault_cov_10pct'] = fault_cov_10
            row[f'{v}_fault_cov_20pct'] = fault_cov_20
            row[f'{v}_fault_cov_final'] = fault_cov_final
            
            # 计算差值 (正值表示前N%覆盖率更高，负值表示覆盖率倒挂)
            try:
                gap_10 = float(fault_cov_10) - float(fault_cov_final)
                gap_20 = float(fault_cov_20) - float(fault_cov_final)
                row[f'{v}_gap_10_final'] = f"{gap_10:+.2f}"
                row[f'{v}_gap_20_final'] = f"{gap_20:+.2f}"
            except:
                row[f'{v}_gap_10_final'] = ''
                row[f'{v}_gap_20_final'] = ''
                
        rows.append(row)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    # 简洁的完成提示
    print(f"\n[汇总] 生成 {len(rows)} 个电路的覆盖率报告: {output_path}")



def main():
    if not os.path.exists(CELL_LIB):
        print(f"[错误] 未找到 {CELL_LIB}")
        return

    os.makedirs(BASE_RESULTS_DIR, exist_ok=True)
    
    rank_files = glob.glob(os.path.join(RANK_DIR, 'gnn_rank_*_v*.txt'))
    print(f"[开始] 故障注入与分析 (并行进程: {WORKER_COUNT})")

    circuit_ranks = {}
    for rank_f in rank_files:
        basename = os.path.basename(rank_f)
        m = re.match(r'gnn_rank_(.+)_(v[12])(_[a-z_]+)?\.txt', basename)
        if not m:
            continue
        circuit_name = m.group(1)
        version_base = m.group(2)
        suffix = m.group(3) or ""
        full_version = f"{version_base}{suffix}"
        
        if circuit_name not in circuit_ranks:
            circuit_ranks[circuit_name] = {}
        circuit_ranks[circuit_name][full_version] = rank_f

    circuit_coverage_data = {}
    injection_times = {}  # 记录每个电路的注入时间

    for circuit_name, versions in circuit_ranks.items():
        verilog_path = os.path.join(INPUT_NETLIST_DIR, f'{circuit_name}.v')
        tb_path = os.path.join(INPUT_NETLIST_DIR, f'tb_{circuit_name}.v')
        
        if not os.path.exists(verilog_path) or not os.path.exists(tb_path):
            print(f"[跳过] {circuit_name}: 文件不存在")
            continue

        circuit_out_dir = os.path.join(BASE_RESULTS_DIR, circuit_name)
        
        injection_start = time.time()
        golden, results = run_circuit_injection_batched(
            circuit_name, verilog_path, tb_path, circuit_out_dir
        )
        injection_times[circuit_name] = time.time() - injection_start
        
        if golden and results:
            circuit_coverage_data[circuit_name] = {}
            for version, rank_file in sorted(versions.items()):
                coverage_data = analyze_ranking_versioned(
                    circuit_name, rank_file, results, circuit_out_dir, version
                )
                if coverage_data:
                    circuit_coverage_data[circuit_name][version] = coverage_data

    summary_csv_path = os.path.join(BASE_RESULTS_DIR, "summary_coverage_timing.csv")
    generate_summary_csv(circuit_coverage_data, summary_csv_path, injection_times)

    print("\n" + "=" * 70)
    print("Verilator 批量故障注入完成!")
    print("=" * 70)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()

