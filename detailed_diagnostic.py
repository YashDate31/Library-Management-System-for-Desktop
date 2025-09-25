#!/usr/bin/env python3
"""
Detailed column mapping diagnostic
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'LibraryApp'))

from database import Database

def detailed_diagnostic():
    print("🔍 Detailed Column Mapping Diagnostic")
    print("=" * 50)
    
    db = Database()
    
    # Get raw data from database method
    books = db.get_books()
    
    print(f"📚 Books returned by get_books(): {len(books)}")
    
    if books:
        print("\n📋 Raw data structure (first book):")
        first_book = books[0]
        print(f"Book tuple length: {len(first_book)}")
        
        for i, value in enumerate(first_book):
            print(f"  Index {i}: {value}")
        
        print("\n📋 All books with detailed column info:")
        for i, book in enumerate(books, 1):
            print(f"\nBook {i}:")
            print(f"  Index 0 (ID): {book[0]}")
            print(f"  Index 1 (Book ID): {book[1]}")
            print(f"  Index 2 (Title): {book[2]}")
            print(f"  Index 3 (Author): {book[3]}")
            print(f"  Index 4 (Should be ISBN): {book[4]}")
            print(f"  Index 5 (Should be Category): {book[5] if len(book) > 5 else 'MISSING'}")
            print(f"  Index 6 (Should be Total Copies): {book[6] if len(book) > 6 else 'MISSING'}")
            print(f"  Index 7 (Should be Available Copies): {book[7] if len(book) > 7 else 'MISSING'}")
            
            if i >= 3:  # Show only first 3 for brevity
                break

if __name__ == "__main__":
    detailed_diagnostic()