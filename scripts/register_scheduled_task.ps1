# Creates a Windows scheduled task that runs the daily pipeline at 8:00 AM.
# Run once from PowerShell:  .\scripts\register_scheduled_task.ps1
# Optional: .\scripts\register_scheduled_task.ps1 -Time "07:30"

param(
    [string]$Time = "08:00",
    [string]$TaskName = "AI News Aggregator Daily"
)

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$ScriptPath = Join-Path $ProjectRoot "scripts\run_daily.ps1"

if (-not (Test-Path $ScriptPath)) {
    Write-Error "Missing script: $ScriptPath"
    exit 1
}

$Action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$ScriptPath`"" `
    -WorkingDirectory $ProjectRoot

$Trigger = New-ScheduledTaskTrigger -Daily -At $Time

$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2)

$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

$existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existing) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "Replaced existing task '$TaskName'."
}

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Principal $Principal `
    -Description "Scrapes AI news, saves to Supabase, generates digests, sends Gmail digest." | Out-Null

Write-Host ""
Write-Host "Scheduled task registered: $TaskName"
Write-Host "  Runs daily at: $Time"
Write-Host "  Script: $ScriptPath"
Write-Host "  Logs: $ProjectRoot\logs\"
Write-Host ""
Write-Host "Test now:  .\scripts\run_daily.ps1"
Write-Host "Open Task Scheduler: taskschd.msc  (look under Task Scheduler Library)"
