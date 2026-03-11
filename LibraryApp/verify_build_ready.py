#!/usr/bin/env python3
"""
Pre-Build Verification Script
Checks all dependencies and files are ready before building the EXE
"""

import sys
import os
from pathlib import Path

def check_module(module_name, package_name=None):
    """Check if a module can be imported"""
    if package_name is None:
        package_name = module_name
    try:
        __import__(module_name)
        print(f"  [OK] {package_name}")
        return True
    except ImportError as e:
        print(f"  [MISSING] {package_name} - {e}")
        return False

def main():
    print("=" * 80)
    print("Pre-Build Verification for GPA's Computer Departmental Library")
    print("=" * 80)
    print()
    
    # Check Python version
    print(f"Python Version: {sys.version}")
    if sys.version_info < (3, 7):
        print("[ERROR] Python 3.7 or higher is required!")
        return False
    print("[OK] Python version is compatible")
    print()
    
    # Check required files
    print("Checking required files...")
    required_files = [
        'main.py',
        'database.py',
        'database_pool.py',
        'email_batch_service.py',
        'sync_manager.py',
        'config_manager.py',
        'autocomplete_widget.py',
        'login_loader.py',
        'logo.png',
        'GPAs_Computer_departmental_library.spec',
    ]
    
    files_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  [OK] {file}")
        else:
            print(f"  [MISSING] {file}")
            files_ok = False
    
    if not files_ok:
        print("\n[ERROR] Some required files are missing!")
        return False
    
    print()
    
    # Check required Python packages
    print("Checking required Python packages...")
    packages = [
        ('tkinter', 'tkinter (GUI)'),
        ('pandas', 'pandas'),
        ('openpyxl', 'openpyxl'),
        ('docx', 'python-docx'),
        ('tkcalendar', 'tkcalendar'),
        ('matplotlib', 'matplotlib'),
        ('xlsxwriter', 'xlsxwriter'),
        ('PIL', 'Pillow'),
        ('flask', 'Flask'),
        ('qrcode', 'qrcode'),
        ('waitress', 'waitress'),
        ('requests', 'requests'),
        ('psycopg2', 'psycopg2-binary'),
        ('dotenv', 'python-dotenv'),
        ('reportlab', 'reportlab'),
        ('PyInstaller', 'pyinstaller'),
    ]
    
    packages_ok = True
    for module, name in packages:
        if not check_module(module, name):
            packages_ok = False
    
    print()
    
    if not packages_ok:
        print("[WARNING] Some packages are missing!")
        print("\nTo install all required packages, run:")
        print("  pip install -r requirements.txt")
        print()
        response = input("Do you want to continue anyway? (y/n): ")
        if response.lower() != 'y':
            return False
    
    # Check Web-Extension files
    print("Checking Web-Extension files...")
    web_files = [
        'Web-Extension/student_portal.py',
        'Web-Extension/run_waitress_portal.py',
        'Web-Extension/frontend/dist/index.html',
    ]
    
    web_ok = True
    for file in web_files:
        if os.path.exists(file):
            print(f"  [OK] {file}")
        else:
            print(f"  [MISSING] {file}")
            web_ok = False
    
    if not web_ok:
        print("\n[WARNING] Some Web-Extension files are missing!")
        print("The Student Portal feature may not work in the EXE.")
    
    print()
    
    # Final verdict
    if files_ok and packages_ok and web_ok:
        print("=" * 80)
        print("[SUCCESS] All checks passed! Ready to build the EXE.")
        print("=" * 80)
        print("\nRun the build script: build_GPAs_library.bat")
        print()
        return True
    elif files_ok:
        print("=" * 80)
        print("[WARNING] Some optional components are missing, but build can proceed.")
        print("=" * 80)
        print()
        return True
    else:
        print("=" * 80)
        print("[ERROR] Critical files are missing. Cannot build EXE.")
        print("=" * 80)
        print()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
