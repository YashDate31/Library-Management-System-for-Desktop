import sqlite3

conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Check requests table schema
cursor.execute("PRAGMA table_info(requests)")
rows = cursor.fetchall()
print("Requests table schema:")
for row in rows:
    print(f"  Column {row[1]}: type={row[2]}")

# Check deletion_requests table schema
cursor.execute("PRAGMA table_info(deletion_requests)")
rows = cursor.fetchall()
print("\nDeletion_requests table schema:")
for row in rows:
    print(f"  Column {row[1]}: type={row[2]}")

conn.close()
