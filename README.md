

-----

# Chicago Crime Data Analysis Project

This project aims to analyze the crime data of the City of Chicago, including analysis of crime trends, type distribution, and geographical distribution.

## Project Structure

```
chicago_crime/
├── data/               # Stores raw data
├── src/               # Source code
│   └── main.py        # Main program
├── notebooks/         # Jupyter notebooks
├── results/           # Analysis results and charts
├── docs/             # Documentation
└── requirements.txt   # Project dependencies
```

## Features

  - Automatically download and load the Chicago crime dataset
  - Data preprocessing and time feature extraction
  - Crime trend analysis (annual, monthly, daily, hourly)
  - Crime type analysis
  - Geographical distribution analysis
  - Generation of visualization charts
  - Generation of analysis reports

## Installation Instructions

1.  Clone the project to your local machine
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the main program:

```bash
python src/main.py
```

The program will automatically:

1.  Download or load data
2.  Perform data preprocessing
3.  Execute analysis
4.  Generate visualization charts
5.  Generate an analysis report

## Output Results

  - Analysis report: `results/analysis_report.txt`
  - Visualization charts: `results/crime_analysis.png`

## Data Source

The data comes from the Chicago Police Department's CLEAR (Citizen Law Enforcement Analysis and Reporting) system, obtained through the City of Chicago's open data portal:

  - **Official Data Source**: [https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2)
  - **Kaggle Dataset**: [https://www.kaggle.com/datasets/chicagopolice/chicago-crime-data](https://www.kaggle.com/datasets/chicagopolice/chicago-crime-data)

## Data Storage Description

**Note**: This GitHub repository does not include the raw data files (CSV and ZIP files) because these files are large and have already been uploaded to a Snowflake data warehouse for processing and analysis.

### How to obtain the data:

1.  **Download raw data**: Download the data files from the data source links above
2.  **Data storage location**: Place the downloaded files in the `data/` directory
3.  **Or use Snowflake**: The data has been uploaded to Snowflake and can be used directly through SQL queries

### Data File Structure:

```
data/
├── chicago_crime_dataset_v2.csv.zip    # Original compressed file
├── extracted/
│   └── chicago_crime_dataset_v2.csv     # Extracted CSV file (approx. 2GB)
└── split_files/                         # Split smaller files (for Snowflake upload)
    ├── chicago_crime_part_001.csv
    ├── chicago_crime_part_002.csv
    └── ...
```

-----

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

1.  克隆项目到本地
2.  安装依赖：
    ```bash
    pip install -r requirements.txt
    ```

## 使用方法

运行主程序：

```bash
python src/main.py
```

程序会自动：

1.  下载或加载数据
2.  进行数据预处理
3.  执行分析
4.  生成可视化图表
5.  生成分析报告

## 输出结果

  - 分析报告：`results/analysis_report.txt`
  - 可视化图表：`results/crime_analysis.png`

## 数据来源

数据来自芝加哥警察局的CLEAR系统，通过芝加哥市开放数据门户获取：

  - **官方数据源**: [https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2)
  - **Kaggle数据集**: [https://www.kaggle.com/datasets/chicagopolice/chicago-crime-data](https://www.kaggle.com/datasets/chicagopolice/chicago-crime-data)

## 数据存储说明

**注意**: 本GitHub仓库不包含原始数据文件（CSV和ZIP文件），因为这些文件较大且已经上传到Snowflake数据仓库中进行处理和分析。

### 如何获取数据：

1.  **下载原始数据**: 从上述数据源链接下载数据文件
2.  **数据存放位置**: 将下载的文件放在 `data/` 目录下
3.  **或使用Snowflake**: 数据已上传到Snowflake，可以直接通过SQL查询使用

### 数据文件结构：

```
data/
├── chicago_crime_dataset_v2.csv.zip    # 原始压缩文件
├── extracted/
│   └── chicago_crime_dataset_v2.csv     # 解压后的CSV文件（约2GB）
└── split_files/                         # 分割后的小文件（用于Snowflake上传）
    ├── chicago_crime_part_001.csv
    ├── chicago_crime_part_002.csv
    └── ...
```