import pandas as pd
from prophet import Prophet
import json
import os

# 数据预处理
df = pd.read_csv('C:/Users/Xuan/Desktop/Micron/micron_front/public/assets/Data.csv')

date_columns = df.columns[5:]

# 将日期列转换为数值类型，非数值转为NaN
for col in date_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 删除包含NaN的行（或填充默认值）
df_clean = df.dropna()

df = df.melt(
    id_vars=['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName'],
    var_name='ds',
    value_name='y'
)
df['ds'] = pd.to_datetime(df['ds'])

# 为每个区域训练模型并生成预测
forecasts = []
for region in df['RegionName'].unique():
    region_data = df[df['RegionName'] == region][['ds', 'y']].dropna()
    if len(region_data) < 10:  # 跳过数据不足的区域
        continue
    
    model = Prophet(interval_width=0.95)
    model.fit(region_data)
    
    future = model.make_future_dataframe(periods=5, freq='ME')
    forecast = model.predict(future)
    
    # 提取预测结果
    last_5 = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(5)
    for _, row in last_5.iterrows():
        forecasts.append({
            'RegionName': region,
            'Date': row['ds'].strftime('%Y-%m-%d'),
            'Price': round(row['yhat'], 2),
            'Lower': round(row['yhat_lower'], 2),
            'Upper': round(row['yhat_upper'], 2)
        })

# 保存预测结果
with open('src/assets/forecast.json', 'w') as f:
    json.dump(forecasts, f)