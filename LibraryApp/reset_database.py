import sqlite3
import os
import sys
from datetime import datetime

def reset_database():
    """Reset the library database with fresh tables and sample data"""
    
    # Determine database path
    if hasattr(sys, '_MEIPASS'):
        # Running as PyInstaller executable
        db_path = os.path.join(os.path.dirname(sys.executable), 'library.db')
    else:
        # Running as script
        db_path = os.path.join(os.path.dirname(__file__), 'library.db')
    
    print(f"Resetting database at: {db_path}")
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Existing database removed.")
    
    # Create fresh database connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create students table with proper schema
    cursor.execute('''
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            enrollment_no TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            department TEXT,
            year TEXT,
            date_registered DATE DEFAULT CURRENT_DATE
        )
    ''')
    
    # Create books table with proper schema
    cursor.execute('''
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT,
            isbn TEXT,
            total_copies INTEGER DEFAULT 1,
            available_copies INTEGER DEFAULT 1,
            date_added DATE DEFAULT CURRENT_DATE
        )
    ''')
    
    # Create borrowed_books table with proper schema
    cursor.execute('''
        CREATE TABLE borrowed_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            book_id INTEGER,
            borrow_date DATE DEFAULT CURRENT_DATE,
            due_date DATE,
            return_date DATE,
            status TEXT DEFAULT 'borrowed',
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (book_id) REFERENCES books (id)
        )
    ''')
    
    # Insert sample students data
    sample_students = [
        ('24210270230', 'Yash Vijay Date', 'yash.date@example.com', '9876543210', 'Computer', '2nd'),
        ('24210270231', 'Rahul Sharma', 'rahul.sharma@example.com', '9876543211', 'Computer', '2nd'),
        ('24210270232', 'Priya Patel', 'priya.patel@example.com', '9876543212', 'Computer', '2nd'),
        ('24210270233', 'Amit Kumar', 'amit.kumar@example.com', '9876543213', 'Computer', '3rd'),
        ('24210270234', 'Sneha Singh', 'sneha.singh@example.com', '9876543214', 'Computer', '3rd'),
        ('24210270235', 'Rohan Verma', 'rohan.verma@example.com', '9876543215', 'Computer', '1st'),
        ('24210270236', 'Kavya Gupta', 'kavya.gupta@example.com', '9876543216', 'Computer', '1st'),
        ('24210270237', 'Arjun Reddy', 'arjun.reddy@example.com', '9876543217', 'Computer', '4th'),
        ('24210270238', 'Pooja Mishra', 'pooja.mishra@example.com', '9876543218', 'Computer', '4th'),
        ('24210270239', 'Vikram Yadav', 'vikram.yadav@example.com', '9876543219', 'Computer', '2nd')
    ]
    
    cursor.executemany('''
        INSERT INTO students (enrollment_no, name, email, phone, department, year)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', sample_students)
    
    # Insert sample books data
    sample_books = [
        ('CS001', 'Introduction to Programming', 'John Smith', 'Programming', '978-0123456789', 5, 5),
        ('CS002', 'Data Structures and Algorithms', 'Jane Doe', 'Programming', '978-0123456790', 3, 3),
        ('CS003', 'Database Management Systems', 'Robert Johnson', 'Database', '978-0123456791', 4, 4),
        ('CS004', 'Computer Networks', 'Emily Brown', 'Networking', '978-0123456792', 3, 3),
        ('CS005', 'Operating Systems', 'Michael Wilson', 'Systems', '978-0123456793', 4, 4),
        ('CS006', 'Software Engineering', 'Sarah Davis', 'Engineering', '978-0123456794', 2, 2),
        ('CS007', 'Web Development', 'David Miller', 'Web', '978-0123456795', 3, 3),
        ('CS008', 'Machine Learning', 'Lisa Anderson', 'AI/ML', '978-0123456796', 2, 2),
        ('CS009', 'Artificial Intelligence', 'James Taylor', 'AI/ML', '978-0123456797', 3, 3),
        ('CS010', 'Cybersecurity Fundamentals', 'Anna Wilson', 'Security', '978-0123456798', 2, 2)
    ]
    
    cursor.executemany('''
        INSERT INTO books (book_id, title, author, category, isbn, total_copies, available_copies)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', sample_books)
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print("Database reset successfully!")
    print(f"Created {len(sample_students)} sample students")
    print(f"Created {len(sample_books)} sample books")
    print("Tables: students, books, borrowed_books")

if __name__ == "__main__":
    reset_database()