#!/usr/bin/env python3
"""
Script to set 2025-2026 as the active academic year
"""

from database import Database

def set_active_year():
    """Set 2025-2026 as active year"""
    db = Database()
    
    print("📅 Setting 2025-2026 as active academic year...")
    print("=" * 50)
    
    # Set 2025-2026 as active
    success, message = db.create_academic_year("2025-2026")
    
    if success:
        print(f"✅ SUCCESS: {message}")
    else:
        print(f"⚠️  {message}")
    
    # Verify
    active_year = db.get_active_academic_year()
    print(f"\n✅ Current Active Year: {active_year}")
    
    print("\n" + "=" * 50)
    print("📅 All Academic Years in Database:")
    print("-" * 50)
    years = db.get_all_academic_years()
    
    for year in years:
        status = " ✅ ACTIVE" if year == active_year else ""
        print(f"   {year}{status}")
    
    print(f"\n📊 Total academic years: {len(years)}")

if __name__ == "__main__":
    set_active_year()
