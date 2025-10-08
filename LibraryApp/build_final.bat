@echo off
echo ========================================
echo Building: Library of Computer department
echo ========================================
echo.

REM Activate virtual environment if it exists
if exist .venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
) else if exist ..\\.venv\Scripts\activate.bat (
    echo Activating parent virtual environment...

.000000
.00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222)...22
2
22222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222
...................................................................................................................................................................................................................................................................................................................................................................................................................................e2+
.+
\zcho.
echo Cleaning previous build files...
if exist "dist\Library of Computer department.exe" del "dist\Library of Computer department.exe"
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo Building executable with PyInstaller...
pyinstaller --clean build_final.spec

echo.
if exist "dist\Library of Computer department.exe" (
    echo ========================================
    echo BUILD SUCCESSFUL!
    echo ========================================
    echo.
    echo Executable created at:
    echo dist\Library of Computer department.exe
    echo.
    echo File size:
    dir "dist\Library of Computer department.exe" | find "Library of Computer department.exe"
    echo.
    echo You can now run: dist\"Library of Computer department.exe"
) else (
    echo ========================================
    echo BUILD FAILED!
    echo ========================================
    echo Please check the output above for errors.
)

echo.
pause
