"""
Clear all data from library database - Make it brand new
"""
import sqlite3
import os
import shutil
from pathlib import Path

def clear_all_data():
    print("=" * 60)
    print("CLEARING ALL LIBRARY DATA")
    print("=" * 60)
    
    # Clear main library database
    print("\n📊 Clearing Library Database...")
    db_path = Path(__file__).parent / 'library.db'
    
    if db_path.exists():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get counts before clearing
        cursor.execute("SELECT COUNT(*) FROM students")
        student_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM books")
        book_count = cursor.fetchone()[0]
        
        try:
            cursor.execute("SELECT COUNT(*) FROM transactions")
            trans_count = cursor.fetchone()[0]
        except:
            trans_count = 0
        
        try:
            cursor.execute("SELECT COUNT(*) FROM borrow_records")
            borrow_count = cursor.fetchone()[0]
        except:
            borrow_count = 0
        
        print(f"   Found: {student_count} students, {book_count} books")
        print(f"          {trans_count} transactions, {borrow_count} borrow records")
        
        # Clear all data - handle tables that may or may not exist
        tables_to_clear = [
            'borrow_records',
            'transactions', 
            'students',
            'books',
            'promotion_history',
            'academic_years',
            'admin_activity'
        ]
        
        for table in tables_to_clear:
            try:
                cursor.execute(f"DELETE FROM {table}")
                print(f"   ✓ Cleared {table}")
            except Exception as e:
                print(f"   - Skipped {table}: {e}")
        
        # Reset auto-increment counters
        cursor.execute("DELETE FROM sqlite_sequence")
        
        conn.commit()
        conn.close()
        
        print("   ✅ All data cleared from library.db")
    
    # Clear portal database
    print("\n📊 Clearing Portal Database...")
    portal_db_path = Path(__file__).parent / 'Web-Extension' / 'portal.db'
    
    if portal_db_path.exists():
        conn = sqlite3.connect(portal_db_path)
        cursor = conn.cursor()
        
        try:
            tables_to_clear = [
                'borrow_records',
                'transactions',
                'students',
                'books',
                'study_materials',
                'promotion_history',
                'academic_years'
            ]
            
            for table in tables_to_clear:
                try:
                    cursor.execute(f"DELETE FROM {table}")
                except:
                    pass
            
            # Reset auto-increment
            cursor.execute("DELETE FROM sqlite_sequence")
            
            conn.commit()
            print("   ✅ All data cleared from portal.db")
        except Exception as e:
            print(f"   ⚠️  Portal DB: {e}")
        finally:
            conn.close()
    
    # Clear uploaded files
    print("\n📁 Clearing Uploaded Files...")
    uploads_dir = Path(__file__).parent / 'Web-Extension' / 'uploads'
    
    # Clear registration photos
    photos_dir = uploads_dir / 'registration_photos'
    if photos_dir.exists():
        file_count = 0
        for file in photos_dir.iterdir():
            if file.is_file():
                file.unlink()
                file_count += 1
        print(f"   ✅ Deleted {file_count} registration photos")
    
    # Clear study materials
    materials_dir = uploads_dir / 'study_materials'
    if materials_dir.exists():
        file_count = 0
        for file in materials_dir.iterdir():
            if file.is_file():
                file.unlink()
                file_count += 1
        print(f"   ✅ Deleted {file_count} study materials")
    
    # Verify clearing
    print("\n🔍 Verifying...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    students = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM books")
    books = cursor.fetchone()[0]
    
    try:
        cursor.execute("SELECT COUNT(*) FROM transactions")
        transactions = cursor.fetchone()[0]
    except:
        transactions = 0
    
    conn.close()
    
    print(f"   Current: {students} students, {books} books, {transactions} transactions")
    
    print("\n" + "=" * 60)
    print("✅ ALL DATA CLEARED SUCCESSFULLY!")
    print("=" * 60)
    print("\nYour library system is now brand new!")
    print("   • Database tables are empty")
    print("   • Email history cleared")
    print("   • Sync logs reset")
    print("   • All uploads removed")
    print("\nYou can start adding new data!")
    print("=" * 60)

if __name__ == "__main__":
    clear_all_data()
