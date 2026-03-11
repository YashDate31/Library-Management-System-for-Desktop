"""
Complete Data Reset - Clears BOTH Local and Remote Databases
This ensures no data comes back after sync
"""
import sqlite3
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try importing PostgreSQL support
try:
    import psycopg2
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False
    psycopg2 = None
    print("⚠️  Warning: psycopg2 not available - cannot clear remote database")

def clear_local_database():
    """Clear local SQLite database"""
    print("\n" + "="*60)
    print("CLEARING LOCAL DATABASE")
    print("="*60)
    
    script_dir = Path(__file__).parent
    db_path = script_dir / 'library.db'
    
    if not db_path.exists():
        print("   ℹ️  Local database doesn't exist")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get table list
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cursor.fetchall() if t[0] != 'sqlite_sequence']
    
    print(f"   Found {len(tables)} tables: {', '.join(tables)}")
    
    # Clear each table
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            cursor.execute(f"DELETE FROM {table}")
            print(f"   ✅ Cleared {table} ({count} records)")
        except Exception as e:
            print(f"   ⚠️  Could not clear {table}: {e}")
    
    # Reset auto-increment
    cursor.execute("DELETE FROM sqlite_sequence")
    
    conn.commit()
    conn.close()
    
    print("   ✅ Local database cleared")

def clear_remote_database():
    """Clear remote PostgreSQL database"""
    print("\n" + "="*60)
    print("CLEARING REMOTE DATABASE")
    print("="*60)
    
    if not POSTGRES_AVAILABLE:
        print("   ❌ Cannot clear remote database - psycopg2 not installed")
        return False
    
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("   ℹ️  No remote database configured (DATABASE_URL not set)")
        return True
    
    try:
        print(f"   Connecting to remote database...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Get table list
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
        """)
        tables = [t[0] for t in cursor.fetchall()]
        
        print(f"   Found {len(tables)} tables: {', '.join(tables)}")
        
        # Clear tables in correct order (child tables first to avoid foreign key violations)
        # Order matters due to foreign key constraints
        ordered_tables = [
            'book_waitlist',
            'book_ratings',
            'access_logs',
            'user_notifications',
            'user_settings',
            'deletion_requests',
            'notices',
            'student_auth',
            'requests',
            'study_materials',
            'borrow_records',
            'transactions',
            'promotion_history',
            'academic_years',
            'admin_activity',
            'books',
            'students'
        ]
        
        # Add any other tables not in the ordered list
        for table in tables:
            if table not in ordered_tables:
                ordered_tables.append(table)
        
        # Clear each table
        for table in ordered_tables:
            if table in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    cursor.execute(f"DELETE FROM {table}")
                    print(f"   ✅ Cleared {table} ({count} records)")
                except Exception as e:
                    print(f"   ⚠️  Could not clear {table}: {e}")
        
        conn.commit()
        conn.close()
        
        print("   ✅ Remote database cleared")
        return True
        
    except Exception as e:
        print(f"   ❌ Error clearing remote database: {e}")
        return False

def clear_portal_database():
    """Clear portal database"""
    print("\n" + "="*60)
    print("CLEARING PORTAL DATABASE")
    print("="*60)
    
    script_dir = Path(__file__).parent
    portal_db_path = script_dir / 'Web-Extension' / 'portal.db'
    
    if not portal_db_path.exists():
        print("   ℹ️  Portal database doesn't exist")
        return
    
    conn = sqlite3.connect(portal_db_path)
    cursor = conn.cursor()
    
    # Get table list
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cursor.fetchall() if t[0] != 'sqlite_sequence']
    
    print(f"   Found {len(tables)} tables")
    
    # Clear each table
    for table in tables:
        try:
            cursor.execute(f"DELETE FROM {table}")
        except:
            pass
    
    cursor.execute("DELETE FROM sqlite_sequence")
    conn.commit()
    conn.close()
    
    print("   ✅ Portal database cleared")

def clear_uploads():
    """Clear uploaded files"""
    print("\n" + "="*60)
    print("CLEARING UPLOADS")
    print("="*60)
    
    script_dir = Path(__file__).parent
    uploads_dir = script_dir / 'Web-Extension' / 'uploads'
    
    # Clear registration photos
    photos_dir = uploads_dir / 'registration_photos'
    if photos_dir.exists():
        count = 0
        for file in photos_dir.iterdir():
            if file.is_file():
                file.unlink()
                count += 1
        print(f"   ✅ Deleted {count} registration photos")
    
    # Clear study materials
    materials_dir = uploads_dir / 'study_materials'
    if materials_dir.exists():
        count = 0
        for file in materials_dir.iterdir():
            if file.is_file():
                file.unlink()
                count += 1
        print(f"   ✅ Deleted {count} study materials")

def main():
    print("\n" + "="*60)
    print("COMPLETE DATABASE RESET")
    print("Local + Remote + Portal + Uploads")
    print("="*60)
    print("\n⚠️  This will permanently delete ALL data from:")
    print("   • Local database (library.db)")
    print("   • Remote PostgreSQL database")
    print("   • Portal database")
    print("   • All uploaded files")
    print("\nThis cannot be undone!")
    print("="*60)
    
    # Clear all databases
    clear_local_database()
    remote_success = clear_remote_database()
    clear_portal_database()
    clear_uploads()
    
    # Final verification
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    script_dir = Path(__file__).parent
    db_path = script_dir / 'library.db'
    
    if db_path.exists():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM students")
        students = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM books")
        books = cursor.fetchone()[0]
        conn.close()
        
        print(f"   Local DB: {students} students, {books} books")
    
    print("\n" + "="*60)
    print("✅ RESET COMPLETE!")
    print("="*60)
    
    if remote_success:
        print("\n✅ Both local AND remote databases are now empty")
        print("   The sync will NOT restore old data")
    else:
        print("\n⚠️  Remote database could not be cleared")
        print("   Old data may sync back when you start the app")
        print("   Install psycopg2 to clear remote database:")
        print("   pip install psycopg2-binary")
    
    print("\n🎉 Your library system is now brand new!")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Reset cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
