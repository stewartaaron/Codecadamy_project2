Write-Host "Current directory: $(Get-Location)"
py db_clean_exportREV2.py    # Executes python code

$DB_NAME = "pipeline.db"  # Name of your SQLite DB

# === DELETE EXISTING DATABASE IF IT EXISTS ===
if (Test-Path $DB_NAME) {
    Write-Host "Deleting existing database: $DB_NAME"
    Remove-Item $DB_NAME
}

# === LOOP THROUGH CSV FILES IN CURRENT DIRECTORY ===
Get-ChildItem -Filter *.csv | ForEach-Object {
    $file = $_.FullName
    $table_name = ($_.BaseName -replace ' ', '_' ).ToLower()
    Write-Host "Importing $file as table $table_name"

    $sqliteCmd = @"
.mode csv
.import `"$file`" $table_name
"@
    $sqliteCmd | sqlite3 $DB_NAME
}

Write-Host "All CSV files imported into $DB_NAME"