#!/usr/bin/env python3
"""
Inspect the actual database structure to find the column mapping issue
"""

import sys
import os
import sqlite3

def inspect_database():
    print("🔍 Database Structure Inspection")
    print("=" * 40)
    
    db_path = os.path.join(os.path.dirname(__file__), 'LibraryApp', 'library.db')
    print(f"Database path: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Get table schema
        cursor.execute("PRAGMA table_info(books)")
        columns = cursor.fetchall()
        
        print("\n📋 Books table structure:")
        for col in columns:
            print(f"  {col[0]}: {col[1]} ({col[2]}) - Nullable: {not col[3]} - Default: {col[4]}")
        
        # Get sample data with column names
        cursor.execute("SELECT * FROM books LIMIT 3")
        rows = cursor.fetchall()
        
        if rows:
            print("\n📚 Sample data with column mapping:")
            column_names = [desc[1] for desc in columns]
            
            for i, row in enumerate(rows, 1):
                print(f"\nBook {i}:")
                for j, (col_name, value) in enumerate(zip(column_names, row)):
                    print(f"  {col_name}: {value}")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    inspect_database()