<#
CLEAN_PROJECT.ps1
Removes old build artifacts and outdated EXE files while keeping:
 - LibraryApp/ (source)
 - Current virtual environment (.venv)
 - The most recent executable you specify
#>

param(
    [string]$Keep = "LibraryManagementSystem_v2.5.0_UI_FIXED.exe"
)

Write-Host "🧹 Cleaning project..." -ForegroundColor Cyan
$root = Get-Location

# 1. Remove build + dist folders inside LibraryApp
$buildPaths = @(
    Join-Path $root 'LibraryApp\build',
    Join-Path $root 'LibraryApp\dist'
)
foreach ($p in $buildPaths) {
    if (Test-Path $p) {
        Write-Host "Removing $p" -ForegroundColor Yellow
        Remove-Item -Recurse -Force $p -ErrorAction SilentlyContinue
    }
}

# 2. Remove old executables except chosen one
Get-ChildItem -Filter '*.exe' | Where-Object { $_.Name -ne $Keep } | ForEach-Object {
    if ( $_.Name -like 'LibraryManagementSystem*' -or $_.Name -like 'LibraryOfComputerDepartment*' ) {
        Write-Host "Deleting old executable: $($_.Name)" -ForegroundColor Yellow
        Remove-Item $_.FullName -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "✅ Cleanup complete. Kept: $Keep" -ForegroundColor Green
