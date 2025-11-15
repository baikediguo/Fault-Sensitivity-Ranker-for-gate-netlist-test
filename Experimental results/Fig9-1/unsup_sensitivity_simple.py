#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
无监督敏感度排名器 - 简化版
============================

功能：对每个topk值生成单一的确定性排名结果

使用方法：
---------
# 默认配置
python unsup_sensitivity_simple.py

# 自定义配置
python unsup_sensitivity_simple.py --epochs 100 --hidden 64
"""

import os
import re
import math
import argparse
import random
import numpy as np
import networkx as nx
from typing import List, Tuple, Dict, Set
import time
import csv

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.nn import GINConv, BatchNorm

from pyverilog.vparser.parser import parse

# -----------------------
# Utils
# -----------------------
def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    try:
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
    except Exception:
        pass

def read_text(path: str) -> str:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def safe_norm(x, eps=1e-12):
    d = x.norm(dim=-1, keepdim=True) + eps
    return x / d

def minmax_norm(arr: np.ndarray) -> np.ndarray:
    if len(arr) == 0:
        return arr
    a = np.asarray(arr, dtype=float)
    lo, hi = np.nanmin(a), np.nanmax(a)
    if not np.isfinite(lo) or not np.isfinite(hi) or abs(hi - lo) < 1e-12:
        return np.zeros_like(a)
    return (a - lo) / (hi - lo)

def z2u01(x: float) -> float:
    # map cosine in [-1,1] -> [0,1]
    return 0.5 * (x + 1.0)

# -----------------------
# Verilog -> Graph
# -----------------------
def get_node_name(net):
    if hasattr(net, 'name'):
        return str(net.name)
    elif hasattr(net, 'var') and hasattr(net, 'ptr'):
        return f"{get_node_name(net.var)}[{get_node_name(net.ptr)}]"
    elif isinstance(net, str):
        return net
    return str(net)

SEQ_CELL_RE = re.compile(r'(DFF|SDFF|DFFR|DFFS|DFFX|DLH|DLR|LATCH)', re.IGNORECASE)
OUT_PORT_HINT = {'Z', 'ZN', 'Q', 'QN', 'OUT', 'Y', 'o_sum'}

def parse_verilog_graph(filepath: str):
    ast, _ = parse([filepath])
    G = nx.DiGraph()
    id_counter = 0
    node_map: Dict[str, int] = {}

    def add_node(name, attrs):
        nonlocal id_counter
        if name not in node_map:
            node_map[name] = id_counter
            G.add_node(id_counter, name=name, **attrs)
            id_counter += 1
        else:
            nid = node_map[name]
            for k, v in attrs.items():
                if k not in G.nodes[nid]:
                    G.nodes[nid][k] = v
        return node_map[name]

    output_nodes: Set[int] = set()
    seq_inst_ids: Set[int] = set()

    def extract_modules(node):
        if hasattr(node, 'children'):
            for c in node.children():
                if c.__class__.__name__ == 'InstanceList':
                    cell_type = str(c.module)
                    for inst in c.instances:
                        inst_name = get_node_name(inst.name)
                        inst_id = add_node(inst_name, {'type': cell_type})

                        if SEQ_CELL_RE.search(cell_type or ''):
                            seq_inst_ids.add(inst_id)

                        for cport in getattr(inst, 'portlist', []) or []:
                            port_name = str(cport.portname)
                            net_name = get_node_name(cport.argname).replace('.', '_')
                            net_id = add_node(net_name, {'type': 'wire'})

                            if port_name.upper() in OUT_PORT_HINT:
                                G.add_edge(inst_id, net_id)
                                output_nodes.add(net_id)
                            else:
                                G.add_edge(net_id, inst_id)
                extract_modules(c)

    extract_modules(ast)
    return G, node_map, output_nodes, seq_inst_ids

# -----------------------
# Feature Engineering
# -----------------------
def compute_struct_features(G: nx.DiGraph,
                            output_ids: Set[int],
                            seq_inst_ids: Set[int]) -> Dict[int, Dict]:
    """
    计算每个节点的结构/拓扑特征（全无标签）
    """
    N = G.number_of_nodes()
    if N == 0:
        return {}

    # 1) 基本度
    indeg = dict(G.in_degree())
    outdeg = dict(G.out_degree())

    # 2) PageRank（有向）
    try:
        pr = nx.pagerank(G, alpha=0.85)
    except Exception:
        pr = {n: 0.0 for n in G.nodes}

    # 3) 介数中心性（近似采样 k）
    k = min(200, max(10, N // 10))
    try:
        bet = nx.betweenness_centrality(G, k=k, normalized=True, seed=42)
    except Exception:
        bet = {n: 0.0 for n in G.nodes}

    # 4) 特征向量中心性（无向）
    try:
        evec = nx.eigenvector_centrality(G.to_undirected(), max_iter=200)
    except Exception:
        evec = {n: 0.0 for n in G.nodes}

    # 5) 到输出的距离（最短距离：min / mean）
    out_list = list(output_ids) if output_ids else []
    dist_min = {n: math.inf for n in G.nodes}
    dist_avg = {n: math.inf for n in G.nodes}
    if out_list:
        for n in G.nodes:
            dists = []
            for t in out_list:
                try:
                    d = nx.shortest_path_length(G, source=n, target=t)
                    dists.append(d)
                except Exception:
                    pass
            if dists:
                dist_min[n] = float(min(dists))
                dist_avg[n] = float(sum(dists) / len(dists))

    # 将 inf 替换为较大值（N）
    for n in G.nodes:
        if not math.isfinite(dist_min[n]):
            dist_min[n] = float(N)
        if not math.isfinite(dist_avg[n]):
            dist_avg[n] = float(N)

    # 6) 近似重收敛度（2-hop 重叠越多，值越大）
    reconv = {}
    for n in G.nodes:
        succ1 = set(G.successors(n))
        twohop_union = set()
        sum_outdeg_nei = 0
        for u in succ1:
            su = set(G.successors(u))
            sum_outdeg_nei += len(su)
            twohop_union |= su
        overlap = max(0, sum_outdeg_nei - len(twohop_union))
        reconv[n] = float(overlap)

    # 7) 近 FF 边界标志：和时序单元相邻（前驱或后继）
    near_ff = {}
    for n in G.nodes:
        flag = 0
        for nb in set(G.predecessors(n)) | set(G.successors(n)):
            typ = G.nodes[nb].get('type', '')
            if typ and typ != 'wire' and SEQ_CELL_RE.search(typ):
                flag = 1
                break
        near_ff[n] = float(flag)

    # 8) 名称长度（弱 proxy）
    name_len = {n: float(len(str(G.nodes[n].get('name', '')))) for n in G.nodes}

    # 9) 是否输出节点
    is_output = {n: 1.0 if n in output_ids else 0.0 for n in G.nodes}

    # 10) "深度"近似：从 n 出发的最大最短路径长度
    depth = {}
    cap = min(200, max(50, N // 5))
    for n in G.nodes:
        try:
            visited = {n: 0}
            frontier = [n]
            maxd = 0
            cnt = 0
            while frontier and cnt < cap:
                nf = []
                for u in frontier:
                    for v in G.successors(u):
                        if v not in visited:
                            visited[v] = visited[u] + 1
                            maxd = max(maxd, visited[v])
                            nf.append(v)
                            cnt += 1
                            if cnt >= cap:
                                break
                    if cnt >= cap:
                        break
                frontier = nf
            depth[n] = float(maxd)
        except Exception:
            depth[n] = 0.0

    # 归一化
    indeg_n = minmax_norm(np.array([indeg[n] for n in G.nodes]))
    outdeg_n = minmax_norm(np.array([outdeg[n] for n in G.nodes]))
    pr_n = minmax_norm(np.array([pr[n] for n in G.nodes]))
    bet_n = minmax_norm(np.array([bet[n] for n in G.nodes]))
    evec_n = minmax_norm(np.array([evec[n] for n in G.nodes]))
    # 距离越小越"敏感"，转 1/dist
    dmin_inv = minmax_norm(1.0 / (np.array([dist_min[n] for n in G.nodes]) + 1e-6))
    davg_inv = minmax_norm(1.0 / (np.array([dist_avg[n] for n in G.nodes]) + 1e-6))
    reconv_n = minmax_norm(np.array([reconv[n] for n in G.nodes]))
    nearff_n = np.array([near_ff[n] for n in G.nodes])  # already 0/1
    namelen_n = minmax_norm(np.array([name_len[n] for n in G.nodes]))
    depth_n = minmax_norm(np.array([depth[n] for n in G.nodes]))
    isout_n = np.array([is_output[n] for n in G.nodes])

    feats = {}
    for idx, n in enumerate(G.nodes):
        feats[n] = {
            'in_deg': float(indeg_n[idx]),
            'out_deg': float(outdeg_n[idx]),
            'pagerank': float(pr_n[idx]),
            'betweenness': float(bet_n[idx]),
            'eigen': float(evec_n[idx]),
            'dist_min_inv': float(dmin_inv[idx]),
            'dist_avg_inv': float(davg_inv[idx]),
            'reconv': float(reconv_n[idx]),
            'near_ff': float(nearff_n[idx]),
            'name_len': float(namelen_n[idx]),
            'depth': float(depth_n[idx]),
            'is_output': float(isout_n[idx]),
        }
    return feats

def build_pyg_data(G: nx.DiGraph,
                   feats: Dict[int, Dict]) -> Tuple[Data, List[int], List[str]]:
    """
    按节点顺序组装 PyG Data，节点名称 list 用于最终输出排序。
    """
    node_ids = list(G.nodes)
    name_list = [G.nodes[n].get('name', str(n)) for n in node_ids]

    # gate type one-hot
    type_set = set(G.nodes[n].get('type', 'UNK') for n in node_ids)
    type_list = sorted(list(type_set))
    type2idx = {t: i for i, t in enumerate(type_list)}

    x_rows = []
    for n in node_ids:
        typ = G.nodes[n].get('type', 'UNK')
        onehot = [0.0] * len(type2idx)
        onehot[type2idx[typ]] = 1.0

        f = feats[n]
        # 拼装最终特征：类型 one-hot + 结构特征
        row = []
        row += onehot
        row += [
            f['in_deg'], f['out_deg'], f['pagerank'], f['betweenness'], f['eigen'],
            f['dist_min_inv'], f['dist_avg_inv'], f['reconv'], f['near_ff'],
            f['name_len'], f['depth'], f['is_output']
        ]
        x_rows.append(row)

    x = torch.tensor(x_rows, dtype=torch.float)
    
    edges = list(G.edges)
    if len(edges) == 0:
        edge_index = torch.empty((2, 0), dtype=torch.long)
    else:
        src = [node_ids.index(u) for (u, v) in edges]
        dst = [node_ids.index(v) for (u, v) in edges]
        edge_index = torch.tensor([src, dst], dtype=torch.long)

    data = Data(x=x, edge_index=edge_index)
    data.node_ids = node_ids
    data.node_names = name_list
    data.type_list = type_list
    return data, node_ids, name_list

# -----------------------
# Self-supervised DGI
# -----------------------
class EncoderGIN(nn.Module):
    def __init__(self, in_dim, hid=128, layers=3, dropout=0.1):
        super().__init__()
        self.layers = layers
        self.convs = nn.ModuleList()
        self.bns = nn.ModuleList()
        for i in range(layers):
            in_c = in_dim if i == 0 else hid
            nn_layer = nn.Sequential(
                nn.Linear(in_c, hid),
                nn.ReLU(),
                nn.Linear(hid, hid),
                nn.ReLU(),
            )
            self.convs.append(GINConv(nn_layer))
            self.bns.append(BatchNorm(hid))
        self.dropout = dropout

    def forward(self, x, edge_index):
        h = x
        for i in range(self.layers):
            h = self.convs[i](h, edge_index)
            h = self.bns[i](h)
            h = F.relu(h)
            h = F.dropout(h, p=self.dropout, training=self.training)
        return h

class DGI(nn.Module):
    """
    简洁 DGI 实现：
    - encoder(x) -> H
    - summary s = sigmoid(mean(H))
    - 判别器： node-level dot(H, W s)
    - 正样本：H，负样本：H_corrupt（x 打乱后编码）
    """
    def __init__(self, encoder: EncoderGIN, hid_dim: int):
        super().__init__()
        self.encoder = encoder
        self.W = nn.Linear(hid_dim, hid_dim, bias=False)

    def forward(self, x, edge_index, x_corrupt):
        h = self.encoder(x, edge_index)
        h_corrupt = self.encoder(x_corrupt, edge_index)

        s = torch.sigmoid(h.mean(dim=0, keepdim=True))  # [1, H]
        sW = self.W(s)  # [1,H]

        pos = torch.sum(h * sW, dim=1)     # [N]
        neg = torch.sum(h_corrupt * sW, dim=1)  # [N]
        return pos, neg, h

    @staticmethod
    def loss_fn(pos, neg):
        # maximize log(sigmoid(pos)) + log(1 - sigmoid(neg))
        return - (torch.log(torch.sigmoid(pos) + 1e-10).mean()
                  + torch.log(1 - torch.sigmoid(neg) + 1e-10).mean())

def train_dgi(data: Data, hidden=128, layers=3, epochs=150, lr=1e-3, dropout=0.1, device='cpu'):
    enc = EncoderGIN(in_dim=data.x.size(1), hid=hidden, layers=layers, dropout=dropout).to(device)
    model = DGI(enc, hid_dim=hidden).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=lr)

    x = data.x.to(device)
    ei = data.edge_index.to(device)

    for ep in range(epochs):
        model.train()
        opt.zero_grad()

        # corrupt by feature permutation
        perm = torch.randperm(x.size(0), device=device)
        x_corrupt = x[perm]

        pos, neg, _ = model(x, ei, x_corrupt)
        loss = DGI.loss_fn(pos, neg)
        loss.backward()
        opt.step()

        if ep % 20 == 0:
            print(f"[DGI] epoch {ep:03d}  loss={loss.item():.4f}")

    model.eval()
    with torch.no_grad():
        pos, neg, H = model(x, ei, x)  # 用本身 x 获取最终 H
    return H.cpu()

# -----------------------
# Scoring fusion
# -----------------------
def fuse_scores(G: nx.DiGraph,
                feats: Dict[int, Dict],
                H: torch.Tensor,
                data: Data,
                output_ids: Set[int]) -> List[Tuple[str, float]]:
    """
    融合策略（无标签）：
      centrality = mean(pagerank, betweenness, eigen)
      proximity  = 0.5*dist_min_inv + 0.5*dist_avg_inv
      reconv     = reconv
      seq        = near_ff
      embed_sim  = cos(node_emb, mean_emb(outputs))
    归一化后线性加权：
      score = 0.25*centrality + 0.25*proximity + 0.20*reconv
            + 0.15*seq + 0.15*embed_sim
    """
    nid_list = data.node_ids
    name_list = data.node_names
    
    # 取输出节点的 embedding 均值
    if output_ids:
        out_idx = [nid_list.index(n) for n in nid_list if n in output_ids]
    else:
        out_idx = []
    
    Hn = F.normalize(H, p=2, dim=1)
    if len(out_idx) > 0:
        out_centroid = Hn[out_idx].mean(dim=0, keepdim=True)  # [1,H]
        out_centroid = F.normalize(out_centroid, p=2, dim=1)
        cos = torch.mm(Hn, out_centroid.t()).squeeze(1).numpy()  # [-1,1]
        embed_sim = np.array([z2u01(float(c)) for c in cos])      # [0,1]
    else:
        embed_sim = np.zeros(Hn.size(0))

    # 取各分量并做 min-max
    pr = np.array([feats[nid]['pagerank'] for nid in nid_list])
    bet = np.array([feats[nid]['betweenness'] for nid in nid_list])
    ev = np.array([feats[nid]['eigen'] for nid in nid_list])
    centrality = minmax_norm((pr + bet + ev) / 3.0)

    prox = minmax_norm(0.5 * np.array([feats[n]['dist_min_inv'] for n in nid_list]) +
                       0.5 * np.array([feats[n]['dist_avg_inv'] for n in nid_list]))

    reconv = minmax_norm(np.array([feats[n]['reconv'] for n in nid_list]))
    seq = np.array([feats[n]['near_ff'] for n in nid_list])  # already 0/1

    # 线性加权
    score = (0.25 * centrality
             + 0.25 * prox
             + 0.20 * reconv
             + 0.15 * seq
             + 0.15 * embed_sim)

    ranked = list(zip(name_list, score.tolist()))
    ranked.sort(key=lambda x: -x[1])
    return ranked

# -----------------------
# Node cleaning
# -----------------------
NODE_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_$]*(\[\d+\])?$')

def clean_nodes(G: nx.DiGraph, output_ids: Set[int], seq_ids: Set[int]):
    remove_ids = set()
    for n in G.nodes:
        name = G.nodes[n].get('name', '')
        if not NODE_RE.match(name) or re.match(r'^(clk|clock|rst|reset|in)', name, re.IGNORECASE):
            remove_ids.add(n)
    G.remove_nodes_from(remove_ids)
    output_ids_clean = {nid for nid in output_ids if nid in G.nodes}
    seq_ids_clean = {nid for nid in seq_ids if nid in G.nodes}
    return G, output_ids_clean, seq_ids_clean

# -----------------------
# 可注入节点筛选
# -----------------------
def get_injectable_nodes(G_sub: nx.DiGraph) -> list:
    """
    返回子图中可注入的节点名称列表
    - 仅 wire 或 reg 类型
    - 排除 clk/clock/rst/reset 前缀
    - 排除输入端口（in/input）和总线口信号 ([ ])
    """
    injectable = []
    for n in G_sub.nodes:
        node_type = G_sub.nodes[n].get('type','').lower()
        name = G_sub.nodes[n].get('name','').lower()
        if node_type not in ('wire','reg'):
            continue
        if re.match(r'^(clk|clock|rst|reset|in|input)', name):
            continue
        if '[' in name or ']' in name:
            continue
        injectable.append(G_sub.nodes[n].get('name',''))
    return injectable


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verilog', type=str, default='pe.synth_dct.v')
    parser.add_argument('--epochs', type=int, default=500, help="训练轮数")
    parser.add_argument('--hidden', type=int, default=128, help="隐藏层维度")
    parser.add_argument('--layers', type=int, default=5)
    parser.add_argument('--dropout', type=float, default=0.2, help="Dropout率")
    parser.add_argument('--seed', type=int, default=20)
    parser.add_argument('--topk_csv', type=str, default='topk.csv', help="CSV 文件包含 topk 列")
    parser.add_argument('--timing_csv', type=str, default='timing.csv', help="保存每个 topk 子图的时间信息")
    parser.add_argument('--gnn_ranks', type=str, default='gnn_ranks', help="GNN 排名结果输出目录")
    parser.add_argument('--keep_ratio', type=float, default=0.2, help="输出排名节点数 = topk × keep_ratio")
    args = parser.parse_args()

    set_seed(args.seed)

    # ====== 基本检查 ======
    if not os.path.exists(args.verilog):
        print(f"❌ 找不到网表文件: {args.verilog}")
        return
    if not os.path.exists(args.topk_csv):
        print(f"❌ 找不到 topk 文件: {args.topk_csv}")
        return

    # ====== 创建输出目录 ======
    os.makedirs(args.gnn_ranks, exist_ok=True)

    # ====== 读取 topk.csv ======
    topk_list = []
    with open(args.topk_csv, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        if 'topk' not in reader.fieldnames:
            print(f"❌ topk.csv 首行没有 'topk' 列，列名={reader.fieldnames}")
            return
        for row in reader:
            try:
                topk_list.append(int(row['topk'].strip()))
            except Exception:
                continue
    if not topk_list:
        print("❌ 没有有效的 topk 数据")
        return
    print(f"✅ 成功读取 {len(topk_list)} 个 topk 值：{topk_list}")

    print("=== Unsupervised Sensitivity Scorer (Top-K Subgraph) ===")
    print(f"[配置] Epochs: {args.epochs}, Hidden: {args.hidden}, Dropout: {args.dropout}")
    print()

    # ====== Step 1: 解析网表 ======
    print(f"[INFO] 解析网表: {args.verilog}")
    G, node_map, output_ids, seq_inst_ids = parse_verilog_graph(args.verilog)

    # ====== Step 2: 结构特征计算（全图） ======
    print("[INFO] 提取结构/拓扑特征...")
    t0_full_feat = time.time()
    feats_full = compute_struct_features(G, output_ids, seq_inst_ids)
    t1_full_feat = time.time()
    full_feat_time = t1_full_feat - t0_full_feat
    print(f"[INFO] 全图特征计算耗时: {full_feat_time:.4f}s")

    # ====== Step 3: 准备时间统计 CSV ======
    csv_fields = ['topk', 'sub_nodes', 'sub_edges', 'prefilter_time', 'subgraph_time', 'feat_time', 'pyg_time', 'dgi_time', 'fuse_time', 'total_time']
    csv_rows = []

    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    # ====== Step 4: 对每个 topk 值做子图分析 ======
    for k in topk_list:
        print(f"\n[INFO] Processing topk={k}")
        
        # ---- 初筛（计入时间） ----
        t0 = time.time()
        scores = np.array([feats_full[n]['pagerank'] + feats_full[n]['dist_min_inv'] for n in G.nodes])
        node_ids_all = np.array(list(G.nodes))
        topk_nids = node_ids_all[scores.argsort()[::-1][:k]]
        t1 = time.time()
        prefilter_time = t1 - t0

        # ---- 子图构造（topk + 邻居）----
        t0 = time.time()
        sub_nodes = set(topk_nids)
        for n in topk_nids:
            sub_nodes |= set(G.predecessors(n)) | set(G.successors(n))
        G_sub = G.subgraph(sub_nodes).copy()
        t1 = time.time()
        subgraph_time = t1 - t0

        # ---- 特征提取 ----
        t0 = time.time()
        feats_sub = {n: feats_full[n] for n in G_sub.nodes}
        t1 = time.time()
        feat_time = t1 - t0

        # ---- 构造 PyG 数据 ----
        t0 = time.time()
        data_sub, node_ids_sub, name_list_sub = build_pyg_data(G_sub, feats_sub)
        t1 = time.time()
        pyg_time = t1 - t0

        # ---- DGI 训练 ----
        t0 = time.time()
        H_sub = train_dgi(data_sub, hidden=args.hidden, layers=args.layers,
                          epochs=args.epochs, dropout=args.dropout, device=device)
        t1 = time.time()
        dgi_time = t1 - t0

        # ---- 融合打分 ----
        t0 = time.time()
        ranked_sub = fuse_scores(G_sub, feats_sub, H_sub, data_sub, output_ids & set(G_sub.nodes))
        t1 = time.time()
        fuse_time = t1 - t0

        # ---- 汇总总时间（包括初筛）----
        total_time = prefilter_time + subgraph_time + feat_time + pyg_time + dgi_time + fuse_time

        # ---- 保存时间记录 ----
        csv_rows.append({
            'topk': k,
            'sub_nodes': G_sub.number_of_nodes(),
            'sub_edges': G_sub.number_of_edges(),
            'prefilter_time': round(prefilter_time, 4),
            'subgraph_time': round(subgraph_time, 4),
            'feat_time': round(feat_time, 4),
            'pyg_time': round(pyg_time, 4),
            'dgi_time': round(dgi_time, 4),
            'fuse_time': round(fuse_time, 4),
            'total_time': round(total_time, 4)
        })

        # ---- 输出排名（仅前 keep_ratio 部分，可注入节点）----
        injectable_names = get_injectable_nodes(G_sub)
        ranked_injectable = [(name, score) for name, score in ranked_sub if name in injectable_names]
        top_count = max(1, math.ceil(k * args.keep_ratio))
        top_nodes = ranked_injectable[:top_count]

        out_txt = os.path.join(args.gnn_ranks, f"gnn_rank_{k}.txt")
        with open(out_txt, 'w', encoding='utf-8') as f:
            for name, score in top_nodes:
                f.write(f"{name} {score:.6f}\n")

        print(f"[INFO] topk={k} 写入前 {top_count}/{len(ranked_injectable)} 个可注入节点到 {out_txt}")

    # ====== Step 5: 写出 timing.csv ======
    with open(args.timing_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields)
        writer.writeheader()
        writer.writerows(csv_rows)
    print(f"\n✅ 所有 top-k 时间记录写入 {args.timing_csv}")


if __name__ == '__main__':
    main()


