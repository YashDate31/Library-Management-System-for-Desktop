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
echo "C:\Users\Yash\OneDrive\Desktop\Library Management System\LibraryApp\dist\LibraryManagementSystem.exe"
echo.
echo You can now copy this .exe file to any Windows PC and run it directly!
echo No Python installation required on the target machine.
echo.
pause