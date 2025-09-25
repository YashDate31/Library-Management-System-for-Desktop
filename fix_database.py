#!/usr/bin/env python3
"""
Fix the books database - correct the category field issue
"""

import sys
import os

# Add the LibraryApp directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'LibraryApp'))

from database import Database
import sqlite3

def fix_books_database():
    print("🔧 Fixing Books Database - Category Field Issue")
    print("=" * 60)
    
    # Initialize database
    db = Database()
    
    # Get current books
    all_books = db.get_books()
    print(f"📚 Current books in database: {len(all_books)}")
    
    if all_books:
        print("\n📋 Current books (before fix):")
        for i, book in enumerate(all_books, 1):
            print(f"{i}. ID: {book[1]} | Title: {book[2]} | Author: {book[3]} | Category: {book[4]}")
    
    # Clear existing books and add correct sample data
    conn = db.get_connection()
    cursor = conn.cursor()
    
    try:
        print("\n🗑️ Clearing existing books...")
        cursor.execute('DELETE FROM books')
        
        print("➕ Adding corrected sample books...")
        # Correct sample books with proper categories
        sample_books = [
            ('B001', 'Introduction to Programming', 'John Smith', '978-0123456789', 'Technology', 5, 5),
            ('B002', 'Database Systems', 'Mary Johnson', '978-0987654321', 'Technology', 3, 3),
            ('B003', 'Engineering Mathematics', 'Robert Brown', '978-0456789123', 'Textbook', 4, 4),
            ('B004', 'Data Structures', 'Alice Wilson', '978-0789123456', 'Technology', 2, 2),
            ('B005', 'Computer Networks', 'David Miller', '978-0321456789', 'Technology', 3, 3),
            ('B006', 'Software Engineering', 'Sarah Davis', '978-0654321987', 'Textbook', 4, 4),
            ('B007', 'Machine Learning Research', 'Dr. Kumar', '978-0987123456', 'Research', 2, 2),
            ('B008', 'AI Fundamentals', 'Prof. Singh', '978-0456987123', 'Textbook', 3, 3),
        ]
        
        for book in sample_books:
            cursor.execute('''
                INSERT INTO books (book_id, title, author, isbn, category, total_copies, available_copies)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', book)
        
        conn.commit()
        print(f"✅ Added {len(sample_books)} books successfully!")
        
        # Verify the fix
        new_books = db.get_books()
        print(f"\n📚 Books after fix: {len(new_books)}")
        
        if new_books:
            print("\n📋 Fixed books:")
            for i, book in enumerate(new_books, 1):
                print(f"{i}. ID: {book[1]} | Title: {book[2]} | Author: {book[3]} | Category: {book[4]}")
        
        # Check filtered books (Computer department categories)
        computer_categories = ["Technology", "Textbook", "Research"]
        filtered_books = [b for b in new_books if b[4] in computer_categories]
        
        print(f"\n🎯 Books in Computer categories {computer_categories}: {len(filtered_books)}")
        
        if filtered_books:
            print("\n✅ Filtered books (what will show in UI):")
            for i, book in enumerate(filtered_books, 1):
                print(f"{i}. ID: {book[1]} | Title: {book[2]} | Category: {book[4]}")
        
        print("\n🎉 Database fix completed successfully!")
        print("The books list should now show items properly in the application.")
        
    except Exception as e:
        print(f"❌ Error fixing database: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_books_database()