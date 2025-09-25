<#!
.SYNOPSIS
  Build a clean release (standard Windows 10/11) and optionally a legacy Win7 build.

.PARAMETER Legacy
  Include to build Windows 7 compatible executable using Python 3.8 and requirements_win7.txt.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File .\release_build.ps1

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File .\release_build.ps1 -Legacy
#>
param(
  [switch]$Legacy
)

Write-Host "=== Library Management System Release Build ===" -ForegroundColor Cyan

# Ensure running from script directory
Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Path)

if (-not (Test-Path .venv)) {
  Write-Host "Creating virtual environment (.venv)" -ForegroundColor Yellow
  py -3.11 -m venv .venv
}

Write-Host "Activating venv (.venv)" -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

Write-Host "Installing/updating standard requirements" -ForegroundColor Yellow
pip install --upgrade pip >$null
pip install -r LibraryApp\requirements.txt

Write-Host "Building standard executable (v5.0)" -ForegroundColor Yellow
python -m PyInstaller LibraryApp\build_app.spec

if ($Legacy) {
  if (-not (Test-Path .venv38)) {
    Write-Host "Creating legacy virtual environment (.venv38)" -ForegroundColor Yellow
    py -3.8 -m venv .venv38
  }
  Write-Host "Activating legacy env (.venv38)" -ForegroundColor Yellow
  & .\.venv38\Scripts\Activate.ps1
  Write-Host "Installing legacy pinned requirements" -ForegroundColor Yellow
  pip install --upgrade pip >$null
  pip install -r requirements_win7.txt
  Write-Host "Building legacy executable (Win7)" -ForegroundColor Yellow
  pyinstaller --clean --noconfirm --name LibraryManagementSystem_win7 --add-data "LibraryApp\library.db;." LibraryApp\main.py
  Write-Host "Re-activating main env" -ForegroundColor Yellow
  & .\.venv\Scripts\Activate.ps1
}

Write-Host "Build(s) complete. Dist contents:" -ForegroundColor Green
Get-ChildItem dist
