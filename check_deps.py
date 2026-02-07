#!/usr/bin/env python3
"""
Quick Installation & Dependency Verification
"""

import subprocess
import sys
import os

def verify_critical_packages():
    """Verify that critical packages are installed"""
    packages = {
        'reportlab': 'reportlab',
        'psycopg2': 'psycopg2',
        'matplotlib': 'matplotlib',
        'pandas': 'pandas',
        'flask': 'flask',
        'pillow': 'PIL',  # Pillow is imported as PIL
        'qrcode': 'qrcode',
        'xlsxwriter': 'xlsxwriter',
        'tkcalendar': 'tkcalendar',
        'sqlalchemy': 'sqlalchemy',
        'dotenv': 'dotenv'
    }
    
    print("\n=== DEPENDENCY CHECK ===\n")
    
    all_ok = True
    for pkg_name, import_name in packages.items():
        try:
            __import__(import_name)
            print(f"[OK] {pkg_name}")
        except ImportError:
            print(f"[MISSING] {pkg_name}")
            all_ok = False
    
    return all_ok

if __name__ == "__main__":
    print("=" * 50)
    print("Library Management System - Dependency Checker")
    print("=" * 50)
    
    if verify_critical_packages():
        print("\n✅ All dependencies are installed!")
        print("\nTo start the application:")
        print("  cd LibraryApp")
        print("  python main.py")
    else:
        print("\n⚠️ Some dependencies are missing!")
        print("\nTo fix, run:")
        print("  pip install -r requirements.txt --no-cache-dir")
        sys.exit(1)
