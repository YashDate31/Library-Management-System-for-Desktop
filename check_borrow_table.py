import sqlite3

conn = sqlite3.connect('LibraryApp/library.db')
cursor = conn.cursor()

# Get borrow_records table structure
cursor.execute("PRAGMA table_info(borrow_records)")
columns = cursor.fetchall()

print("borrow_records table structure:")
for col in columns:
    print(f"  - {col[1]} ({col[2]})")

print("\nChecking for data in borrow_records:")
cursor.execute("SELECT * FROM borrow_records")
records = cursor.fetchall()
print(f"Found {len(records)} records")

if records:
    print("\nFirst record raw values:")
    for i, val in enumerate(records[0]):
        col_name = columns[i][1] if i < len(columns) else f"col_{i}"
        print(f"  [{i}] {col_name} = {val} (type: {type(val).__name__})")

conn.close()
