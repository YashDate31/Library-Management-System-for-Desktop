#!/usr/bin/env python3
"""
Diagnostic Script for Library Management System
This script will help diagnose the empty books list issue
"""

import sys
import os

# Add the LibraryApp directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'LibraryApp'))

from database import Database

def diagnose_books_issue():
    print("🔍 Library Management System - Books Diagnosis")
    print("=" * 50)
    
    # Initialize database
    db = Database()
    
    # Get all books from database
    all_books = db.get_books()
    print(f"\n📚 Total books in database: {len(all_books)}")
    
    if all_books:
        print("\n📋 All books in database:")
        for i, book in enumerate(all_books, 1):
            print(f"{i}. ID: {book[1]} | Title: {book[2]} | Author: {book[3]} | Category: {book[5]}")
    
    # Check filtered books (Computer department categories)
    computer_categories = ["Technology", "Textbook", "Research"]
    filtered_books = [b for b in all_books if b[5] in computer_categories]
    
    print(f"\n🎯 Books in Computer categories {computer_categories}: {len(filtered_books)}")
    
    if filtered_books:
        print("\n✅ Filtered books (what should show in UI):")
        for i, book in enumerate(filtered_books, 1):
            print(f"{i}. ID: {book[1]} | Title: {book[2]} | Category: {book[5]}")
    else:
        print("\n❌ No books found in Computer categories!")
        print("This explains why the books list appears empty.")
        
        if all_books:
            print("\n💡 Available categories in database:")
            categories = set(book[5] for book in all_books)
            for category in sorted(categories):
                print(f"   - {category}")
            
            print(f"\n🔧 Solution: Add books with categories: {', '.join(computer_categories)}")
    
    print("\n" + "=" * 50)
    print("Diagnosis complete!")

if __name__ == "__main__":
    diagnose_books_issue()