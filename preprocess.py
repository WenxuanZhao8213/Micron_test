import pandas as pd
import json
import os
from datetime import datetime

# 读取原始数据
df = pd.read_csv('C:/Users/Xuan/Desktop/Micron/micron_front/public/assets/Data.csv')

# 清洗 Price 数据，确保其为数值类型
def clean_price(value):
    try:
        # 尝试将值转换为浮点数
        return float(value)
    except (ValueError, TypeError):
        # 如果转换失败，返回 NaN（表示无效值）
        return float('nan')

# 清洗所有 Price 列
for col in df.columns[5:]:  # 从第6列开始是 Price 数据
    df[col] = df[col].apply(clean_price)

# 转换原始数据为长格式
long_df = df.melt(
    id_vars=['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName'],
    var_name='Date',
    value_name='Price'
)

# 再次清洗长格式数据中的 Price 列
long_df['Price'] = long_df['Price'].apply(clean_price)

# 删除 Price 为 NaN 的行
long_df = long_df.dropna(subset=['Price'])

def format_date(date_str):
    try:
        # 解析原始日期格式
        date_obj = datetime.strptime(date_str, "%m/%d/%Y")
        # 转换为目标格式
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        # 如果日期格式无效，返回原始值
        return date_str

# 应用日期格式化函数
long_df['Date'] = long_df['Date'].apply(format_date)

# 检查清洗后的数据
print("清洗后的 Price 统计信息:")
print(long_df['Price'].describe())  # 检查 Price 的统计信息
print("\n清洗后的数据行数:", len(long_df))

# 保存清洗后的数据为 JSON
long_df.to_json('src/assets/data.json', orient='records')

# 运行模型训练脚本
# os.system('python model_train.py')