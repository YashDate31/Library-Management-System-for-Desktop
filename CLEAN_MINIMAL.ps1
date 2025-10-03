param(
  [ValidateSet('dev','exe')]
  [string]$Mode = 'dev',
  [switch]$WhatIf
)

$ErrorActionPreference = 'Stop'

function Get-SizeMB($Path) {
  if (Test-Path $Path) {
    $bytes = (Get-ChildItem -Path $Path -Recurse -File -Force | Measure-Object -Sum Length).Sum
    [math]::Round(($bytes / 1MB), 2)
  } else { 0 }
}

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$lib  = Join-Path $root 'LibraryApp'
$dist = Join-Path $lib  'dist'

Write-Host "Root:" $root
$before = Get-SizeMB $root
Write-Host ("BEFORE_TOTAL_MB=" + $before)

# Files/folders to always remove (if present)
$removeFolders = @(
  (Join-Path $root 'build'),
  (Join-Path $lib  'build'),
  (Join-Path $root 'dist') # top-level dist, not LibraryApp\dist
)

# Old/backup/test/sample files to remove from LibraryApp
$removeFiles = @(
  'sample_books.csv','sample_books.xlsx',
  'sample_students.csv','sample_students.xlsx','sample_students_import.xlsx',
  'create_sample_excel.py','create_sample_students.py','csv_to_excel.py','students_tab_clean.py',
  'test_add_book.py','temp_borrow_test.py','test_docx_import.py','test_excel.py','test_import.xlsx',
  'main_backup.py','main_corrected.py','main_new.py','main_old.py',
  'library_pre_build_backup.db','library_pre_clean_backup.db',
  'final_verification.py','fix_duplicate.py','fix_encoding.py','fix_syntax.py','reset_database.py','launcher.py',
  'build_final.bat','CHANGES_SUMMARY.md'
) | ForEach-Object { Join-Path $lib $_ }

# Spec files to keep
$keepSpecs = @('build_app.spec','build_updated_app.spec')

# 1) Remove EXEs from root
Get-ChildItem -Path $root -File -Filter *.exe -Force | ForEach-Object {
  if ($WhatIf) { Write-Host "[WhatIf] DEL" $_.FullName } else { Remove-Item -Force $_.FullName }
}

# 2) Clean LibraryApp\dist (keep only latest app EXE and DB)
$keepExe = 'LibraryManagementSystem_v5.0_FINAL.exe'
if (Test-Path $dist) {
  Get-ChildItem -Path $dist -File -Force | ForEach-Object {
    $n = $_.Name
    if ($n -ne $keepExe -and $n -ne 'library.db') {
      if ($WhatIf) { Write-Host "[WhatIf] DEL" $_.FullName } else { Remove-Item -Force $_.FullName }
    }
  }
}

# 3) Remove build artifact folders
foreach ($f in $removeFolders) {
  if (Test-Path $f) {
    if ($WhatIf) { Write-Host "[WhatIf] RMDIR" $f } else { Remove-Item -Recurse -Force $f }
  }
}

# 4) Remove __pycache__ recursively under LibraryApp
Get-ChildItem -Path $lib -Directory -Recurse -Filter __pycache__ -Force | ForEach-Object {
  if ($WhatIf) { Write-Host "[WhatIf] RMDIR" $_.FullName } else { Remove-Item -Recurse -Force $_.FullName }
}

# 5) Remove duplicate root DB
$rootDb = Join-Path $root 'library.db'
if (Test-Path $rootDb) {
  if ($WhatIf) { Write-Host "[WhatIf] DEL" $rootDb } else { Remove-Item -Force $rootDb }
}

# 6) Remove old/backup/test/sample files
foreach ($fp in $removeFiles) {
  if (Test-Path $fp) {
    if ($WhatIf) { Write-Host "[WhatIf] DEL" $fp } else { Remove-Item -Force $fp }
  }
}

# 7) Remove old spec variants (keep primary two)
Get-ChildItem -Path $lib -File -Filter *.spec -Force | Where-Object { $_.Name -notin $keepSpecs } | ForEach-Object {
  if ($WhatIf) { Write-Host "[WhatIf] DEL" $_.FullName } else { Remove-Item -Force $_.FullName }
}

# 8) Mode-specific cleanup
if ($Mode -eq 'exe') {
  # Remove the virtual environment and most sources, keeping only dist output and minimal docs
  $venv = Join-Path $root '.venv'
  if (Test-Path $venv) {
    if ($WhatIf) { Write-Host "[WhatIf] RMDIR" $venv } else { Remove-Item -Recurse -Force $venv }
  }
  # Optionally remove source files except main/minimal, but we will be conservative: keep LibraryApp folder for now
  Write-Host "Mode=exe: venv removed. Sources retained (conservative)."
} else {
  Write-Host "Mode=dev: keeping venv and sources."
}

$after = Get-SizeMB $root
Write-Host ("AFTER_TOTAL_MB=" + $after)
Write-Host ("FREED_MB=" + [math]::Round(($before - $after), 2))
Write-Host "CLEANUP_DONE"
