#!/usr/bin/env python3
"""
Script to add academic year 2025-2026 to the database
"""

from database import Database

def add_academic_year():
    """Add academic year 2025-2026"""
    db = Database()
    
    # Create academic year 2025-2026
    success, message = db.create_academic_year("2025-2026")
    
    if success:
        print(f"✅ SUCCESS: {message}")
        print(f"Academic year '2025-2026' has been added and set as active.")
    else:
        print(f"❌ ERROR: {message}")
    
    # Show all academic years
    years = db.get_all_academic_years()
    print(f"\n📅 All Academic Years in Database:")
    for year in years:
        active_year = db.get_active_academic_year()
        status = "✅ ACTIVE" if year == active_year else ""
        print(f"   - {year} {status}")

if __name__ == "__main__":
    add_academic_year()
