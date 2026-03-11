"""
Quick script to clean Supabase and do a fresh sync from local database
This ensures cloud database matches local database exactly
"""
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

try:
    import psycopg2
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False
    print("❌ psycopg2 not installed. Install with: pip install psycopg2-binary")
    exit(1)

def clean_cloud_database():
    """Delete all library data from cloud database"""
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ No DATABASE_URL found in .env file")
        return False
    
    print("\n" + "="*60)
    print("CLEAN SUPABASE AND FRESH SYNC")
    print("="*60)
    print("\nThis will:")
    print("1. Delete all books and students from Supabase cloud")
    print("2. Sync fresh data from local database")
    print("\n⚠️  WARNING: This will clear cloud database!")
    print("="*60)
    
    response = input("\nType 'YES' to continue: ")
    if response != 'YES':
        print("❌ Cancelled")
        return False
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("\n🔄 Cleaning Supabase...")
        
        # Delete in correct order (child tables first, parent tables last)
        tables_to_clean = [
            'admin_activity',
            'borrow_records',
            'books',
            'students'
        ]
        
        for table in tables_to_clean:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                
                if count > 0:
                    cursor.execute(f"DELETE FROM {table}")
                    conn.commit()
                    print(f"  ✅ Deleted {count} records from {table}")
                else:
                    print(f"  ℹ️  {table} already empty")
                    
            except Exception as e:
                print(f"  ⚠️  {table}: {e}")
                conn.rollback()
        
        conn.close()
        print("\n✅ Supabase cloud database cleaned!")
        print("\nNow trigger a manual sync from the application:")
        print("  Settings → Cloud Sync → Sync Now")
        print("\nThis will upload all your local data to the clean cloud database.")
        print("="*60 + "\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == '__main__':
    clean_cloud_database()
