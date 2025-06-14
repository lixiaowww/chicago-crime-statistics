import snowflake.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. 连接 Snowflake
conn = snowflake.connector.connect(
    user='lixiaowww',
    password='Sean0105@winnipeg!',
    account='gzhlbee-bv06447',
    warehouse='warehouse',
    database='CHICAGO_CRIME',
    schema='STATISTICS'
)

# 2. 读取全量数据（如数据量极大，可分批读取）
sql = "SELECT * FROM CHICAGO_CRIME_COPY"
df = pd.read_sql(sql, conn)
conn.close()

# 3. 前五大犯罪类型
top5_types = df['PRIMARY_TYPE'].value_counts().head(5)
plt.figure(figsize=(8,5))
sns.barplot(x=top5_types.values, y=top5_types.index)
plt.title('Top 5 Crime Types')
plt.xlabel('Count')
plt.savefig('top5_crime_types.png')
plt.close()

# 4. 犯罪率前五的区域
top5_areas = df['COMMUNITY_AREA'].value_counts().head(5)
plt.figure(figsize=(8,5))
sns.barplot(x=top5_areas.values, y=top5_areas.index)
plt.title('Top 5 Crime Areas')
plt.xlabel('Count')
plt.savefig('top5_crime_areas.png')
plt.close()

# 5. 犯罪率最高的日期
top5_dates = df['DATE'].value_counts().head(5)
plt.figure(figsize=(8,5))
sns.barplot(x=top5_dates.values, y=top5_dates.index)
plt.title('Top 5 Crime Dates')
plt.xlabel('Count')
plt.savefig('top5_crime_dates.png')
plt.close()

# 6. 类型-区域关系热力图
pivot_type_area = pd.pivot_table(df, index='PRIMARY_TYPE', columns='COMMUNITY_AREA', aggfunc='size', fill_value=0)
plt.figure(figsize=(12,8))
sns.heatmap(pivot_type_area.loc[top5_types.index, top5_areas.index], annot=True, fmt='d', cmap='Reds')
plt.title('Top Crime Types vs Top Areas')
plt.savefig('type_area_heatmap.png')
plt.close()

# 7. 类型-日期关系热力图
pivot_type_date = pd.pivot_table(df, index='PRIMARY_TYPE', columns='DATE', aggfunc='size', fill_value=0)
plt.figure(figsize=(12,8))
sns.heatmap(pivot_type_date.loc[top5_types.index, top5_dates.index], annot=True, fmt='d', cmap='Blues')
plt.title('Top Crime Types vs Top Dates')
plt.savefig('type_date_heatmap.png')
plt.close()

# 8. 地理分布热力图（如有 LATITUDE, LONGITUDE 字段）
if 'LATITUDE' in df.columns and 'LONGITUDE' in df.columns:
    plt.figure(figsize=(10,8))
    sns.kdeplot(x=df['LONGITUDE'], y=df['LATITUDE'], cmap='Reds', fill=True, bw_adjust=0.5)
    plt.title('Crime Geographic Distribution')
    plt.savefig('geo_heatmap.png')
    plt.close()

# 9. 时间序列趋势图（如有日期字段）
df['DATE'] = pd.to_datetime(df['DATE'])
df['YEAR_MONTH'] = df['DATE'].dt.to_period('M')
monthly_counts = df.groupby('YEAR_MONTH').size()
plt.figure(figsize=(12,6))
monthly_counts.plot()
plt.title('Monthly Crime Trend')
plt.xlabel('Year-Month')
plt.ylabel('Crime Count')
plt.savefig('monthly_trend.png')
plt.close()

# 10. 英文报告自动生成
with open('chicago_crime_report.md', 'w') as f:
    f.write("# Chicago Crime Data Analysis Report\n\n")
    f.write("## 1. Top 5 Crime Types\n")
    f.write("![](top5_crime_types.png)\n\n")
    f.write("## 2. Top 5 Crime Areas\n")
    f.write("![](top5_crime_areas.png)\n\n")
    f.write("## 3. Top 5 Crime Dates\n")
    f.write("![](top5_crime_dates.png)\n\n")
    f.write("## 4. Top Crime Types vs Top Areas\n")
    f.write("![](type_area_heatmap.png)\n\n")
    f.write("## 5. Top Crime Types vs Top Dates\n")
    f.write("![](type_date_heatmap.png)\n\n")
    if os.path.exists('geo_heatmap.png'):
        f.write("## 6. Crime Geographic Distribution\n")
        f.write("![](geo_heatmap.png)\n\n")
    f.write("## 7. Monthly Crime Trend\n")
    f.write("![](monthly_trend.png)\n\n")
    f.write("## 8. Conclusions & Suggestions\n")
    f.write("Based on the analysis, the government should focus on the top crime types and high-risk areas, strengthen patrols during high-crime dates, and implement targeted prevention strategies.\n")

print("Analysis complete! All charts and the report have been saved in the current directory.")