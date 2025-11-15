#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全节点注入 + 评分 + 排名
直接对全节点进行注入，然后打一次分，进行排名
"""

import os, re, csv, time, math, subprocess, json, random, glob
from typing import List, Tuple, Dict
import numpy as np
import argparse

# ===== 配置 =====
ORIGINAL_NETLIST = 'pe.synth_dct.v'
TB_TEMPLATE      = 'tb_1.v'          # testbench 文件
CELL_LIB         = 'cells.v'
LOGDIR           = 'sim_logs'
os.makedirs(LOGDIR, exist_ok=True)

RESULTS_DIR = 'full_injection_results'
RANK_OUTPUT_DIR = 'gnn_ranks_1'
os.makedirs(RANK_OUTPUT_DIR, exist_ok=True)

STUCK_VALUES = [0, 1]
INJECT_DELAY_CYCLES = 5
MAX_VVP_SECONDS = 60
MAX_UNKNOWN_RATIO = 0.2

OSUM_HEX_RE = re.compile(r'^o_sum=([0-9a-fA-FxzXZ]+)')

# ======================== 工具函数 ========================
def run_cmd(cmd: List[str], capture=False) -> Tuple[int, str]:
    if capture:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        out, _ = proc.communicate()
        return proc.returncode, out
    else:
        rc = subprocess.call(cmd)
        return rc, ''

# ====== 注入 tb 生成函数 ======
def make_injected_tb(tb_text: str, target_net: str, stuck: int) -> str:
    safe_net = re.sub(r"[^A-Za-z0-9_$\[\]]", "_", target_net)
    inj_block = f"""
// --- fault injection block ---
initial begin
    wait (reset == 0);
    repeat({INJECT_DELAY_CYCLES}) @(posedge clock);
    force uut.{safe_net} = 1'b{stuck};
    $display("FAULT_INJECTED: {safe_net} sa{stuck}");
