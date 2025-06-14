import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def load_data():
    """
    加载芝加哥犯罪数据集
    """
    try:
        # 尝试从本地加载数据
        df = pd.read_csv('../data/chicago_crime.csv')
    except FileNotFoundError:
        # 如果本地没有数据，从网络下载
        url = "https://data.cityofchicago.org/resource/ijzp-q8t2.csv"
        df = pd.read_csv(url)
        # 保存到本地
        df.to_csv('../data/chicago_crime.csv', index=False)
    
    return df

def preprocess_data(df):
    """
    数据预处理
    """
    # 转换日期时间列
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 提取时间特征
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['Hour'] = df['Date'].dt.hour
    df['DayOfWeek'] = df['Date'].dt.day_name()
    
    return df

def analyze_crime_trends(df):
    """
    分析犯罪趋势
    """
    # 按年份统计犯罪数量
    yearly_crimes = df.groupby('Year').size()
    
    # 按月份统计犯罪数量
    monthly_crimes = df.groupby('Month').size()
    
    # 按星期统计犯罪数量
    daily_crimes = df.groupby('DayOfWeek').size()
    
    # 按小时统计犯罪数量
    hourly_crimes = df.groupby('Hour').size()
    
    return {
        'yearly': yearly_crimes,
        'monthly': monthly_crimes,
        'daily': daily_crimes,
        'hourly': hourly_crimes
    }

def analyze_crime_types(df):
    """
    分析犯罪类型
    """
    # 统计主要犯罪类型
    primary_types = df['Primary Type'].value_counts()
    
    # 统计犯罪描述
    descriptions = df['Description'].value_counts()
    
    return {
        'primary_types': primary_types,
        'descriptions': descriptions
    }

def analyze_locations(df):
    """
    分析犯罪地点
    """
    # 统计社区区域
    community_areas = df['Community Area'].value_counts()
    
    # 统计地点类型
    location_types = df['Location Description'].value_counts()
    
    return {
        'community_areas': community_areas,
        'location_types': location_types
    }

def create_visualizations(df, trends, crime_types, locations):
    """
    创建可视化图表
    """
    # 创建图形
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. 年度犯罪趋势
    trends['yearly'].plot(kind='line', ax=axes[0,0])
    axes[0,0].set_title('年度犯罪趋势')
    axes[0,0].set_xlabel('年份')
    axes[0,0].set_ylabel('犯罪数量')
    
    # 2. 主要犯罪类型分布
    crime_types['primary_types'].head(10).plot(kind='bar', ax=axes[0,1])
    axes[0,1].set_title('前10种主要犯罪类型')
    axes[0,1].set_xlabel('犯罪类型')
    axes[0,1].set_ylabel('数量')
    plt.xticks(rotation=45)
    
    # 3. 每日犯罪分布
    trends['daily'].plot(kind='bar', ax=axes[1,0])
    axes[1,0].set_title('每日犯罪分布')
    axes[1,0].set_xlabel('星期')
    axes[1,0].set_ylabel('犯罪数量')
    
    # 4. 社区区域犯罪分布
    locations['community_areas'].head(10).plot(kind='bar', ax=axes[1,1])
    axes[1,1].set_title('前10个犯罪高发社区')
    axes[1,1].set_xlabel('社区区域')
    axes[1,1].set_ylabel('犯罪数量')
    
    plt.tight_layout()
    plt.savefig('../results/crime_analysis.png')
    plt.close()

def generate_report(df, trends, crime_types, locations):
    """
    生成分析报告
    """
    report = []
    
    # 1. 基本统计信息
    report.append("=== 芝加哥犯罪数据分析报告 ===")
    report.append(f"\n总犯罪数量: {len(df):,}")
    report.append(f"数据时间范围: {df['Date'].min()} 到 {df['Date'].max()}")
    
    # 2. 犯罪趋势分析
    report.append("\n=== 犯罪趋势分析 ===")
    report.append("\n年度犯罪趋势:")
    report.append(trends['yearly'].to_string())
    
    # 3. 犯罪类型分析
    report.append("\n=== 犯罪类型分析 ===")
    report.append("\n主要犯罪类型分布:")
    report.append(crime_types['primary_types'].head(10).to_string())
    
    # 4. 地点分析
    report.append("\n=== 地点分析 ===")
    report.append("\n犯罪高发社区:")
    report.append(locations['community_areas'].head(10).to_string())
    
    # 保存报告
    with open('../results/analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))

def main():
    # 加载数据
    print("正在加载数据...")
    df = load_data()
    
    # 数据预处理
    print("正在预处理数据...")
    df = preprocess_data(df)
    
    # 分析犯罪趋势
    print("正在分析犯罪趋势...")
    trends = analyze_crime_trends(df)
    
    # 分析犯罪类型
    print("正在分析犯罪类型...")
    crime_types = analyze_crime_types(df)
    
    # 分析地点
    print("正在分析犯罪地点...")
    locations = analyze_locations(df)
    
    # 创建可视化
    print("正在创建可视化...")
    create_visualizations(df, trends, crime_types, locations)
    
    # 生成报告
    print("正在生成分析报告...")
    generate_report(df, trends, crime_types, locations)
    
    print("分析完成！结果已保存到results目录。")

if __name__ == "__main__":
    main() 