#!/usr/bin/env python3
"""
Installation & Dependency Verification Script
Ensures all required packages are installed and working
"""

import subprocess
import sys
import os

def check_python_version():
    """Verify Python 3.8+ is installed"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"[ERROR] Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"[OK] Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """Install all required packages from requirements.txt"""
    print("\n[INFO] Installing dependencies from requirements.txt...")
    
    try:
        # Install from root requirements.txt
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "-r", "requirements.txt",
            "--no-cache-dir",
            "-q"
        ])
        print("[OK] Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to install dependencies: {e}")
        return False

def verify_critical_packages():
    """Verify that critical packages are installed and importable"""
    critical_packages = {
        'reportlab': 'PDF generation',
        'psycopg2': 'PostgreSQL connection',
        'matplotlib': 'Dashboard charts',
        'pandas': 'Data analysis & Excel',
        'flask': 'Web server',
        'pillow': 'Image processing',
        'qrcode': 'QR code generation',
        'xlsxwriter': 'Excel export',
        'tkcalendar': 'Calendar widget',
        'sqlalchemy': 'ORM support',
        'python_dotenv': 'Environment config',
    }
    
    print("\n[INFO] Verifying critical packages...")
    all_ok = True
    
    for package, description in critical_packages.items():
        try:
            __import__(package)
            print(f"  [OK] {package:20} - {description}")
        except ImportError as e:
            print(f"  [ERROR] {package:20} - MISSING ({description})")
            all_ok = False
    
    return all_ok

def check_database_files():
    """Check for database files"""
    print("\n[INFO] Checking database files...")
    db_path = os.path.join(os.path.dirname(__file__), 'LibraryApp', 'library.db')
    
    if os.path.exists(db_path):
        size = os.path.getsize(db_path)
        print(f"  [OK] library.db found ({size:,} bytes)")
    else:
        print(f"  [INFO] library.db not found (will be created on first run)")

def check_environment():
    """Check for environment variables"""
    print("\n[INFO] Checking environment configuration...")
    
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        # Mask password for security
        masked = database_url.replace(
            database_url[database_url.find(':')+1:database_url.find('@')],
            '***:****'
        )
        print(f"  [OK] DATABASE_URL configured: {masked[:60]}...")
    else:
        print(f"  [INFO] DATABASE_URL not set (will use local SQLite only)")

def main():
    """Main installation verification routine"""
    print("=" * 70)
    print(" Library Management System - Installation Verification")
    print("=" * 70)
    
    # Step 1: Check Python version
    if not check_python_version():
        print("\n[ERROR] Python version check failed!")
        sys.exit(1)
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("\n[ERROR] Dependency installation failed!")
        print("Try running: pip install -r requirements.txt --no-cache-dir")
        sys.exit(1)
    
    # Step 3: Verify critical packages
    if not verify_critical_packages():
        print("\n[ERROR] Some critical packages are missing!")
        print("Try running: pip install -r requirements.txt --force-reinstall")
        sys.exit(1)
    
    # Step 4: Check database
    check_database_files()
    
    # Step 5: Check environment
    check_environment()
    
    # Success message
    print("\n" + "=" * 70)
    print(" [OK] Installation verification completed successfully!")
    print("=" * 70)
    print("\nYou can now run the application:")
    print("  cd LibraryApp")
    print("  python main.py")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
