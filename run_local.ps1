# 运行本项目的本地开发环境：后端 + 前端
# 在 PowerShell 中执行：
#   .\run_local.ps1

$backendDir = Join-Path $PSScriptRoot 'backend'
$frontendDir = Join-Path $PSScriptRoot 'frontend'

Write-Host "Starting backend in $backendDir..."
Start-Process powershell -ArgumentList "-NoExit", "cd '$backendDir'; uvicorn app:app --reload --host 0.0.0.0 --port 8001"

Write-Host "Starting frontend server in $frontendDir..."
Start-Process powershell -ArgumentList "-NoExit", "cd '$frontendDir'; python -m http.server 5500"

Start-Sleep -Seconds 2
Write-Host "Opening browser to http://127.0.0.1:5500"
Start-Process "http://127.0.0.1:5500"