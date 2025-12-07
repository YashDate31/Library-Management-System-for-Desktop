import sqlite3
import os

DB_NAME = 'library.db'

def migrate_db():
    if not os.path.exists(DB_NAME):
        print("Database not found!")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(students)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'password' not in columns:
            print("Adding password column...")
            cursor.execute("ALTER TABLE students ADD COLUMN password TEXT DEFAULT 'student123'")
            conn.commit()
            print("Column added successfully with default 'student123'.")
        else:
            print("Column 'password' already exists.")
            
    except Exception as e:
        print(f"Migration failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_db()
