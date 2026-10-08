param([switch]$SkipDependencies)
$ErrorActionPreference = 'Stop'
$bpaRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $bpaRoot
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw 'Install Python 3.12 or newer with PATH enabled, then rerun.'
}
if (-not (Test-Path -LiteralPath '.venv/Scripts/python.exe')) {
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Python environment creation failed.' }
}
if (-not $SkipDependencies) {
    & ./.venv/Scripts/python.exe -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
}
& ./.venv/Scripts/python.exe -m harness.cli init
if ($LASTEXITCODE -ne 0) { throw 'Local setup failed.' }
& ./.venv/Scripts/python.exe -m harness.cli doctor
Write-Host 'Next: SETUP.md. Sign in privately and run the platform checks there.'
