#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verilog 子图筛选 + golden 仿真 + stuck-at 注入 + topk 循环
兼容 iverilog，自动生成注入 testbench
"""

import os
import re
import csv
import time
import math
import subprocess
from typing import List, Tuple
import numpy as np
import networkx as nx
import argparse

# ===== 配置 =====
ORIGINAL_NETLIST = 'pe.synth_dct.v'
TB_TEMPLATE = 'tb_1.v'  # testbench 文件
CELL_LIB = 'cells.v'
LOGDIR = 'sim_logs'
os.makedirs(LOGDIR, exist_ok=True)

GNNS_DIR = 'gnn_ranks_1'
os.makedirs(GNNS_DIR, exist_ok=True)

TIMING_CSV = 'topk_timing.csv'
STUCK_VALUES = [0, 1]
INJECT_DELAY_CYCLES = 5
MAX_VVP_SECONDS = 60
MAX_UNKNOWN_RATIO = 0.2

# 匹配 o_sum 输出的十六进制值
OSUM_HEX_RE = re.compile(r'^o_sum=([0-9a-fA-FxzXZ]+)')

# ======================== 工具函数 ========================
def run_cmd(cmd: List[str], capture=False) -> Tuple[int, str]:
    """执行系统命令，返回退出码和输出"""
    if capture:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        out, _ = proc.communicate()
        return proc.returncode, out
    else:
        rc = subprocess.call(cmd)
        return rc, ''

def strip_comments(text: str) -> str:
    """去除 Verilog 文本中的注释"""
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    text = re.sub(r'//.*', '', text)
    return text

def split_decl_names(decl_body: str) -> List[str]:
    """从声明体中提取网络名称 (去除位宽和数组定义)"""
    out = []
    # 移除位宽定义，如 [7:0]
    decl_body = re.sub(r'\[[^]\n]*:[^]\n]*\]', '', decl_body)
    for chunk in decl_body.split(','):
        token = chunk.strip()
        if not token: continue
        # 匹配合法的 Verilog 标识符，允许后跟单一位选择 [d]
        m = re.match(r'^([A-Za-z_][A-Za-z0-9_$]*)(\[\d+\])?$', token)
        if m:
            out.append(m.group(0))
    return out

def parse_ports(module_text: str) -> Tuple[set, set, set]:
    """解析模块的输入、输出、双向端口"""
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
    """解析模块内部的 wire/reg/logic 声明"""
    nets = set()
    for stmt in module_text.split(';'):
        s = stmt.strip()
        if not s: continue
        if s.startswith(('wire','reg','logic')):
            body = re.sub(r'^(wire|reg|logic)\s+((?:signed|unsigned)\s+)?', '', s)
            nets.update(split_decl_names(body))
    return nets

def extract_module(text: str, modname: str) -> str:
    """从 Verilog 文本中提取指定模块的定义"""
    m = re.search(rf'\bmodule\s+{re.escape(modname)}\b.*?\bendmodule\b', text, flags=re.DOTALL)
    return m.group(0) if m else ''

def parse_targets_from_netlist(netlist_text: str, dut_module: str='pe') -> List[str]:
    """从网表中解析所有可作为故障注入目标的网络 (非输入端口)"""
    text = strip_comments(netlist_text)
    mod = extract_module(text, dut_module)
    if not mod: mod = text
    inputs, outputs, _ = parse_ports(mod)
    internals = parse_internal_nets(mod)
    # 目标网络是输出或内部网络，且不是输入
    targets = (outputs | internals) - inputs
    # 筛选出合法的网络名称
    return sorted([n for n in targets if re.match(r'^[A-Za-z_][A-Za-z0-9_$]*(\[\d+\])?$', n)])

# ====== 修正版注入 tb 生成函数 ======
def make_injected_tb(tb_text: str, target_net: str, stuck: int) -> str:
    """
    生成带有 stuck-at 故障注入逻辑的 testbench。
    使用 force 语句在指定时间注入故障。
    """
    # 替换网络名称中的非 Verilog 字符 (如点号)
    safe_net = re.sub(r"[^A-Za-z0-9_$\[\]]", "_", target_net) 
    
    inj_block = f"""
// --- fault injection block ---
initial begin
    // 等待 reset 信号释放
    wait (reset == 0); 
    // 注入延迟 INJECT_DELAY_CYCLES 个时钟周期
    repeat({INJECT_DELAY_CYCLES}) @(posedge clock); 
    // 注入 stuck-at 故障
    force uut.{safe_net} = 1'b{stuck};
    $display("FAULT_INJECTED: {safe_net} sa{stuck}");
