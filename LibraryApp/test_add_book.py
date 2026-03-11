"""
Quick Test Script: Add a Test Book to Verify Database Sync
This script adds a test book to library.db and checks if it appears in the portal.
"""

import sqlite3
import os
from datetime import datetime

# Get the path to library.db
db_path = 'library.db'

print("=" * 70)
print("DATABASE SYNC TEST - Adding Test Book")
print("=" * 70)
print()

# Connect to database
print(f"[1] Connecting to database: {os.path.abspath(db_path)}")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create a test book
test_book_id = f"TEST_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
test_title = f"Test Book - Portal Sync Test {datetime.now().strftime('%H:%M:%S')}"
test_author = "Test Author"
test_category = "Testing"

print(f"[2] Adding test book:")
print(f"    Book ID: {test_book_id}")
print(f"    Title: {test_title}")
print(f"    Author: {test_author}")
print()

try:
    # Add the test book
    cursor.execute('''
        INSERT INTO books (book_id, title, author, isbn, category, total_copies, available_copies)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (test_book_id, test_title, test_author, '', test_category, 5, 5))
    
    conn.commit()
    print("[3] ✅ Test book added successfully!")
    print()
    
    # Verify it's in the database
    cursor.execute("SELECT COUNT(*) FROM books WHERE book_id = ?", (test_book_id,))
    count = cursor.fetchone()[0]
    
    if count > 0:
        print(f"[4] ✅ Verified: Test book exists in database")
    else:
        print(f"[4] ❌ ERROR: Test book not found after insertion!")
    
    print()
    
    # Show all books count
    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]
    print(f"[5] Total books in database: {total_books}")
    print()
    
    # Show recent books
    print("[6] Recent books in database:")
    cursor.execute("SELECT book_id, title, author FROM books ORDER BY book_id DESC LIMIT 5")
    books = cursor.fetchall()
    
    if books:
        for b in books:
            print(f"    - {b[0]}: {b[1]} by {b[2]}")
    else:
        print("    (No books found)")
    
    print()
    print("=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print()
    print("1. If the Student Portal is running, RESTART it now")
    print("   (Stop the portal server and start it again)")
    print()
    print("2. Open the Student Portal in your browser:")
    print("   http://localhost:5000")
    print()
    print("3. Navigate to the Books section")
    print()
    print("4. You should see the test book:")
    print(f"   '{test_title}'")
    print()
    print("5. If you DON'T see it:")
    print("   a. Check the portal logs for errors")
    print("   b. Visit: http://localhost:5000/api/debug/database")
    print("   c. This will show database info and book count")
    print()
    print("=" * 70)
    
except sqlite3.IntegrityError as e:
    print(f"[ERROR] Book ID already exists: {e}")
    print("This is okay - it means a test book was added before.")
except Exception as e:
    print(f"[ERROR] Failed to add test book: {e}")
    import traceback
    traceback.print_exc()
finally:
    conn.close()
    print()
    print("Test completed!")
