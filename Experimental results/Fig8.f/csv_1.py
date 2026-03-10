import csv
import os

# 配置参数
OUTPUT_FILE = r'D:\work_code\statistical FI\topk.csv'  # 绝对路径
START = 100                  # 起始值
END = 150                # 结束值（可自行调整）
STEP = 5                 # 步长间隔
MAX_COUNT = 1000            # 最多生成数量

# 确保目录存在
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

# 生成 tok 列表
toks = list(range(START, END + 1, STEP))
if len(toks) > MAX_COUNT:
    toks = toks[:MAX_COUNT]

# 写入 CSV，第一行列名为 'tok'
with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['topk'])  # <-- 添加列名
    for tok in toks:
        writer.writerow([tok])

print(f'✅ 已生成 {len(toks)} 个 tok 值到 {OUTPUT_FILE}')
