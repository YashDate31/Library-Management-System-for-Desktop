"""
Check and clear Supabase remote database
"""
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

try:
    import psycopg2
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False
    print("❌ psycopg2 not installed. Install with: pip install psycopg2-binary")
    exit(1)

def check_and_clear_supabase():
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ No DATABASE_URL found in .env file")
        return
    
    print("Connecting to Supabase PostgreSQL...")
    print(f"Database: {database_url.split('@')[1].split('/')[0]}")
    print()
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
        """)
        tables = [t[0] for t in cursor.fetchall()]
        
        print(f"Found {len(tables)} tables in Supabase database")
        print("="*60)
        
        # Check current counts
        total_records = 0
        table_counts = {}
        
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                table_counts[table] = count
                total_records += count
                if count > 0:
                    print(f"  {table}: {count} records")
            except Exception as e:
                print(f"  {table}: Error - {e}")
        
        print("="*60)
        print(f"Total records across all tables: {total_records}")
        print()
        
        if total_records == 0:
            print("✅ Supabase database is already empty!")
            conn.close()
            return
        
        # Ask for confirmation
        print("⚠️  WARNING: This will DELETE ALL DATA from Supabase!")
        response = input("Type 'DELETE' to confirm: ")
        
        if response != 'DELETE':
            print("❌ Cancelled")
            conn.close()
            return
        
        print("\n🔄 Deleting all data from Supabase...")
        print("="*60)
        
        # Delete in correct order (child tables first)
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
        
        # Add any other tables
        for table in tables:
            if table not in ordered_tables:
                ordered_tables.append(table)
        
        deleted_count = 0
        for table in ordered_tables:
            if table in tables:
                try:
                    count = table_counts.get(table, 0)
                    if count > 0:
                        cursor.execute(f"DELETE FROM {table}")
                        deleted_count += count
                        print(f"  ✅ Deleted {count} records from {table}")
                except Exception as e:
                    print(f"  ❌ Error clearing {table}: {e}")
        
        conn.commit()
        conn.close()
        
        print("="*60)
        print(f"✅ Successfully deleted {deleted_count} total records!")
        print("✅ Supabase database is now empty")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_and_clear_supabase()
