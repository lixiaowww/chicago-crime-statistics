# Snowflake Batch Upload Script for Chicago Crime Data
# This script uploads split CSV files to Snowflake using SnowSQL

param(
    [string]$SnowSQLPath = "snowsql",
    [int]$MaxFiles = 15,
    [switch]$TestConnection,
    [switch]$DryRun
)

# Snowflake configuration - use environment variables if available
$Account = if ($env:SNOWFLAKE_ACCOUNT) { $env:SNOWFLAKE_ACCOUNT } else { "gzhlbee-bv06447" }
$User = if ($env:SNOWFLAKE_USER) { $env:SNOWFLAKE_USER } else { "lixiaowww" }
$Password = if ($env:SNOWFLAKE_PASSWORD) { $env:SNOWFLAKE_PASSWORD } else { "Sean0105@winnipeg!" }
$Database = if ($env:SNOWFLAKE_DATABASE) { $env:SNOWFLAKE_DATABASE } else { "covid_database" }
$Schema = if ($env:SNOWFLAKE_SCHEMA) { $env:SNOWFLAKE_SCHEMA } else { "covid_schema" }
$Warehouse = if ($env:SNOWFLAKE_WAREHOUSE) { $env:SNOWFLAKE_WAREHOUSE } else { "warehouse" }

# File paths
$SplitFilesDir = "C:\AS\chicago_crime\data\split_files"
$LogFile = "C:\AS\chicago_crime\upload_log.txt"

Write-Host "Snowflake Batch Upload Script" -ForegroundColor Green
Write-Host "=" * 40 -ForegroundColor Green
Write-Host "Account: $Account"
Write-Host "User: $User"
Write-Host "Database: $Database"
Write-Host "Schema: $Schema"
Write-Host "Files Directory: $SplitFilesDir"
Write-Host ""

# Initialize log file
"Upload started at $(Get-Date)" | Out-File $LogFile -Encoding UTF8

# Check if files exist
if (!(Test-Path $SplitFilesDir)) {
    Write-Error "Split files directory not found: $SplitFilesDir"
    exit 1
}

# Get all CSV files
$CsvFiles = Get-ChildItem -Path $SplitFilesDir -Filter "chicago_crime_part_*.csv" | Sort-Object Name
Write-Host "Found $($CsvFiles.Count) CSV files to upload" -ForegroundColor Yellow

if ($CsvFiles.Count -eq 0) {
    Write-Error "No CSV files found in $SplitFilesDir"
    exit 1
}

# Limit number of files if specified
if ($MaxFiles -gt 0 -and $CsvFiles.Count -gt $MaxFiles) {
    $CsvFiles = $CsvFiles[0..($MaxFiles-1)]
    Write-Host "Limited to first $MaxFiles files" -ForegroundColor Yellow
}

# Test connection function
function Test-SnowflakeConnection {
    Write-Host "Testing Snowflake connection..." -ForegroundColor Yellow
    
    $TestSQL = @"
SELECT CURRENT_USER(), CURRENT_DATABASE(), CURRENT_SCHEMA();
"@
    
    $TempSQLFile = "$env:TEMP\test_connection.sql"
    $TestSQL | Out-File $TempSQLFile -Encoding ASCII
    
    try {
        $Result = & $SnowSQLPath -c chicago_crime -f $TempSQLFile
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Connection successful!" -ForegroundColor Green
            return $true
        } else {
            Write-Host "✗ Connection failed!" -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "✗ Connection test error: $_" -ForegroundColor Red
        return $false
    } finally {
        Remove-Item $TempSQLFile -ErrorAction SilentlyContinue
    }
}

# Create database and table function
function Initialize-Database {
    Write-Host "Initializing database and table..." -ForegroundColor Yellow
    
    $InitSQL = @"
CREATE DATABASE IF NOT EXISTS $Database;
USE DATABASE $Database;
CREATE SCHEMA IF NOT EXISTS $Schema;
USE SCHEMA $Schema;
USE WAREHOUSE $Warehouse;

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

CREATE OR REPLACE FILE FORMAT csv_format
TYPE = 'CSV'
FIELD_DELIMITER = ','
SKIP_HEADER = 1
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
ESCAPE_UNENCLOSED_FIELD = '\\';
"@
    
    $TempSQLFile = "$env:TEMP\init_db.sql"
    $InitSQL | Out-File $TempSQLFile -Encoding ASCII
    
    try {
        $Result = & $SnowSQLPath -c chicago_crime -f $TempSQLFile
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Database and table initialized!" -ForegroundColor Green
            return $true
        } else {
            Write-Host "✗ Database initialization failed!" -ForegroundColor Red
            Write-Host $Result
            return $false
        }
    } catch {
        Write-Host "✗ Database initialization error: $_" -ForegroundColor Red
        return $false
    } finally {
        Remove-Item $TempSQLFile -ErrorAction SilentlyContinue
    }
}

