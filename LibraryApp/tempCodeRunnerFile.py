#!/usr/bin/env python3
"""
Add Demo Data to Library Management System
Creates sample students, books, and transactions for testing
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add path for database import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database import Database

def add_demo_students(db):
    """Add demo students to database"""
    print("Adding demo students...")
    
    demo_students = [
        ('220501001', 'Rajesh Kumar', 'rajesh.kumar@iare.ac.in', '9876543210', 'CSE', '1st Year'),
        ('220501002', 'Priya Sharma', 'priya.sharma@iare.ac.in', '9876543211', 'CSE', '1st Year'),
        ('210501003', 'Amit Patel', 'amit.patel@iare.ac.in', '9876543212', 'CSE', '2nd Year'),
        ('210501004', 'Sneha Reddy', 'sneha.reddy@iare.ac.in', '9876543213', 'CSE', '2nd Year'),
        ('200501005', 'Vikram Singh', 'vikram.singh@iare.ac.in', '9876543214', 'CSE', '3rd Year'),
        ('200501006', 'Divya Iyer', 'divya.iyer@iare.ac.in', '9876543215', 'CSE', '3rd Year'),
        ('190501007', 'Arjun Nair', 'arjun.nair@iare.ac.in', '9876543216', 'CSE', '4th Year'),
        ('190501008', 'Kavya Rao', 'kavya.rao@iare.ac.in', '9876543217', 'CSE', '4th Year'),
        ('220501009', 'Rahul Verma', 'rahul.verma@iare.ac.in', '9876543218', 'CSE', '1st Year'),
        ('210501010', 'Anjali Menon', 'anjali.menon@iare.ac.in', '9876543219', 'CSE', '2nd Year'),
        ('200501011', 'Siddharth Das', 'siddharth.das@iare.ac.in', '9876543220', 'CSE', '3rd Year'),
        ('190501012', 'Pooja Gupta', 'pooja.gupta@iare.ac.in', '9876543221', 'CSE', '4th Year'),
        ('220501013', 'Karan Joshi', 'karan.joshi@iare.ac.in', '9876543222', 'CSE', '1st Year'),
        ('210501014', 'Nisha Kapoor', 'nisha.kapoor@iare.ac.in', '9876543223', 'CSE', '2nd Year'),
        ('200501015', 'Aditya Mishra', 'aditya.mishra@iare.ac.in', '9876543224', 'CSE', '3rd Year'),
    ]
    
    conn = db.get_connection()
    cursor = conn.cursor()
    
    added_count = 0
    for student in demo_students:
        try:
            # Check if student already exists
            cursor.execute("SELECT enrollment_no FROM students WHERE enrollment_no = ?", (student[0],))
            if cursor.fetchone():
                print(f"  Student {student[0]} already exists, skipping...")
                continue
            
            cursor.execute('''INSERT INTO students 
                (enrollment_no, name, email, phone, department, year) 
                VALUES (?, ?, ?, ?, ?, ?)''', student)
            added_count += 1
            print(f"  Added: {student[1]} ({student[0]})")
        except Exception as e:
            print(f"  Error adding {student[0]}: {e}")
    
    conn.commit()
    conn.close()
    print(f"✓ Successfully added {added_count} demo students\n")
    return added_count

def add_demo_books(db):
    """Add demo books to database"""
    print("Adding demo books...")
    
    demo_books = [
        # Programming Books - only book_id, title, author, category, total_copies, available_copies
        ('PY001', 'Python Programming', 'Mark Lutz', 'Programming', 5, 5),
        ('PY002', 'Python Crash Course', 'Eric Matthes', 'Programming', 3, 3),
        ('JAVA001', 'Head First Java', 'Kathy Sierra', 'Programming', 4, 4),
        ('JAVA002', 'Effective Java', 'Joshua Bloch', 'Programming', 3, 3),
        ('CPP001', 'C++ Primer', 'Stanley Lippman', 'Programming', 4, 4),
        ('JS001', 'JavaScript: The Good Parts', 'Douglas Crockford', 'Programming', 3, 3),
        
        # Data Structures & Algorithms
        ('DSA001', 'Introduction to Algorithms', 'Thomas Cormen', 'Data Structures', 5, 5),
        ('DSA002', 'Data Structures and Algorithms', 'Aho Ullman', 'Data Structures', 4, 4),
        ('DSA003', 'Algorithm Design Manual', 'Steven Skiena', 'Data Structures', 3, 3),
        
        # Database Books
        ('DB001', 'Database System Concepts', 'Silberschatz', 'Database', 4, 4),
        ('DB002', 'SQL Performance Explained', 'Markus Winand', 'Database', 3, 3),
        ('DB003', 'MongoDB: The Definitive Guide', 'Shannon Bradshaw', 'Database', 3, 3),
        
        # Web Development
        ('WEB001', 'Learning Web Design', 'Jennifer Robbins', 'Web Development', 4, 4),
        ('WEB002', 'Django for Beginners', 'William Vincent', 'Web Development', 3, 3),
        ('WEB003', 'React in Action', 'Mark Thomas', 'Web Development', 3, 3),
        
        # Artificial Intelligence
        ('AI001', 'Artificial Intelligence', 'Stuart Russell', 'AI & ML', 4, 4),
        ('ML001', 'Pattern Recognition', 'Christopher Bishop', 'AI & ML', 3, 3),
        ('ML002', 'Deep Learning', 'Ian Goodfellow', 'AI & ML', 4, 4),
        
        # Networking
        ('NET001', 'Computer Networks', 'Andrew Tanenbaum', 'Networking', 5, 5),
        ('NET002', 'TCP/IP Illustrated', 'W. Richard Stevens', 'Networking', 3, 3),
        
        # Operating Systems
        ('OS001', 'Operating System Concepts', 'Silberschatz', 'Operating Systems', 5, 5),
        ('OS002', 'Modern Operating Systems', 'Andrew Tanenbaum', 'Operating Systems', 4, 4),
        
        # Software Engineering
        ('SE001', 'Clean Code', 'Robert Martin', 'Software Engineering', 4, 4),
        ('SE002', 'Design Patterns', 'Gang of Four', 'Software Engineering', 3, 3),
        ('SE003', 'The Pragmatic Programmer', 'Hunt & Thomas', 'Software Engineering', 3, 3),
    ]
    
    conn = db.get_connection()
    cursor = conn.cursor()
    
    added_count = 0
    for book in demo_books:
        try:
            # Check if book already exists
            cursor.execute("SELECT book_id FROM books WHERE book_id = ?", (book[0],))
            if cursor.fetchone():
                print(f"  Book {book[0]} already exists, skipping...")
                continue
            
            # Insert with only existing columns
            cursor.execute('''INSERT INTO books 
                (book_id, title, author, category, total_copies, available_copies) 
                VALUES (?, ?, ?, ?, ?, ?)''', book)
            conn.commit()
            added_count += 1
            print(f"  Added: {book[1]} by {book[2]}")
        except Exception as e:
            print(f"  Error adding {book[0]}: {e}")
    
    conn.close()
    print(f"✓ Successfully added {added_count} demo books\n")
    return added_count

def add_demo_transactions(db):
    """Add demo transactions (borrow records) to database"""
    print("Adding demo transactions...")
    
    # Get students and books for creating realistic transactions
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Get all students
    cursor.execute("SELECT enrollment_no FROM students LIMIT 10")
    students = [row[0] for row in cursor.fetchall()]
    
    # Get all books
    cursor.execute("SELECT book_id FROM books WHERE available_copies > 0 LIMIT 15")
    books = [row[0] for row in cursor.fetchall()]
    
    if not students or not books:
        print("  No students or books available for transactions")
        conn.close()
        return 0
    
    added_count = 0
    today = datetime.now()
    
    # Create various transaction scenarios
    transaction_scenarios = [
        # Active loans (borrowed recently)
        {'days_ago': 1, 'status': 'active', 'count': 3},
        {'days_ago': 3, 'status': 'active', 'count': 2},
        {'days_ago': 5, 'status': 'active', 'count': 2},
        
        # Overdue loans
        {'days_ago': 10, 'status': 'overdue', 'count': 2},
        {'days_ago': 15, 'status': 'overdue', 'count': 1},
        
        # Returned books
        {'days_ago': 20, 'status': 'returned', 'return_days_ago': 13, 'count': 3},
        {'days_ago': 30, 'status': 'returned', 'return_days_ago': 23, 'count': 2},
    ]
    
    used_combinations = set()
    
    for scenario in transaction_scenarios:
        for _ in range(scenario['count']):
            # Get unique student-book combination
            attempts = 0
            while attempts < 50:
                student = random.choice(students)
                book = random.choice(books)
                combo = (student, book)
                
                if combo not in used_combinations:
                    used_combinations.add(combo)
                    break
                attempts += 1
            
            if attempts >= 50:
                continue
            
            borrow_date = (today - timedelta(days=scenario['days_ago'])).strftime('%Y-%m-%d')
            due_date = (today - timedelta(days=scenario['days_ago']) + timedelta(days=7)).strftime('%Y-%m-%d')
            
            return_date = None
            fine = 0
            status = 'borrowed'
            
            if scenario['status'] == 'returned':
                return_date = (today - timedelta(days=scenario['return_days_ago'])).strftime('%Y-%m-%d')
                # Calculate fine if returned late
                due = datetime.strptime(due_date, '%Y-%m-%d')
                ret = datetime.strptime(return_date, '%Y-%m-%d')
                if ret > due:
                    days_late = (ret - due).days
                    fine = days_late * 5  # 5 rupees per day
            elif scenario['status'] == 'overdue':
                # Calculate fine for overdue books
                due = datetime.strptime(due_date, '%Y-%m-%d')
                days_late = (today - due).days
                fine = days_late * 5
            
            try:
                # Check if transaction already exists
                cursor.execute('''SELECT id FROM borrow_records 
                    WHERE enrollment_no = ? AND book_id = ? AND borrow_date = ?''',
                    (student, book, borrow_date))
                
                if cursor.fetchone():
                    continue
                
                cursor.execute('''INSERT INTO borrow_records 
                    (enrollment_no, book_id, borrow_date, due_date, return_date, status, fine, academic_year) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                    (student, book, borrow_date, due_date, return_date, status, fine, '2024-25'))
                
                # Update book availability if not returned
                if return_date is None:
                    cursor.execute('''UPDATE books SET available_copies = available_copies - 1 
                        WHERE book_id = ? AND available_copies > 0''', (book,))
                
                added_count += 1
                status_text = f"{scenario['status']} {'(Fine: ₹' + str(fine) + ')' if fine > 0 else ''}"
                print(f"  Added: {student} borrowed {book} on {borrow_date} - {status_text}")
                
            except Exception as e:
                print(f"  Error adding transaction: {e}")
    
    conn.commit()
    conn.close()
    print(f"✓ Successfully added {added_count} demo transactions\n")
    return added_count

def add_demo_admin_activity(db):
    """Add sample admin activity logs"""
    print("Adding demo admin activity logs...")
    
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS admin_activity (
            id SERIAL PRIMARY KEY,
            timestamp TEXT NOT NULL,
            action TEXT NOT NULL,
            details TEXT,
            admin_user TEXT
        )''')
        conn.commit()
    except:
        pass
    
    activities = [
        (datetime.now() - timedelta(days=1), 'System Login', 'Admin logged into the system', 'Admin'),
        (datetime.now() - timedelta(days=1, hours=2), 'Student Added', 'Added new student: Rajesh Kumar (220501001)', 'Admin'),
        (datetime.now() - timedelta(days=2), 'Book Added', 'Added new book: Python Programming (PY001)', 'Admin'),
        (datetime.now() - timedelta(days=3), 'Book Issued', 'Issued book PY001 to student 220501001', 'Admin'),
        (datetime.now() - timedelta(days=5), 'Book Returned', 'Book JAVA001 returned by student 210501003', 'Admin'),
        (datetime.now() - timedelta(days=7), 'Report Generated', 'Generated Students Report - Excel format', 'Admin'),
        (datetime.now() - timedelta(days=10), 'Settings Updated', 'Updated library fine settings', 'Admin'),
    ]
    
    added_count = 0
    for activity in activities:
        try:
            timestamp = activity[0].strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''INSERT INTO admin_activity (timestamp, action, details, admin_user)
                VALUES (?, ?, ?, ?)''', (timestamp, activity[1], activity[2], activity[3]))
            added_count += 1
        except Exception as e:
            print(f"  Error adding activity: {e}")
    
    conn.commit()
    conn.close()
    print(f"✓ Successfully added {added_count} admin activity logs\n")
    return added_count

def main():
    """Main function to add all demo data"""
    print("=" * 60)
    print("IARE Library Management System - Demo Data Generator")
    print("=" * 60)
    print()
    
    # Initialize database
    db = Database()
    
    # Add demo data
    students_added = add_demo_students(db)
    books_added = add_demo_books(db)
    transactions_added = add_demo_transactions(db)
    activities_added = add_demo_admin_activity(db)
    
    # Summary
    print("=" * 60)
    print("DEMO DATA SUMMARY")
    print("=" * 60)
    print(f"Students Added:      {students_added}")
    print(f"Books Added:         {books_added}")
    print(f"Transactions Added:  {transactions_added}")
    print(f"Activity Logs Added: {activities_added}")
    print("=" * 60)
    print("\n✓ Demo data has been successfully added to the database!")
    print("You can now test the Reports feature with this sample data.\n")

if __name__ == "__main__":
    main()
