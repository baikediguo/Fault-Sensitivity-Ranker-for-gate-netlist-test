import pandas as pd
import numpy as np
import os

# 读取数据
df = pd.read_excel('data.xlsx')

# 创建文件夹
os.makedirs('node', exist_ok=True)
os.makedirs('fault', exist_ok=True)

# 定义规模范围
scale_ranges = {
    '小规模': (200, 400),
    '中规模': (600, 800),
    '大规模': (1200, 1400),
    '超大规模': (1800, 2000)
}

# 定义列顺序（按数值从大到小）：statistical → sensitive → exhaustive → random
node_columns_ordered = [
    'TOP-K',
    'statistical node coverage',    # 1. 最大 (100.00)
    'sensitive node coverage',      # 2. (88.65)
    'exhaustive node coverage(%)',  # 3. (83.04)
    'random node coverage(%)'       # 4. 最小 (67.90)
]

fault_columns_ordered = [
    'TOP-K',
    'statistical fault coverage',   # 1. 最大 (75.80)
    'sensitive fault coverage',     # 2. (64.49)
    'exhaustive fault coverage(%)', # 3. (57.25)
    'random fault coverage(%)'      # 4. 最小 (44.36)
]

# 处理数据函数（不使用插值，直接处理原始数据）
def process_data(data, divide_topk=True, calc_change=False, max_value=100):
    """
    处理数据：TOP-K除以5，计算变化值的绝对值
    divide_topk: 是否将TOP-K除以5
    calc_change: 是否计算相对第一个值的变化（默认False，保留绝对值）
    """
    result = data.copy()
    
    # 将TOP-K除以5并改名为 nodes
    if divide_topk:
        result['nodes'] = result['TOP-K'] / 5.0
    else:
        result['nodes'] = result['TOP-K']
    
    # 删除原来的TOP-K列
    result = result.drop(columns=['TOP-K'])
    
    # 重新排列列，将nodes放在第一列
    cols = ['nodes'] + [c for c in result.columns if c != 'nodes']
    result = result[cols]
    
    # 对每一列进行处理
    for col in result.columns:
        if col != 'nodes':
            y = result[col].values
            # 限制数据不超过100
            y = np.clip(y, None, max_value)
            
            # 计算相对第一个值的变化，然后取绝对值
            if calc_change:
                first_value = y[0]
                y = np.abs(y - first_value)
            
            result[col] = y
    
    return result

print("=" * 80)
print("重新生成数据（覆盖率变化值的绝对值）")
print("=" * 80)
print("排序：statistical → sensitive → exhaustive → random")
print("TOP-K → nodes (值 ÷ 5)")
print("覆盖率 → |当前值 - 第一个值| (变化值的绝对值)")
print("=" * 80)

# 处理每个规模范围
for scale_name, (min_val, max_val) in scale_ranges.items():
    print(f"\n处理 {scale_name} ({min_val}-{max_val})...")
    
    # 筛选数据
    mask = (df['TOP-K'] >= min_val) & (df['TOP-K'] <= max_val)
    filtered_df = df[mask].copy()
    
    if len(filtered_df) == 0:
        print(f"  警告: {scale_name} 没有数据")
        continue
    
    # 处理 node 数据（按新顺序选择列）
    node_data = filtered_df[node_columns_ordered].copy()
    node_data_processed = process_data(node_data, divide_topk=True, calc_change=True, max_value=100)
    
    # 验证范围
    nodes_range = f"{node_data_processed['nodes'].min():.1f}-{node_data_processed['nodes'].max():.1f}"
    coverage_cols = [c for c in node_data_processed.columns if c != 'nodes']
    change_max = node_data_processed[coverage_cols].max().max()
    
    # 保存 node 数据
    node_filename = f'node/{scale_name}_node.xlsx'
    node_data_processed.to_excel(node_filename, index=False)
    print(f"  ✓ Node: {node_filename}")
    print(f"     列顺序: nodes → statistical → sensitive → exhaustive → random")
    print(f"     nodes范围: {nodes_range}")
    print(f"     变化值绝对值范围: 0 ~ {change_max:.2f}")
    
    # 处理 fault 数据（按新顺序选择列）
    fault_data = filtered_df[fault_columns_ordered].copy()
    fault_data_processed = process_data(fault_data, divide_topk=True, calc_change=True, max_value=100)
    
    # 验证范围
    coverage_cols = [c for c in fault_data_processed.columns if c != 'nodes']
    change_max = fault_data_processed[coverage_cols].max().max()
    
    # 保存 fault 数据
    fault_filename = f'fault/{scale_name}_fault.xlsx'
    fault_data_processed.to_excel(fault_filename, index=False)
    print(f"  ✓ Fault: {fault_filename}")
    print(f"     列顺序: nodes → statistical → sensitive → exhaustive → random")
    print(f"     nodes范围: {nodes_range}")
    print(f"     变化值绝对值范围: 0 ~ {change_max:.2f}")

print("\n" + "=" * 80)
print("✓ 所有数据处理完成！")
print("✓ TOP-K 已改为 nodes（值除以5）")
print("✓ 覆盖率已改为变化值的绝对值 |当前值 - 第一个值|")
print("✓ 列已按覆盖率从大到小排序")
print("=" * 80)

