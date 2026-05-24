# Runs the full pipeline: scrape -> enrich -> AI digests -> email.
# Used by Windows Task Scheduler (see register_scheduled_task.ps1).

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$LogDir = Join-Path $ProjectRoot "logs"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$LogFile = Join-Path $LogDir ("pipeline_{0:yyyy-MM-dd}.log" -f (Get-Date))

function Write-Log([string]$Message) {
    $line = "{0} {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Message
    Add-Content -Path $LogFile -Value $line -Encoding utf8
    Write-Host $line
}

try {
    Write-Log "Starting AI news aggregator pipeline in $ProjectRoot"

    $uv = Get-Command uv -ErrorAction Stop
    Write-Log "Using uv at $($uv.Source)"

    & $uv.Source run python main.py 2>&1 | ForEach-Object {
        $text = $_.ToString()
        Add-Content -Path $LogFile -Value $text -Encoding utf8
        Write-Host $text
    }

    $exitCode = $LASTEXITCODE
    if ($null -eq $exitCode) { $exitCode = 0 }
    Write-Log "Pipeline finished with exit code $exitCode"
    exit $exitCode
}
catch {
    Write-Log "ERROR: $_"
    exit 1
}
