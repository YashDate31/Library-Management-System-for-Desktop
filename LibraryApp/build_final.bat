@echo off
setlocal ENABLEDELAYEDEXPANSION

echo ==================================================
echo Building FINAL CLEAN Executable (v3.4.0_FINAL_CLEAN)
echo ==================================================

cd /d "%~dp0"

if not exist "..\.venv\Scripts\python.exe" (
  echo [ERROR] Virtual environment Python not found at ..\.venv\Scripts\python.exe
  echo Please ensure your venv exists.
  pause
  exit /b 1
)

REM Clean previous dist/build for fresh build
if exist build rd /s /q build
if exist dist rd /s /q dist

"..\.venv\Scripts\python.exe" -m PyInstaller build_final.spec
if %errorlevel% neq 0 (
  echo Build failed.
  pause
  exit /b 1
)

echo.
echo Build complete.
echo Output EXE: %cd%\dist\LibraryOfComputerDepartment_v3.4.0_FINAL_CLEAN.exe
echo.
echo You can now run the EXE. Version label inside app should show: v3.4.0_FINAL_CLEAN
pause
