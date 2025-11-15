import numpy as np
import pandas as pd
import re
import os

# =========================
# 输入文件列表
# =========================
input_files = [
    "exhaustive.xlsx",
    "statistical.xlsx",
    "sensitive.xlsx",
    "random.csv"
]

# 输出文件
output_file = "coverage_results.csv"

# =========================
# 遍历每个文件
# =========================
all_results = []

for input_file in input_files:
    if not os.path.exists(input_file):
        print(f"⚠️ 文件不存在，跳过：{input_file}")
        continue

    # 读取文件
    ext = os.path.splitext(input_file)[1].lower()
    if ext == ".csv":
        df = pd.read_csv(input_file)
    elif ext in [".xlsx", ".xls"]:
        df = pd.read_excel(input_file)
    else:
        print(f"⚠️ 不支持的文件类型，跳过：{input_file}")
        continue

    # 自动识别 Test Nodes 列
    node_cols = [c for c in df.columns if re.search(r"TestNode|test nodes", c, re.IGNORECASE)]
    if len(node_cols) == 0:
        print(f"❌ {input_file} 未找到 Test Node 列，跳过")
        continue
    test_nodes_col = node_cols[0]
    test_nodes = df[test_nodes_col].to_numpy()

    # 自动识别时间列
    time_cols = [c for c in df.columns if re.search("time", c, re.IGNORECASE)]
    if len(time_cols) == 0:
        print(f"❌ {input_file} 未找到时间列，跳过")
        continue
    time_col = time_cols[0]
    time = df[time_col].to_numpy()
    max_time = time[-1]

    # 自动识别 Coverage 列
    coverage_cols = [c for c in df.columns if re.search("coverage", c, re.IGNORECASE)]
    if len(coverage_cols) == 0:
        print(f"❌ {input_file} 未找到 Coverage 列，跳过")
        continue

    # =========================
    # 对每个 Coverage 列计算指标
    # =========================
    file_result = {"SourceFile": input_file}  # 保留源文件（包含后缀）
    for col in coverage_cols:
        coverage = df[col].to_numpy()

        # 1️⃣ 基于 Test Nodes 的 AUC & 平均覆盖率
        auc_val = np.trapz(coverage, x=test_nodes)
        avg_cov = np.mean(coverage)

        # 2️⃣ 新指标：CoverageSumPerTime
        coverage_sum_per_time = coverage.sum() / max_time

        # 保存结果
        file_result[f"{col}_AUC"] = auc_val
        file_result[f"{col}_AvgCoverage"] = avg_cov
        file_result[f"{col}_CoverageSumPerTime"] = coverage_sum_per_time

    all_results.append(file_result)

# =========================
# 保存结果（追加模式）
# =========================
if len(all_results) == 0:
    print("❌ 没有有效数据计算结果")
else:
    res_df = pd.DataFrame(all_results)
    if os.path.exists(output_file):
        res_df.to_csv(output_file, mode='a', index=False, header=False, float_format="%.6f")
    else:
        res_df.to_csv(output_file, index=False, float_format="%.6f")

    print(f"✅ 已计算并保存/追加结果至：{output_file}")
    print(res_df)
