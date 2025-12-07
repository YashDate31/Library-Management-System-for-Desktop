import sqlite3
import os
import sys
import random
from datetime import datetime, timedelta
from database import Database

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def populate():
    print("Initializing Database connection...")
    db = Database()
    
    # ---------------------------------------------------------
    # 1. ADD STUDENTS
    # ---------------------------------------------------------
    print("\n--- Adding Dummy Students ---")
    departments = ["Computer"]
    years = ["1st", "2nd", "3rd"]
    
    first_names = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan",
                   "Diya", "Saanvi", "Ananya", "Aadhya", "Pari", "Mira", "Kiara", "Ira", "Riya", "Myra"]
    last_names = ["Patil", "Deshmukh", "Joshi", "Kulkarni", "Kale", "Pawar", "Shinde", "Chavan", "More", "Gaikwad",
                  "Jadhav", "Sawant", "Bhosale", "Wagh", "Kamble", "Mane", "Ghatge", "Thorat", "Mohite", "Shetty"]

    students_data = []
    
    # Generate 25 students
    for i in range(25):
        enrollment = f"220{6001 + i}"
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        email = f"{enrollment}@student.example.com"
        phone = f"98{random.randint(10000000, 99999999)}"
        dept = "Computer"
        year = random.choice(years)
        
        students_data.append((enrollment, name, email, phone, dept, year))
        
        success, msg = db.add_student(enrollment, name, email, phone, dept, year)
        if success:
            print(f"Added Student: {name} ({enrollment})")
        else:
            print(f"Skipped Student (might exist): {name}")

    # ---------------------------------------------------------
    # 2. ADD BOOKS
    # ---------------------------------------------------------
    print("\n--- Adding Dummy Books ---")
    categories = ["Technology", "Textbook", "Research", "General"]
    
    books_source = [
        ("Clean Code", "Robert Martin", "Technology"),
        ("Introduction to Algorithms", "Cormen", "Textbook"),
        ("Design Patterns", "Gamma et al.", "Technology"),
        ("The Pragmatic Programmer", "Andrew Hunt", "Technology"),
        ("Artificial Intelligence", "Russell & Norvig", "Textbook"),
        ("Database System Concepts", "Silberschatz", "Textbook"),
        ("Operating System Concepts", "Galvin", "Textbook"),
        ("Computer Networks", "Tanenbaum", "Textbook"),
        ("Head First Java", "Kathy Sierra", "Technology"),
        ("Python Crash Course", "Eric Matthes", "Technology"),
        ("Deep Learning", "Ian Goodfellow", "Research"),
        ("Data Structures using C", "Reema Thareja", "Textbook"),
        ("Web Design Playground", "Paul McFedries", "Technology"),
        ("Soft Skills", "John Sonmez", "General"),
        ("Cracking the Coding Interview", "Gayle Laakmann", "General")
    ]
    
    books_data = []

    for i, (title, author, cat) in enumerate(books_source):
        book_id = f"BK{1001 + i}"
        isbn = f"978-{random.randint(100, 999)}-{random.randint(10000, 99999)}"
        copies = random.randint(3, 8)
        
        books_data.append(book_id)
        
        success, msg = db.add_book(book_id, title, author, isbn, cat, copies)
        if success:
            print(f"Added Book: {title} ({book_id}) - {copies} Copies")
        else:
            print(f"Skipped Book (might exist): {title}")

    # ---------------------------------------------------------
    # 3. ADD TRANSACTIONS
    # ---------------------------------------------------------
    print("\n--- Adding Borrow Transactions ---")
    
    # We need to manually insert into borrow_records table to force past dates for "Overdue" testing
    # doing it via db.borrow_book would limit us to today's date logic or require hacking it.
    # So we will use direct SQL for flexibility here.
    
    conn = db.get_connection()
    cursor = conn.cursor()
    
    today = datetime.now()
    
    # 1. Active Borrows (On Time) - Borrowed 2 days ago, due in 5 days
    for _ in range(5):
        student_en = random.choice(students_data)[0]
        book_id = random.choice(books_data)
        
        borrow_date = (today - timedelta(days=2)).strftime('%Y-%m-%d')
        due_date = (today + timedelta(days=5)).strftime('%Y-%m-%d')
        
        # Check availability roughly (ignoring race cons for dummy script)
        cursor.execute("SELECT available_copies FROM books WHERE book_id=?", (book_id,))
        avail = cursor.fetchone()[0]
        if avail > 0:
            cursor.execute("""
                INSERT INTO borrow_records (enrollment_no, book_id, borrow_date, due_date, status, academic_year)
                VALUES (?, ?, ?, ?, ?, '2025-2026')
            """, (student_en, book_id, borrow_date, due_date, 'borrowed'))
            
            cursor.execute("UPDATE books SET available_copies = available_copies - 1 WHERE book_id=?", (book_id,))
            print(f"Added Active Borrow: {student_en} took {book_id}")

    # 2. Overdue Borrows - Borrowed 10 days ago, due 3 days ago
    for _ in range(5):
        student_en = random.choice(students_data)[0]
        book_id = random.choice(books_data)
        
        borrow_date = (today - timedelta(days=10)).strftime('%Y-%m-%d')
        due_date = (today - timedelta(days=3)).strftime('%Y-%m-%d')
        
        cursor.execute("SELECT available_copies FROM books WHERE book_id=?", (book_id,))
        avail = cursor.fetchone()[0]
        if avail > 0:
            cursor.execute("""
                INSERT INTO borrow_records (enrollment_no, book_id, borrow_date, due_date, status, academic_year)
                VALUES (?, ?, ?, ?, ?, '2025-2026')
            """, (student_en, book_id, borrow_date, due_date, 'borrowed'))
            
            cursor.execute("UPDATE books SET available_copies = available_copies - 1 WHERE book_id=?", (book_id,))
            print(f"Added Overdue Borrow: {student_en} took {book_id}")

    # 3. Returned Books (History)
    for _ in range(5):
        student_en = random.choice(students_data)[0]
        book_id = random.choice(books_data)
        
        borrow_date = (today - timedelta(days=20)).strftime('%Y-%m-%d')
        due_date = (today - timedelta(days=13)).strftime('%Y-%m-%d')
        return_date = (today - timedelta(days=15)).strftime('%Y-%m-%d') # Returned early
        
        cursor.execute("""
            INSERT INTO borrow_records (enrollment_no, book_id, borrow_date, due_date, return_date, status, academic_year)
            VALUES (?, ?, ?, ?, ?, 'returned', '2025-2026')
        """, (student_en, book_id, borrow_date, due_date, return_date))
        print(f"Added Returned History: {student_en} returned {book_id}")

    conn.commit()
    conn.close()
    
    print("\n--- Dummy Data Population Complete! ---")
    print(f"Data Path: {db.db_path}")

if __name__ == "__main__":
    populate()
