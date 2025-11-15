#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verilog 子图筛选 + golden 仿真 + stuck-at 注入 + topk 循环
兼容 iverilog，自动生成注入 testbench
"""

import os, re, csv, time, math, subprocess, json, random, glob
from typing import List, Tuple, Dict
import numpy as np
import networkx as nx
import argparse

# ===== 配置 =====
ORIGINAL_NETLIST = 'pe.synth_dct.v'
TB_TEMPLATE      = 'tb_1.v'          # testbench 文件
CELL_LIB         = 'cells.v'
LOGDIR           = 'sim_logs'
os.makedirs(LOGDIR, exist_ok=True)

GNNS_DIR = 'gnn_ranks'
os.makedirs(GNNS_DIR, exist_ok=True)

# 全节点注入结果目录
RESULTS_DIR = 'full_injection_results'

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

def parse_targets_from_netlist(netlist_text: str, dut_module: str='pe') -> List[str]:
    text = strip_comments(netlist_text)
    mod = extract_module(text, dut_module)
    if not mod: mod = text
    inputs, outputs, _ = parse_ports(mod)
    internals = parse_internal_nets(mod)
    targets = (outputs | internals) - inputs
    return sorted([n for n in targets if re.match(r'^[A-Za-z_][A-Za-z0-9_$]*(\[\d+\])?$', n)])

# ====== 修正版注入 tb 生成函数 ======
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

# ====== 解析 verilog 构建图 ======
SEQ_CELL_RE = re.compile(r'(DFF|SDFF|DFFR|DFFS|DFFX|DLH|DLR|LATCH)', re.IGNORECASE)
OUT_PORT_HINT = {'Z','ZN','Q','QN','OUT','Y','o_sum'}

def get_node_name(net):
    if hasattr(net,'name'): return str(net.name)
    elif hasattr(net,'var') and hasattr(net,'ptr'): return f"{get_node_name(net.var)}[{get_node_name(net.ptr)}]"
    elif isinstance(net,str): return net
    return str(net)

def parse_verilog_graph(filepath: str):
    from pyverilog.vparser.parser import parse
    ast,_ = parse([filepath])
    G = nx.DiGraph()
    node_map,id_counter = {},0
    output_nodes, seq_inst_ids = set(), set()

    def add_node(name, attrs):
        nonlocal id_counter
        if name not in node_map:
            node_map[name] = id_counter
            G.add_node(id_counter, name=name, **attrs)
            id_counter += 1
        else:
            nid = node_map[name]
            for k,v in attrs.items():
                if k not in G.nodes[nid]:
                    G.nodes[nid][k]=v
        return node_map[name]

    def extract_modules(node):
        if hasattr(node,'children'):
            for c in node.children():
                if c.__class__.__name__=='InstanceList':
                    cell_type = str(c.module)
                    for inst in c.instances:
                        inst_name = get_node_name(inst.name)
                        inst_id = add_node(inst_name, {'type': cell_type})
                        if SEQ_CELL_RE.search(cell_type or ''): seq_inst_ids.add(inst_id)
                        for cport in getattr(inst,'portlist',[]) or []:
                            port_name = str(cport.portname)
                            net_name = get_node_name(cport.argname).replace('.','_')
                            net_id = add_node(net_name, {'type':'wire'})
                            if port_name.upper() in OUT_PORT_HINT:
                                G.add_edge(inst_id, net_id)
                                output_nodes.add(net_id)
                            else:
                                G.add_edge(net_id, inst_id)
                extract_modules(c)
    extract_modules(ast)
    return G, node_map, output_nodes, seq_inst_ids

# ====== 子图结构特征 ======
def compute_struct_features(G, output_ids, seq_inst_ids):
    feats = {}
    pr = nx.pagerank(G)
    for n in G.nodes():
        feats[n] = {'pagerank': pr.get(n,0), 'dist_min_inv':0.0}
        dists = [nx.shortest_path_length(G,n,t) for t in output_ids if nx.has_path(G,n,t)]
        if dists: feats[n]['dist_min_inv'] = 1.0/(min(dists)+1)
    return feats

# ====== 获取可注入节点 ======
def get_injectable_nodes(G_sub: nx.DiGraph) -> list:
    injectable = []
    for n in G_sub.nodes:
        node_type = G_sub.nodes[n].get('type','').lower()
        name = G_sub.nodes[n].get('name','').lower()
        if node_type not in ('wire','reg'): continue
        if re.match(r'^(clk|clock|rst|reset|in|input)', name): continue
        if '[' in name or ']' in name: continue
        injectable.append(G_sub.nodes[n].get('name',''))
    return injectable

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


def generate_randomized_rank(node_list_with_scores: List[Tuple[str, float]], 
                             random_seed: int, 
                             noise_level: float = 0.3) -> List[Tuple[str, float]]:
    """
    生成随机化的排名列表
    使用多种随机化策略增强随机性，提高故障覆盖率的随机性
    
    Args:
        node_list_with_scores: [(node_name, score), ...] 已排序的节点列表
        random_seed: 随机种子
        noise_level: 噪声水平 (0.0-1.0)，越大随机性越强
    """
    if not node_list_with_scores:
        return []
    
    random.seed(random_seed)
    num_nodes = len(node_list_with_scores)
    
    # 提取得分范围
    scores = [s for _, s in node_list_with_scores]
    if not scores:
        return node_list_with_scores
    
    min_score, max_score = min(scores), max(scores)
    score_range = max_score - min_score if max_score > min_score else 1.0
    
    # 策略1: 大幅增加噪声水平，增强扰动
    effective_noise_level = noise_level * 2.0  # 增加噪声倍数
    
    # 策略2: 使用多种噪声分布（正态分布 + 均匀分布混合）
    perturbed = []
    for node, score in node_list_with_scores:
        # 混合噪声：70%均匀分布 + 30%正态分布
        if random.random() < 0.7:
            # 均匀分布噪声
            noise = random.uniform(-effective_noise_level * score_range, effective_noise_level * score_range)
        else:
            # 正态分布噪声（更大的随机性）
            noise = random.gauss(0, effective_noise_level * score_range * 0.5)
            noise = max(-effective_noise_level * score_range * 1.5, 
                       min(effective_noise_level * score_range * 1.5, noise))
        
        perturbed_score = score + noise
        perturbed.append((node, perturbed_score))
    
    # 按扰动后的得分重新排序
    result = sorted(perturbed, key=lambda x: x[1], reverse=True)
    
    # 策略3: 增强的交换操作 - 不仅交换相邻节点，还交换远距离节点
    # 相邻节点交换（概率更高）
    for i in range(len(result) - 1):
        if random.random() < 0.4:  # 40% 概率交换相邻节点
            result[i], result[i+1] = result[i+1], result[i]
    
    # 远距离节点交换（增加随机性）
    num_long_swaps = max(1, num_nodes // 4)  # 交换约25%的节点
    for _ in range(num_long_swaps):
        # 随机选择两个距离较远的节点
        i = random.randint(0, num_nodes - 1)
        # 计算允许的最大跳跃距离（至少跳20%的位置）
        max_jump = max(1, int(num_nodes * 0.2))
        jump = random.randint(max_jump, min(max_jump * 3, num_nodes - 1))
        j = (i + jump) % num_nodes
        
        if random.random() < 0.6:  # 60%概率进行交换
            result[i], result[j] = result[j], result[i]
    
    # 策略4: 随机分组后重组（Fisher-Yates shuffle 变体）
    # 将列表分成多个随机大小的组，然后随机打乱组内顺序
    if num_nodes > 3:
        # 随机分组
        group_size = random.randint(2, max(3, num_nodes // 3))
        num_groups = (num_nodes + group_size - 1) // group_size
        
        for group_idx in range(num_groups):
            start_idx = group_idx * group_size
            end_idx = min(start_idx + group_size, num_nodes)
            
            if end_idx - start_idx > 1:
                # 对组内元素进行随机重排
                group = result[start_idx:end_idx]
                random.shuffle(group)
                result[start_idx:end_idx] = group
    
    # 策略5: 局部随机重排 - 对前N%和后M%的节点进行额外的随机化
    if num_nodes > 5:
        # 对前20%的节点进行随机化
        top_count = max(1, int(num_nodes * 0.2))
        top_group = result[:top_count]
        random.shuffle(top_group)
        result[:top_count] = top_group
        
        # 对后30%的节点进行随机化
        bottom_count = max(1, int(num_nodes * 0.3))
        bottom_group = result[-bottom_count:]
        random.shuffle(bottom_group)
        result[-bottom_count:] = bottom_group
    
    # 策略6: 基于位置的加权随机交换
    # 允许节点随机跳跃到新的位置（不仅仅是相邻交换）
    for _ in range(max(1, num_nodes // 3)):
        i = random.randint(0, num_nodes - 1)
        # 允许节点跳跃到列表的任何位置（但有偏好，跳跃距离服从几何分布）
        max_jump_dist = min(num_nodes - 1, int(num_nodes * 0.5))
        jump_dist = random.choices(
            range(1, max_jump_dist + 1),
            weights=[1.0 / (d + 1) for d in range(1, max_jump_dist + 1)]  # 距离越远权重越小
        )[0]
        
        direction = random.choice([-1, 1])
        new_pos = max(0, min(num_nodes - 1, i + direction * jump_dist))
        
        if random.random() < 0.5:  # 50%概率进行跳跃交换
            result[i], result[new_pos] = result[new_pos], result[i]
    
    return result


# ====== 主函数 ======
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verilog', type=str, default=ORIGINAL_NETLIST)
    parser.add_argument('--topk_csv', type=str, default='topk.csv')
    parser.add_argument('--timing_csv', type=str, default='timing.csv')
    parser.add_argument('--gnn_ranks', type=str, default=GNNS_DIR)
    parser.add_argument('--keep_ratio', type=float, default=0.2, help='输出排名节点数 = topk × keep_ratio')
    parser.add_argument('--num_runs', type=int, default=100, help='每个topk生成的随机化文件数量')
    parser.add_argument('--noise_level', type=float, default=0.5, help='随机噪声水平 (0.0-1.0)，默认0.5以增强随机性')
    args = parser.parse_args()

    os.makedirs(args.gnn_ranks, exist_ok=True)

    # ====== 加载全节点注入结果 ======
    print('='*70)
    print('加载全节点注入结果')
    print('='*70)
    node_scores, node_results = load_full_injection_results()
    if node_scores is None:
        return
    
    # ====== topk.csv ======
    print(f'\n[1/4] 读取 topk 配置: {args.topk_csv}')
    topk_list = []
    with open(args.topk_csv, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        if 'topk' not in reader.fieldnames: 
            print("❌ topk.csv 没有 topk 列")
            return
        for row in reader:
            try: 
                topk_list.append(int(row['topk'].strip()))
            except: 
                continue
    if not topk_list: 
        print("❌ 没有有效 topk 数据")
        return
    print(f"✅ topk: {topk_list}")

    # ====== 解析网表构建图 ======
    print(f'\n[2/4] 解析网表构建图: {args.verilog}')
    G, node_map, output_ids, seq_inst_ids = parse_verilog_graph(args.verilog)
    feats_full = compute_struct_features(G, output_ids, seq_inst_ids)
    print(f'✅ 图节点数={G.number_of_nodes()}, 边数={G.number_of_edges()}')

    # ====== 为每个 topk 生成随机化的 gnn_rank 文件（使用子图筛选） ======
    print(f'\n[3/4] 对每个 topk 进行子图筛选并生成 {args.num_runs} 个随机化 gnn_rank 文件...')
    csv_rows = []
    
    for idx, k in enumerate(topk_list, 1):
        print(f'\n  [{idx}/{len(topk_list)}] Processing topk={k}')
        
        # ====== 子图筛选机制（仿照 unsup_sensitivity copy.py） ======
        # 1. 使用结构特征（pagerank + dist_min_inv）对全图节点排序
        scores = np.array([feats_full[n]['pagerank'] + feats_full[n]['dist_min_inv'] for n in G.nodes()])
        node_ids_all = np.array(list(G.nodes()))
        topk_nids = node_ids_all[scores.argsort()[::-1][:k]]
        
        # 2. 构建子图：topk节点 + 它们的邻居（前驱和后继）
        sub_nodes = set(topk_nids)
        for n in topk_nids:
            sub_nodes |= set(G.predecessors(n)) | set(G.successors(n))
        G_sub = G.subgraph(sub_nodes).copy()
        
        print(f'    [子图] 子图节点数={G_sub.number_of_nodes()}, 边数={G_sub.number_of_edges()}')
        
        # 3. 在子图上筛选可注入节点
        injectable_nodes = get_injectable_nodes(G_sub)
        print(f'    [子图] 可注入节点数={len(injectable_nodes)}')
        
        if not injectable_nodes:
            print(f'    ⚠️ topk={k}: 子图中没有可注入节点，跳过')
            continue
        
        # 4. 从全节点注入结果中获取可注入节点的得分
        injectable_with_scores = []
        for node_name in injectable_nodes:
            # 如果节点在全节点注入结果中，使用其得分
            if node_name in node_scores:
                injectable_with_scores.append((node_name, node_scores[node_name]))
            else:
                # 如果不在全节点注入结果中，在子图中找到对应的节点ID，使用结构特征得分作为备选
                node_id = None
                for nid in G_sub.nodes():
                    if G_sub.nodes[nid].get('name') == node_name:
                        node_id = nid
                        break
                
                # 如果在子图中找到，使用结构特征得分
                if node_id is not None and node_id in feats_full:
                    struct_score = feats_full[node_id]['pagerank'] + feats_full[node_id]['dist_min_inv']
                    injectable_with_scores.append((node_name, struct_score))
                else:
                    # 如果都找不到，使用0.0得分
                    injectable_with_scores.append((node_name, 0.0))
        
        # 按得分排序
        injectable_with_scores = sorted(injectable_with_scores, key=lambda x: x[1], reverse=True)
        
        # 5. 计算要保存的节点数量（基于 keep_ratio）
        top_count = max(1, math.ceil(k * args.keep_ratio))
        
        # 6. 为每个 run 生成随机化的排名
        for run_id in range(1, args.num_runs + 1):
            # 生成随机化排名
            randomized_rank = generate_randomized_rank(
                injectable_with_scores[:top_count], 
                random_seed=k * 1000 + run_id,  # 每个topk和run有唯一种子
                noise_level=args.noise_level
            )
            
            # 生成文件名
            out_txt = os.path.join(args.gnn_ranks, f"gnn_rank_{k}_run{run_id}.txt")
            with open(out_txt, 'w', encoding='utf-8') as f:
                for n, s in randomized_rank:
                    f.write(f"{n} {s:.6f}\n")
        
        print(f'    ✅ 已生成 {args.num_runs} 个 gnn_rank 文件 (gnn_rank_{k}_run1.txt ~ gnn_rank_{k}_run{args.num_runs}.txt)')
        
        # 记录 CSV 数据（不包含时间）
        csv_rows.append({
            'topk': k,
            'sub_nodes': G_sub.number_of_nodes(),
            'sub_edges': G_sub.number_of_edges(),
            'injectable_nodes': len(injectable_nodes),
            'num_rank_files': args.num_runs
        })

    # 保存 CSV（不包含时间字段）
    print(f'\n[4/4] 保存统计信息...')
    with open(args.timing_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['topk', 'sub_nodes', 'sub_edges', 'injectable_nodes', 'num_rank_files'])
        writer.writeheader()
        writer.writerows(csv_rows)
    print(f"✅ 统计信息已写入 {args.timing_csv}")

if __name__=='__main__':
    main()
