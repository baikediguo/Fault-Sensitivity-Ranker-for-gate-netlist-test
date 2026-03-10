import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 设置matplotlib参数以提高SVG清晰度
plt.rcParams['figure.dpi'] = 900
plt.rcParams['savefig.dpi'] = 900
plt.rcParams['svg.fonttype'] = 'none'  # 确保SVG中的文字是可选的（保留为文本而非路径）
plt.rcParams['figure.facecolor'] = 'none'  # 设置为透明背景
plt.rcParams['axes.linewidth'] = 1.5  # 增加坐标轴线宽
plt.rcParams['grid.linewidth'] = 1.0  # 网格线宽

# 设置字体为新罗马（Times New Roman）
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'Times', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'stix'  # 数学文本字体

# 读取Excel文件
df = pd.read_excel('data.xlsx')

# 定义百分位数组（10%, 20%, 30%, ..., 100%）- 共10个点
percentile_groups = ['10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']

# 提取数据列
sensitive_node_coverage = df['sensitive node coverage'].values
sensitive_fault_coverage = df['sensitive fault coverage'].values
statistical_node_coverage = df['statistical node coverage'].values
statistical_fault_coverage = df['statistical fault coverage'].values

# Accuracy数据等于Coverage数据（数值相同）
sensitive_node_accuracy = sensitive_node_coverage.copy()
sensitive_fault_accuracy = sensitive_fault_coverage.copy()
statistical_node_accuracy = statistical_node_coverage.copy()
statistical_fault_accuracy = statistical_fault_coverage.copy()

# 预测值：覆盖率为100%
predicted_coverage = 100.0

# 计算RMSE的函数
def calculate_rmse(actual_values, predicted_value):
    """计算RMSE"""
    mse = np.mean((actual_values - predicted_value) ** 2)
    rmse = np.sqrt(mse)
    return rmse

# 数据总行数
total_rows = len(df)
rows_per_group = total_rows // 10  # 每组10行（100行分成10组）

# 计算每个百分位组的RMSE - 八条线（Coverage + Accuracy）
sensitive_node_coverage_rmse_values = []
sensitive_node_accuracy_rmse_values = []
sensitive_fault_coverage_rmse_values = []
sensitive_fault_accuracy_rmse_values = []
statistical_node_coverage_rmse_values = []
statistical_node_accuracy_rmse_values = []
statistical_fault_coverage_rmse_values = []
statistical_fault_accuracy_rmse_values = []

for i in range(10):
    # 计算每组的行范围
    start_idx = i * rows_per_group
    end_idx = start_idx + rows_per_group
    
    # 获取该范围内的实际值（Coverage）
    sensitive_node_coverage_in_range = sensitive_node_coverage[start_idx:end_idx]
    sensitive_fault_coverage_in_range = sensitive_fault_coverage[start_idx:end_idx]
    statistical_node_coverage_in_range = statistical_node_coverage[start_idx:end_idx]
    statistical_fault_coverage_in_range = statistical_fault_coverage[start_idx:end_idx]
    
    # 获取该范围内的实际值（Accuracy，数值等于Coverage）
    sensitive_node_accuracy_in_range = sensitive_node_accuracy[start_idx:end_idx]
    sensitive_fault_accuracy_in_range = sensitive_fault_accuracy[start_idx:end_idx]
    statistical_node_accuracy_in_range = statistical_node_accuracy[start_idx:end_idx]
    statistical_fault_accuracy_in_range = statistical_fault_accuracy[start_idx:end_idx]
    
    # 计算RMSE - Coverage
    sensitive_node_coverage_rmse = calculate_rmse(sensitive_node_coverage_in_range, predicted_coverage)
    sensitive_fault_coverage_rmse = calculate_rmse(sensitive_fault_coverage_in_range, predicted_coverage)
    statistical_node_coverage_rmse = calculate_rmse(statistical_node_coverage_in_range, predicted_coverage)
    statistical_fault_coverage_rmse = calculate_rmse(statistical_fault_coverage_in_range, predicted_coverage)
    
    # Accuracy直接使用平均值，不计算RMSE
    sensitive_node_accuracy_value = np.mean(sensitive_node_accuracy_in_range)
    sensitive_fault_accuracy_value = np.mean(sensitive_fault_accuracy_in_range)
    statistical_node_accuracy_value = np.mean(statistical_node_accuracy_in_range)
    statistical_fault_accuracy_value = np.mean(statistical_fault_accuracy_in_range)
    
    sensitive_node_coverage_rmse_values.append(sensitive_node_coverage_rmse)
    sensitive_node_accuracy_rmse_values.append(sensitive_node_accuracy_value)
    sensitive_fault_coverage_rmse_values.append(sensitive_fault_coverage_rmse)
    sensitive_fault_accuracy_rmse_values.append(sensitive_fault_accuracy_value)
    statistical_node_coverage_rmse_values.append(statistical_node_coverage_rmse)
    statistical_node_accuracy_rmse_values.append(statistical_node_accuracy_value)
    statistical_fault_coverage_rmse_values.append(statistical_fault_coverage_rmse)
    statistical_fault_accuracy_rmse_values.append(statistical_fault_accuracy_value)

