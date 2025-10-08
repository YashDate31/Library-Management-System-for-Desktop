#!/usr/bin/env python3
"""
Script to add the next 15 academic years to the database
"""

from database import Database

def add_15_academic_years():
    """Add the next 15 academic years starting from 2026-2027"""
    db = Database()
    
    # Current year is 2025-2026, so start from 2026
    start_year = 2026
    years_to_add = 15
    
    print("📅 Adding next 15 academic years...")
    print("=" * 50)
    
    added_count = 0
    skipped_count = 0
    
    for i in range(years_to_add):
        year = start_year + i
        academic_year = f"{year}-{year + 1}"
        
        success, message = db.create_academic_year(academic_year)
        
        if success:
            print(f"✅ {academic_year}: {message}")
            added_count += 1
        else:
            print(f"⚠️  {academic_year}: {message}")
            skipped_count += 1
    
    print("\n" + "=" * 50)
    print(f"✅ Successfully added: {added_count} years")
    print(f"⚠️  Skipped (already exist): {skipped_count} years")
    
    # Show all academic years
    print("\n📅 All Academic Years in Database:")
    print("-" * 50)
    years = db.get_all_academic_years()
    active_year = db.get_active_academic_year()
    
    for year in years:
        status = " ✅ ACTIVE" if year == active_year else ""
        print(f"   {year}{status}")
    
    print(f"\n📊 Total academic years: {len(years)}")

if __name__ == "__main__":
    add_15_academic_years()