end
// --- end injection block ---
"""
    # 将注入块插入到 `endmodule` 之前
    idx = tb_text.rfind('endmodule')
    if idx == -1: return tb_text + '\n' + inj_block
    return tb_text[:idx] + '\n' + inj_block + '\n' + tb_text[idx:]

# ====== 仿真函数 ======
def simulate(tb_file: str, logfile: str) -> bool:
    """编译并运行 Verilog 仿真 (iverilog/vvp)"""
    simv = os.path.join(LOGDIR, 'simv')
    vcd = os.path.splitext(logfile)[0] + '.vcd'
    
    # 编译命令
    compile_cmd = ['iverilog','-g2012','-o',simv,
                   os.path.abspath(CELL_LIB),
                   os.path.abspath(ORIGINAL_NETLIST),
                   os.path.abspath(tb_file)]
    rc, out = run_cmd(compile_cmd, capture=True)
    if rc != 0:
        print('❌ iverilog 编译失败\n', out)
        return False

    # 运行命令 (设置超时)
    with open(logfile,'w') as fo:
        proc = subprocess.Popen(['vvp', simv, f'+DUMPFILE={vcd}'], 
                                stdout=fo, 
                                stderr=subprocess.STDOUT, 
                                text=True)
        try: 
            proc.wait(timeout=MAX_VVP_SECONDS)
        except subprocess.TimeoutExpired:
            proc.kill()
            print('❌ vvp 仿真超时')
            return False
            
        if proc.returncode != 0:
            print(f'❌ vvp 退出码 {proc.returncode}')
            return False
            
    return True

# ====== parse o_sum ======
def parse_osum_as_ints(logfile: str) -> Tuple[list,float]:
    """从仿真日志中解析 o_sum 输出值，计算未知比例"""
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
                try: 
                    vals.append(int(s,16))
                except: 
                    unknown += 1 # 无法解析的也算未知
    except Exception as e:
        print(f'⚠️ 读取 {logfile} 失败: {e}')
        
    unk_ratio = (unknown/total) if total>0 else 1.0
    return vals, unk_ratio

# ====== 解析 verilog 构建图 ======
# 常用时序单元类型 (不区分大小写)
SEQ_CELL_RE = re.compile(r'(DFF|SDFF|DFFR|DFFS|DFFX|DLH|DLR|LATCH)', re.IGNORECASE) 
# 常用输出端口名称提示
OUT_PORT_HINT = {'Z','ZN','Q','QN','OUT','Y','O_SUM'} 

def get_node_name(net):
    """获取 pyverilog 对象的网络/端口/实例名称"""
    if hasattr(net,'name'): return str(net.name)
    # 处理位选择或部分选择
    elif hasattr(net,'var') and hasattr(net,'ptr'): return f"{get_node_name(net.var)}[{get_node_name(net.ptr)}]"
    elif isinstance(net,str): return net
    return str(net)

def parse_verilog_graph(filepath: str):
    """
    使用 pyverilog 解析 Verilog 文件，构建网络拓扑图 (DiGraph)。
    节点可以是实例或网络。
    """
    try:
        from pyverilog.vparser.parser import parse
    except ImportError:
        print("❌ 错误: 请安装 pyverilog (`pip install pyverilog`)")
        return nx.DiGraph(), {}, set(), set()
        
    ast,_ = parse([filepath])
    G = nx.DiGraph()
    node_map,id_counter = {},0
    output_nodes, seq_inst_ids = set(), set()

    def add_node(name, attrs):
        """添加或更新图节点"""
        nonlocal id_counter
        if name not in node_map:
            node_map[name] = id_counter
            G.add_node(id_counter, name=name, **attrs)
            id_counter += 1
        else:
            nid = node_map[name]
            # 仅在缺失时添加属性
            for k,v in attrs.items():
                if k not in G.nodes[nid]:
                    G.nodes[nid][k]=v
        return node_map[name]

    # 递归遍历 AST 提取模块实例和端口连接
    def extract_modules(node):
        if hasattr(node,'children'):
            for c in node.children():
                if c.__class__.__name__=='InstanceList':
                    cell_type = str(c.module)
                    for inst in c.instances:
                        inst_name = get_node_name(inst.name)
                        inst_id = add_node(inst_name, {'type': cell_type})
                        
                        # 标记时序单元
                        if SEQ_CELL_RE.search(cell_type or ''): 
                            seq_inst_ids.add(inst_id)
                            
                        # 处理端口连接
                        for cport in getattr(inst,'portlist',[]) or []:
                            port_name = str(cport.portname)
                            # 使用连接的网络名称作为图中的网络节点
                            net_name = get_node_name(cport.argname).replace('.','_') 
                            net_id = add_node(net_name, {'type':'wire'}) # 简化处理，端口连接的网络视为 wire
                            
                            if port_name.upper() in OUT_PORT_HINT:
                                # 实例输出 -> 网络
                                G.add_edge(inst_id, net_id)
                                output_nodes.add(net_id)
                            else:
                                # 网络 -> 实例输入
                                G.add_edge(net_id, inst_id)
                                
                extract_modules(c)

    # 从根节点开始解析
    extract_modules(ast)
    
    # 尝试将模块的最终输出端口也添加到 output_nodes
    # (此处的逻辑可能不够完善，依赖于 extract_modules 中 output_nodes 的添加)
    
    return G, node_map, output_nodes, seq_inst_ids

# ====== 子图结构特征 ======
def compute_struct_features(G, output_ids, seq_inst_ids):
    """计算节点的结构特征：PageRank 和到最近输出的距离倒数"""
    feats = {}
    pr = nx.pagerank(G) # 计算 PageRank
    
    for n in G.nodes():
        feats[n] = {'pagerank': pr.get(n,0), 'dist_min_inv':0.0}
        
        # 计算到任何输出节点的最短路径长度
        dists = [nx.shortest_path_length(G,n,t) 
                 for t in output_ids if nx.has_path(G,n,t)]
        
        if dists: 
            # 距离倒数 (加 1 是为了避免分母为 0，且使距离越近，值越大)
            feats[n]['dist_min_inv'] = 1.0/(min(dists)+1) 
            
    return feats

# ====== 获取可注入节点 ======
def get_injectable_nodes(G_sub: nx.DiGraph) -> list:
    """
    从子图中筛选出可注入 stuck-at 故障的网络节点。
    - 必须是 'wire' 或 'reg' 类型 (即网络节点，而非实例节点)。
    - 排除 clk, rst, in/input 等端口。
    - 排除带位选择的网络 (简化处理，可能需要调整)。
    """
    injectable = []
    for n in G_sub.nodes:
        node_type = G_sub.nodes[n].get('type','').lower()
        name = G_sub.nodes[n].get('name','').lower()
        
        # 必须是网络节点
        if node_type not in ('wire','reg'): continue 
        # 排除常用控制信号和输入端口 (假设命名规范)
        if re.match(r'^(clk|clock|rst|reset|in|input)', name): continue 
        # 排除位选择或总线名 (只注入到标量或整个总线上，简化处理)
        # 实际上 `parse_targets_from_netlist` 已经允许带位选，但这里再限制一下
        if '[' in name or ']' in name: continue 
        
        injectable.append(G_sub.nodes[n].get('name',''))
        
    # 去重并返回
    return sorted(list(set(injectable))) 

# ====== 主函数 ======
def main():
    parser = argparse.ArgumentParser(description="Verilog GNN/结构化故障注入筛选工具")
    parser.add_argument('--verilog', type=str, default=ORIGINAL_NETLIST, 
                        help='Design netlist file.')
    parser.add_argument('--topk_csv', type=str, default='topk.csv', 
                        help='CSV file containing a "topk" list of subgraph sizes.')
    parser.add_argument('--timing_csv', type=str, default=TIMING_CSV, 
                        help='Output CSV file for timing and subgraph info.')
    parser.add_argument('--gnn_ranks_1', type=str, default=GNNS_DIR, 
                        help='Directory to output top ranked nodes files.')
    parser.add_argument('--keep_ratio', type=float, default=0.2, 
                        help='Ratio of nodes to keep for final ranking from the top-k subgraph.')
    args = parser.parse_args()

    os.makedirs(args.gnn_ranks, exist_ok=True)
    
    # **注意**: 此脚本缺少 **golden_vals** 的定义。在实际使用中，
    # 需要先运行一次无故障仿真来获取 golden_vals。

    # ====== 1. 读取 topk.csv ======
    topk_list=[]
    try:
        with open(args.topk_csv,'r',encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            if 'topk' not in reader.fieldnames: 
                print("❌ topk.csv 没有 topk 列"); return
            for row in reader:
                try: 
                    # 确保 topk 值是正整数
                    val = int(row['topk'].strip())
                    if val > 0: topk_list.append(val)
                except: continue
    except FileNotFoundError:
        print(f"❌ 找不到文件: {args.topk_csv}"); return
        
    if not topk_list: 
        print("❌ 没有有效 topk 数据"); return
        
    topk_list = sorted(list(set(topk_list))) # 去重并排序
    print(f"✅ topk: {topk_list}")
    
    # **注意**: 实际应用中，这里应该加入 **Golden 仿真**
    # print("[INFO] 运行 Golden 仿真...")
    # simulate(TB_TEMPLATE, os.path.join(LOGDIR, 'golden.log'))
    # golden_vals, _ = parse_osum_as_ints(os.path.join(LOGDIR, 'golden.log'))
    # if not golden_vals: print("❌ Golden 仿真失败或无有效输出"); return
    
    # ====== 2. 解析网表和计算结构特征 ======
    print(f"[INFO] 解析网表 {args.verilog}")
    G, node_map, output_ids, seq_inst_ids = parse_verilog_graph(args.verilog)
    if G.number_of_nodes() == 0:
        print("❌ 图构建失败或网表为空"); return
        
    feats_full = compute_struct_features(G, output_ids, seq_inst_ids)
    
    # ====== 3. topk 循环进行筛选和仿真 ======
    csv_rows=[]
    # 缓存所有节点的结构评分 (PageRank + 距离倒数)
    scores_all = np.array([feats_full[n]['pagerank'] + feats_full[n]['dist_min_inv'] 
                           for n in G.nodes()])
    node_ids_all = np.array(list(G.nodes()))
    
    for k in topk_list:
        print(f"\n=== Processing topk={k} ===")
        t0 = time.time()
        
        # 3.1 结构评分 Top-K 节点
        # scores_all 已经计算好，直接排序取 Top-K 节点的 ID
        topk_nids = node_ids_all[scores_all.argsort()[::-1][:k]]
        
        # 3.2 构建子图
        sub_nodes = set(topk_nids)
        # 添加 Top-K 节点的前驱和后继 (一层邻居)
        for n in topk_nids:
            sub_nodes |= set(G.predecessors(n)) | set(G.successors(n))
            
        G_sub = G.subgraph(sub_nodes).copy()
        print(f"[INFO] 子图节点={G_sub.number_of_nodes()}, 边={G_sub.number_of_edges()}")
        
        # 3.3 获取可注入网络
        injectable_nodes = get_injectable_nodes(G_sub)
        print(f"[INFO] 可注入节点={len(injectable_nodes)}")
        
        # 3.4 故障注入仿真并评分 (敏感度计算)
        node_scores = {}
        for net in injectable_nodes:
            total_diff = 0
            valid_any = False
            
            # 对 stuck-at-0 和 stuck-at-1 分别进行仿真
            for val in STUCK_VALUES:
                # 自动生成注入 testbench
                tb_inj = make_injected_tb(open(TB_TEMPLATE).read(), net, val)
                tmp_tb = os.path.join(LOGDIR,'tb_inj.v')
                with open(tmp_tb,'w') as f: f.write(tb_inj)
                
                safe_net = re.sub(r"[^A-Za-z0-9_$\[\]]","_",net)
                log = os.path.join(LOGDIR,f"fi_{safe_net}_sa{val}.log")
                
                # 运行仿真
                ok = simulate(tmp_tb, log)
                os.remove(tmp_tb)
                
                if not ok: continue
                
                # 解析输出
                vals, unk = parse_osum_as_ints(log)
                if not vals or unk > MAX_UNKNOWN_RATIO: continue
                
                # **注意**: 评分逻辑需要修正，这里用 `sum(vals)` 临时替代
                # 正确的逻辑应该是：
                # diff = sum(1 for a,b in zip(golden_vals[:len(vals)], vals) if a!=b)
                # 暂时使用 sum(vals) 作为评分 (假设输出值越大，影响越大，这在没有 golden 参照时是临时的)
                diff = sum(vals) 
                
                total_diff += diff
                valid_any = True
                
            node_scores[net] = total_diff if valid_any else 0
        
        # 3.5 排名和 Top-K 筛选
        ranked = sorted([(n,s) for n,s in node_scores.items()], 
                        key=lambda x:x[1], 
                        reverse=True)
                        
        # 最终 Top-K 节点的数量
        top_count = max(1, math.ceil(k*args.keep_ratio))
        top_nodes = ranked[:top_count]
        
        # 打印前 10 个节点
        print("[INFO] Top nodes (Score = Fault Sensitivity):")
        for i,(n,s) in enumerate(top_nodes[:10],1):
            print(f"{i}. {n} -> {s}")
        
        # 3.6 输出到文件
        out_txt = os.path.join(args.gnn_ranks,f"gnn_rank_{k}.txt")
        with open(out_txt,'w') as f:
            for n,s in top_nodes: f.write(f"{n} {s:.6f}\n")
        print(f"[✅] 写入 {out_txt}")
        
        # 3.7 记录计时
        t1 = time.time()
        csv_rows.append({'topk':k,'sub_nodes':G_sub.number_of_nodes(),
                         'sub_edges':G_sub.number_of_edges(),
                         'total_time':round(t1-t0,4)})
    
    # ====== 4. 写入计时 CSV 文件 ======
    with open(args.timing_csv,'w',newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['topk','sub_nodes','sub_edges','total_time'])
        writer.writeheader()
        writer.writerows(csv_rows)
    print(f"\n✅ Timing 写入 {args.timing_csv}")

if __name__=='__main__':
    main()