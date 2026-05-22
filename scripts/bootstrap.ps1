param(
    [switch]$Dev
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Venv = Join-Path $Root ".venv"
$Python = Join-Path $Venv "Scripts\python.exe"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python 3.11+ is required and was not found in PATH."
}

if (-not (Test-Path $Python)) {
    python -m venv $Venv
}

& $Python -m pip install --upgrade pip
if ($Dev) {
    & $Python -m pip install -e "$Root[dev]"
} else {
    & $Python -m pip install -e $Root
}

Push-Location (Join-Path $Root "frontend")
try {
    npm install
} finally {
    Pop-Location
}

if (-not (Test-Path (Join-Path $Root ".env")) -and (Test-Path (Join-Path $Root "env.example"))) {
    Copy-Item (Join-Path $Root "env.example") (Join-Path $Root ".env")
}

New-Item -ItemType Directory -Force -Path (Join-Path $Root "data") | Out-Null
& $Python -m backend.cli init-db
