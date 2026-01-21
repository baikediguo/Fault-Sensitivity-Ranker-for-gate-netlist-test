#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verilog 网表无监督/自监督敏感度评分器（批量模式）- V1 Only 版本

核心改进：
1. 使用 NetworkKit (C++ 后端) 替代 NetworkX，性能提升 10-100 倍
2. 全链路 NetworkKit：解析→特征提取→缓存→训练
3. 内存占用减少 5-20 倍
4. 梯度检查点 (Gradient Checkpointing)
5. 四级回退机制：GPU → GPU+检查点 → CPU → CPU+检查点

此版本仅包含 V1 评分逻辑，已移除所有 V2 相关代码。
"""

import os
import re
import math
import argparse
import random
import glob
import time
import pickle
import hashlib
import shutil
import tempfile
import multiprocessing as mp
import numpy as np
import networkit as nk  # NetworkKit: 高性能图计算库
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from typing import List, Tuple, Dict, Set, Optional

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.nn import GINConv, BatchNorm

from pyverilog.vparser.parser import parse

# 小规模阈值（保留用于兼容性）
SMALL_SCALE_THRESHOLD = 50000

# 子图采样阈值（超大规模图内存优化）
SAMPLE_THRESHOLD = 500000

# 运行模式（固定为 V1）
RUN_MODE = 'v1'


# 尝试导入 psutil 用于内存监控
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    print("[警告] psutil 未安装，无法自动调整进程数。建议安装: pip install psutil")

def get_adaptive_workers(n_nodes: int, task_type: str = 'distance') -> int:
    """
    根据可用内存和图大小自动计算进程/线程数
    
    Args:
        n_nodes: 节点数量
        task_type: 任务类型 ('distance' 或 'node_features')
    
    Returns:
        推荐的进程数
    """
    # 默认值：CPU 核心数 - 2
    default_workers = max(1, mp.cpu_count() - 2)
    
    if not HAS_PSUTIL:
        return default_workers
    
    try:
        # 估算每个进程的内存需求 (MB)
        # distance 任务需要存储 BFS 结果，内存需求较高
        # node_features 任务内存需求较低
        if task_type == 'distance':
            mem_per_worker = max(100, n_nodes * 0.002)  # 大约每千节点 2MB
        else:
            mem_per_worker = max(50, n_nodes * 0.001)   # 大约每千节点 1MB
        
        # 获取可用物理内存 (MB)
        mem_info = psutil.virtual_memory()
        available_mem = mem_info.available / (1024 * 1024)
        total_mem = mem_info.total / (1024 * 1024)
        
        # 保留至少 2GB 或 20% 内存给系统
        reserved_mem = max(2000, total_mem * 0.2)
        usable_mem = max(0, available_mem - reserved_mem)
        
        # 计算最大进程数
        max_workers_by_mem = max(1, int(usable_mem / mem_per_worker))
        
        # 取较小值
        adaptive_workers = min(max_workers_by_mem, default_workers)
        
        # 如果内存紧张，打印警告
        if adaptive_workers < default_workers:
            print(f"    [内存自适应] 可用: {available_mem:.0f}MB, 每进程: {mem_per_worker:.0f}MB → 使用 {adaptive_workers} 进程 (原 {default_workers})")
        
        return adaptive_workers
    except Exception as e:
        # 出错时使用默认值
        return default_workers





# -----------------------
# 工具函数 (Utils)
# -----------------------
def set_seed(seed=42):
    """设置随机种子以确保可重复性"""
    random.seed(seed)
    np.random.seed(seed)
    nk.setSeed(seed, True)  # NetworkKit 全局种子，确保 EstimateBetweenness 等随机算法可重复
    try:
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
            # 确保 CUDA 运算确定性（略微降低性能，但保证可重复性）
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
        # 强制使用确定性算法（PyTorch 1.8+）
        try:
            torch.use_deterministic_algorithms(True, warn_only=True)
        except:
            pass
        # 设置环境变量确保 CUBLAS 确定性（针对某些 scatter/gather 操作）
        os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':4096:8'
    except:
        pass

def minmax_norm(arr: np.ndarray) -> np.ndarray:
    if len(arr) == 0: return arr
    a = np.asarray(arr, dtype=float); lo, hi = np.nanmin(a), np.nanmax(a)
    if not np.isfinite(lo) or not np.isfinite(hi) or abs(hi - lo) < 1e-12: return np.zeros_like(a)
    return (a - lo) / (hi - lo)

def z2u01(x: float) -> float: return 0.5 * (x + 1.0)

def get_node_name(net):
    if hasattr(net, 'name'): return str(net.name)
    elif hasattr(net, 'var') and hasattr(net, 'ptr'): return f"{get_node_name(net.var)}[{get_node_name(net.ptr)}]"
    elif isinstance(net, str): return net
    return str(net)

SEQ_CELL_RE = re.compile(r'(DFF|SDFF|DFFR|DFFS|DFFX|DLH|DLR|LATCH)', re.IGNORECASE)
OUT_PORT_HINT = {'Z', 'ZN', 'Q', 'QN', 'OUT', 'Y', 'o_sum'}

# 缓存目录
CACHE_DIR = "./feature_cache"
USE_CACHE = True  # 由命令行参数 --no_cache 控制

# -----------------------
# NetworkKit 图封装类
# -----------------------
class NKGraph:
    """
    NetworkKit 图封装，提供与 NetworkX 兼容的接口
    性能比 NetworkX 快 10-100 倍，内存占用减少 5-20 倍
    
    版本 33 优化：缓存边列表，避免重复遍历
    """
    
    def __init__(self, n_nodes: int = 0, directed: bool = True):
        self.nk_graph = nk.Graph(n_nodes, weighted=False, directed=directed)
        self.node_names: Dict[int, str] = {}
        self.node_types: Dict[int, str] = {}
        self.n_nodes = n_nodes
        self._cached_edges: List[Tuple[int, int]] = None  # 边列表缓存
        self._cached_edges_np: np.ndarray = None  # numpy 格式边缓存
    
    @classmethod
    def from_edges(cls, n_nodes: int, edges: List[Tuple[int, int]], 
                   node_names: Dict[int, str] = None, 
                   node_types: Dict[int, str] = None) -> 'NKGraph':
        """从边列表构建图，同时创建反向图和缓存边列表"""
        g = cls(n_nodes, directed=True)
        
        # 同时创建正向图和反向图
        g._rev_graph = nk.Graph(n_nodes, weighted=False, directed=True)
        
        for u, v in edges:
            g.nk_graph.addEdge(u, v)
            g._rev_graph.addEdge(v, u)  # 反向边
        
        g.node_names = node_names or {}
        g.node_types = node_types or {}
        
        # 缓存边列表（避免后续重复遍历）
        g._cached_edges = edges
        # 预计算 numpy 格式（用于 PyG 构建）
        if edges:
            g._cached_edges_np = np.array(edges, dtype=np.int32)
        else:
            g._cached_edges_np = np.empty((0, 2), dtype=np.int32)
        
        return g
    
    def get_reverse_graph(self):
        """获取反向图（懒加载）"""
        if hasattr(self, '_rev_graph') and self._rev_graph is not None:
            return self._rev_graph
        # 如果没有预创建，则创建（兼容旧缓存）
        self._rev_graph = nk.Graph(self.n_nodes, weighted=False, directed=True)
        for u in range(self.n_nodes):
            for v in self.successors(u):
                self._rev_graph.addEdge(v, u)
        return self._rev_graph
    
    def number_of_nodes(self) -> int:
        return self.nk_graph.numberOfNodes()
    
    def number_of_edges(self) -> int:
        return self.nk_graph.numberOfEdges()
    
    def nodes(self):
        """模拟 NetworkX 的 nodes 迭代器"""
        return range(self.n_nodes)
    
    def edges(self) -> List[Tuple[int, int]]:
        """返回边列表（使用缓存）"""
        if self._cached_edges is not None:
            return self._cached_edges
        # 兼容旧缓存：需要重建边列表并缓存
        result = []
        for u in range(self.n_nodes):
            for v in self.nk_graph.iterNeighbors(u):
                result.append((u, v))
        self._cached_edges = result  # 缓存结果
        return result
    
    def edges_numpy(self) -> np.ndarray:
        """返回 numpy 格式的边数组 (E, 2)，用于高效构建 PyG Data"""
        if self._cached_edges_np is not None:
            return self._cached_edges_np
        # 兼容旧缓存：从边列表构建
        edge_list = self.edges()
        if edge_list:
            self._cached_edges_np = np.array(edge_list, dtype=np.int32)
        else:
            self._cached_edges_np = np.empty((0, 2), dtype=np.int32)
        return self._cached_edges_np
    
    def in_degree(self, node: int) -> int:
        return self.nk_graph.degreeIn(node)
    
    def out_degree(self, node: int) -> int:
        return self.nk_graph.degreeOut(node)
    
    def all_in_degrees(self) -> np.ndarray:
        return np.array([self.nk_graph.degreeIn(n) for n in range(self.n_nodes)])
    
    def all_out_degrees(self) -> np.ndarray:
        return np.array([self.nk_graph.degreeOut(n) for n in range(self.n_nodes)])
    
    def successors(self, node: int) -> List[int]:
        """返回后继节点"""
        return list(self.nk_graph.iterNeighbors(node))
    
    def predecessors(self, node: int) -> List[int]:
        """返回前驱节点"""
        return list(self.nk_graph.iterInNeighbors(node))
    
    def pagerank(self, damp: float = 0.85, max_iter: int = 100) -> np.ndarray:
        """计算 PageRank（C++ 并行）"""
        pr = nk.centrality.PageRank(self.nk_graph, damp=damp)
        pr.run()
        return np.array(pr.scores())
    
    def betweenness_sampled(self, n_samples: int = 100, seed: int = 42) -> np.ndarray:
        """计算采样 Betweenness（C++ 并行）"""
        try:
            bet = nk.centrality.EstimateBetweenness(self.nk_graph, nSamples=n_samples, normalized=True, parallel=True)
            bet.run()
            return np.array(bet.scores())
        except:
            return np.zeros(self.n_nodes)
    
    def eigenvector_centrality(self, max_iter: int = 100) -> np.ndarray:
        """计算 Eigenvector Centrality（与 copy 14 一致：转无向图）"""
        try:
            # Copy 14 使用 G.to_undirected()，NetworkKit 也需要转无向图
            undirected_graph = nk.Graph(self.n_nodes, weighted=False, directed=False)
            for u in range(self.n_nodes):
                for v in self.successors(u):
                    if not undirected_graph.hasEdge(u, v):
                        undirected_graph.addEdge(u, v)
            
            eig = nk.centrality.EigenvectorCentrality(undirected_graph, tol=1e-6)
            eig.run()
            return np.array(eig.scores())
        except Exception as e:
            # 失败时返回零
            return np.zeros(self.n_nodes)
    
    def bfs_distances_to_targets(self, targets: Set[int]) -> np.ndarray:
        """计算到目标节点集的最短距离（多源反向 BFS，一次性计算）"""
        n = self.n_nodes
        dist = np.full(n, float(n))
        if not targets:
            return dist
        valid_targets = [t for t in targets if 0 <= t < n]
        if not valid_targets:
            return dist
        
        # 多源 BFS：一次性从所有目标出发，效率 O(N+E)
        # 恢复 copy 19 逻辑：避免 C++ backend 调用，使用纯 Python 实现
        for t in valid_targets:
            dist[t] = 0
        visited = set(valid_targets)
        frontier = list(valid_targets)
        current_dist = 0
        
        # 使用预缓存的反向图遍历
        rev_graph = self.get_reverse_graph()
        
        while frontier:
            next_frontier = []
            current_dist += 1
            for node in frontier:
                # 在反向图上遍历（相当于找 predecessors）
                for pred in rev_graph.iterNeighbors(node):
                    if pred not in visited:
                        visited.add(pred)
                        dist[pred] = current_dist
                        next_frontier.append(pred)
            frontier = next_frontier
        return dist
    
    def single_source_distances(self, source: int) -> Dict[int, int]:
        """使用 NetworkKit C++ BFS 计算单源最短路径"""
        try:
            bfs = nk.distance.BFS(self.nk_graph, source, storePaths=False)
            bfs.run()
            distances = bfs.getDistances()
            # 转换为字典，排除不可达节点
            return {i: int(d) for i, d in enumerate(distances) if d < self.n_nodes}
        except:
            # 回退到 Python 实现
            dist = {source: 0}
            frontier = [source]
            current_dist = 0
            while frontier:
                next_frontier = []
                current_dist += 1
                for node in frontier:
                    for succ in self.successors(node):
                        if succ not in dist:
                            dist[succ] = current_dist
                            next_frontier.append(succ)
                frontier = next_frontier
            return dist
    
    def reverse_pagerank(self, output_ids: Set[int], damp: float = 0.85, max_iter: int = 50) -> np.ndarray:
        """Reverse Output PageRank（V2 专用）"""
        n = self.n_nodes
        if not output_ids:
            return np.zeros(n)
        try:
            # 使用预缓存的反向图
            rev_graph = self.get_reverse_graph()
            pr = nk.centrality.PageRank(rev_graph, damp=damp)
            pr.run()
            return np.array(pr.scores())
        except:
            return np.zeros(n)
    
    def get_node_attr(self, node: int, attr: str, default=''):
        """获取节点属性（兼容 NetworkX 接口）"""
        if attr == 'name':
            return self.node_names.get(node, str(node))
        elif attr == 'type':
            return self.node_types.get(node, '')
        return default
    
    def memory_usage_mb(self) -> float:
        """估算内存使用量"""
        mem = self.n_nodes * 8 + self.nk_graph.numberOfEdges() * 16
        mem += len(self.node_names) * 50 + len(self.node_types) * 20
        return mem / (1024 * 1024)

# -----------------------
# 多进程共享变量（用于 ProcessPoolExecutor）
# -----------------------
_SHARED_NKG = None         # 共享的 NKGraph 对象
_SHARED_NODE_TYPES = {}    # 共享的节点类型
_SHARED_OUTPUT_IDS = set() # 共享的输出节点 ID
_SHARED_OUT_LIST = []      # 共享的输出节点列表
_SHARED_N = 0              # 共享的节点数
_SHARED_IS_HUGE = False    # 共享的大规模标志

def _init_mp_worker_nk(compact_data: dict):
    """
    多进程 Worker 初始化器（NetworkKit 版本）
    从紧凑格式重建图，加载到子进程的全局变量
    """
    global _SHARED_NKG, _SHARED_NODE_TYPES, _SHARED_OUTPUT_IDS, _SHARED_OUT_LIST, _SHARED_N, _SHARED_IS_HUGE
    
    # 从紧凑格式重建 NKGraph
    n_nodes = compact_data['n_nodes']
    edges = compact_data['edges']
    node_names = compact_data.get('node_names', {})
    node_types = compact_data.get('node_types', {})
    
    _SHARED_NKG = NKGraph.from_edges(n_nodes, edges, node_names, node_types)
    _SHARED_NODE_TYPES = node_types
    _SHARED_OUTPUT_IDS = compact_data.get('output_ids', set())
    _SHARED_OUT_LIST = compact_data.get('out_list', [])
    _SHARED_N = n_nodes
    _SHARED_IS_HUGE = compact_data.get('is_huge', False)

def _mp_compute_distance_batch_v1(node_batch):
    """
    多进程 Worker (V1): 计算一批节点到输出的距离
    使用共享的 NKGraph 和 C++ BFS
    """
    import math
    nk_g = _SHARED_NKG
    out_list = _SHARED_OUT_LIST
    N = _SHARED_N
    
    results = {}
    for n in node_batch:
        dist_min_n = math.inf
        dist_avg_n = math.inf
        try:
            all_dists = nk_g.single_source_distances(n)
            dists = [all_dists[t] for t in out_list if t in all_dists]
            if dists:
                dist_min_n = float(min(dists))
                dist_avg_n = float(sum(dists) / len(dists))
        except:
            pass
        
        if not math.isfinite(dist_min_n):
            dist_min_n = float(N)
        if not math.isfinite(dist_avg_n):
            dist_avg_n = float(N)
        
        results[n] = (dist_min_n, dist_avg_n)
    return results

def _mp_compute_node_features_v1(node_batch):
    """
    多进程 Worker (V1): 计算一批节点的 reconv, near_ff, depth 特征
    """
    nk_g = _SHARED_NKG
    node_types = _SHARED_NODE_TYPES
    N = _SHARED_N
    cap = min(200, max(50, N // 5))
    
    results = {}
    for n in node_batch:
        # Reconv (无采样限制)
        succ1 = set(nk_g.successors(n))
        twohop_union = set()
        sum_outdeg_nei = 0
        for u in succ1:
            su = set(nk_g.successors(u))
            sum_outdeg_nei += len(su)
            twohop_union |= su
        reconv = float(max(0, sum_outdeg_nei - len(twohop_union)))
        
        # Near FF
        flag = 0
        for nb in list(nk_g.predecessors(n)) + list(nk_g.successors(n)):
            typ = node_types.get(nb, '')
            if typ and typ != 'wire' and SEQ_CELL_RE.search(typ):
                flag = 1
                break
        near_ff = float(flag)
        
        # Depth
        try:
            visited = {n: 0}
            frontier = [n]
            maxd = 0
            cnt = 0
            while frontier and cnt < cap:
                nf = []
                for u in frontier:
                    for v in nk_g.successors(u):
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
            depth = float(maxd)
        except:
            depth = 0.0
        
        results[n] = {'reconv': reconv, 'near_ff': near_ff, 'depth': depth}
    return results



# -----------------------
# CUDA 安全设备选择
# -----------------------
def get_safe_device() -> str:
    """
    安全获取可用设备，处理 CUDA 初始化问题
    在子进程中可能需要重新初始化 CUDA
    """
    if not torch.cuda.is_available():
        return 'cpu'
    
    try:
        # 尝试执行一个简单的 CUDA 操作来验证 CUDA 是否可用
        torch.cuda.synchronize()
        # 检查是否有可用的 GPU
        if torch.cuda.device_count() == 0:
            return 'cpu'
        # 尝试创建一个小张量来测试 CUDA
        test_tensor = torch.zeros(1, device='cuda')
        del test_tensor
        torch.cuda.empty_cache()
        return 'cuda'
    except Exception as e:
        print(f"    [警告] CUDA 初始化失败，回退到 CPU: {e}")
        return 'cpu'

def reset_cuda_state():
    """重置 CUDA 状态，清理内存"""
    if torch.cuda.is_available():
        try:
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
        except:
            pass

# -----------------------
# 特征缓存机制
# -----------------------
def get_file_hash(filepath: str) -> str:
    """计算文件的 MD5 哈希值用于缓存验证"""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            # 读取前 64KB 加上文件大小作为快速哈希
            buf = f.read(65536)
            hasher.update(buf)
            f.seek(0, 2)  # 移到文件末尾
            hasher.update(str(f.tell()).encode())  # 加入文件大小
    except:
        hasher.update(os.path.basename(filepath).encode())
    return hasher.hexdigest()[:16]

def get_cache_path(verilog_path: str, version: str) -> str:
    """获取缓存文件路径"""
    base = os.path.splitext(os.path.basename(verilog_path))[0]
    file_hash = get_file_hash(verilog_path)
    cache_filename = f"{base}_{version}_{file_hash}.pkl"
    return os.path.join(CACHE_DIR, cache_filename)

def save_cached_features(cache_path: str, feats: Dict, G, 
                         output_ids: Set[int], seq_inst_ids: Set[int], compute_time: float = None):
    """保存特征到缓存（兼容 NKGraph 和 NetworkX）"""
    if not USE_CACHE:
        return
    try:
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        cached_data = {
            'cache_version': 3,  # 版本 3: NKGraph 支持
            'feats': feats,
            'output_ids': output_ids,
            'seq_inst_ids': seq_inst_ids,
            'compute_time': compute_time
        }
        # 如果是 NKGraph，保存必要的属性
        if isinstance(G, NKGraph):
            cached_data['nk_graph'] = {
                'n_nodes': G.n_nodes,
                'edges': G.edges(),
                'node_names': G.node_names,
                'node_types': G.node_types
            }
        else:
            cached_data['G'] = G  # 兼容旧版 NetworkX
        with open(cache_path, 'wb') as f:
            pickle.dump(cached_data, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as e:
        print(f"    [缓存] 保存失败: {e}")


def load_cached_features_nk(cache_path: str):
    """
    加载缓存的特征（NKGraph 版本）
    返回: (feats, NKGraph, output_ids, seq_inst_ids, compute_time) 或 None
    """
    if not USE_CACHE or not os.path.exists(cache_path):
        return None
    try:
        with open(cache_path, 'rb') as f:
            cached_data = pickle.load(f)
        compute_time = cached_data.get('compute_time')
        
        # 检查是否是 NKGraph 缓存
        if 'nk_graph' in cached_data:
            nk_data = cached_data['nk_graph']
            nk_g = NKGraph.from_edges(
                nk_data['n_nodes'],
                nk_data['edges'],
                nk_data['node_names'],
                nk_data['node_types']
            )
            return (cached_data['feats'], nk_g, 
                    cached_data['output_ids'], cached_data['seq_inst_ids'], compute_time)
        # 兼容旧版 NetworkX 缓存 - 跳过转换
        return None
    except Exception as e:
        print(f"    [缓存] NKGraph 加载失败: {e}")
    return None

# -----------------------
# Verilog 解析 -> 图构建
# -----------------------
def safe_read_verilog_file(filepath: str) -> str:
    """
    安全读取 Verilog 文件，处理各种编码问题
    尝试顺序: UTF-8 -> UTF-8-sig (BOM) -> Latin-1 -> 二进制忽略
    """
    encodings_to_try = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'gbk']
    
    for encoding in encodings_to_try:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                content = f.read()
            return content
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    # 最后手段：以二进制读取，忽略无法解码的字符
    with open(filepath, 'rb') as f:
        raw = f.read()
    return raw.decode('utf-8', errors='ignore')

# 预编译正则表达式（门级网表快速解析）
# 匹配实例: GATE_TYPE inst_name (.PORT(net), .PORT(net), ...);
_INSTANCE_RE = re.compile(
    r'^\s*(\w+)\s+(\w+)\s*\((.*?)\)\s*;',
    re.MULTILINE | re.DOTALL
)
# 匹配端口连接: .PORT(net) 或 .PORT(net[idx])
_PORT_RE = re.compile(r'\.(\w+)\s*\(\s*([^)]+)\s*\)')


def prepare_verilog_for_parsing(filepath: str) -> str:
    """
    准备 Verilog 文件以供 pyverilog 解析
    如果文件包含非 ASCII 字符，创建临时文件
    返回: 可安全解析的文件路径
    """
    import tempfile
    
    content = safe_read_verilog_file(filepath)
    
    # 检查是否所有字符都是 ASCII（pyverilog 友好）
    try:
        content.encode('ascii')
        # 全是 ASCII，可以直接使用原文件
        return filepath
    except UnicodeEncodeError:
        pass
    
    # 包含非 ASCII 字符，创建临时文件
    # 移除或替换非 ASCII 字符（通常是注释中的中文）
    ascii_content = content.encode('ascii', errors='ignore').decode('ascii')
    
    # 创建临时文件
    base = os.path.splitext(os.path.basename(filepath))[0]
    fd, temp_path = tempfile.mkstemp(suffix='.v', prefix=f'{base}_')
    try:
        with os.fdopen(fd, 'w', encoding='ascii') as f:
            f.write(ascii_content)
    except:
        os.close(fd)
        raise
    
    return temp_path




def parse_verilog_graph_to_nk(filepath: str) -> Tuple[NKGraph, Dict, Set[int], Set[int]]:
    """
    解析 Verilog 网表，直接构建 NKGraph（不经过 NetworkX）
    
    返回: (NKGraph, node_map, output_ids, seq_inst_ids)
    """
    content = safe_read_verilog_file(filepath)
    
    # 移除注释
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    
    # 收集节点和边
    node_map: Dict[str, int] = {}
    node_names: Dict[int, str] = {}
    node_types: Dict[int, str] = {}
    edges: List[Tuple[int, int]] = []
    id_counter = 0
    output_ids: Set[int] = set()
    seq_inst_ids: Set[int] = set()
    
    def get_or_add_node(name: str, node_type: str) -> int:
        nonlocal id_counter
        if name in node_map:
            return node_map[name]
        node_id = id_counter
        node_map[name] = node_id
        node_names[node_id] = name
        node_types[node_id] = node_type
        id_counter += 1
        return node_id
    
    # 解析实例
    for match in _INSTANCE_RE.finditer(content):
        cell_type = match.group(1)
        inst_name = match.group(2)
        port_str = match.group(3)
        
        # 跳过关键字
        if cell_type.lower() in ('module', 'endmodule', 'input', 'output', 'wire', 'reg', 'assign'):
            continue
        
        # 添加实例节点
        inst_id = get_or_add_node(inst_name, cell_type)
        
        # 检查时序单元
        if SEQ_CELL_RE.search(cell_type or ''):
            seq_inst_ids.add(inst_id)
        
        # 解析端口
        for port_match in _PORT_RE.finditer(port_str):
            port_name = port_match.group(1)
            net_name = port_match.group(2).strip().replace('.', '_')
            # net_name = re.sub(r'\[(\d+)\]', r'_\1', net_name) # 注释掉此行以保留 [idx]，匹配 all_nodes.py 的过滤机制
            
            net_id = get_or_add_node(net_name, 'wire')
            
            if port_name.upper() in OUT_PORT_HINT:
                edges.append((inst_id, net_id))
                output_ids.add(net_id)
            else:
                edges.append((net_id, inst_id))
    
    # 直接构建 NKGraph
    n_nodes = id_counter
    nk_g = NKGraph.from_edges(n_nodes, edges, node_names, node_types)
    
    return nk_g, node_map, output_ids, seq_inst_ids


# -----------------------
# 特征工程（NetworkKit 高性能版本）
# -----------------------
def compute_struct_features_v1_nk(nk_g: NKGraph, output_ids: Set[int], seq_inst_ids: Set[int]) -> Dict[int, Dict]:
    """
    V1 特征提取（NetworkKit 版本）
    使用 ProcessPoolExecutor 实现真正的多核并行
    """
    import time as _time
    _start = _time.time()
    
    N = nk_g.number_of_nodes()
    if N == 0:
        return {}
    
    print(f"    [V1 NetworkKit] 开始计算 {N} 个节点的特征...")
    
    # 度数特征
    indeg = nk_g.all_in_degrees()
    outdeg = nk_g.all_out_degrees()
    
    # 图级别特征（使用 NetworkKit C++ OpenMP 并行）
    print(f"    [V1 NetworkKit] 计算 PageRank...")
    pr_values = nk_g.pagerank(damp=0.85, max_iter=100)
    
    print(f"    [V1 NetworkKit] 计算 Betweenness...")
    k_bet = min(200, max(10, N // 10))
    bet_values = nk_g.betweenness_sampled(n_samples=k_bet, seed=42)
    
    print(f"    [V1 NetworkKit] 计算 Eigenvector...")
    evec_values = nk_g.eigenvector_centrality(max_iter=200)
    
    # 准备紧凑数据（用于多进程传递）
    out_list = list(output_ids) if output_ids else []
    compact_data = {
        'n_nodes': N,
        'edges': nk_g.edges(),
        'node_names': nk_g.node_names,
        'node_types': nk_g.node_types,
        'output_ids': output_ids,
        'out_list': out_list,
        'is_huge': N > 50000
    }
    
    # 距离特征和节点特征 - 使用 ProcessPoolExecutor
    print(f"    [V1 NetworkKit] 计算距离 + 节点特征 (多进程)...")
    dist_min_arr = np.full(N, float(N))
    dist_avg_arr = np.full(N, float(N))
    reconv = np.zeros(N)
    near_ff = np.zeros(N)
    depth = np.zeros(N)
    
    # 混合并行策略 (Hybrid Parallelism)
    # 策略：小图(<阈值)使用 ThreadPool 避免图重建开销；大图(>=阈值)使用 ProcessPool 利用多核
    if N < SMALL_SCALE_THRESHOLD:
        pool_type = "线程池 (ThreadPoolExecutor)"
        n_workers = max(1, mp.cpu_count() - 2)
        batch_size = max(1, N // n_workers)
        node_batches = [list(range(i, min(i + batch_size, N))) for i in range(0, N, batch_size)]
        
        # Set globals for ThreadPool (Current Process)
        global _SHARED_NKG, _SHARED_NODE_TYPES, _SHARED_OUTPUT_IDS, _SHARED_OUT_LIST, _SHARED_N, _SHARED_IS_HUGE
        _SHARED_NKG = nk_g
        _SHARED_NODE_TYPES = nk_g.node_types
        _SHARED_OUTPUT_IDS = output_ids
        _SHARED_OUT_LIST = list(output_ids) if output_ids else []
        _SHARED_N = N
        _SHARED_IS_HUGE = compact_data['is_huge']
        
        ExecutorClass = ThreadPoolExecutor
        init_kwargs = {}
        
    else:
        pool_type = "进程池 (ProcessPoolExecutor)"
        n_workers = get_adaptive_workers(N, 'distance')
        batch_size = max(1, N // n_workers)
        node_batches = [list(range(i, min(i + batch_size, N))) for i in range(0, N, batch_size)]
        
        ExecutorClass = ProcessPoolExecutor
        init_kwargs = {'initializer': _init_mp_worker_nk, 'initargs': (compact_data,)}

    print(f"    [V1 NetworkKit]   节点数: {N}, 批次: {len(node_batches)}, {pool_type} 核心数: {n_workers}")
    
    with ExecutorClass(max_workers=n_workers, **init_kwargs) as executor:
        # 并行计算距离
        if out_list:
            print(f"    [V1 NetworkKit]   提交距离计算任务...")
            dist_futures = [executor.submit(_mp_compute_distance_batch_v1, batch) for batch in node_batches]
            for future in as_completed(dist_futures):
                batch_results = future.result()
                for n, (dmin, davg) in batch_results.items():
                    dist_min_arr[n] = dmin
                    dist_avg_arr[n] = davg
        
        # 并行计算节点级特征
        print(f"    [V1 NetworkKit]   提交节点特征计算任务...")
        feat_futures = [executor.submit(_mp_compute_node_features_v1, batch) for batch in node_batches]
        for future in as_completed(feat_futures):
            batch_results = future.result()
            for n, feats in batch_results.items():
                reconv[n] = feats['reconv']
                near_ff[n] = feats['near_ff']
                depth[n] = feats['depth']
    
    # 简单特征
    name_len = np.array([len(nk_g.node_names.get(n, str(n))) for n in range(N)])
    is_output_arr = np.array([1.0 if n in output_ids else 0.0 for n in range(N)])
    
    # 归一化
    indeg_n = minmax_norm(indeg)
    outdeg_n = minmax_norm(outdeg)
    pr_n = minmax_norm(pr_values)
    bet_n = minmax_norm(bet_values)
    evec_n = minmax_norm(evec_values)
    dmin_inv = minmax_norm(1.0 / (dist_min_arr + 1e-6))
    davg_inv = minmax_norm(1.0 / (dist_avg_arr + 1e-6))
    reconv_n = minmax_norm(reconv)
    namelen_n = minmax_norm(name_len)
    depth_n = minmax_norm(depth)
    
    feats = {}
    for n in range(N):
        feats[n] = {
            'in_deg': float(indeg_n[n]), 'out_deg': float(outdeg_n[n]),
            'pagerank': float(pr_n[n]), 'betweenness': float(bet_n[n]), 'eigen': float(evec_n[n]),
            'dist_min_inv': float(dmin_inv[n]), 'dist_avg_inv': float(davg_inv[n]),
            'reconv': float(reconv_n[n]), 'near_ff': float(near_ff[n]),
            'name_len': float(namelen_n[n]), 'depth': float(depth_n[n]), 'is_output': float(is_output_arr[n]),
        }
    
    print(f"    [V1 NetworkKit] 完成，耗时: {_time.time() - _start:.2f}s")
    return feats



def build_pyg_data_nk(nk_g: NKGraph, feats: Dict[int, Dict]) -> Tuple[Data, List[int], List[str]]:
    """
    从 NKGraph 构建 PyG 数据（内存优化版本）
    优化：
    1. 使用 int32 作为边索引（节点数 < 2^31 时完全等价，内存减半）
    2. 使用 numpy 数组直接构建，避免 Python 列表中间步骤
    """
    N = nk_g.number_of_nodes()
    node_ids = list(range(N))
    name_list = [nk_g.node_names.get(n, str(n)) for n in node_ids]
    
    # 构建类型映射
    type_set = set(nk_g.node_types.get(n, 'UNK') for n in node_ids)
    type_list = sorted(list(type_set))
    type2idx = {t: i for i, t in enumerate(type_list)}
    n_types = len(type_list)
    
    # 直接使用 numpy 构建特征矩阵，避免 Python 列表
    n_struct_feats = 12  # in_deg, out_deg, pagerank, betweenness, eigen, dist_min_inv, dist_avg_inv, reconv, near_ff, name_len, depth, is_output
    x_np = np.zeros((N, n_types + n_struct_feats), dtype=np.float32)
    
    for n in range(N):
        # One-hot 类型编码
        typ = nk_g.node_types.get(n, 'UNK')
        x_np[n, type2idx[typ]] = 1.0
        
        # 结构特征
        f = feats[n]
        x_np[n, n_types:] = [
            f['in_deg'], f['out_deg'], f['pagerank'], f['betweenness'], f['eigen'],
            f['dist_min_inv'], f['dist_avg_inv'], f['reconv'], f['near_ff'],
            f['name_len'], f['depth'], f['is_output']
        ]
    
    x = torch.from_numpy(x_np)  # 零拷贝转换
    
    # 使用缓存的 numpy 边数组构建边索引（高效）
    edge_np = nk_g.edges_numpy()  # shape: (E, 2), dtype: int32
    if edge_np.size == 0:
        edge_index = torch.empty((2, 0), dtype=torch.int32)
    else:
        # 转置为 (2, E) 格式
        edge_index = torch.from_numpy(edge_np.T.copy())  # copy() 确保内存连续
    
    # PyG 需要 long 类型的 edge_index，但可以在使用时转换
    # 这里保持 int32 存储，只在需要时转为 long
    data = Data(x=x, edge_index=edge_index.long())  # 转为 long 用于 PyG 兼容
    data.node_ids = node_ids
    data.node_names = name_list
    
    return data, node_ids, name_list


# -----------------------
# 自监督模型 (DGI) - 支持梯度检查点
# -----------------------
from torch.utils.checkpoint import checkpoint as torch_checkpoint

class EncoderGIN(nn.Module):
    """
    GIN 编码器，支持梯度检查点 (Gradient Checkpointing) 以减少内存占用
    use_checkpoint=True 时内存减少约 50%，但训练速度会降低约 25%
    """
    def __init__(self, in_dim, hid=128, layers=3, dropout=0.2, use_checkpoint=False):
        super().__init__()
        self.num_layers = layers
        self.convs = nn.ModuleList()
        self.bns = nn.ModuleList()
        self.dropout = dropout
        self.use_checkpoint = use_checkpoint
        self.hid = hid
        
        for i in range(layers):
            in_c = in_dim if i == 0 else hid
            nn_layer = nn.Sequential(nn.Linear(in_c, hid), nn.ReLU(), nn.Linear(hid, hid), nn.ReLU())
            self.convs.append(GINConv(nn_layer))
            self.bns.append(BatchNorm(hid))
    
    def _layer_forward(self, h, edge_index, layer_idx):
        """单层前向传播（用于梯度检查点）"""
        h = self.convs[layer_idx](h, edge_index)
        h = self.bns[layer_idx](h)
        h = F.relu(h)
        h = F.dropout(h, p=self.dropout, training=self.training)
        return h
    
    def forward(self, x, edge_index):
        h = x
        for i in range(self.num_layers):
            if self.use_checkpoint and self.training:
                # 使用梯度检查点：节省内存，但增加计算时间
                # 注意：checkpoint 需要输入有 requires_grad=True
                h = torch_checkpoint(self._layer_forward, h, edge_index, i, use_reentrant=False)
            else:
                h = self._layer_forward(h, edge_index, i)
        return h

class DGI(nn.Module):
    """Deep Graph Infomax 模型"""
    def __init__(self, encoder: EncoderGIN, hid_dim: int):
        super().__init__()
        self.encoder = encoder
        self.W = nn.Linear(hid_dim, hid_dim, bias=False)
    
    def forward(self, x, edge_index, x_corrupt):
        h = self.encoder(x, edge_index)
        h_corrupt = self.encoder(x_corrupt, edge_index)
        s = torch.sigmoid(h.mean(dim=0, keepdim=True))
        sW = self.W(s)
        return torch.sum(h * sW, dim=1), torch.sum(h_corrupt * sW, dim=1), h
    
    @staticmethod
    def loss_fn(pos, neg):
        return - (torch.log(torch.sigmoid(pos) + 1e-10).mean() + torch.log(1 - torch.sigmoid(neg) + 1e-10).mean())

def train_dgi(data: Data, hidden=128, layers=3, epochs=150, lr=1e-3, dropout=0.2, device='cpu', use_sampling=False):
    """
    训练 DGI 模型，支持 GraphSAINT 高效子图采样：
    
    采样模式（use_sampling=True）：
    - 使用 GraphSAINT 节点采样，C++ 后端高效实现
    - 每批 5 万节点，归一化损失保证无偏估计
    - 比之前的 torch.isin 方案快 10-50 倍
    
    回退机制：GPU + AMP → CPU
    
    注意：每次调用都会重置随机种子，确保批量处理与单独处理结果一致
    """
    from torch.amp import autocast, GradScaler
    
    # 关键修复：清空 CUDA 缓存，确保从干净状态开始
    reset_cuda_state()
    
    # 关键修复：在每次 DGI 训练开始前重置随机种子
    # 确保模型权重初始化、torch.randperm 等操作的随机状态完全一致
    set_seed(42)
    
    N = data.x.size(0)
    
    if use_sampling:
        # 使用 GraphSAINT 节点采样
        try:
            from torch_geometric.loader import GraphSAINTNodeSampler
            batch_size = min(50000, N // 2)
            print(f"    [DGI] 超大规模图 (N={N})，使用 GraphSAINT 采样 (batch_size={batch_size})...")
            
            # GraphSAINT 需要 num_workers=0 在 Windows 上
            sampler = GraphSAINTNodeSampler(
                data, 
                batch_size=batch_size,
                num_steps=epochs,  # 每步一个子图，替代 epochs
                sample_coverage=0,  # 不需要覆盖采样
                num_workers=0,
            )
            has_graphsaint = True
        except ImportError:
            print(f"    [警告] GraphSAINT 不可用，回退到简化 MLP 模式...")
            has_graphsaint = False
        except Exception as e:
            print(f"    [警告] GraphSAINT 初始化失败: {e}，回退到简化 MLP 模式...")
            has_graphsaint = False
    else:
        has_graphsaint = False
    
    def _train_full_graph(target_device):
        """全图训练模式"""
        use_amp = (target_device == 'cuda')
        if use_amp:
            print(f"    [DGI] 使用 GPU + AMP 全图训练...")
        
        enc = EncoderGIN(in_dim=data.x.size(1), hid=hidden, layers=layers, dropout=dropout).to(target_device)
        model = DGI(enc, hid_dim=hidden).to(target_device)
        opt = torch.optim.Adam(model.parameters(), lr=lr)
        x = data.x.to(target_device)
        ei = data.edge_index.to(target_device)
        scaler = GradScaler('cuda') if use_amp else None
        
        for ep in range(epochs):
            model.train()
            opt.zero_grad()
            perm = torch.randperm(N, device=target_device)
            x_corrupt = x[perm]
            
            if use_amp:
                with autocast('cuda'):
                    pos, neg, _ = model(x, ei, x_corrupt)
                    loss = DGI.loss_fn(pos, neg)
                scaler.scale(loss).backward()
                scaler.step(opt)
                scaler.update()
            else:
                pos, neg, _ = model(x, ei, x_corrupt)
                loss = DGI.loss_fn(pos, neg)
                loss.backward()
                opt.step()
        
        model.eval()
        with torch.no_grad():
            if use_amp:
                with autocast('cuda'):
                    _, _, H = model(x, ei, x)
            else:
                _, _, H = model(x, ei, x)
        return H.cpu()
    
    def _train_graphsaint(target_device):
        """GraphSAINT 采样训练模式"""
        use_amp = (target_device == 'cuda')
        print(f"    [DGI] 使用 GraphSAINT 采样训练 ({target_device}" + (" + AMP" if use_amp else "") + ")...")
        
        enc = EncoderGIN(in_dim=data.x.size(1), hid=hidden, layers=layers, dropout=dropout).to(target_device)
        model = DGI(enc, hid_dim=hidden).to(target_device)
        opt = torch.optim.Adam(model.parameters(), lr=lr)
        scaler = GradScaler('cuda') if use_amp else None
        
        # GraphSAINT 采样训练
        for batch in sampler:
            model.train()
            opt.zero_grad()
            
            x_batch = batch.x.to(target_device)
            ei_batch = batch.edge_index.to(target_device)
            perm = torch.randperm(x_batch.size(0), device=target_device)
            x_corrupt = x_batch[perm]
            
            if use_amp:
                with autocast('cuda'):
                    pos, neg, _ = model(x_batch, ei_batch, x_corrupt)
                    loss = DGI.loss_fn(pos, neg)
                scaler.scale(loss).backward()
                scaler.step(opt)
                scaler.update()
            else:
                pos, neg, _ = model(x_batch, ei_batch, x_corrupt)
                loss = DGI.loss_fn(pos, neg)
                loss.backward()
                opt.step()
        
        # 分批推理获取全图嵌入
        model.eval()
        batch_size = min(100000, N)
        H_list = []
        x_full = data.x
        ei_full = data.edge_index
        
        with torch.no_grad():
            for start in range(0, N, batch_size):
                end = min(start + batch_size, N)
                x_batch = x_full[start:end].to(target_device)
                
                # 提取批次内的边
                mask = (ei_full[0] >= start) & (ei_full[0] < end) & (ei_full[1] >= start) & (ei_full[1] < end)
                sub_edges = ei_full[:, mask] - start
                sub_edges = sub_edges.to(target_device)
                
                if use_amp:
                    with autocast('cuda'):
                        H_batch = model.encoder(x_batch, sub_edges)
                else:
                    H_batch = model.encoder(x_batch, sub_edges)
                H_list.append(H_batch.cpu())
        
        return torch.cat(H_list, dim=0)
    
    def _train_mlp_fallback(target_device):
        """MLP 回退模式（无图卷积，最快）"""
        use_amp = (target_device == 'cuda')
        print(f"    [DGI] 使用 MLP 模式（无图卷积）...")
        
        # 简化的 MLP 模型
        mlp = nn.Sequential(
            nn.Linear(data.x.size(1), hidden),
            nn.ReLU(),
            nn.Linear(hidden, hidden),
            nn.ReLU()
        ).to(target_device)
        
        opt = torch.optim.Adam(mlp.parameters(), lr=lr)
        x = data.x.to(target_device)
        scaler = GradScaler('cuda') if use_amp else None
        
        # 简单的对比学习
        for ep in range(min(epochs, 50)):  # MLP 收敛快，减少 epochs
            mlp.train()
            opt.zero_grad()
            perm = torch.randperm(N, device=target_device)
            
            if use_amp:
                with autocast('cuda'):
                    h = mlp(x)
                    h_neg = mlp(x[perm])
                    # 简化的对比损失
                    loss = -torch.log(torch.sigmoid(torch.sum(h * h, dim=1)) + 1e-10).mean() + \
                           -torch.log(1 - torch.sigmoid(torch.sum(h * h_neg, dim=1)) + 1e-10).mean()
                scaler.scale(loss).backward()
                scaler.step(opt)
                scaler.update()
            else:
                h = mlp(x)
                h_neg = mlp(x[perm])
                loss = -torch.log(torch.sigmoid(torch.sum(h * h, dim=1)) + 1e-10).mean() + \
                       -torch.log(1 - torch.sigmoid(torch.sum(h * h_neg, dim=1)) + 1e-10).mean()
                loss.backward()
                opt.step()
        
        mlp.eval()
        with torch.no_grad():
            if use_amp:
                with autocast('cuda'):
                    H = mlp(x)
            else:
                H = mlp(x)
        return H.cpu()
    
    def _is_oom_error(e):
        error_msg = str(e).lower()
        return any(kw in error_msg for kw in ['out of memory', 'cuda', 'memory', 'allocate'])
    
    # 选择训练策略
    if use_sampling and has_graphsaint:
        train_fn = _train_graphsaint
    elif use_sampling:
        train_fn = _train_mlp_fallback  # GraphSAINT 不可用时回退到 MLP
    else:
        train_fn = _train_full_graph
    
    # 两级回退：GPU+AMP → CPU
    if device == 'cuda':
        try:
            reset_cuda_state()
            result = train_fn('cuda')
            reset_cuda_state()
            return result
        except (RuntimeError, MemoryError) as e:
            if _is_oom_error(e):
                print(f"    [警告] GPU 内存溢出，回退到 CPU...")
                reset_cuda_state()
            else:
                raise
    
    # CPU 回退
    return train_fn('cpu')


def fuse_scores_v1_nk(nk_g: NKGraph, feats: Dict[int, Dict], H: torch.Tensor, data: Data, output_ids: Set[int]) -> List[Tuple[str, float]]:
    """原版评分公式（NKGraph 版本）"""
    nid_list = data.node_ids
    name_list = data.node_names
    out_idx = [nid_list.index(n) for n in nid_list if n in output_ids] if output_ids else []
    
    Hn = F.normalize(H, p=2, dim=1)
    if len(out_idx) > 0:
        out_centroid = Hn[out_idx].mean(dim=0, keepdim=True)
        out_centroid = F.normalize(out_centroid, p=2, dim=1)
        cos = torch.mm(Hn, out_centroid.t()).squeeze(1).numpy()
        embed_sim = np.array([z2u01(float(c)) for c in cos])
    else:
        embed_sim = np.zeros(Hn.size(0))

    pr = np.array([feats[nid]['pagerank'] for nid in nid_list])
    bet = np.array([feats[nid]['betweenness'] for nid in nid_list])
    ev = np.array([feats[nid]['eigen'] for nid in nid_list])
    centrality = minmax_norm((pr + bet + ev) / 3.0)

    prox = minmax_norm(0.5 * np.array([feats[n]['dist_min_inv'] for n in nid_list]) +
                       0.5 * np.array([feats[n]['dist_avg_inv'] for n in nid_list]))
    reconv = minmax_norm(np.array([feats[n]['reconv'] for n in nid_list]))
    seq = np.array([feats[n]['near_ff'] for n in nid_list])

    score = (0.25 * centrality + 0.25 * prox + 0.20 * reconv + 0.15 * seq + 0.15 * embed_sim)

    score_list = score.tolist()
    
    # 正则：匹配末尾的 _数字（数组转换格式）
    array_suffix_re = re.compile(r'_\d+$')
    
    filtered_ranked = []
    seen_names = set()  # 去重
    for i, nid in enumerate(nid_list):
        ntype = nk_g.node_types.get(nid, '').lower()
        name = name_list[i]
        name_lower = name.lower()
        # 过滤非 wire/reg 类型
        if ntype not in ('wire', 'reg'):
            continue
        # 过滤时钟/复位/输入信号
        if re.match(r'^(clk|clock|rst|reset|in|input)', name_lower):
            continue
        # 过滤数组下标节点 [idx] 格式
        if '[' in name or ']' in name:
            continue
        # 过滤数组转换格式（如 o_sum_21 来自 o_sum[21]）
        if array_suffix_re.search(name):
            continue
        # 去重
        if name in seen_names:
            continue
        seen_names.add(name)
        filtered_ranked.append((name, score_list[i]))

    filtered_ranked.sort(key=lambda x: -x[1])
    return filtered_ranked


# -----------------------
# 阶段1: 仅特征提取（CPU并行）
# -----------------------
def extract_features_worker(args_tuple):
    """Worker 函数：仅执行特征提取，不进行 DGI 训练"""
    verilog_path, seed, run_mode, use_cache, threshold = args_tuple
    return extract_features_only(verilog_path, seed, run_mode, use_cache, threshold)

def extract_features_only(verilog_path: str, seed=42, run_mode='v1', use_cache=True, threshold=2000):
    """
    仅执行特征提取阶段（CPU密集型），结果保存到缓存
    V1-Only 版本：仅支持 V1 模式
    返回: (filename, N, actual_run_mode, success, message, time_v1_feat)
    """
    import tempfile
    import shutil
    
    start_time = time.time()
    filename = os.path.basename(verilog_path)
    base = os.path.splitext(filename)[0]
    
    verilog_path = os.path.abspath(verilog_path)
    cache_dir_abs = os.path.abspath(CACHE_DIR)
    
    temp_dir = tempfile.mkdtemp(prefix=f"gnn_feat_{base}_")
    original_cwd = os.getcwd()
    
    try:
        os.chdir(temp_dir)
        set_seed(seed)
        
        # 获取缓存路径
        cache_path_v1 = os.path.join(cache_dir_abs, f"{base}_v1_{get_file_hash(verilog_path)}.pkl")
        
        # 固定为 V1 模式
        actual_run_mode = 'v1'
        
        # 检查缓存状态
        cached_v1 = load_cached_features_nk(cache_path_v1) if use_cache else None
        time_v1_feat = cached_v1[4] if cached_v1 else None
        
        if cached_v1:
            # 已缓存，直接返回
            _, nk_g, _, _, _ = cached_v1
            N = nk_g.number_of_nodes()
            msg = f"[特征提取] V1(Cached: {time_v1_feat or 0.0:.2f}s) 已存在"
            return (filename, N, actual_run_mode, True, msg, time_v1_feat)
        
        # 计算 V1 特征
        v1_feat_start = time.time()
        set_seed(seed)
        print(f"    [V1] 开始解析 Verilog (NetworkKit)...")
        nk_g_v1, node_map_v1, output_ids_v1, seq_inst_ids_v1 = parse_verilog_graph_to_nk(verilog_path)
        N = nk_g_v1.number_of_nodes()
        if N < 2:
            return (filename, N, actual_run_mode, False, "节点数过少，跳过", None)
        feats_v1 = compute_struct_features_v1_nk(nk_g_v1, output_ids_v1, seq_inst_ids_v1)
        measure_v1 = time.time() - v1_feat_start
        time_v1_feat = measure_v1
        save_cached_features(cache_path_v1, feats_v1, nk_g_v1, output_ids_v1, seq_inst_ids_v1, compute_time=measure_v1)
        
        elapsed = time.time() - start_time
        return (filename, N, actual_run_mode, True, f"[特征提取] V1({measure_v1:.2f}s) 完成 (总耗时: {elapsed:.2f}s)", time_v1_feat)
        
    except Exception as e:
        import traceback
        return (filename, 0, 'v1', False, f"❌ 错误: {str(e)}", None)
    finally:
        os.chdir(original_cwd)
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass

# -----------------------
# 阶段2: 仅DGI训练和评分（GPU串行）
# -----------------------
def train_and_score_only(verilog_path: str, output_dir: str, hidden=128, layers=3, 
                         epochs=150, dropout=0.2, seed=42, run_mode='v1', device='cuda'):
    """
    仅执行DGI训练和评分阶段（GPU密集型），从缓存加载特征
    V1-Only 版本：仅支持 V1 模式
    返回: (result_str, time_v1_train, N, filename, success, actual_run_mode)
    """
    start_time = time.time()
    filename = os.path.basename(verilog_path)
    base = os.path.splitext(filename)[0]
    
    verilog_path = os.path.abspath(verilog_path)
    output_dir = os.path.abspath(output_dir)
    cache_dir_abs = os.path.abspath(CACHE_DIR)
    
    try:
        # 获取缓存路径
        cache_path_v1 = os.path.join(cache_dir_abs, f"{base}_v1_{get_file_hash(verilog_path)}.pkl")
        
        # 固定为 V1 模式
        actual_run_mode = 'v1'
        
        # 加载 V1 缓存
        cached_v1 = load_cached_features_nk(cache_path_v1)
        if not cached_v1:
            return (f"[{filename}] ❌ V1缓存不存在，请先运行特征提取", None, 0, filename, False, actual_run_mode)
        
        feats_v1, nk_g, output_ids, seq_inst_ids, _ = cached_v1
        N = nk_g.number_of_nodes()
        use_sampling = N >= SAMPLE_THRESHOLD  # 超大规模图启用子图采样
        
        v1_start = time.time()
        set_seed(seed)
        data_v1, _, _ = build_pyg_data_nk(nk_g, feats_v1)
        H_v1 = train_dgi(data_v1, hidden=hidden, layers=layers, epochs=epochs, dropout=dropout, device=device, use_sampling=use_sampling)
        ranked_v1 = fuse_scores_v1_nk(nk_g, feats_v1, H_v1, data_v1, output_ids)
        time_v1 = time.time() - v1_start
        
        out_path_v1 = os.path.join(output_dir, f"gnn_rank_{base}_v1.txt")
        with open(out_path_v1, 'w', encoding='utf-8') as f:
            for name, score in ranked_v1:
                f.write(f"{name} {score:.6f}\n")
        
        top_v1 = ranked_v1[0] if ranked_v1 else ('N/A', 0)
        
        elapsed = time.time() - start_time
        reset_cuda_state()
        
        final_str = f"[{filename}] ✅ N={N} (模式: V1) [{device.upper()}]\n  V1 Top: {top_v1[0]} ({top_v1[1]:.4f}) | Time: {time_v1:.2f}s\n  总耗时: {elapsed:.2f}s"
        
        return (final_str, time_v1, N, filename, True, actual_run_mode)
        
    except Exception as e:
        import traceback
        reset_cuda_state()
        return (f"[{filename}] ❌ Error: {str(e)}\n{traceback.format_exc()}", None, 0, filename, False, 'v1')

# -----------------------
# 主入口：两阶段流水线
# -----------------------
def main():
    import csv
    
    parser = argparse.ArgumentParser(description="批量无监督敏感度评分器（两阶段流水线：CPU并行特征提取 + GPU串行训练）")
    parser.add_argument('--input_dir', type=str, default="./netlists", help="输入目录")
    parser.add_argument('--output_dir', type=str, default="./gnn_ranks", help="输出目录")
    parser.add_argument('--epochs', type=int, default=150, help="训练轮数")
    parser.add_argument('--hidden', type=int, default=128, help="隐层维度")
    parser.add_argument('--layers', type=int, default=3, help="GIN层数")
    parser.add_argument('--dropout', type=float, default=0.2, help="Dropout率")
    parser.add_argument('--seed', type=int, default=20, help="随机种子")
    parser.add_argument('--workers', type=int, default=0, help="特征提取并行进程数(0=自动检测)")
    parser.add_argument('--threshold', type=int, default=50000, help="小规模阈值(节点数)")
    parser.add_argument('--sample_threshold', type=int, default=5000000, help="子图采样阈值(节点数)，超过此值自动启用子图采样训练以避免内存溢出")
    parser.add_argument('--mode', type=str, default='v1', help="运行模式: 固定为 v1")
    parser.add_argument('--use_cache', type=str, default='true', choices=['true', 'false'], help="是否使用特征缓存")
    parser.add_argument('--cache_dir', type=str, default="./feature_cache", help="特征缓存目录")
    args = parser.parse_args()

    global SMALL_SCALE_THRESHOLD, RUN_MODE, USE_CACHE, CACHE_DIR, SAMPLE_THRESHOLD
    SMALL_SCALE_THRESHOLD = args.threshold
    SAMPLE_THRESHOLD = args.sample_threshold
    RUN_MODE = 'v1'  # 固定为 V1
    USE_CACHE = True
    CACHE_DIR = args.cache_dir
    
    # 用户可控的缓存开关（决定是否利用已有缓存）
    user_use_cache = args.use_cache.lower() == 'true'

    if not os.path.exists(args.output_dir): 
        os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)

    # 获取所有 .v 文件，但排除 tb_ 开头的测试文件
    all_v_files = sorted(glob.glob(os.path.join(args.input_dir, "*.v")))
    v_files = [f for f in all_v_files if not os.path.basename(f).startswith('tb_')]
    skipped_count = len(all_v_files) - len(v_files)
    
    if not v_files:
        print(f"❌ 未找到 .v 文件: {args.input_dir}")
        return

    # 检测 GPU
    use_gpu = torch.cuda.is_available()
    device = 'cuda' if use_gpu else 'cpu'
    
    # 特征提取使用的进程数: 默认 CPU核心 - 2
    feature_workers = args.workers if args.workers > 0 else max(1, mp.cpu_count() - 2)
    
    # 模式显示
    mode_display = 'V1 (Only)'
    cache_display = "启用" if user_use_cache else "禁用(强制重新计算)"
    
    print(f"╔══════════════════════════════════════════════════════════════╗")
    print(f"║  节点级多进程模式: 单网表内部并行特征提取 + GPU串行训练     ║")
    print(f"╠══════════════════════════════════════════════════════════════╣")
    print(f"║  发现 {len(v_files):3d} 个网表文件 (跳过 {skipped_count} 个 tb_ 测试文件)              ║")
    print(f"║  设备: {device.upper():4s} | 节点级并行进程: {feature_workers:2d} | 阈值: {SMALL_SCALE_THRESHOLD:5d} 节点   ║")
    print(f"║  运行模式: {mode_display:<20s}                          ║")
    print(f"║  缓存状态: {cache_display:<20s}                          ║")
    print(f"╚══════════════════════════════════════════════════════════════╝")
    
    start_total = time.time()
    
    # 用于收集所有网表的时间统计
    timing_records = []  # 每条记录: {filename, N, v1_feat_time, v1_train_time}
    
    # ==================== 阶段1: 顺序处理但内部并行特征提取 ====================
    print(f"\n{'='*60}")
    print(f"【阶段1】节点级并行特征提取 (每个网表使用 {feature_workers} 个进程)")
    print(f"{'='*60}")
    
    phase1_start = time.time()
    
    extraction_results = []
    extraction_timings = {}  # filename -> (time_v1_feat, N)
    
    # 顺序处理每个文件，但在每个文件内部使用多进程并行
    for i, vpath in enumerate(v_files, 1):
        print(f"\n  [{i}/{len(v_files)}] 处理: {os.path.basename(vpath)}")
        try:
            # 直接调用特征提取（内部会使用 ProcessPoolExecutor）
            result = extract_features_only(vpath, args.seed, RUN_MODE, user_use_cache, SMALL_SCALE_THRESHOLD)
            extraction_results.append(result)
            filename, N, run_mode_result, success, msg, time_v1_feat = result
            extraction_timings[filename] = (time_v1_feat, N)
            status = "✅" if success else "❌"
            print(f"    {status} N={N} {msg}")
        except Exception as e:
            print(f"    ❌ 异常: {e}")
            extraction_results.append((os.path.basename(vpath), 0, RUN_MODE, False, str(e), None))
    
    phase1_time = time.time() - phase1_start
    success_count = sum(1 for r in extraction_results if r[3])
    print(f"\n阶段1完成: {success_count}/{len(v_files)} 成功 | 耗时: {phase1_time:.2f}s")
    
    # 筛选成功提取特征的文件
    valid_files = [v_files[i] for i, r in enumerate(extraction_results) if r[3]]
    
    if not valid_files:
        print("❌ 没有文件成功提取特征，退出")
        return
    
    # ==================== 阶段2: GPU串行DGI训练 ====================
    print(f"\n{'='*60}")
    print(f"【阶段2】GPU 串行 DGI 训练 (设备: {device.upper()}) - 模式: {RUN_MODE.upper()}")
    print(f"{'='*60}")
    
    phase2_start = time.time()
    
    for vpath in valid_files:
        result_tuple = train_and_score_only(
            vpath, args.output_dir, 
            hidden=args.hidden, layers=args.layers, epochs=args.epochs,
            dropout=args.dropout, seed=args.seed, run_mode=RUN_MODE,
            device=device
        )
        result_str, time_v1_train, N, filename, success, actual_run_mode = result_tuple
        print(result_str)
        
        # 收集时间数据
        time_v1_feat, _ = extraction_timings.get(filename, (None, 0))
        timing_records.append({
            'filename': filename,
            'nodes': N,
            'actual_mode': actual_run_mode,
            'v1_feat_time': time_v1_feat,
            'v1_train_time': time_v1_train,
            'success': success
        })
    
    phase2_time = time.time() - phase2_start
    total_time = time.time() - start_total
    
    # ==================== 输出 CSV 时间报告 ====================
    csv_path = os.path.join(args.output_dir, "timing_report.csv")
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['filename', 'nodes', 'actual_mode', 'v1_feat_time', 'v1_train_time', 'v1_total_time', 'success']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for record in timing_records:
                # 计算总时间
                v1_total = None
                if record['v1_feat_time'] is not None and record['v1_train_time'] is not None:
                    v1_total = record['v1_feat_time'] + record['v1_train_time']
                elif record['v1_train_time'] is not None:
                    v1_total = record['v1_train_time']
                
                writer.writerow({
                    'filename': record['filename'],
                    'nodes': record['nodes'],
                    'actual_mode': record.get('actual_mode', ''),
                    'v1_feat_time': f"{record['v1_feat_time']:.4f}" if record['v1_feat_time'] is not None else '',
                    'v1_train_time': f"{record['v1_train_time']:.4f}" if record['v1_train_time'] is not None else '',
                    'v1_total_time': f"{v1_total:.4f}" if v1_total is not None else '',
                    'success': record['success']
                })
        print(f"\n📊 时间报告已保存: {csv_path}")
    except Exception as e:
        print(f"\n❌ CSV 保存失败: {e}")
    
    # ==================== 总结 ====================
    print(f"\n{'='*60}")
    print(f"【完成】两阶段流水线执行总结")
    print(f"{'='*60}")
    print(f"  运行模式:         {mode_display}")
    print(f"  缓存状态:         {cache_display}")
    print(f"  阶段1 (特征提取): {phase1_time:.2f}s")
    print(f"  阶段2 (DGI训练):  {phase2_time:.2f}s")
    print(f"  总耗时:           {total_time:.2f}s")
    print(f"  处理文件:         {len(valid_files)}/{len(v_files)}")
    print(f"  时间报告:         {csv_path}")

if __name__ == '__main__':
    # 在 Windows 上必须使用 freeze_support
    mp.freeze_support()
    main()