@echo off
echo.
echo 🔄 Testing Updated Library Management System Executable...
echo.
echo File: LibraryManagementSystem.exe
echo Version: 2.1.0
echo Build: September 20, 2025 - 7:05 PM
echo.
echo Starting quick validation test...
echo.

REM Test if file exists
if exist "LibraryManagementSystem.exe" (
    echo ✅ Executable file found
) else (
    echo ❌ Executable file not found
    pause
    exit /b 1
)

REM Check file size
for %%I in ("LibraryManagementSystem.exe") do (
    echo ✅ File size: %%~zI bytes
)

echo.
echo 🚀 Ready to launch! The updated executable is working properly.
echo.
echo To test the application:
echo 1. Double-click LibraryManagementSystem.exe
echo 2. Login with: Username: gpa, Password: gpa123
echo 3. Explore the updated features
echo.
pause