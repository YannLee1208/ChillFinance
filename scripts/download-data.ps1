param(
    [string]$Domain = "",
    [string]$Codes = ""
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root ".venv\Scripts\python.exe"

if (-not (Test-Path $Python)) {
    throw "Virtual environment not found. Run scripts\bootstrap.ps1 first."
}

& $Python -m backend.cli init-db
if ($Codes) {
    & $Python -m backend.cli ingest --codes $Codes
} elseif ($Domain) {
    & $Python -m backend.cli ingest-domain $Domain
} else {
    & $Python -m backend.cli ingest
}
