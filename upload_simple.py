#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Chicago Crime Data Upload Script
Uses basic HTTP requests to interact with Snowflake
"""

import os
import csv
import pandas as pd
from pathlib import Path

def analyze_split_files():
    """Analyze the split CSV files"""
    split_dir = Path(r"C:\AS\chicago_crime\data\split_files")
    
    if not split_dir.exists():
        print(f"Directory {split_dir} does not exist")
        return
    
    csv_files = list(split_dir.glob("chicago_crime_part_*.csv"))
    csv_files.sort()
    
    print(f"Found {len(csv_files)} CSV files:")
    print("=" * 50)
    
    total_size = 0
    total_rows = 0
    
    for i, file_path in enumerate(csv_files):
        file_size = file_path.stat().st_size
        total_size += file_size
        
        # Count rows in file
        with open(file_path, 'r', encoding='utf-8') as f:
            row_count = sum(1 for line in f) - 1  # Subtract header
        
        total_rows += row_count
        
        print(f"{i+1:2d}. {file_path.name}")
        print(f"    Size: {file_size/1024/1024:.2f} MB")
        print(f"    Rows: {row_count:,}")
        
        if i < 5:  # Show first 5 files in detail
            # Show sample data
            df = pd.read_csv(file_path, nrows=3)
            print(f"    Columns: {', '.join(df.columns[:5])}...")
            print()
    
    print(f"\nSummary:")
    print(f"Total files: {len(csv_files)}")
    print(f"Total size: {total_size/1024/1024:.2f} MB")
    print(f"Total rows: {total_rows:,}")
    print(f"Average file size: {total_size/len(csv_files)/1024/1024:.2f} MB")
    print(f"Average rows per file: {total_rows//len(csv_files):,}")
    
    # Check if files are suitable for Snowflake
    max_file_size = max(f.stat().st_size for f in csv_files) / 1024 / 1024
    print(f"\nSnowflake Compatibility:")
    print(f"Largest file: {max_file_size:.2f} MB")
    
    if max_file_size < 50:
        print("✓ All files are under 50MB - suitable for Snowflake upload")
    else:
        print("⚠ Some files exceed 50MB - may need further splitting")
    
    return csv_files

def create_snowflake_sql_commands(csv_files):
    """Create SQL commands for Snowflake upload"""
    
    sql_commands = []
    
    # Create database and schema
    sql_commands.append("""
-- Create database and schema
CREATE DATABASE IF NOT EXISTS covid_database;
USE DATABASE covid_database;
CREATE SCHEMA IF NOT EXISTS covid_schema;
USE SCHEMA covid_schema;
""")
    
    # Create table
    sql_commands.append("""
-- Create Chicago Crime table
CREATE OR REPLACE TABLE CHICAGO_CRIME (
    ID VARCHAR(50),
    CASE_NUMBER VARCHAR(50),
    DATE VARCHAR(50),
    BLOCK VARCHAR(100),
    IUCR VARCHAR(10),
    PRIMARY_TYPE VARCHAR(100),
    DESCRIPTION VARCHAR(200),
    LOCATION_DESCRIPTION VARCHAR(100),
    ARREST BOOLEAN,
    DOMESTIC BOOLEAN,
    BEAT VARCHAR(10),
    DISTRICT VARCHAR(10),
    WARD VARCHAR(10),
    COMMUNITY_AREA VARCHAR(10),
    FBI_CODE VARCHAR(10),
    X_COORDINATE VARCHAR(20),
    Y_COORDINATE VARCHAR(20),
    YEAR VARCHAR(10),
    UPDATED_ON VARCHAR(50),
    LATITUDE VARCHAR(20),
    LONGITUDE VARCHAR(20),
    LOCATION VARCHAR(100),
    HISTORICAL_WARDS_2003_2015 VARCHAR(10),
    ZIP_CODES VARCHAR(10),
    COMMUNITY_AREAS VARCHAR(10),
    CENSUS_TRACTS VARCHAR(10),
    WARDS VARCHAR(10),
    BOUNDARIES_ZIP_CODES VARCHAR(10),
    POLICE_DISTRICTS VARCHAR(10),
    POLICE_BEATS VARCHAR(10)
);
""")
    
    # Create file format
    sql_commands.append("""
-- Create file format for CSV
CREATE OR REPLACE FILE FORMAT csv_format
TYPE = 'CSV'
FIELD_DELIMITER = ','
SKIP_HEADER = 1
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
ESCAPE_UNENCLOSED_FIELD = '\\';
""")
    
    # Upload commands for each file
    for i, file_path in enumerate(csv_files[:5]):  # Show first 5 files as example
        file_name = file_path.name
        sql_commands.append(f"""
-- Upload {file_name}
-- Step 1: Upload file to stage
PUT 'file://C:/AS/chicago_crime/data/split_files/{file_name}' @~/staged;

-- Step 2: Copy data from stage to table
COPY INTO CHICAGO_CRIME
FROM @~/staged/{file_name}
FILE_FORMAT = csv_format
ON_ERROR = 'CONTINUE';
""")
    
    if len(csv_files) > 5:
        sql_commands.append(f"""
-- ... Repeat the above process for remaining {len(csv_files) - 5} files ...
-- You can upload all files using a loop or batch process
""")
    
    # Final verification
    sql_commands.append("""
-- Verify upload
SELECT COUNT(*) as total_records FROM CHICAGO_CRIME;
SELECT * FROM CHICAGO_CRIME LIMIT 10;
""")
    
    return sql_commands

def main():
    """Main function"""
    print("Chicago Crime Dataset Analysis and Snowflake Upload Preparation")
    print("=" * 65)
    
    # Analyze split files
    csv_files = analyze_split_files()
    
    if csv_files:
        # Create SQL commands
        sql_commands = create_snowflake_sql_commands(csv_files)
        
        # Save SQL commands to file
        sql_file = Path(r"C:\AS\chicago_crime\snowflake_upload_commands.sql")
        with open(sql_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sql_commands))
        
        print(f"\n📝 Created SQL command file: {sql_file}")
        print("\n🔧 Next Steps:")
        print("1. Install Snowflake CLI or use Snowflake Web Interface")
        print("2. Connect to your Snowflake account:")
        print(f"   Account: gzhlbee-bv06447")
        print(f"   User: lixiaowww")
        print("3. Execute the SQL commands in the generated file")
        print("4. Monitor the upload progress and verify data integrity")
        
        print("\n💡 Alternative: Use Snowflake Web Interface")
        print("1. Log into Snowflake web console")
        print("2. Use the 'Load Data' wizard")
        print("3. Upload files one by one (they're now small enough)")
        print("4. Snowflake will automatically detect the schema")

if __name__ == "__main__":
    try:
        import pandas as pd
        main()
    except ImportError:
        print("Installing pandas...")
        os.system("pip install pandas")
        import pandas as pd
        main()

