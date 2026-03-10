"""
运行 unsup_sensitivity.py 并生成泰勒图数据
该脚本会：
1. 解析 Verilog 网表构建图
2. 计算每个节点的5个特征维度得分
3. 基于这些得分计算泰勒图所需的统计指标（标准差、RMSE、相关系数）
"""

import os
import sys
import time
import numpy as np
import pandas as pd
import networkx as nx
from typing import List, Tuple, Dict, Set

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.nn import GINConv, BatchNorm

# 导入原 unsup_sensitivity.py 中的函数
sys.path.insert(0, os.path.dirname(__file__))
from unsup_sensitivity import (
    set_seed, parse_verilog_graph, compute_struct_features,
    build_pyg_data, EncoderGIN, DGI, train_dgi, minmax_norm, z2u01
)

def compute_five_features(G: nx.DiGraph,
                          feats: Dict[int, Dict],
                          H: torch.Tensor,
                          data: Data,
                          output_ids: Set[int]) -> pd.DataFrame:
    """
    计算每个节点在5个维度上的得分，并返回DataFrame
    
    五个维度：
    1. Centrality (中心性) = mean(pagerank, betweenness, eigen)
    2. Proximity (接近性) = 0.5*dist_min_inv + 0.5*dist_avg_inv
    3. Reconvergence (重收敛) = reconv
    4. Sequential (时序) = near_ff
    5. Embedding (嵌入相似度) = cos(node_emb, mean_emb(outputs))
    """
    nid_list = data.node_ids
    name_list = data.node_names
    
    # 1. Embedding similarity
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
    
    # 2. Centrality
    pr = np.array([feats[nid]['pagerank'] for nid in nid_list])
    bet = np.array([feats[nid]['betweenness'] for nid in nid_list])
    ev = np.array([feats[nid]['eigen'] for nid in nid_list])
    centrality_raw = (pr + bet + ev) / 3.0
    centrality = minmax_norm(centrality_raw)
    
    # 3. Proximity
    prox_raw = 0.5 * np.array([feats[n]['dist_min_inv'] for n in nid_list]) + \
               0.5 * np.array([feats[n]['dist_avg_inv'] for n in nid_list])
    proximity = minmax_norm(prox_raw)
    
    # 4. Reconvergence
    reconv_raw = np.array([feats[n]['reconv'] for n in nid_list])
    reconvergence = minmax_norm(reconv_raw)
    
    # 5. Sequential
    sequential = np.array([feats[n]['near_ff'] for n in nid_list])  # already 0/1
    
    # 创建DataFrame
    df = pd.DataFrame({
        'Node_Name': name_list,
        'Centrality': centrality,
        'Proximity': proximity,
        'Reconvergence': reconvergence,
        'Sequential': sequential,
        'Embedding': embed_sim
    })
    
    return df

def calculate_taylor_metrics(node_scores_df: pd.DataFrame) -> pd.DataFrame:
    """
    基于节点的5个维度得分，计算泰勒图所需的统计指标
    
    策略：
    - 观察值（Observed）：各个单独参数的实际得分
    - 预测值（Predicted/Reference）：5个参数的融合打分（加权平均）
    - 评估每个单独参数与融合打分的一致性
    
    参数:
        node_scores_df: 每个节点的5个维度得分
    
    返回:
        包含每个特征的标准差、RMSE、相关系数的DataFrame
    """
    features = ['Centrality', 'Proximity', 'Reconvergence', 'Sequential', 'Embedding']
    
    # 使用与 unsup_sensitivity.py 一致的权重
    weights = {
        'Centrality': 0.25,
        'Proximity': 0.25,
        'Reconvergence': 0.20,
        'Sequential': 0.15,
        'Embedding': 0.15
    }
    
    print("\n[INFO] 计算泰勒图统计指标...")
    print(f"  权重配置: Centrality={weights['Centrality']}, Proximity={weights['Proximity']}, "
          f"Reconvergence={weights['Reconvergence']}, Sequential={weights['Sequential']}, "
          f"Embedding={weights['Embedding']}")
    
    # 计算融合打分（预测值/参考值）：5个参数的加权平均
    fusion_score = np.zeros(len(node_scores_df))
    for feat in features:
        fusion_score += weights[feat] * node_scores_df[feat].values
    
    print(f"\n  融合打分（预测值）统计: 均值={np.mean(fusion_score):.6f}, 标准差={np.std(fusion_score, ddof=1):.6f}")
    
    taylor_metrics = []
    
    for feature in features:
        # 观察值：单独参数的实际得分
        obs = node_scores_df[feature].values
        
        # 预测值：融合打分（所有参数的加权平均）
        pred = fusion_score
        
        # 1. 标准差 - 观察值的标准差（用于泰勒图）
        std_obs = np.std(obs, ddof=1)
        
        # 2. 参考标准差 - 预测值（理想模型）的标准差
        std_pred = np.std(pred, ddof=1)
        
        # 3. RMSE - 均方根误差
        rmse = np.sqrt(np.mean((obs - pred) ** 2))
        
        # 4. 相关系数 - 皮尔逊相关系数
        if std_pred > 1e-10 and std_obs > 1e-10:
            corr = np.corrcoef(obs, pred)[0, 1]
        else:
            corr = 0.0
        
        # 5. 中心化RMSE
        bias = np.mean(obs) - np.mean(pred)
        crmsd = np.sqrt(rmse**2 - bias**2) if rmse**2 >= bias**2 else rmse
        
        taylor_metrics.append({
            'Feature': feature,
            'Weight': weights[feature],
            'Standard Deviation': std_obs,  # 观察值的标准差
            'RMSE': rmse,
            'Correlation Coefficient': corr,
            'Reference_STD': std_pred,  # 参考值的标准差
            'Centered_RMSE': crmsd,
            'Bias': bias,
            'Mean_Observed': np.mean(obs),
            'Mean_Predicted': np.mean(pred),
            'N_Nodes': len(obs)
        })
        
        print(f"\n特征: {feature} (权重={weights[feature]})")
        print(f"  节点数: {len(obs)}")
        print(f"  观察值（该参数得分）均值: {np.mean(obs):.6f}, 标准差: {std_obs:.6f}")
        print(f"  预测值（融合打分）均值: {np.mean(pred):.6f}, 标准差: {std_pred:.6f}")
        print(f"  偏差 (Bias): {bias:.6f}")
        print(f"  RMSE: {rmse:.6f}")
        print(f"  中心化RMSE: {crmsd:.6f}")
        print(f"  相关系数: {corr:.6f}")
    
    return pd.DataFrame(taylor_metrics)

