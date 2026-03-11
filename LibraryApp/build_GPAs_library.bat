@echo off
REM ==============================================================================
REM GPA's Computer Departmental Library - EXE Build Script
REM ==============================================================================
REM This script builds a complete, bug-free executable for the Library Management System
REM Build Date: 2026-03-11
REM ==============================================================================

echo.
echo ================================================================================
echo   Building GPA's Computer Departmental Library EXE
echo ================================================================================
echo.
echo This will take 5-10 minutes depending on your system...
echo Please DO NOT close this window or interrupt the process!
echo.
echo [Step 1/6] Preparing build environment...
echo.

REM Navigate to LibraryApp directory
cd /d "c:\Users\Yash\OneDrive\Desktop\Library-Management-System-for-Desktop\LibraryApp"

REM Check if virtual environment is activated
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not available in PATH!
    echo Please ensure Python is installed and added to PATH.
    pause
    exit /b 1
)

echo [OK] Python is available
echo.
echo [Step 2/6] Verifying required files...
echo.

REM Check for required files
if not exist "main.py" (
    echo [ERROR] main.py not found!
    pause
    exit /b 1
)
echo [OK] main.py found

if not exist "logo.png" (
    echo [ERROR] logo.png not found!
    pause
    exit /b 1
)
echo [OK] logo.png found

if not exist "logo.ico" (
    echo [WARNING] logo.ico not found, creating it...
    python -c "from PIL import Image; img = Image.open('logo.png'); img.save('logo.ico')"
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to create logo.ico
        pause
        exit /b 1
    )
)
echo [OK] logo.ico ready

if not exist "library.db" (
    echo [WARNING] library.db not found - a new database will be created when you first run the EXE
)

if not exist "GPAs_Computer_departmental_library.spec" (
    echo [ERROR] GPAs_Computer_departmental_library.spec not found!
    pause
    exit /b 1
)
echo [OK] All required files verified
echo.

echo [Step 3/6] Checking PyInstaller installation...
echo.
python -c "import PyInstaller" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] PyInstaller not found, installing...
    pip install pyinstaller
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to install PyInstaller
        pause
        exit /b 1
    )
)
echo [OK] PyInstaller is ready
echo.

echo [Step 4/6] Cleaning previous build artifacts...
echo.
if exist "build" (
    rmdir /s /q build
    echo [OK] Removed old build directory
)
if exist "dist" (
    rmdir /s /q dist
    echo [OK] Removed old dist directory
)
if exist "__pycache__" (
    rmdir /s /q __pycache__
    echo [OK] Removed __pycache__
)
echo.

echo [Step 5/6] Building executable (this may take several minutes)...
echo.
echo *** PLEASE WAIT - DO NOT INTERRUPT ***
echo.

pyinstaller --clean --noconfirm GPAs_Computer_departmental_library.spec

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================================================
    echo   BUILD SUCCESSFUL!
    echo ================================================================================
    echo.
    echo [Step 6/6] Verifying build output...
    echo.
    
    if exist "dist\GPAs_Computer_departmental_library.exe" (
        echo [OK] Executable created successfully!
        echo.
        echo Location: %cd%\dist\GPAs_Computer_departmental_library.exe
        echo.
        
        REM Get file size
        for %%A in ("dist\GPAs_Computer_departmental_library.exe") do (
            set size=%%~zA
        )
        echo File size: %size% bytes
        echo.
        
        REM List the exe file details
        dir "dist\GPAs_Computer_departmental_library.exe" | findstr "GPAs_Computer_departmental_library.exe"
        echo.
        echo ================================================================================
        echo   IMPORTANT NOTES:
        echo ================================================================================
        echo.
        echo 1. The executable is located in the 'dist' folder
        echo 2. You can run it by double-clicking: GPAs_Computer_departmental_library.exe
        echo 3. The EXE includes ALL features:
        echo    - Complete Library Management System
        echo    - Student Portal (Web Extension)
        echo    - Email notifications
        echo    - Analytics and reporting
        echo    - Export to Excel, Word, and PDF
        echo    - QR code generation
        echo.
        echo 4. First-time users will need to login with:
        echo    Username: gpa
        echo    Password: gpa123
        echo.
        echo 5. The database (library.db) and configuration files must be in the 
        echo    same folder as the EXE when you run it.
        echo.
        echo Enjoy your Library Management System!
        echo.
        echo ================================================================================
        
    ) else (
        echo [ERROR] Executable was not created!
        echo Build process completed but no EXE file found.
        echo Please check the build output above for errors.
    )
) else (
    echo.
    echo ================================================================================
    echo   BUILD FAILED!
    echo ================================================================================
    echo.
    echo Error Code: %ERRORLEVEL%
    echo.
    echo Please check the error messages above and try again.
    echo Common issues:
    echo   - Missing dependencies (run: pip install -r requirements.txt)
    echo   - Insufficient disk space
    echo   - Antivirus blocking PyInstaller
    echo.
    echo If you need help, check the build log in: build/GPAs_Computer_departmental_library/
    echo.
)

echo.
pause
