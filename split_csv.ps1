# CSV File Splitter for Snowflake Upload
# Splits large CSV file into smaller chunks suitable for Snowflake

param(
    [string]$InputFile = "C:\AS\chicago_crime\data\extracted\chicago_crime_dataset_v2.csv",
    [string]$OutputDir = "C:\AS\chicago_crime\data\split_files",
    [int]$MaxSizeMB = 50,
    [int]$LinesPerChunk = 100000  # Approximately 50MB chunks
)

# Create output directory
if (!(Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force
}

Write-Host "Starting to split CSV file: $InputFile"
Write-Host "Output directory: $OutputDir"
Write-Host "Target size per file: ${MaxSizeMB}MB"

# Read the header line
$header = Get-Content $InputFile -Head 1
Write-Host "Header: $($header.Substring(0, [Math]::Min(100, $header.Length)))..."

# Count total lines (excluding header)
$totalLines = (Get-Content $InputFile | Measure-Object -Line).Lines - 1
Write-Host "Total data lines: $totalLines"

# Calculate number of files needed
$numFiles = [Math]::Ceiling($totalLines / $LinesPerChunk)
Write-Host "Will create approximately $numFiles files"

# Split the file
$currentFile = 1
$currentLine = 0
$reader = [System.IO.File]::OpenText($InputFile)

try {
    # Skip header in reader
    $reader.ReadLine() | Out-Null
    
    while ($reader.Peek() -ge 0) {
        $outputFile = Join-Path $OutputDir "chicago_crime_part_$('{0:D3}' -f $currentFile).csv"
        $writer = [System.IO.StreamWriter]::new($outputFile)
        
        try {
            # Write header to each file
            $writer.WriteLine($header)
            
            # Write data lines
            for ($i = 0; $i -lt $LinesPerChunk -and $reader.Peek() -ge 0; $i++) {
                $line = $reader.ReadLine()
                $writer.WriteLine($line)
                $currentLine++
            }
            
            Write-Host "Created file $currentFile`: $outputFile ($i lines)"
        }
        finally {
            $writer.Close()
        }
        
        $currentFile++
    }
}
finally {
    $reader.Close()
}

Write-Host "Split complete! Created $($currentFile - 1) files"
Write-Host "Total lines processed: $currentLine"

# Show file sizes
Get-ChildItem -Path $OutputDir -Filter "*.csv" | Select-Object Name, @{Name="Size(MB)";Expression={[math]::Round($_.Length/1MB,2)}} | Format-Table