def main():
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print(f"[INFO] 工作目录: {os.getcwd()}")
    
    # 优先使用 pe.synth_dct.v，这是主要的综合网表文件
    if os.path.exists('pe.synth_dct.v'):
        verilog_file = 'pe.synth_dct.v'
    else:
        # 检查是否有其他Verilog文件
        all_files = os.listdir('.')
        print(f"[DEBUG] 当前目录文件: {[f for f in all_files if f.endswith('.v')]}")
        verilog_files = [f for f in all_files if f.endswith('.v') and f not in ['cells.v', 'tb_1.v']]
        
        if not verilog_files:
            print("❌ 当前目录没有找到合适的 .v (Verilog) 网表文件")
            print("请将 Verilog 网表文件放在当前目录，或修改脚本指定文件路径")
            return
        
        verilog_file = verilog_files[0]
    
    print(f"[INFO] 使用 Verilog 文件: {verilog_file}")
    
    # 设置参数
    set_seed(42)
    hidden = 128
    layers = 3
    epochs = 150
    dropout = 0.2
    
    total_start = time.time()
    print("\n" + "=" * 80)
    print("运行无监督敏感性评分器并生成泰勒图数据")
    print("=" * 80)
    
    # 1. 解析网表
    print(f"\n[步骤 1/5] 解析 Verilog 网表: {verilog_file}")
    t0 = time.time()
    G, node_map, output_ids, seq_inst_ids = parse_verilog_graph(verilog_file)
    print(f"  节点数: {G.number_of_nodes()}, 边数: {G.number_of_edges()}, 输出net数: {len(output_ids)}")
    print(f"  耗时: {time.time()-t0:.2f}s")
    
    # 2. 提取结构特征
    print(f"\n[步骤 2/5] 提取结构/拓扑特征")
    t0 = time.time()
    feats = compute_struct_features(G, output_ids, seq_inst_ids)
    print(f"  耗时: {time.time()-t0:.2f}s")
    
    # 3. 构造PyG数据
    print(f"\n[步骤 3/5] 构造 PyG 数据")
    t0 = time.time()
    data, node_ids, name_list = build_pyg_data(G, feats)
    print(f"  耗时: {time.time()-t0:.2f}s")
    
    # 4. 自监督DGI训练
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"\n[步骤 4/5] 自监督 DGI 训练 (device={device}, epochs={epochs})")
    t0 = time.time()
    H = train_dgi(data, hidden=hidden, layers=layers, epochs=epochs,
                  lr=1e-3, dropout=dropout, device=device)
    print(f"  耗时: {time.time()-t0:.2f}s")
    
    # 5. 计算5个维度的得分
    print(f"\n[步骤 5/5] 计算每个节点的5个维度得分")
    t0 = time.time()
    node_scores_df = compute_five_features(G, feats, H, data, output_ids)
    print(f"  耗时: {time.time()-t0:.2f}s")
    
    # 保存节点得分
    node_scores_df.to_csv('node_five_features_scores.csv', index=False)
    print(f"\n✅ 节点得分已保存到: node_five_features_scores.csv")
    print(f"   共 {len(node_scores_df)} 个节点")
    
    # 显示前10个节点的得分
    print("\n前10个节点的5个维度得分：")
    print(node_scores_df.head(10).to_string(index=False))
    
    # 计算泰勒图统计指标
    print("\n" + "=" * 80)
    print("计算泰勒图统计指标")
    print("=" * 80)
    
    taylor_metrics_df = calculate_taylor_metrics(node_scores_df)
    
    # 保存完整统计数据
    taylor_metrics_df.to_csv('taylor_data_from_gnn.csv', index=False)
    print(f"\n✅ 详细泰勒图数据已保存到: taylor_data_from_gnn.csv")
    
    # 保存简化版本（与原始格式一致）
    taylor_simple = taylor_metrics_df[['Feature', 'Weight', 'Standard Deviation', 'RMSE', 'Correlation Coefficient']]
    taylor_simple.to_csv('taylor_data.csv', index=False)
    print(f"✅ 简化泰勒图数据已保存到: taylor_data.csv (已覆盖)")
    
    print("\n" + "=" * 80)
    print("泰勒图评估指标汇总：")
    print("=" * 80)
    print(taylor_simple.to_string(index=False))
    
    # 统计摘要
    print("\n" + "=" * 80)
    print("5个特征维度的统计摘要：")
    print("=" * 80)
    print(node_scores_df[['Centrality', 'Proximity', 'Reconvergence', 'Sequential', 'Embedding']].describe())
    
    total_time = time.time() - total_start
    print(f"\n✅ 全部完成！总耗时: {total_time:.2f}s")
    print(f"\n现在可以运行绘图脚本来生成泰勒图：")
    print(f"  python 图7-4-2多模型评估指标不同样式泰勒图\\ 绘制示例.py")

if __name__ == '__main__':
    main()

