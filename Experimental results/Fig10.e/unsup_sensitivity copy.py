#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
无监督敏感度排名器 - 增强版
============================

功能：对每个topk值生成多个不同的排名结果（默认100个，可配置）

增强功能：通过多种方式增加每次排名的差异性
1. 不同的随机种子 - 基础差异来源
2. 输入特征噪声 - 在GNN输入时添加噪声
3. Dropout - 训练过程中的随机性
4. 特征分数噪声 - 在最终打分时添加噪声
5. 融合权重扰动 - 随机调整结构特征和嵌入特征的权重

使用方法：
---------
# 默认配置（生成100个排名）
python "unsup_sensitivity copy.py"

# 自定义运行次数（例如生成50个排名）
python "unsup_sensitivity copy.py" --num_runs 50

# 自定义配置以进一步增大差异
python "unsup_sensitivity copy.py" --dropout 0.4 --input_noise 0.08 --noise_level 0.18 --weight_noise 0.22

# 配置参数说明：
--num_runs: 每个topk生成的排名数量（默认100）
--dropout: 0.3-0.5，越高差异越大（但太高可能影响质量）
--input_noise: 0.03-0.1，输入特征噪声水平
--noise_level: 0.1-0.2，最终打分时的噪声水平
--weight_noise: 0.15-0.25，融合权重的随机扰动范围
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
import os
import csv
import math
import time
import argparse
import pandas as pd

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
    # 用单源最短路，汇总所有输出的距离的 min/mean
    # G 是有向图，找从节点 i 到 输出节点 t 的距离
    out_list = list(output_ids) if output_ids else []
    dist_min = {n: math.inf for n in G.nodes}
    dist_avg = {n: math.inf for n in G.nodes}
    if out_list:
        for n in G.nodes:
            dists = []
            # 只在可达子图里算最短路，避免全图 BFS 过慢
            # 这里采用逐个输出求 (n->t) 的最短路长度（若存在）
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

    # 10) “深度”近似：从 n 出发的最大最短路径长度（可达子图）
    # 注意：计算开销较大，做个轻量近似：对每个节点取它能到达的最多 200 个点的最短路最大值
    depth = {}
    cap = min(200, max(50, N // 5))
    for n in G.nodes:
        try:
            # 受限 BFS
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
    # 距离越小越“敏感”，转 1/dist
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
                   feats: Dict[int, Dict],
                   input_noise: float = 0.0) -> Tuple[Data, List[int], List[str]]:
    """
    按节点顺序组装 PyG Data，节点名称 list 用于最终输出排序。
    
    Args:
        G: 图结构
        feats: 节点特征字典
        input_noise: 输入特征噪声水平 (0-1)，为0时不添加噪声
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
    
    # 添加输入噪声（只对连续特征，不对one-hot编码）
    if input_noise > 0:
        num_onehot = len(type2idx)
        noise = torch.randn_like(x[:, num_onehot:]) * input_noise
        x[:, num_onehot:] = torch.clamp(x[:, num_onehot:] + noise, 0, 1)
    
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
    def __init__(self, in_dim, hid=128, layers=3, dropout=0.2):
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

def train_dgi(data: Data, hidden=128, layers=3, epochs=150, lr=1e-3, dropout=0.2, device='cpu'):
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
                output_ids: Set[int],
                noise_level: float = 0.0,
                weight_noise: float = 0.0) -> List[Tuple[str, float]]:
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
    
    Args:
        noise_level: 特征噪声水平 (0-1)，默认0
        weight_noise: 权重扰动范围 (0-1)，默认0
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

    # 添加随机噪声到特征分数
    if noise_level > 0:
        centrality_noise = np.random.uniform(-noise_level, noise_level, size=centrality.shape)
        centrality = np.clip(centrality + centrality_noise, 0, 1)
        
        prox_noise = np.random.uniform(-noise_level, noise_level, size=prox.shape)
        prox = np.clip(prox + prox_noise, 0, 1)
        
        reconv_noise = np.random.uniform(-noise_level, noise_level, size=reconv.shape)
        reconv = np.clip(reconv + reconv_noise, 0, 1)
        
        embed_noise = np.random.uniform(-noise_level, noise_level, size=embed_sim.shape)
        embed_sim = np.clip(embed_sim + embed_noise, 0, 1)

    # 随机调整融合权重
    if weight_noise > 0:
        # 生成5个权重并归一化
        base_weights = np.array([0.25, 0.25, 0.20, 0.15, 0.15])
        weight_perturbation = np.random.uniform(-weight_noise, weight_noise, size=5)
        weights = base_weights + weight_perturbation
        weights = np.clip(weights, 0.05, 0.5)  # 保持在合理范围
        weights = weights / weights.sum()  # 归一化使和为1
        w1, w2, w3, w4, w5 = weights
    else:
        w1, w2, w3, w4, w5 = 0.25, 0.25, 0.20, 0.15, 0.15

    # 线性加权
    score = (w1 * centrality
             + w2 * prox
             + w3 * reconv
             + w4 * seq
             + w5 * embed_sim)

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

def get_injectable_nodes(G_sub: nx.DiGraph) -> list[str]:
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
    parser.add_argument('--epochs', type=int, default=150, 
                        help="训练轮数，越少差异越大 (建议50-150)")
    parser.add_argument('--hidden', type=int, default=128,
                        help="隐藏层维度 (建议32-128)")
    parser.add_argument('--layers', type=int, default=3)
    parser.add_argument('--dropout', type=float, default=0.3,
                        help="Dropout率，越高差异越大 (建议0.3-0.5)")
    parser.add_argument('--seed', type=int, default=20)
    parser.add_argument('--topk_csv', type=str, default='topk.csv', help="CSV 文件包含 topk 列")
    parser.add_argument('--timing_csv', type=str, default='timing_200runs.csv', help="保存每个 topk 子图的时间信息")
    parser.add_argument('--gnn_ranks', type=str, default='gnn_ranks_200runs', help="GNN 排名结果输出目录")
    parser.add_argument('--keep_ratio', type=float, default=0.2, help="输出排名节点数 = topk × keep_ratio")
    parser.add_argument('--noise_level', type=float, default=0.15,
                        help="特征噪声水平 (0-1)，越高排名差异越大 (建议0.1-0.2)")
    parser.add_argument('--weight_noise', type=float, default=0.2,
                        help="融合权重扰动范围 (0-1)，越高差异越大 (建议0.15-0.25)")
    parser.add_argument('--input_noise', type=float, default=0.05,
                        help="输入特征噪声水平 (0-1)，越高差异越大 (建议0.03-0.1)")
    parser.add_argument('--num_runs', type=int, default=200,
                        help="每个topk生成的排名结果数量 (默认100)")
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
    print(f"[配置] 每个topk运行次数: {args.num_runs}")
    print(f"[配置] Dropout: {args.dropout} (越高差异越大)")
    print(f"[配置] 输入噪声: {args.input_noise} (越高差异越大)")
    print(f"[配置] 特征噪声: {args.noise_level} (越高差异越大)")
    print(f"[配置] 权重扰动: {args.weight_noise} (越高差异越大)")
    print(f"[配置] Epochs: {args.epochs}, Hidden: {args.hidden}")
    print(f"[提示] 建议调整范围: dropout(0.3-0.5), input_noise(0.03-0.1), noise_level(0.1-0.2), weight_noise(0.15-0.25)")
    print()

    # ====== Step 1: 解析网表 ======
    print(f"[INFO] 解析网表: {args.verilog}")
    G, node_map, output_ids, seq_inst_ids = parse_verilog_graph(args.verilog)

    # ====== Step 2: 结构特征计算（全图） ======
    print("[INFO] 提取结构/拓扑特征...")
    feats_full = compute_struct_features(G, output_ids, seq_inst_ids)

    # ====== Step 3: 准备时间统计 CSV ======
    csv_fields = ['topk', 'run', 'sub_nodes', 'sub_edges', 'feat_time', 'pyg_time', 'dgi_time', 'fuse_time', 'escaped_faults']
    csv_rows = []
    
    # 尝试从 coverage_statistics.csv 读取 escaped_faults 数据
    escaped_faults_dict = {}  # {(topk, run): escaped_faults}
    coverage_csv_path = os.path.join('full_injection_results', 'coverage_statistics.csv')
    if os.path.exists(coverage_csv_path):
        try:
            with open(coverage_csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        topk_val = int(row['topk'])
                        run_val = int(row['run'])
                        escaped_faults_val = int(row['escaped_faults'])
                        escaped_faults_dict[(topk_val, run_val)] = escaped_faults_val
                    except (KeyError, ValueError):
                        continue
            print(f"[INFO] 从 {coverage_csv_path} 读取了 {len(escaped_faults_dict)} 条 escaped_faults 数据")
        except Exception as e:
            print(f"[WARN] 读取 coverage_statistics.csv 失败: {e}")
    else:
        print(f"[WARN] 未找到 {coverage_csv_path}，escaped_faults 将设置为 0")

    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    # ====== Step 4: 对每个 topk 值做子图分析 ======
    for k in topk_list:
        print(f"\n[INFO] Processing topk={k}")
        
        # ---- 初筛（不计入时间） ----
        scores = np.array([feats_full[n]['pagerank'] + feats_full[n]['dist_min_inv'] for n in G.nodes])
        node_ids_all = np.array(list(G.nodes))
        topk_nids = node_ids_all[scores.argsort()[::-1][:k]]

        # ---- 子图构造（topk + 邻居）----
        sub_nodes = set(topk_nids)
        for n in topk_nids:
            sub_nodes |= set(G.predecessors(n)) | set(G.successors(n))
        G_sub = G.subgraph(sub_nodes).copy()

        # ====== 对每个topk生成N个不同的排名 ======
        for run_idx in range(args.num_runs):
            # 使用不同的随机种子
            current_seed = args.seed + k * 1000 + run_idx
            set_seed(current_seed)
            
            print(f"[INFO] TopK={k}, Run={run_idx+1}/{args.num_runs}, Seed={current_seed}")

            # ---- 特征提取 ----
            t0 = time.time()
            feats_sub = {n: feats_full[n] for n in G_sub.nodes}
            t1 = time.time()
            feat_time = t1 - t0

            # ---- 构造 PyG 数据（添加输入噪声） ----
            t0 = time.time()
            data_sub, node_ids_sub, name_list_sub = build_pyg_data(G_sub, feats_sub, input_noise=args.input_noise)
            t1 = time.time()
            pyg_time = t1 - t0

            # ---- DGI 训练 ----
            t0 = time.time()
            H_sub = train_dgi(data_sub, hidden=args.hidden, layers=args.layers,
                              epochs=args.epochs, dropout=args.dropout, device=device)
            t1 = time.time()
            dgi_time = t1 - t0

            # ---- 融合打分（添加特征噪声和权重扰动） ----
            t0 = time.time()
            ranked_sub = fuse_scores(G_sub, feats_sub, H_sub, data_sub, output_ids & set(G_sub.nodes),
                                   noise_level=args.noise_level, weight_noise=args.weight_noise)
            t1 = time.time()
            fuse_time = t1 - t0

            # ---- 获取 escaped_faults ----
            escaped_faults = escaped_faults_dict.get((k, run_idx + 1), 0)

            # ---- 保存时间记录（escaped_faults 替代 total_time） ----
            csv_rows.append({
                'topk': k,
                'run': run_idx + 1,
                'sub_nodes': G_sub.number_of_nodes(),
                'sub_edges': G_sub.number_of_edges(),
                'feat_time': round(feat_time, 4),
                'pyg_time': round(pyg_time, 4),
                'dgi_time': round(dgi_time, 4),
                'fuse_time': round(fuse_time, 4),
                'escaped_faults': escaped_faults
            })

            # ---- 输出排名（仅前 keep_ratio 部分，可注入节点）----
            injectable_names = get_injectable_nodes(G_sub)
            ranked_injectable = [(name, score) for name, score in ranked_sub if name in injectable_names]
            top_count = max(1, math.ceil(k * args.keep_ratio))
            top_nodes = ranked_injectable[:top_count]

            out_txt = os.path.join(args.gnn_ranks, f"gnn_rank_{k}_run{run_idx+1}.txt")
            with open(out_txt, 'w', encoding='utf-8') as f:
                for name, score in top_nodes:
                    f.write(f"{name} {score:.6f}\n")

            print(f"[INFO] topk={k}, run={run_idx+1} 写入前 {top_count}/{len(ranked_injectable)} 个可注入节点到 {out_txt}")

    # ====== Step 5: 写出 timing.csv ======
    with open(args.timing_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields)
        writer.writeheader()
        writer.writerows(csv_rows)
    print(f"\n✅ 所有 top-k 时间记录写入 {args.timing_csv}")


if __name__ == '__main__':
    main()




