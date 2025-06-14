@echo off
echo Starting complete CSV file splitting...
powershell -Command "& { $InputFile = 'C:\AS\chicago_crime\data\extracted\chicago_crime_dataset_v2.csv'; $OutputDir = 'C:\AS\chicago_crime\data\split_files'; $LinesPerChunk = 100000; $header = Get-Content $InputFile -Head 1; $reader = [System.IO.File]::OpenText($InputFile); $reader.ReadLine() | Out-Null; $currentFile = 1; $currentLine = 0; while ($reader.Peek() -ge 0) { $outputFile = Join-Path $OutputDir "chicago_crime_part_$($currentFile.ToString('D3')).csv"; $writer = [System.IO.StreamWriter]::new($outputFile); $writer.WriteLine($header); for ($i = 0; $i -lt $LinesPerChunk -and $reader.Peek() -ge 0; $i++) { $line = $reader.ReadLine(); $writer.WriteLine($line); $currentLine++ }; $writer.Close(); Write-Host "Created file $currentFile : $(Split-Path $outputFile -Leaf) ($i lines)"; $currentFile++; if ($currentFile -gt 80) { break } }; $reader.Close(); Write-Host "Split complete! Created $($currentFile - 1) files"; Write-Host "Total lines processed: $currentLine" }"
echo File splitting completed!
pause

