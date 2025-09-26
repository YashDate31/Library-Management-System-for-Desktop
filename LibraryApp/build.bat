@echo off
echo Building Library Management System...
echo.

REM Navigate to the app directory
cd /d "C:\Users\Yash\OneDrive\Desktop\Library Management System\LibraryApp"

REM Activate virtual environment and build the executable
"C:/Users/Yash/OneDrive/Desktop/Library Management System/.venv/Scripts/python.exe" -m PyInstaller "C:/Users/Yash/OneDrive/Desktop/Library Management System/LibraryApp/build_app.spec"

echo.
echo Build complete! 
echo.
echo The executable file is located at:
set "OUT_EXE=C:\Users\Yash\OneDrive\Desktop\Library Management System\LibraryApp\dist\LibraryManagementSystem_v5.0_FINAL.exe"
if exist "%OUT_EXE%" (
	echo "%OUT_EXE%"
	echo.
	echo Tip: Create a shortcut to this EXE for quick launches.
 ) else (
	echo Could not find the expected EXE at:
	echo   "%OUT_EXE%"
	echo If the build used a different spec/name, check the dist folder for the generated file.
 )
echo.
echo You can now copy this .exe file to any Windows PC and run it directly!
echo No Python installation required on the target machine.
echo.
pause