# 转换为numpy数组以便绘图
x_positions = np.arange(len(percentile_groups))

# 创建图表，增大图像尺寸以提高清晰度，并给图例留出空间，背景透明
fig = plt.figure(figsize=(18, 10), facecolor='none', dpi=900)

# 定义八种不同的颜色
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']

# 绘制八条曲线，每条线使用不同颜色，增大线宽和标记以提高清晰度
# Sensitive Node Coverage RMSE
plt.plot(x_positions, sensitive_node_coverage_rmse_values, 'o-', color=colors[0], linewidth=3.0, markersize=12, markeredgewidth=1.5, label='Sensitive Node Coverage RMSE')

# Sensitive Fault Coverage RMSE
plt.plot(x_positions, sensitive_fault_coverage_rmse_values, 'o-', color=colors[1], linewidth=3.0, markersize=12, markeredgewidth=1.5, label='Sensitive Fault Coverage RMSE')

# Statistical Node Coverage RMSE
plt.plot(x_positions, statistical_node_coverage_rmse_values, 'o-', color=colors[2], linewidth=3.0, markersize=12, markeredgewidth=1.5, label='Statistical Node Coverage RMSE')

# Statistical Fault Coverage RMSE
plt.plot(x_positions, statistical_fault_coverage_rmse_values, 'o-', color=colors[3], linewidth=3.0, markersize=12, markeredgewidth=1.5, label='Statistical Fault Coverage RMSE')

# Sensitive Node Accuracy (虚线，直接使用平均值，不计算RMSE)
plt.plot(x_positions, sensitive_node_accuracy_rmse_values, 's--', color=colors[4], linewidth=3.0, markersize=12, markeredgewidth=1.5, alpha=0.85, label='Sensitive Node Accuracy')

# Sensitive Fault Accuracy (虚线)
plt.plot(x_positions, sensitive_fault_accuracy_rmse_values, 's--', color=colors[5], linewidth=3.0, markersize=12, markeredgewidth=1.5, alpha=0.85, label='Sensitive Fault Accuracy')

# Statistical Node Accuracy (虚线)
plt.plot(x_positions, statistical_node_accuracy_rmse_values, 's--', color=colors[6], linewidth=3.0, markersize=12, markeredgewidth=1.5, alpha=0.85, label='Statistical Node Accuracy')

# Statistical Fault Accuracy (虚线)
plt.plot(x_positions, statistical_fault_accuracy_rmse_values, 's--', color=colors[7], linewidth=3.0, markersize=12, markeredgewidth=1.5, alpha=0.85, label='Statistical Fault Accuracy')

# 设置坐标轴标签，增大字体以提高清晰度
plt.xlabel('The top-K number of nodes', fontsize=16, fontweight='bold')
plt.ylabel('RMSE / Accuracy Value', fontsize=16, fontweight='bold')

# 设置x轴刻度，增大字体
plt.xticks(x_positions, percentile_groups, fontsize=14)

# 计算y轴数据的最大值，以便设置合适的y轴范围
all_values = (list(sensitive_node_coverage_rmse_values) + list(sensitive_fault_coverage_rmse_values) +
              list(statistical_node_coverage_rmse_values) + list(statistical_fault_coverage_rmse_values) +
              list(sensitive_node_accuracy_rmse_values) + list(sensitive_fault_accuracy_rmse_values) +
              list(statistical_node_accuracy_rmse_values) + list(statistical_fault_accuracy_rmse_values))
max_value = max(all_values)
min_value = min(all_values)

# 设置y轴范围
y_max = 115  # y轴最大值固定为115
y_min = -5   # y轴最小值固定为-5
plt.ylim(y_min, y_max)
plt.yticks(fontsize=14)

# 设置坐标轴线宽
ax = plt.gca()
ax.spines['top'].set_linewidth(1.5)
ax.spines['right'].set_linewidth(1.5)
ax.spines['bottom'].set_linewidth(1.5)
ax.spines['left'].set_linewidth(1.5)

# 添加网格，增加线宽以提高清晰度
plt.grid(True, alpha=0.4, linestyle='--', linewidth=1.2)

# 添加图例，分两列，放在右上角，增大字体
plt.legend(loc='upper right', ncol=2, framealpha=0.95, fontsize=11, edgecolor='black', fancybox=True, frameon=True)

# 调整布局
plt.tight_layout()

# 保存图表（在显示之前保存，避免图形状态丢失），提高SVG质量，设置为透明背景
fig.savefig('rmse_comparison.svg', format='svg', bbox_inches='tight', pad_inches=0.15, transparent=True, metadata={'Creator': 'Matplotlib', 'Title': 'RMSE Comparison Chart'})
print("\n图表已保存为 'rmse_comparison.svg'")

# 显示图表
plt.show()