end
// --- end injection block ---
"""
    idx = tb_text.rfind('endmodule')
    if idx == -1: return tb_text + '\n' + inj_block
    return tb_text[:idx] + '\n' + inj_block + '\n' + tb_text[idx:]

# ====== 仿真函数 ======
def simulate(tb_file: str, logfile: str) -> bool:
    simv = os.path.join(LOGDIR, 'simv')
    vcd  = os.path.splitext(logfile)[0] + '.vcd'
    compile_cmd = ['iverilog','-g2012','-o',simv,
                   os.path.abspath(CELL_LIB),
                   os.path.abspath(ORIGINAL_NETLIST),
                   os.path.abspath(tb_file)]
    rc, out = run_cmd(compile_cmd, capture=True)
    if rc != 0:
        print('❌ iverilog 编译失败\n', out)
        return False
    with open(logfile,'w') as fo:
        proc = subprocess.Popen(['vvp', simv, f'+DUMPFILE={vcd}'], stdout=fo, stderr=subprocess.STDOUT, text=True)
        try: proc.wait(timeout=MAX_VVP_SECONDS)
        except subprocess.TimeoutExpired:
            proc.kill()
            print('❌ vvp 仿真超时')
            return False
    if proc.returncode != 0:
        print(f'❌ vvp 退出码 {proc.returncode}')
        return False
    return True

# ====== parse o_sum ======
def parse_osum_as_ints(logfile: str) -> Tuple[list,int]:
    vals, total, unknown = [], 0, 0
    try:
        with open(logfile,'r',encoding='utf-8',errors='ignore') as f:
            for line in f:
                m = OSUM_HEX_RE.match(line.strip())
                if not m: continue
                total += 1
                s = m.group(1).lower()
                if 'x' in s or 'z' in s:
                    unknown += 1
                    continue
                try: vals.append(int(s,16))
                except: unknown += 1
    except Exception as e:
        print(f'⚠️ 读取 {logfile} 失败: {e}')
    unk_ratio = (unknown/total) if total>0 else 1.0
    return vals, unk_ratio

# ====== 加载全节点注入结果 ======
def load_full_injection_results() -> Tuple[Dict, Dict]:
    """
    从 full_node_injection_and_statistics_1.py 生成的结果中加载节点得分
    返回: (node_scores, node_results)
    """
    results_file = os.path.join(RESULTS_DIR, 'full_injection_results.json')
    
    if not os.path.exists(results_file):
        print(f'❌ 未找到全节点注入结果文件: {results_file}')
        print('请先运行 full_node_injection_and_statistics_1.py 生成全节点注入结果')
        return None, None
    
    print(f'[INFO] 加载全节点注入结果: {results_file}')
    with open(results_file, 'r', encoding='utf-8') as f:
        node_results = json.load(f)
    
    # 计算每个节点的综合得分（基于 diff_count）
    node_scores = {}
    for node, faults in node_results.items():
        total_diff = 0
        for fault_type in ['sa0', 'sa1']:
            fault_result = faults.get(fault_type)
            if fault_result and fault_result.get('status') == 'success':
                total_diff += fault_result.get('diff_count', 0)
        node_scores[node] = total_diff
    
    print(f'✅ 已加载 {len(node_scores)} 个节点的得分')
    return node_scores, node_results

# ====== 从网表中提取所有节点 ======
def parse_targets_from_netlist(netlist_text: str, dut_module: str='pe') -> List[str]:
    """从网表中提取所有可注入节点"""
    def strip_comments(text: str) -> str:
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        text = re.sub(r'//.*', '', text)
        return text

    def split_decl_names(decl_body: str) -> List[str]:
        out = []
        decl_body = re.sub(r'\[[^]\n]*:[^]\n]*\]', '', decl_body)
        for chunk in decl_body.split(','):
            token = chunk.strip()
            if not token: continue
            m = re.match(r'^([A-Za-z_][A-Za-z0-9_$]*)(\[\d+\])?$', token)
            if m:
                out.append(m.group(0))
        return out

    def parse_ports(module_text: str) -> Tuple[set, set, set]:
        inputs, outputs, inouts = set(), set(), set()
        for stmt in module_text.split(';'):
            s = stmt.strip()
            if not s: continue
            if s.startswith('input'):
                body = re.sub(r'^input\s+((?:wire|reg|logic|signed|unsigned)\s+)*', '', s)
                inputs.update(split_decl_names(body))
            elif s.startswith('output'):
                body = re.sub(r'^output\s+((?:wire|reg|logic|signed|unsigned)\s+)*', '', s)
                outputs.update(split_decl_names(body))
            elif s.startswith('inout'):
                body = re.sub(r'^inout\s+((?:wire|reg|logic|signed|unsigned)\s+)*', '', s)
                inouts.update(split_decl_names(body))
        return inputs, outputs, inouts

    def parse_internal_nets(module_text: str) -> set:
        nets = set()
        for stmt in module_text.split(';'):
            s = stmt.strip()
            if not s: continue
            if s.startswith(('wire','reg','logic')):
                body = re.sub(r'^(wire|reg|logic)\s+((?:signed|unsigned)\s+)?', '', s)
                nets.update(split_decl_names(body))
        return nets

    def extract_module(text: str, modname: str) -> str:
        m = re.search(rf'\bmodule\s+{re.escape(modname)}\b.*?\bendmodule\b', text, flags=re.DOTALL)
        return m.group(0) if m else ''

    text = strip_comments(netlist_text)
    mod = extract_module(text, dut_module)
    if not mod: mod = text
    inputs, outputs, _ = parse_ports(mod)
    internals = parse_internal_nets(mod)
    targets = (outputs | internals) - inputs
    return sorted([n for n in targets if re.match(r'^[A-Za-z_][A-Za-z0-9_$]*(\[\d+\])?$', n)])

# ====== 主函数 ======
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verilog', type=str, default=ORIGINAL_NETLIST)
    parser.add_argument('--rank_output', type=str, default=RANK_OUTPUT_DIR)
    parser.add_argument('--rank_file', type=str, default='gnn_rank_1.txt')
    args = parser.parse_args()

    os.makedirs(args.rank_output, exist_ok=True)

    # ====== 加载全节点注入结果 ======
    print('='*70)
    print('加载全节点注入结果')
    print('='*70)
    node_scores, node_results = load_full_injection_results()
    if node_scores is None:
        return
    
    # ====== 从网表中提取所有节点（如果注入结果中没有的节点） ======
    print(f'\n[1/3] 读取网表文件: {args.verilog}')
    try:
        with open(args.verilog, 'r', encoding='utf-8') as f:
            netlist_text = f.read()
    except Exception as e:
        print(f'❌ 读取网表文件失败: {e}')
        return
    
    all_nodes = parse_targets_from_netlist(netlist_text)
    print(f'✅ 从网表中提取到 {len(all_nodes)} 个节点')
    
    # ====== 构建节点得分列表 ======
    print(f'\n[2/3] 构建节点得分列表并排序...')
    node_score_list = []
    
    # 对于有注入结果的节点，使用注入得分
    for node in all_nodes:
        if node in node_scores:
            score = node_scores[node]
            node_score_list.append((node, score))
        else:
            # 对于没有注入结果的节点，使用0分
            node_score_list.append((node, 0.0))
    
    # 按得分降序排序
    node_score_list = sorted(node_score_list, key=lambda x: x[1], reverse=True)
    
    print(f'✅ 已排序 {len(node_score_list)} 个节点')
    print(f'   最高得分: {node_score_list[0][1]:.6f} ({node_score_list[0][0]})')
    print(f'   最低得分: {node_score_list[-1][1]:.6f} ({node_score_list[-1][0]})')
    
    # ====== 保存排名结果 ======
    print(f'\n[3/3] 保存排名结果...')
    rank_file_path = os.path.join(args.rank_output, args.rank_file)
    
    with open(rank_file_path, 'w', encoding='utf-8') as f:
        for node, score in node_score_list:
            f.write(f"{node} {score:.6f}\n")
    
    print(f'✅ 排名结果已保存到: {rank_file_path}')
    
    # ====== 保存统计信息 ======
    stats_file = os.path.join(args.rank_output, 'rank_statistics.csv')
    with open(stats_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['total_nodes', 'nodes_with_score', 'nodes_without_score', 
                                               'max_score', 'min_score', 'avg_score', 'median_score'])
        
        nodes_with_score = sum(1 for _, score in node_score_list if score > 0)
        nodes_without_score = len(node_score_list) - nodes_with_score
        scores = [score for _, score in node_score_list]
        max_score = max(scores) if scores else 0
        min_score = min(scores) if scores else 0
        avg_score = sum(scores) / len(scores) if scores else 0
        median_score = sorted(scores)[len(scores)//2] if scores else 0
        
        writer.writeheader()
        writer.writerow({
            'total_nodes': len(node_score_list),
            'nodes_with_score': nodes_with_score,
            'nodes_without_score': nodes_without_score,
            'max_score': f'{max_score:.6f}',
            'min_score': f'{min_score:.6f}',
            'avg_score': f'{avg_score:.6f}',
            'median_score': f'{median_score:.6f}'
        })
    
    print(f'✅ 统计信息已保存到: {stats_file}')
    
    # ====== 打印前20名节点 ======
    print(f'\n前20名节点:')
    print('-'*70)
    print(f'{"排名":<6} {"节点名":<40} {"得分":<10}')
    print('-'*70)
    for idx, (node, score) in enumerate(node_score_list[:20], 1):
        print(f'{idx:<6} {node:<40} {score:<10.6f}')
    print('-'*70)

if __name__=='__main__':
    main()