# Upload single file function
function Upload-File {
    param([System.IO.FileInfo]$File)
    
    $FileName = $File.Name
    $FilePath = $File.FullName.Replace('\', '/')
    
    Write-Host "Uploading $FileName..." -ForegroundColor Cyan
    
    $UploadSQL = @"
USE DATABASE $Database;
USE SCHEMA $Schema;
USE WAREHOUSE $Warehouse;

-- Upload file to stage
PUT 'file://$FilePath' @~/staged;

-- Copy data from stage to table
COPY INTO CHICAGO_CRIME
FROM @~/staged/$FileName
FILE_FORMAT = csv_format
ON_ERROR = 'CONTINUE';

-- Show results
SELECT 
    'Upload completed for $FileName' as status,
    COUNT(*) as total_records_in_table
FROM CHICAGO_CRIME;
"@
    
    $TempSQLFile = "$env:TEMP\upload_$([System.IO.Path]::GetFileNameWithoutExtension($FileName)).sql"
    $UploadSQL | Out-File $TempSQLFile -Encoding ASCII
    
    try {
        if ($DryRun) {
            Write-Host "[DRY RUN] Would upload: $FileName" -ForegroundColor Yellow
            return $true
        }
        
        $StartTime = Get-Date
        $Result = & $SnowSQLPath -c chicago_crime -f $TempSQLFile
        $EndTime = Get-Date
        $Duration = ($EndTime - $StartTime).TotalSeconds
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ $FileName uploaded successfully! (${Duration}s)" -ForegroundColor Green
            "$(Get-Date) - SUCCESS: $FileName uploaded in ${Duration}s" | Out-File $LogFile -Append -Encoding UTF8
            return $true
        } else {
            Write-Host "✗ $FileName upload failed!" -ForegroundColor Red
            Write-Host $Result -ForegroundColor Red
            "$(Get-Date) - FAILED: $FileName upload failed" | Out-File $LogFile -Append -Encoding UTF8
            return $false
        }
    } catch {
        Write-Host "✗ Upload error for $FileName : $_" -ForegroundColor Red
        "$(Get-Date) - ERROR: $FileName - $_" | Out-File $LogFile -Append -Encoding UTF8
        return $false
    } finally {
        Remove-Item $TempSQLFile -ErrorAction SilentlyContinue
    }
}

# Main execution
try {
    # Test connection if requested
    if ($TestConnection) {
        if (!(Test-SnowflakeConnection)) {
            Write-Error "Connection test failed. Please check your credentials and network."
            exit 1
        }
        Write-Host ""
    }
    
    # Initialize database and table
    if (!(Initialize-Database)) {
        Write-Error "Database initialization failed."
        exit 1
    }
    Write-Host ""
    
    # Upload files
    $SuccessCount = 0
    $FailCount = 0
    $TotalFiles = $CsvFiles.Count
    
    Write-Host "Starting batch upload of $TotalFiles files..." -ForegroundColor Green
    Write-Host ""
    
    foreach ($File in $CsvFiles) {
        $FileNum = $CsvFiles.IndexOf($File) + 1
        Write-Host "[$FileNum/$TotalFiles] " -NoNewline -ForegroundColor White
        
        if (Upload-File -File $File) {
            $SuccessCount++
        } else {
            $FailCount++
        }
        
        # Brief pause between uploads
        Start-Sleep -Seconds 2
    }
    
    # Summary
    Write-Host ""
    Write-Host "Upload Summary:" -ForegroundColor Green
    Write-Host "================" -ForegroundColor Green
    Write-Host "Total files: $TotalFiles"
    Write-Host "Successful: $SuccessCount" -ForegroundColor Green
    Write-Host "Failed: $FailCount" -ForegroundColor Red
    Write-Host "Log file: $LogFile"
    
    "Upload completed at $(Get-Date) - Success: $SuccessCount, Failed: $FailCount" | Out-File $LogFile -Append -Encoding UTF8
    
    if ($SuccessCount -gt 0) {
        Write-Host ""
        Write-Host "✓ Upload process completed! Check Snowflake for your data." -ForegroundColor Green
    }
    
} catch {
    Write-Error "Script execution failed: $_"
    "$(Get-Date) - SCRIPT ERROR: $_" | Out-File $LogFile -Append -Encoding UTF8
    exit 1
}

Write-Host ""
Write-Host "Script completed. Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

