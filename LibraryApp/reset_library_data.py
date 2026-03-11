"""
Complete Library System Data Reset Script
This script will clear ALL data and make the system brand new.
USE WITH CAUTION - This deletes everything!
"""

import os
import shutil
import json
import sqlite3
from pathlib import Path

def clear_all_data():
    """Reset library system to brand new state"""
    
    # Get the script's directory
    script_dir = Path(__file__).parent
    web_extension_dir = script_dir / 'Web-Extension'
    
    print("=" * 60)
    print("LIBRARY SYSTEM COMPLETE RESET")
    print("=" * 60)
    print("\nThis will DELETE ALL data including:")
    print("  - All books and students")
    print("  - All issue/return records")
    print("  - Email history")
    print("  - Uploaded photos and study materials")
    print("  - All logs and sync data")
    print("=" * 60)
    
    response = input("\nAre you SURE you want to continue? (type 'YES' to confirm): ")
    if response != 'YES':
        print("\n❌ Reset cancelled.")
        return
    
    print("\n🔄 Starting complete data reset...\n")
    
    # Step 1: Delete main library database
    library_db = script_dir / 'library.db'
    if library_db.exists():
        try:
            library_db.unlink()
            print("✅ Deleted main library database (library.db)")
        except Exception as e:
            print(f"⚠️  Could not delete library.db: {e}")
    
    # Step 2: Delete portal database
    portal_db = web_extension_dir / 'portal.db'
    if portal_db.exists():
        try:
            portal_db.unlink()
            print("✅ Deleted web portal database (portal.db)")
        except Exception as e:
            print(f"⚠️  Could not delete portal.db: {e}")
    
    # Step 3: Clear email history
    email_history = script_dir / 'email_history.json'
    if email_history.exists():
        try:
            with open(email_history, 'w', encoding='utf-8') as f:
                json.dump([], f)
            print("✅ Cleared email history")
        except Exception as e:
            print(f"⚠️  Could not clear email_history.json: {e}")
    
    # Step 4: Clear sync log
    sync_log = script_dir / 'sync_log.json'
    if sync_log.exists():
        try:
            with open(sync_log, 'w', encoding='utf-8') as f:
                json.dump({"last_sync": None, "status": "ready"}, f, indent=4)
            print("✅ Cleared sync log")
        except Exception as e:
            print(f"⚠️  Could not clear sync_log.json: {e}")
    
    # Step 5: Clear uploaded files
    uploads_dir = web_extension_dir / 'uploads'
    
    # Clear registration photos
    photos_dir = uploads_dir / 'registration_photos'
    if photos_dir.exists():
        try:
            for file in photos_dir.iterdir():
                if file.is_file():
                    file.unlink()
            print("✅ Cleared all registration photos")
        except Exception as e:
            print(f"⚠️  Could not clear registration photos: {e}")
    
    # Clear study materials
    materials_dir = uploads_dir / 'study_materials'
    if materials_dir.exists():
        try:
            for file in materials_dir.iterdir():
                if file.is_file():
                    file.unlink()
            print("✅ Cleared all study materials")
        except Exception as e:
            print(f"⚠️  Could not clear study materials: {e}")
    
    # Step 6: Clear log files
    log_files = [
        web_extension_dir / 'portal_errors.log',
        web_extension_dir / 'waitress_portal_stderr.log',
        web_extension_dir / 'waitress_portal_stdout.log'
    ]
    
    for log_file in log_files:
        if log_file.exists():
            try:
                with open(log_file, 'w', encoding='utf-8') as f:
                    f.write('')
                print(f"✅ Cleared {log_file.name}")
            except Exception as e:
                print(f"⚠️  Could not clear {log_file.name}: {e}")
    
    # Step 7: Reinitialize databases
    print("\n🔄 Reinitializing fresh databases...\n")
    
    try:
        # Import and create fresh database
        from database import Database
        
        print("Creating fresh local database...")
        db = Database(force_local=True)
        print("✅ Fresh local database created")
        
        # Create fresh portal database if web extension exists
        if web_extension_dir.exists():
            portal_db_path = web_extension_dir / 'portal.db'
            print("Creating fresh portal database...")
            
            # Create portal database with same schema
            conn = sqlite3.connect(portal_db_path)
            cursor = conn.cursor()
            
            # Create tables (basic schema)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    enrollment_no INTEGER UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    email TEXT,
                    phone TEXT,
                    department TEXT,
                    year INTEGER,
                    semester INTEGER,
                    photo_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT,
                    isbn TEXT UNIQUE,
                    category TEXT,
                    quantity INTEGER DEFAULT 1,
                    available_quantity INTEGER DEFAULT 1,
                    location TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS issued_books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER,
                    book_id INTEGER,
                    issue_date DATE NOT NULL,
                    due_date DATE NOT NULL,
                    return_date DATE,
                    fine REAL DEFAULT 0,
                    status TEXT DEFAULT 'issued',
                    FOREIGN KEY (student_id) REFERENCES students (id),
                    FOREIGN KEY (book_id) REFERENCES books (id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS study_materials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    subject TEXT,
                    category TEXT,
                    semester INTEGER,
                    year INTEGER,
                    uploaded_by TEXT,
                    file_path TEXT NOT NULL,
                    file_size INTEGER,
                    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    description TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            print("✅ Fresh portal database created")
            
    except Exception as e:
        print(f"⚠️  Error reinitializing databases: {e}")
    
    print("\n" + "=" * 60)
    print("✅ RESET COMPLETE!")
    print("=" * 60)
    print("\nYour library system is now brand new with:")
    print("  ✓ Empty databases")
    print("  ✓ No students or books")
    print("  ✓ No history or logs")
    print("  ✓ Clean uploads folder")
    print("\nYou can now start fresh!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        clear_all_data()
    except KeyboardInterrupt:
        print("\n\n❌ Reset cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error during reset: {e}")
        print("\nPlease check the error and try again.")
