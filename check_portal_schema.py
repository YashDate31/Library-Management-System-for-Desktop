import sqlite3
import os

# Check portal.db
db_path = r"C:\Users\Yash\OneDrive\Desktop\Library-Management-System-for-Desktop\LibraryApp\Web-Extension\portal.db"
print(f"Checking {db_path}")
print(f"File exists: {os.path.exists(db_path)}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("All tables in portal.db:")
for table in tables:
    print(f"  - {table[0]}")

# Check requests table schema
if any(t[0] == 'requests' for t in tables):
    cursor.execute("PRAGMA table_info(requests)")
    rows = cursor.fetchall()
    print("\nRequests table schema:")
    for row in rows:
        print(f"  Column {row[1]}: type={row[2]}")
else:
    print("\nRequests table does NOT exist")

# Check deletion_requests table schema
if any(t[0] == 'deletion_requests' for t in tables):
    cursor.execute("PRAGMA table_info(deletion_requests)")
    rows = cursor.fetchall()
    print("\nDeletion_requests table schema:")
    for row in rows:
        print(f"  Column {row[1]}: type={row[2]}")
else:
    print("\nDeletion_requests table does NOT exist")

conn.close()
