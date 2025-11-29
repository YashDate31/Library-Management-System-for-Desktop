import sqlite3
import os

db_path = 'library.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("=== LIBRARY DATABASE STRUCTURE ===")
    print(f"Database file: {os.path.abspath(db_path)}")
    print(f"File size: {os.path.getsize(db_path)} bytes")
    print()
    
    if tables:
        print("Tables found:")
        for table in tables:
            table_name = table[0]
            print(f"\n📋 Table: {table_name}")
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            print("   Columns:")
            for col in columns:
                print(f"     - {col[1]} ({col[2]})")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"   Records: {count}")
            
            # Show sample data if available
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
                sample_data = cursor.fetchall()
                print("   Sample data:")
                for row in sample_data:
                    print(f"     {row}")
    else:
        print("No tables found in database.")
    
    conn.close()
else:
    print(f"Database file '{db_path}' not found!")
    print("Available files in current directory:")
    for file in os.listdir('.'):
        if file.endswith('.db'):
            print(f"  - {file}")

            