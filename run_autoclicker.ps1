# Advanced Auto Clicker Launcher
Write-Host "Advanced Auto Clicker" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan
Write-Host ""

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "Starting application..." -ForegroundColor Green

try {
    & "C:/Users/Nadeesh Malaka/AppData/Local/Programs/Python/Python310/python.exe" main.py
} catch {
    Write-Host "Error starting application: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}