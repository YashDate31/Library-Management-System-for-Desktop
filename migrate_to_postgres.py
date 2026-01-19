import sqlite3
import psycopg2
import os
import sys
from psycopg2.extras import execute_values
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Configuration
SQLITE_DB_PATH = os.path.join('LibraryApp', 'library.db')
PORTAL_DB_PATH = os.path.join('LibraryApp', 'Web-Extension', 'portal.db')
DATABASE_URL = os.getenv('DATABASE_URL')

def get_sqlite_conn(db_path):
    if not os.path.exists(db_path):
        print(f"SQLite DB not found at {db_path}")
        return None
    return sqlite3.connect(db_path)

def get_postgres_conn():
    if not DATABASE_URL:
        print("DATABASE_URL is not set in .env")
        return None
    try:
        return psycopg2.connect(DATABASE_URL)
    except Exception as e:
        print(f"Failed to connect to Postgres: {e}")
        return None

def migrate_table(sqlite_cursor, pg_cursor, table_name, columns, conflict_column=None):
    """Migrate a single table from SQLite to Postgres"""
    print(f"Migrating table: {table_name}...")
    
    # Read from SQLite
    try:
        sqlite_cursor.execute(f"SELECT {', '.join(columns)} FROM {table_name}")
        rows = sqlite_cursor.fetchall()
    except Exception as e:
        print(f"Skipping {table_name} (Source error: {e})")
        return

    if not rows:
        print(f" - No data in {table_name}")
        return

    # Write to Postgres
    # Construct INSERT SQL
    # placeholders = %s (implicit in execute_values)
    col_str = ', '.join(columns)
    
    # Handle conflict if specified
    on_conflict = ""
    if conflict_column:
        on_conflict = f"ON CONFLICT ({conflict_column}) DO NOTHING"
        
    sql = f"INSERT INTO {table_name} ({col_str}) VALUES %s {on_conflict}"
    
    try:
        execute_values(pg_cursor, sql, rows)
        print(f" - Migrated {len(rows)} rows.")
    except Exception as e:
        print(f" - Error writing to Postgres: {e}")

def main():
    print("--- Starting Migration to PostgreSQL ---")
    
    if not DATABASE_URL:
        print("Error: DATABASE_URL not found. Please set it in .env file.")
        return

    pg_conn = get_postgres_conn()
    if not pg_conn:
        return

    pg_cursor = pg_conn.cursor()

    # 1. Migrate Core Library Data
    sqlite_lib = get_sqlite_conn(SQLITE_DB_PATH)
    if sqlite_lib:
        print(f"Connected to {SQLITE_DB_PATH}")
        lib_cursor = sqlite_lib.cursor()
        
        # students
        migrate_table(lib_cursor, pg_cursor, 'students', 
                      ['enrollment_no', 'name', 'email', 'phone', 'department', 'year', 'date_registered'], 
                      conflict_column='enrollment_no')
                      
        # books
        migrate_table(lib_cursor, pg_cursor, 'books', 
                      ['book_id', 'title', 'author', 'isbn', 'category', 'total_copies', 'available_copies', 'date_added'], 
                      conflict_column='book_id')
                      
        # transactions (no unique constraint usually, but let's assume id is serial and we migrate data without id to let pg generate new ids OR we intentionally omit id)
        # Assuming we want to keep history.
        migrate_table(lib_cursor, pg_cursor, 'transactions', 
                      ['enrollment_no', 'book_id', 'borrow_date', 'due_date', 'return_date', 'fine', 'status'])
        
        # borrow_records
        migrate_table(lib_cursor, pg_cursor, 'borrow_records', 
                      ['enrollment_no', 'book_id', 'borrow_date', 'due_date', 'return_date', 'status', 'fine', 'academic_year'])
                      
        # academic_years
        migrate_table(lib_cursor, pg_cursor, 'academic_years', 
                      ['year_name', 'start_date', 'end_date', 'is_active'],
                      conflict_column='year_name')

        sqlite_lib.close()

    # 2. Migrate Portal Data
    sqlite_portal = get_sqlite_conn(PORTAL_DB_PATH)
    if sqlite_portal:
        print(f"Connected to {PORTAL_DB_PATH}")
        portal_cursor = sqlite_portal.cursor()
        
        # student_auth
        migrate_table(portal_cursor, pg_cursor, 'student_auth', 
                      ['enrollment_no', 'password', 'is_first_login', 'last_changed'],
                      conflict_column='enrollment_no')
                      
        # requests
        migrate_table(portal_cursor, pg_cursor, 'requests', 
                      ['enrollment_no', 'request_type', 'details', 'status', 'created_at'])
                      
        # notices
        migrate_table(portal_cursor, pg_cursor, 'notices', 
                      ['title', 'message', 'active', 'created_at'])
                      
        # user_settings
        migrate_table(portal_cursor, pg_cursor, 'user_settings', 
                      ['enrollment_no', 'email', 'library_alerts', 'loan_reminders', 'theme', 'language', 'data_consent'],
                      conflict_column='enrollment_no')

        sqlite_portal.close()

    pg_conn.commit()
    pg_conn.close()
    print("--- Migration Completed Successfully ---")

if __name__ == "__main__":
    main()
