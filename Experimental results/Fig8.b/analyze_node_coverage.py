"""
Analyze fault coverage for the first 50 test nodes
Find the first turning point as the optimal point
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
import pylab as pl

# Read two data files
print("=" * 60)
print("Fault Coverage Turning Point Analysis")
print("=" * 60)

# Read data
dataset1 = pd.read_csv("coverage_statistics.csv")
dataset2 = pd.read_csv("coverage_sensitive.csv")

# Extract data for the first 50 test nodes
data1 = dataset1.head(50).copy()
data2 = dataset2.head(50).copy()

print(f"\nData File 1 (coverage_statistics.csv):")
print(f"  Total samples: {len(dataset1)}")
print(f"  Analysis samples: {len(data1)} (first 50 nodes)")

print(f"\nData File 2 (coverage_sensitive.csv):")
print(f"  Total samples: {len(dataset2)}")
print(f"  Analysis samples: {len(data2)} (first 50 nodes)")

# Define turning point detection function
def find_turning_point(nodes, coverage):
    """
    Find the first turning point
    Turning point is defined as: the first point where the next point has lower coverage than the current point
    """
    # Find the first point where coverage[i] > coverage[i+1]
    for i in range(len(coverage) - 1):
        if coverage[i] > coverage[i + 1]:
            return i + 1  # Return the index (1-based) of the turning point
    
    # If no turning point found (coverage keeps increasing), return the last point
    return len(coverage)

# Analyze both datasets
results = {}

for name, data in [("coverage_statistics", data1), ("coverage_sensitive", data2)]:
    nodes = data['tested_nodes'].values
    coverage = data['fault_coverage(%)'].values
    
    # Find turning point
    turning_point_idx = find_turning_point(nodes, coverage)
    turning_point_node = nodes[turning_point_idx - 1]  # Convert to 0-based index
    turning_point_coverage = coverage[turning_point_idx - 1]
    
    results[name] = {
        'nodes': nodes,
        'coverage': coverage,
        'turning_point_idx': turning_point_idx,
        'turning_point_node': turning_point_node,
        'turning_point_coverage': turning_point_coverage,
        'data': data
    }
    
    print(f"\n{name} Analysis Results:")
    print(f"  Turning point position: Node {turning_point_idx}")
    print(f"  Turning point node number: {turning_point_node}")
    print(f"  Turning point fault coverage: {turning_point_coverage:.2f}%")

# Generate chart (keep original style)
plt.figure(figsize=(12, 6), facecolor='none')

colors = ['red', 'blue']
labels = ['coverage_statistics', 'coverage_sensitive']
linestyles = ['dashed', 'dashdot']
optimal_markers = ['o', 's']  # Different markers for optimal points
optimal_colors = ['green', 'orange']  # Different colors for optimal points

for idx, (name, result) in enumerate(results.items()):
    nodes = result['nodes']
    coverage = result['coverage']
    turning_point_node = result['turning_point_node']
    turning_point_coverage = result['turning_point_coverage']
    
    # Plot curve (red dashed line, blue dashdot line with markers)
    plt.plot(nodes, coverage, color=colors[idx], linestyle=linestyles[idx], marker='o',
             markerfacecolor=colors[idx], markersize=6, linewidth=2, 
             label=f'{name} (turning point: node={turning_point_node})')
    
    # Mark optimal point with different legend for each dataset
    plt.scatter([turning_point_node], [turning_point_coverage], 
                color=optimal_colors[idx], s=200, marker=optimal_markers[idx], 
                edgecolors='darkgreen' if idx == 0 else 'darkorange', 
                linewidths=2, zorder=5,
                label=f'{name} Optimal Point (node={turning_point_node})')

plt.title('Statistical vs Sensitive', fontsize=14, fontweight='bold')
plt.xlabel('The Number of Nodes', fontsize=12)
plt.ylabel('Fault Coverage (%)', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('fault_coverage_turning_point.svg', format='svg', bbox_inches='tight', transparent=True)
print("\nChart saved: fault_coverage_turning_point.svg")

# Generate data documentation
print("\nGenerating data documentation...")
doc_content = []
doc_content.append("=" * 80)
doc_content.append("故障覆盖率转折点分析数据说明文档")
doc_content.append("=" * 80)
doc_content.append("")
doc_content.append("生成时间: " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))
doc_content.append("")
doc_content.append("=" * 80)
doc_content.append("一、分析目的")
doc_content.append("=" * 80)
doc_content.append("分析前50个测试节点的故障覆盖率变化趋势，找到第一个转折点。")
doc_content.append("转折点表示故障覆盖率开始下降的节点位置。")
doc_content.append("第一个转折点越晚出现，说明测试质量越高，因为故障覆盖率能够")
doc_content.append("在更多节点上保持较高水平或持续增长。")
doc_content.append("")
doc_content.append("=" * 80)
doc_content.append("二、数据集基本信息")
doc_content.append("=" * 80)
doc_content.append(f"数据文件1: coverage_statistics.csv")
doc_content.append(f"  总样本数: {len(dataset1)}")
doc_content.append(f"  分析样本数: {len(data1)} (前50个节点)")
doc_content.append(f"  节点数范围: {data1['tested_nodes'].min()} - {data1['tested_nodes'].max()}")
doc_content.append(f"  故障覆盖率范围: {data1['fault_coverage(%)'].min():.2f}% - {data1['fault_coverage(%)'].max():.2f}%")
doc_content.append("")
doc_content.append(f"数据文件2: coverage_sensitive.csv")
doc_content.append(f"  总样本数: {len(dataset2)}")
doc_content.append(f"  分析样本数: {len(data2)} (前50个节点)")
doc_content.append(f"  节点数范围: {data2['tested_nodes'].min()} - {data2['tested_nodes'].max()}")
doc_content.append(f"  故障覆盖率范围: {data2['fault_coverage(%)'].min():.2f}% - {data2['fault_coverage(%)'].max():.2f}%")
doc_content.append("")
doc_content.append("=" * 80)
doc_content.append("三、转折点定义与检测方法")
doc_content.append("=" * 80)
doc_content.append("")
doc_content.append("1. 转折点的定义:")
doc_content.append("   转折点是第一个使得下一个节点的故障覆盖率低于当前节点的节点位置。")
doc_content.append("   换句话说，转折点是覆盖率开始下降的第一个点。")
doc_content.append("   在转折点之前，故障覆盖率通常保持较高水平或持续增长；")
doc_content.append("   在转折点之后，故障覆盖率开始下降。")
doc_content.append("")
doc_content.append("2. 检测方法:")
doc_content.append("   找到第一个点i，使得coverage[i] > coverage[i+1]。")
doc_content.append("   这表示故障覆盖率已达到峰值并开始下降。")
doc_content.append("")
doc_content.append("3. 转折点的意义:")
doc_content.append("   转折点越晚出现，说明测试质量越高，因为：")
doc_content.append("   - 故障覆盖率能在更多节点上保持较高水平")
doc_content.append("   - 测试策略能够更有效地覆盖故障")
doc_content.append("   - 测试效率更高，在达到最优性能前测试更多节点")
doc_content.append("")
doc_content.append("=" * 80)
doc_content.append("四、分析结果")
doc_content.append("=" * 80)

for name, result in results.items():
    nodes = result['nodes']
    coverage = result['coverage']
    turning_point_idx = result['turning_point_idx']
    turning_point_node = result['turning_point_node']
    turning_point_coverage = result['turning_point_coverage']
    
    doc_content.append("")
    doc_content.append(f"{name} 数据集:")
    doc_content.append(f"  转折点位置: 第 {turning_point_idx} 个节点")
    doc_content.append(f"  转折点节点数: {turning_point_node}")
    doc_content.append(f"  转折点故障覆盖率: {turning_point_coverage:.2f}%")
    
    if turning_point_idx < len(coverage):
        next_coverage = coverage[turning_point_idx] if turning_point_idx < len(coverage) else coverage[-1]
        doc_content.append(f"  下一个节点故障覆盖率: {next_coverage:.2f}%")
        doc_content.append(f"  覆盖率下降: {turning_point_coverage - next_coverage:.2f}%")
    
    doc_content.append(f"  转折点前平均故障覆盖率: {coverage[:turning_point_idx].mean():.2f}%")
    if turning_point_idx < len(coverage):
        doc_content.append(f"  转折点后平均故障覆盖率: {coverage[turning_point_idx:].mean():.2f}%")
        doc_content.append(f"  故障覆盖率下降幅度: {coverage[turning_point_idx-1] - coverage[-1]:.2f}% (从转折点到第50个节点)")
    
    # Calculate average coverage for first 10 nodes
    if len(coverage) >= 10:
        doc_content.append(f"  前10个节点平均故障覆盖率: {coverage[:10].mean():.2f}%")
    
    # Calculate statistics before and after turning point
    if turning_point_idx > 1:
        before_coverage = coverage[:turning_point_idx]
        after_coverage = coverage[turning_point_idx:]
        if len(after_coverage) > 0:
            doc_content.append(f"  转折点前节点数: {turning_point_idx}")
            doc_content.append(f"  转折点后节点数: {50 - turning_point_idx}")
            doc_content.append(f"  转折点前覆盖率变化: {before_coverage[0]:.2f}% → {before_coverage[-1]:.2f}%")
            doc_content.append(f"  转折点后覆盖率变化: {after_coverage[0]:.2f}% → {after_coverage[-1]:.2f}%")

# Compare two datasets
doc_content.append("")
doc_content.append("=" * 80)
doc_content.append("五、数据集对比分析")
doc_content.append("=" * 80)

stats_idx = results['coverage_statistics']['turning_point_idx']
sensitive_idx = results['coverage_sensitive']['turning_point_idx']

doc_content.append(f"")
doc_content.append(f"转折点位置对比:")
doc_content.append(f"  coverage_statistics: 第 {stats_idx} 个节点")
doc_content.append(f"  coverage_sensitive: 第 {sensitive_idx} 个节点")

if stats_idx > sensitive_idx:
    doc_content.append(f"")
    doc_content.append(f"结论: coverage_statistics 的转折点更晚（晚 {stats_idx - sensitive_idx} 个节点），")
    doc_content.append(f"      说明其测试质量更高，能够在更多节点上保持较高的故障覆盖率。")
elif sensitive_idx > stats_idx:
    doc_content.append(f"")
    doc_content.append(f"结论: coverage_sensitive 的转折点更晚（晚 {sensitive_idx - stats_idx} 个节点），")
    doc_content.append(f"      说明其测试质量更高，能够在更多节点上保持较高的故障覆盖率。")
else:
    doc_content.append(f"")
    doc_content.append(f"结论: 两个数据集的转折点位置相同，测试质量相当。")

doc_content.append("")
doc_content.append("=" * 80)
doc_content.append("六、图表说明")
doc_content.append("=" * 80)
doc_content.append("")
doc_content.append("生成的图表文件: fault_coverage_turning_point.svg")
doc_content.append("")
doc_content.append("图表元素说明:")
doc_content.append("  X轴（横轴）: The Number of Nodes")
doc_content.append("     - 含义: 测试的节点数量")
doc_content.append("     - 范围: 1到50个节点")
doc_content.append("     - 作用: 表示随着测试节点数量的增加，故障覆盖率的变化趋势")
doc_content.append("")
doc_content.append("  Y轴（纵轴）: Fault Coverage (%)")
doc_content.append("     - 含义: 故障覆盖率百分比")
doc_content.append("     - 范围: 通常在0%到100%之间")
doc_content.append("     - 作用: 衡量测试对故障的覆盖程度，数值越高表示覆盖越好")
doc_content.append("")
doc_content.append("  曲线样式:")
doc_content.append("     - 红色虚线: coverage_statistics 数据集的故障覆盖率曲线")
doc_content.append("     - 蓝色点划线: coverage_sensitive 数据集的故障覆盖率曲线")
doc_content.append("     - 圆点标记: 每个节点对应的故障覆盖率数据点")
doc_content.append("     - 绿色圆点: 标识 coverage_statistics 的最优点（转折点）")
doc_content.append("     - 橙色方块: 标识 coverage_sensitive 的最优点（转折点）")
doc_content.append("")
doc_content.append("  网格线: 辅助读取坐标值")
doc_content.append("")
doc_content.append("  使用建议:")
doc_content.append("     - 观察曲线趋势，识别故障覆盖率的变化模式")
doc_content.append("     - 找到标记的转折点位置")
doc_content.append("     - 比较不同数据集转折点的早晚，评估测试质量")
doc_content.append("")

# Detailed data table
doc_content.append("=" * 80)
doc_content.append("七、前50个节点详细数据")
doc_content.append("=" * 80)

for name, result in results.items():
    data = result['data']
    turning_point_node = result['turning_point_node']
    
    doc_content.append("")
    doc_content.append(f"{name} 数据集前50个节点数据:")
    doc_content.append("  节点数 | 故障覆盖率(%) | 节点覆盖率(%) | 逃逸节点 | 逃逸故障")
    doc_content.append("  " + "-" * 60)
    
    for idx in range(min(50, len(data))):
        row = data.iloc[idx]
        marker = " <-- 转折点" if row['tested_nodes'] == turning_point_node else ""
        doc_content.append(f"  {int(row['tested_nodes']):5d} | {row['fault_coverage(%)']:13.2f} | {row['node_coverage(%)']:13.2f} | {int(row['escaped_nodes']):8d} | {int(row['escaped_faults']):8d}{marker}")

doc_content.append("")
doc_content.append("=" * 80)
doc_content.append("八、分析结论")
doc_content.append("=" * 80)
doc_content.append("")
doc_content.append("1. 转折点识别:")
for name, result in results.items():
    turning_point_node = result['turning_point_node']
    turning_point_coverage = result['turning_point_coverage']
    doc_content.append(f"   - {name}: 转折点出现在第 {turning_point_node} 个节点，")
    doc_content.append(f"     此时故障覆盖率为 {turning_point_coverage:.2f}%")
doc_content.append("")
doc_content.append("2. 测试质量评估:")
if stats_idx > sensitive_idx:
    doc_content.append(f"   coverage_statistics 的转折点更晚（第 {stats_idx} vs 第 {sensitive_idx} 个节点），")
    doc_content.append(f"   说明其测试质量更高，能够在更多节点上保持较高的故障覆盖率。")
elif sensitive_idx > stats_idx:
    doc_content.append(f"   coverage_sensitive 的转折点更晚（第 {sensitive_idx} vs 第 {stats_idx} 个节点），")
    doc_content.append(f"   说明其测试质量更高，能够在更多节点上保持较高的故障覆盖率。")
else:
    doc_content.append(f"   两个数据集的转折点位置相同，测试质量相当。")
doc_content.append("")
doc_content.append("3. 应用建议:")
doc_content.append("   - 转折点之前的节点测试效率最高，故障覆盖率保持较高水平")
doc_content.append("   - 转折点之后需要考虑优化测试策略以提高覆盖率")
doc_content.append("   - 转折点越晚出现，说明测试策略越有效")
doc_content.append("")
doc_content.append("=" * 80)
doc_content.append("文档结束")
doc_content.append("=" * 80)

# Save documentation
doc_file = "fault_coverage_turning_point_analysis.txt"
with open(doc_file, 'w', encoding='utf-8') as f:
    f.write("\n".join(doc_content))
print(f"Data documentation generated: {doc_file}")

print("\n" + "=" * 60)
print("Analysis Complete!")
print("=" * 60)
print("\nGenerated Files:")
print("  fault_coverage_turning_point.svg - Fault coverage turning point analysis chart")
print(f"  {doc_file} - Data documentation")

plt.show()
