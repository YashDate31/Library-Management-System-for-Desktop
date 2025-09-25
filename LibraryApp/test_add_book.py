#!/usr/bin/env python3
"""
Test script to verify book adding functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import Database
import sqlite3

def test_add_book():
    """Test adding a book and verify it's stored correctly"""
    print("🧪 Testing book adding functionality...")
    
    # Initialize database
    db = Database()
    
    # Test book data
    test_book = {
        'book_id': 'TEST001',
        'title': 'Test Book for Debugging',
        'author': 'Test Author',
        'isbn': '123-456-789',
        'category': 'Technology',
        'total_copies': 5
    }
    
    print(f"📚 Adding test book: {test_book['title']}")
    
    # Add the book
    success, message = db.add_book(
        test_book['book_id'],
        test_book['title'],
        test_book['author'],
        test_book['isbn'],
        test_book['category'],
        test_book['total_copies']
    )
    
    print(f"Result: {success} - {message}")
    
    if success:
        # Verify the book was actually added
        print("🔍 Verifying book was added to database...")
        books = db.get_books()
        
        # Look for our test book
        test_book_found = False
        for book in books:
            if book[1] == test_book['book_id']:  # book_id is at index 1
                test_book_found = True
                print(f"✅ Book found in database:")
                print(f"   ID: {book[1]}")
                print(f"   Title: {book[2]}")
                print(f"   Author: {book[3]}")
                print(f"   ISBN: {book[4]}")
                print(f"   Category: {book[5]}")
                print(f"   Total Copies: {book[6]}")
                print(f"   Available: {book[7]}")
                break
        
        if not test_book_found:
            print("❌ Book was not found in database despite success message!")
        
        # Clean up - remove test book
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE book_id = ?", (test_book['book_id'],))
        conn.commit()
        conn.close()
        print("🧹 Test book removed from database")
    
    return success

def check_database_state():
    """Check current database state"""
    print("\n📊 Current database state:")
    
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        # Count total books
        cursor.execute("SELECT COUNT(*) FROM books")
        total_books = cursor.fetchone()[0]
        print(f"   Total books: {total_books}")
        
        # Count by category
        cursor.execute("SELECT category, COUNT(*) FROM books GROUP BY category")
        categories = cursor.fetchall()
        for cat, count in categories:
            print(f"   {cat}: {count} books")
        
        # Show last 3 books added
        cursor.execute("SELECT book_id, title, category FROM books ORDER BY id DESC LIMIT 3")
        recent_books = cursor.fetchall()
        print("\n   Most recent books:")
        for book in recent_books:
            print(f"   • {book[0]}: {book[1]} ({book[2]})")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")

def main():
    print("🔧 Book Adding Debug Test")
    print("=" * 50)
    
    # Check current state
    check_database_state()
    
    print("\n" + "=" * 50)
    
    # Test adding functionality
    success = test_add_book()
    
    print("\n" + "=" * 50)
    
    if success:
        print("✅ Book adding functionality is working correctly!")
        print("💡 If books aren't showing in UI, the issue is in the refresh logic.")
    else:
        print("❌ Book adding functionality has issues!")
        print("💡 Check database permissions and integrity.")

if __name__ == "__main__":
    main()