# 保存数据到CSV文件
data_df = pd.DataFrame({
    'Percentile': percentile_groups,
    'Sensitive_Node_Coverage_RMSE': sensitive_node_coverage_rmse_values,
    'Sensitive_Node_Accuracy': sensitive_node_accuracy_rmse_values,
    'Sensitive_Fault_Coverage_RMSE': sensitive_fault_coverage_rmse_values,
    'Sensitive_Fault_Accuracy': sensitive_fault_accuracy_rmse_values,
    'Statistical_Node_Coverage_RMSE': statistical_node_coverage_rmse_values,
    'Statistical_Node_Accuracy': statistical_node_accuracy_rmse_values,
    'Statistical_Fault_Coverage_RMSE': statistical_fault_coverage_rmse_values,
    'Statistical_Fault_Accuracy': statistical_fault_accuracy_rmse_values
})
data_df.to_csv('coverage_statistics.csv', index=False, encoding='utf-8-sig')
print("\n数据已保存到 'coverage_statistics.csv'")

# 计算统计信息并保存到文档
def calculate_stats(values):
    return {
        'min': np.min(values),
        'max': np.max(values),
        'mean': np.mean(values),
        'std': np.std(values)
    }

stats_data = {
    'Sensitive Node Coverage RMSE': calculate_stats(sensitive_node_coverage_rmse_values),
    'Sensitive Node Accuracy': calculate_stats(sensitive_node_accuracy_rmse_values),
    'Sensitive Fault Coverage RMSE': calculate_stats(sensitive_fault_coverage_rmse_values),
    'Sensitive Fault Accuracy': calculate_stats(sensitive_fault_accuracy_rmse_values),
    'Statistical Node Coverage RMSE': calculate_stats(statistical_node_coverage_rmse_values),
    'Statistical Node Accuracy': calculate_stats(statistical_node_accuracy_rmse_values),
    'Statistical Fault Coverage RMSE': calculate_stats(statistical_fault_coverage_rmse_values),
    'Statistical Fault Accuracy': calculate_stats(statistical_fault_accuracy_rmse_values)
}

# 生成数值说明文档
with open('数据说明.txt', 'w', encoding='utf-8') as f:
    f.write("图表数值说明文档\n")
    f.write("=" * 40 + "\n\n")
    f.write("1. 数据概览\n")
    f.write("-" * 40 + "\n")
    f.write(f"数据文件: coverage_statistics.csv\n")
    f.write(f"数据点总数: {len(percentile_groups)} (10个百分位点)\n\n")
    
    f.write("X轴数据 (Performance Percentile - 性能百分位):\n")
    f.write(f"  范围: {percentile_groups[0]} 到 {percentile_groups[-1]}\n")
    f.write(f"  间隔: 10%\n\n")
    
    f.write("Y轴数据统计:\n\n")
    for name, stats in stats_data.items():
        f.write(f"  {name}:\n")
        f.write(f"    最小值: {stats['min']:.4f}\n")
        f.write(f"    最大值: {stats['max']:.4f}\n")
        f.write(f"    平均值: {stats['mean']:.4f}\n")
        f.write(f"    标准差: {stats['std']:.4f}\n\n")
    
    f.write("2. 详细数值数据\n")
    f.write("-" * 40 + "\n\n")
    f.write("Percentile,Sensitive_Node_Coverage_RMSE,Sensitive_Node_Accuracy,")
    f.write("Sensitive_Fault_Coverage_RMSE,Sensitive_Fault_Accuracy,")
    f.write("Statistical_Node_Coverage_RMSE,Statistical_Node_Accuracy,")
    f.write("Statistical_Fault_Coverage_RMSE,Statistical_Fault_Accuracy\n")
    for i, pct in enumerate(percentile_groups):
        f.write(f"{pct},{sensitive_node_coverage_rmse_values[i]:.4f},{sensitive_node_accuracy_rmse_values[i]:.4f},")
        f.write(f"{sensitive_fault_coverage_rmse_values[i]:.4f},{sensitive_fault_accuracy_rmse_values[i]:.4f},")
        f.write(f"{statistical_node_coverage_rmse_values[i]:.4f},{statistical_node_accuracy_rmse_values[i]:.4f},")
        f.write(f"{statistical_fault_coverage_rmse_values[i]:.4f},{statistical_fault_accuracy_rmse_values[i]:.4f}\n")

print("数值说明文档已保存到 '数据说明.txt'")

# 打印RMSE值
print("\nRMSE值:")
print("Percentile\tSens_Node_Cov\tSens_Node_Acc\tSens_Fault_Cov\tSens_Fault_Acc\tStat_Node_Cov\tStat_Node_Acc\tStat_Fault_Cov\tStat_Fault_Acc")
for i, pct in enumerate(percentile_groups):
    print(f"{pct}\t\t{sensitive_node_coverage_rmse_values[i]:.4f}\t\t{sensitive_node_accuracy_rmse_values[i]:.4f}\t\t{sensitive_fault_coverage_rmse_values[i]:.4f}\t\t{sensitive_fault_accuracy_rmse_values[i]:.4f}\t\t{statistical_node_coverage_rmse_values[i]:.4f}\t\t{statistical_node_accuracy_rmse_values[i]:.4f}\t\t{statistical_fault_coverage_rmse_values[i]:.4f}\t\t{statistical_fault_accuracy_rmse_values[i]:.4f}")
