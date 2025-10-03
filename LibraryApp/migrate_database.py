#!/usr/bin/env python3
"""
Database migration script to add academic_year column to borrow_records table
"""

import sqlite3
import os
import sys

def migrate_database():
    """Add academic_year column to borrow_records if it doesn't exist"""
    
    # Get database path
    if hasattr(sys, '_MEIPASS'):
        db_path = os.path.join(os.path.dirname(sys.executable), 'library.db')
    else:
        db_path = os.path.join(os.path.dirname(__file__), 'library.db')
    
    print(f"📂 Database path: {db_path}")
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if academic_year column exists
        cursor.execute("PRAGMA table_info(borrow_records)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'academic_year' not in columns:
            print("➕ Adding academic_year column to borrow_records table...")
            cursor.execute('ALTER TABLE borrow_records ADD COLUMN academic_year TEXT')
            conn.commit()
            print("✅ Successfully added academic_year column!")
        else:
            print("✅ academic_year column already exists!")
        
        # Check if promotion_history table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='promotion_history'")
        if not cursor.fetchone():
            print("➕ Creating promotion_history table...")
            cursor.execute('''
                CREATE TABLE promotion_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    enrollment_no TEXT NOT NULL,
                    student_name TEXT NOT NULL,
                    old_year TEXT NOT NULL,
                    new_year TEXT NOT NULL,
                    letter_number TEXT,
                    academic_year TEXT,
                    promotion_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (enrollment_no) REFERENCES students (enrollment_no)
                )
            ''')
            conn.commit()
            print("✅ Successfully created promotion_history table!")
        else:
            print("✅ promotion_history table already exists!")
        
        # Check if academic_years table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='academic_years'")
        if not cursor.fetchone():
            print("➕ Creating academic_years table...")
            cursor.execute('''
                CREATE TABLE academic_years (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    year_name TEXT UNIQUE NOT NULL,
                    start_date DATE,
                    end_date DATE,
                    is_active INTEGER DEFAULT 0,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            print("✅ Successfully created academic_years table!")
        else:
            print("✅ academic_years table already exists!")
        
        print("\n🎉 Database migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Database Migration Script")
    print("=" * 60)
    migrate_database()
