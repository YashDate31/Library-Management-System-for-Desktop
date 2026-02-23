@echo off
echo ============================================
echo Building GPA_CO_LMS.exe
echo ============================================
echo.
echo This will take 3-5 minutes...
echo Please do NOT close this window!
echo.

cd /d "c:\Users\Yash\OneDrive\Desktop\Library-Management-System-for-Desktop\LibraryApp"

pyinstaller --clean --noconfirm GPA_CO_LMS.spec

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================
    echo BUILD SUCCESSFUL!
    echo ============================================
    echo.
    echo Executable created at:
    echo %cd%\dist\GPA_CO_LMS.exe
    echo.
    dir /B "dist\GPA_CO_LMS.exe"
) else (
    echo.
    echo ============================================
    echo BUILD FAILED!
    echo ============================================
    echo Error Code: %ERRORLEVEL%
)

echo.
pause
