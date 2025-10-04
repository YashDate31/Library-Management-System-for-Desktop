"""
Add 20 Academic Years to the database
Academic Year runs from July to June
"""

import sqlite3
from datetime import datetime

# Get database connection
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create academic_years table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS academic_years (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year_name TEXT UNIQUE NOT NULL,
        is_active INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Generate 20 academic years starting from 2020-2021
# Academic year runs from July to June
academic_years = []
start_year = 2020
for i in range(20):
    year_start = start_year + i
    year_end = year_start + 1
    year_name = f"{year_start}-{year_end}"
    academic_years.append(year_name)

print("Adding 20 Academic Years to the database...")
print("Academic Year Period: July to June")
print("=" * 50)

added_count = 0
existing_count = 0

for year_name in academic_years:
    try:
        cursor.execute('''
            INSERT INTO academic_years (year_name, is_active)
            VALUES (?, 0)
        ''', (year_name,))
        print(f"✅ Added: {year_name}")
        added_count += 1
    except sqlite3.IntegrityError:
        print(f"⚠️  Already exists: {year_name}")
        existing_count += 1

# Set current academic year as active (2025-2026 for October 2025)
# Academic year 2025-2026 runs from July 2025 to June 2026
current_year = "2025-2026"
cursor.execute('UPDATE academic_years SET is_active = 0')  # Deactivate all
cursor.execute('UPDATE academic_years SET is_active = 1 WHERE year_name = ?', (current_year,))

conn.commit()
conn.close()

print("=" * 50)
print(f"\n✅ Successfully added {added_count} new academic years")
print(f"⚠️  {existing_count} academic years already existed")
print(f"\n🎓 Current Active Academic Year: {current_year}")
print(f"   Period: July 2025 to June 2026")
print("\n📚 All Academic Years in Database:")
print("-" * 50)

# Display all years
conn = sqlite3.connect('library.db')
cursor = conn.cursor()
cursor.execute('SELECT year_name, is_active FROM academic_years ORDER BY year_name')
years = cursor.fetchall()
for year_name, is_active in years:
    status = "✅ ACTIVE" if is_active else "  "
    year_start, year_end = year_name.split('-')
    print(f"{status} {year_name} (July {year_start} - June {year_end})")
conn.close()

print("-" * 50)
print("\n🎉 Academic years setup complete!")
print("\n📝 Important Notes:")
print("   • Academic year runs from JULY to JUNE")
print("   • Example: 2025-2026 = July 2025 to June 2026")
print("   • Promote students at end of June each year")
print("   • New academic year starts in July")
