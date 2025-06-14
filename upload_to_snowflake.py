#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Snowflake Data Upload Script for Chicago Crime Dataset
Uploads split CSV files to Snowflake database
"""

import snowflake.connector
import os
import glob
from pathlib import Path

# Snowflake configuration from environment variables
CONFIG = {
    'account': os.getenv('SNOWFLAKE_ACCOUNT', 'gzhlbee-bv06447'),
    'user': os.getenv('SNOWFLAKE_USER', 'lixiaowww'),
    'password': os.getenv('SNOWFLAKE_PASSWORD', 'Sean0105@winnipeg!'),
    'database': os.getenv('SNOWFLAKE_DATABASE', 'covid_database'),
    'schema': os.getenv('SNOWFLAKE_SCHEMA', 'covid_schema'),
    'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE', 'warehouse')
}

def create_connection():
    """Create Snowflake connection"""
    try:
        conn = snowflake.connector.connect(
            user=CONFIG['user'],
            password=CONFIG['password'],
            account=CONFIG['account'],
            warehouse=CONFIG['warehouse'],
            database=CONFIG['database'],
            schema=CONFIG['schema']
        )
        print(f"Successfully connected to Snowflake account: {CONFIG['account']}")
        return conn
    except Exception as e:
        print(f"Error connecting to Snowflake: {e}")
        return None

def create_table(cursor):
    """Create the Chicago Crime table if it doesn't exist"""
    create_table_sql = """
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
    )
    """
    
    try:
        cursor.execute(create_table_sql)
        print("Table CHICAGO_CRIME created successfully")
        return True
    except Exception as e:
        print(f"Error creating table: {e}")
        return False

def upload_files(cursor, file_directory):
    """Upload CSV files to Snowflake"""
    csv_files = glob.glob(os.path.join(file_directory, "chicago_crime_part_*.csv"))
    csv_files.sort()
    
    print(f"Found {len(csv_files)} CSV files to upload")
    
    successful_uploads = 0
    
    for file_path in csv_files:
        file_name = os.path.basename(file_path)
        print(f"Uploading {file_name}...")
        
        try:
            # Create stage for file upload
            stage_sql = f"PUT 'file://{file_path.replace(os.sep, '/')}' @~/staged"
            cursor.execute(stage_sql)
            
            # Copy data from stage to table
            copy_sql = f"""
            COPY INTO CHICAGO_CRIME
            FROM @~/staged/{file_name}
            FILE_FORMAT = (TYPE = 'CSV' FIELD_DELIMITER = ',' SKIP_HEADER = 1 ESCAPE_UNENCLOSED_FIELD = '\\"')
            ON_ERROR = 'CONTINUE'
            """
            cursor.execute(copy_sql)
            
            print(f"✓ Successfully uploaded {file_name}")
            successful_uploads += 1
            
        except Exception as e:
            print(f"✗ Error uploading {file_name}: {e}")
    
    print(f"Upload completed: {successful_uploads}/{len(csv_files)} files successful")
    return successful_uploads

def main():
    """Main function"""
    print("Chicago Crime Data Upload to Snowflake")
    print("=" * 40)
    
    # File directory containing split CSV files
    file_directory = r"C:\AS\chicago_crime\data\split_files"
    
    if not os.path.exists(file_directory):
        print(f"Error: Directory {file_directory} does not exist")
        return
    
    # Create connection
    conn = create_connection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        # Create table
        if create_table(cursor):
            # Upload files
            upload_files(cursor, file_directory)
            
            # Show record count
            cursor.execute("SELECT COUNT(*) FROM CHICAGO_CRIME")
            count = cursor.fetchone()[0]
            print(f"\nTotal records in CHICAGO_CRIME table: {count:,}")
        
    except Exception as e:
        print(f"Error during upload process: {e}")
    
    finally:
        conn.close()
        print("Connection closed")

if __name__ == "__main__":
    main()

