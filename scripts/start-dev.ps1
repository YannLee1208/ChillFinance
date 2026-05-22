param(
    [int]$BackendPort = 8000,
    [int]$FrontendPort = 5173
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root ".venv\Scripts\python.exe"

if (-not (Test-Path $Python)) {
    throw "Virtual environment not found. Run scripts\bootstrap.ps1 first."
}

$env:VITE_API_BASE_URL = "http://127.0.0.1:$BackendPort"

Start-Process powershell -WindowStyle Hidden -WorkingDirectory $Root -ArgumentList @(
    "-NoExit",
    "-Command",
    "& '$Python' -m uvicorn backend.app:create_app --factory --host 127.0.0.1 --port $BackendPort --reload"
)

Start-Process powershell -WindowStyle Hidden -WorkingDirectory (Join-Path $Root "frontend") -ArgumentList @(
    "-NoExit",
    "-Command",
    "`$env:VITE_API_BASE_URL='http://127.0.0.1:$BackendPort'; npm run dev -- --host 127.0.0.1 --port $FrontendPort"
)

Write-Host "Backend:  http://127.0.0.1:$BackendPort"
Write-Host "Frontend: http://127.0.0.1:$FrontendPort"
