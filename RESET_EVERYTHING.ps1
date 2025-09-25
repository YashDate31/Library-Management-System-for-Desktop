# ===============================================================================
# COMPLETE RESET SCRIPT - Library Management System
# This will DELETE EVERYTHING and start fresh!
# ===============================================================================

Write-Host "🚨 COMPLETE RESET - Library Management System 🚨" -ForegroundColor Red
Write-Host "This will DELETE ALL FILES in the current directory!" -ForegroundColor Yellow
Write-Host ""

# Confirm deletion
$confirmation = Read-Host "Type 'DELETE_ALL' to confirm complete reset"
if ($confirmation -ne "DELETE_ALL") {
    Write-Host "❌ Reset cancelled. No files were deleted." -ForegroundColor Green
    exit
}

Write-Host "🗑️  Starting complete reset..." -ForegroundColor Red

# Get current directory (should be Library Management System)
$currentDir = Get-Location

# Delete all files and folders except this reset script
Get-ChildItem -Path $currentDir -Exclude "RESET_EVERYTHING.ps1" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "✅ All files deleted successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📁 Creating fresh project structure..." -ForegroundColor Cyan

# Create LibraryApp directory
New-Item -ItemType Directory -Path "LibraryApp" -Force | Out-Null

Write-Host "✅ Fresh project structure created!" -ForegroundColor Green
Write-Host ""
Write-Host "🎯 Next steps:" -ForegroundColor Yellow
Write-Host "1. Run the build script that will be created" -ForegroundColor White
Write-Host "2. All files will be recreated from scratch" -ForegroundColor White
Write-Host "3. A fresh, working Library Management System will be ready" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Reset complete! Ready for fresh start." -ForegroundColor Green