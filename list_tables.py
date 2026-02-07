import sqlite3

conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("All tables in database:")
for table in tables:
    print(f"  - {table[0]}")

conn.close()
