
-- Create database and schema
CREATE DATABASE IF NOT EXISTS covid_database;
USE DATABASE covid_database;
CREATE SCHEMA IF NOT EXISTS covid_schema;
USE SCHEMA covid_schema;


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


-- Create file format for CSV
CREATE OR REPLACE FILE FORMAT csv_format
TYPE = 'CSV'
FIELD_DELIMITER = ','
SKIP_HEADER = 1
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
ESCAPE_UNENCLOSED_FIELD = '\';


-- Upload chicago_crime_part_001.csv
-- Step 1: Upload file to stage
PUT 'file://C:/AS/chicago_crime/data/split_files/chicago_crime_part_001.csv' @~/staged;

-- Step 2: Copy data from stage to table
COPY INTO CHICAGO_CRIME
FROM @~/staged/chicago_crime_part_001.csv
FILE_FORMAT = csv_format
ON_ERROR = 'CONTINUE';


-- Upload chicago_crime_part_002.csv
-- Step 1: Upload file to stage
PUT 'file://C:/AS/chicago_crime/data/split_files/chicago_crime_part_002.csv' @~/staged;

-- Step 2: Copy data from stage to table
COPY INTO CHICAGO_CRIME
FROM @~/staged/chicago_crime_part_002.csv
FILE_FORMAT = csv_format
ON_ERROR = 'CONTINUE';


-- Upload chicago_crime_part_003.csv
-- Step 1: Upload file to stage
PUT 'file://C:/AS/chicago_crime/data/split_files/chicago_crime_part_003.csv' @~/staged;

-- Step 2: Copy data from stage to table
COPY INTO CHICAGO_CRIME
FROM @~/staged/chicago_crime_part_003.csv
FILE_FORMAT = csv_format
ON_ERROR = 'CONTINUE';


-- Upload chicago_crime_part_004.csv
-- Step 1: Upload file to stage
PUT 'file://C:/AS/chicago_crime/data/split_files/chicago_crime_part_004.csv' @~/staged;

-- Step 2: Copy data from stage to table
COPY INTO CHICAGO_CRIME
FROM @~/staged/chicago_crime_part_004.csv
FILE_FORMAT = csv_format
ON_ERROR = 'CONTINUE';


-- Upload chicago_crime_part_005.csv
-- Step 1: Upload file to stage
PUT 'file://C:/AS/chicago_crime/data/split_files/chicago_crime_part_005.csv' @~/staged;

-- Step 2: Copy data from stage to table
COPY INTO CHICAGO_CRIME
FROM @~/staged/chicago_crime_part_005.csv
FILE_FORMAT = csv_format
ON_ERROR = 'CONTINUE';


-- ... Repeat the above process for remaining 10 files ...
-- You can upload all files using a loop or batch process


-- Verify upload
SELECT COUNT(*) as total_records FROM CHICAGO_CRIME;
SELECT * FROM CHICAGO_CRIME LIMIT 10;
