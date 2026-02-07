import sqlite3
import os

db_path = r"C:\Users\Yash\OneDrive\Desktop\Library-Management-System-for-Desktop\LibraryApp\Web-Extension\portal.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check requests table data
print("First few rows from requests table:")
cursor.execute("SELECT req_id, created_at, status FROM requests LIMIT 3")
for row in cursor.fetchall():
    print(f"  req_id={row[0]}, created_at={row[1]}, status={row[2]}")

# Check deletion_requests table data
print("\nFirst few rows from deletion_requests table:")
cursor.execute("SELECT id, timestamp, status FROM deletion_requests LIMIT 3")
for row in cursor.fetchall():
    print(f"  id={row[0]}, timestamp={row[1]}, status={row[2]}")

# Try the actual query manually
print("\n\nTrying the actual query from request-history endpoint:")
try:
    query = """
        SELECT id as req_id, enrollment_no, request_type, details, status, created_at
        FROM requests
        WHERE status IN ('approved', 'rejected')
         AND created_at >= date('now', '-7 days')
        ORDER BY created_at DESC LIMIT 100
    """
    cursor.execute(query)
    results = cursor.fetchall()
    print(f"Query succeeded! Rows returned: {len(results)}")
except Exception as e:
    print(f"Query failed: {e}")

conn.close()
