# 芝加哥犯罪数据分析项目

这个项目旨在分析芝加哥市的犯罪数据，包括犯罪趋势、类型分布和地理分布等方面的分析。

## 项目结构

```
chicago_crime/
├── data/               # 存放原始数据
├── src/               # 源代码
│   └── main.py        # 主程序
├── notebooks/         # Jupyter notebooks
├── results/           # 分析结果和图表
├── docs/             # 文档
└── requirements.txt   # 项目依赖
```

## 功能特点

- 自动下载和加载芝加哥犯罪数据集
- 数据预处理和时间特征提取
- 犯罪趋势分析（年度、月度、每日、每小时）
- 犯罪类型分析
- 地理分布分析
- 可视化图表生成
- 分析报告生成

## 安装说明

1. 克隆项目到本地
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

运行主程序：
```bash
python src/main.py
```

程序会自动：
1. 下载或加载数据
2. 进行数据预处理
3. 执行分析
4. 生成可视化图表
5. 生成分析报告

## 输出结果

- 分析报告：`results/analysis_report.txt`
- 可视化图表：`results/crime_analysis.png`

## 数据来源

数据来自芝加哥警察局的CLEAR系统，通过芝加哥市开放数据门户获取：
https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2 