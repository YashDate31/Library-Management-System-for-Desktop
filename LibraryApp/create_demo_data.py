#!/usr/bin/env python3
"""
Demo Database Populator for Library Management System
Creates realistic test data including students, books, and various transaction types
"""

import sqlite3
import os
import sys
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database import Database

def create_demo_data():
    """Populate database with comprehensive demo data"""
    
    print("=" * 60)
    print("📚 Library Management System - Demo Data Generator")
    print("=" * 60)
    
    # Initialize database
    db = Database()
    
    # Sample data
    students_data = [
        # 1st Year
        ("2024CS001", "Aarav Sharma", "aarav.sharma@student.gpa.edu", "9876543210", "Computer", "1st Year"),
        ("2024CS002", "Diya Patel", "diya.patel@student.gpa.edu", "9876543211", "Computer", "1st Year"),
        ("2024CS003", "Arjun Reddy", "arjun.reddy@student.gpa.edu", "9876543212", "Computer", "1st Year"),
        ("2024CS004", "Ananya Singh", "ananya.singh@student.gpa.edu", "9876543213", "Computer", "1st Year"),
        ("2024CS005", "Vihaan Kumar", "vihaan.kumar@student.gpa.edu", "9876543214", "Computer", "1st Year"),
        
        # 2nd Year
        ("2023CS001", "Ishaan Gupta", "ishaan.gupta@student.gpa.edu", "9876543220", "Computer", "2nd Year"),
        ("2023CS002", "Saanvi Verma", "saanvi.verma@student.gpa.edu", "9876543221", "Computer", "2nd Year"),
        ("2023CS003", "Aditya Joshi", "aditya.joshi@student.gpa.edu", "9876543222", "Computer", "2nd Year"),
        ("2023CS004", "Myra Desai", "myra.desai@student.gpa.edu", "9876543223", "Computer", "2nd Year"),
        ("2023CS005", "Reyansh Mehta", "reyansh.mehta@student.gpa.edu", "9876543224", "Computer", "2nd Year"),
        
        # 3rd Year
        ("2022CS001", "Vivaan Agarwal", "vivaan.agarwal@student.gpa.edu", "9876543230", "Computer", "3rd Year"),
        ("2022CS002", "Kiara Kapoor", "kiara.kapoor@student.gpa.edu", "9876543231", "Computer", "3rd Year"),
        ("2022CS003", "Ayaan Shah", "ayaan.shah@student.gpa.edu", "9876543232", "Computer", "3rd Year"),
        ("2022CS004", "Navya Rao", "navya.rao@student.gpa.edu", "9876543233", "Computer", "3rd Year"),
        
        # Pass Out
        ("2021CS001", "Kabir Malhotra", "kabir.malhotra@alumni.gpa.edu", "9876543240", "Computer", "Pass Out"),
        ("2021CS002", "Zara Khan", "zara.khan@alumni.gpa.edu", "9876543241", "Computer", "Pass Out"),
    ]
    
    books_data = [
        # Programming Books
        ("PY001", "Python Programming", "Mark Lutz", "O'Reilly", "Programming", 5),
        ("PY002", "Automate the Boring Stuff with Python", "Al Sweigart", "No Starch Press", "Programming", 3),
        ("JAVA001", "Head First Java", "Kathy Sierra", "O'Reilly", "Programming", 4),
        ("JAVA002", "Effective Java", "Joshua Bloch", "Addison-Wesley", "Programming", 2),
        ("CPP001", "C++ Primer", "Stanley Lippman", "Addison-Wesley", "Programming", 3),
        
        # Web Development
        ("WEB001", "HTML and CSS", "Jon Duckett", "Wiley", "Web Development", 4),
        ("WEB002", "JavaScript: The Good Parts", "Douglas Crockford", "O'Reilly", "Web Development", 3),
        ("WEB003", "React Up and Running", "Stoyan Stefanov", "O'Reilly", "Web Development", 2),
        
        # Data Structures & Algorithms
        ("DSA001", "Introduction to Algorithms", "Cormen", "MIT Press", "Algorithms", 3),
        ("DSA002", "Data Structures Using C", "Reema Thareja", "Oxford", "Algorithms", 5),
        ("DSA003", "Algorithm Design Manual", "Steven Skiena", "Springer", "Algorithms", 2),
        
        # Database
        ("DB001", "Database System Concepts", "Silberschatz", "McGraw-Hill", "Database", 4),
        ("DB002", "SQL in 10 Minutes", "Ben Forta", "Sams", "Database", 3),
        
        # Operating Systems
        ("OS001", "Operating System Concepts", "Silberschatz", "Wiley", "Operating Systems", 3),
        ("OS002", "Modern Operating Systems", "Tanenbaum", "Pearson", "Operating Systems", 2),
        
        # Networks
        ("NET001", "Computer Networks", "Tanenbaum", "Pearson", "Networks", 3),
        ("NET002", "TCP/IP Illustrated", "Stevens", "Addison-Wesley", "Networks", 2),
        
        # AI/ML
        ("AI001", "Artificial Intelligence", "Russell & Norvig", "Pearson", "AI/ML", 2),
        ("ML001", "Machine Learning", "Tom Mitchell", "McGraw-Hill", "AI/ML", 2),
        ("ML002", "Deep Learning", "Ian Goodfellow", "MIT Press", "AI/ML", 1),
        
        # Software Engineering
        ("SE001", "Software Engineering", "Pressman", "McGraw-Hill", "Software Engineering", 3),
        ("SE002", "Clean Code", "Robert Martin", "Prentice Hall", "Software Engineering", 2),
        
        # Mathematics
        ("MATH001", "Discrete Mathematics", "Kenneth Rosen", "McGraw-Hill", "Mathematics", 4),
        ("MATH002", "Linear Algebra", "Gilbert Strang", "Wellesley", "Mathematics", 2),
    ]
    
    print("\n📝 Adding Students...")
    students_added = 0
    for enrollment, name, email, phone, dept, year in students_data:
        success, msg = db.add_student(enrollment, name, email, phone, dept, year)
        if success:
            students_added += 1
            print(f"  ✓ Added: {name} ({enrollment}) - {year}")
        else:
            print(f"  ⚠ Skipped: {name} - {msg}")
    
    print(f"\n✅ Students added: {students_added}/{len(students_data)}")
    
    print("\n📚 Adding Books...")
    books_added = 0
    for book_id, title, author, publisher, category, copies in books_data:
        success, msg = db.add_book(book_id, title, author, publisher, category, copies)
        if success:
            books_added += 1
            print(f"  ✓ Added: {title} ({book_id}) - {copies} copies")
        else:
            print(f"  ⚠ Skipped: {title} - {msg}")
    
    print(f"\n✅ Books added: {books_added}/{len(books_data)}")
    
    # Create various types of transactions
    print("\n📋 Creating Transactions...")
    
    today = datetime.now()
    transactions_created = 0
    
    # Transaction scenarios
    scenarios = [
        # Active loans (pending returns)
        {"enrollment": "2024CS001", "book_id": "PY001", "days_ago": 2, "status": "active"},
        {"enrollment": "2024CS002", "book_id": "WEB001", "days_ago": 5, "status": "active"},
        {"enrollment": "2023CS001", "book_id": "DSA001", "days_ago": 3, "status": "active"},
        
        # Overdue transactions (past due date)
        {"enrollment": "2023CS002", "book_id": "JAVA001", "days_ago": 15, "status": "overdue"},
        {"enrollment": "2023CS003", "book_id": "DB001", "days_ago": 20, "status": "overdue"},
        {"enrollment": "2022CS001", "book_id": "OS001", "days_ago": 25, "status": "overdue"},
        {"enrollment": "2022CS002", "book_id": "NET001", "days_ago": 12, "status": "overdue"},
        
        # Recently returned (completed)
        {"enrollment": "2024CS003", "book_id": "PY002", "days_ago": 10, "returned_days_ago": 3, "status": "returned"},
        {"enrollment": "2024CS004", "book_id": "WEB002", "days_ago": 14, "returned_days_ago": 7, "status": "returned"},
        {"enrollment": "2023CS004", "book_id": "CPP001", "days_ago": 20, "returned_days_ago": 13, "status": "returned"},
        
        # Returned with fine (late return)
        {"enrollment": "2023CS005", "book_id": "DSA002", "days_ago": 18, "returned_days_ago": 2, "status": "returned_late"},
        {"enrollment": "2022CS003", "book_id": "AI001", "days_ago": 25, "returned_days_ago": 5, "status": "returned_late"},
    ]
    
    for scenario in scenarios:
        enrollment = scenario["enrollment"]
        book_id = scenario["book_id"]
        days_ago = scenario["days_ago"]
        status = scenario["status"]
        
        borrow_date = (today - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        due_date = (today - timedelta(days=days_ago) + timedelta(days=7)).strftime("%Y-%m-%d")
        
        # Issue the book
        success, msg = db.borrow_book(enrollment, book_id, borrow_date, due_date)
        
        if success:
            transactions_created += 1
            
            # Get transaction ID
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id FROM transactions 
                WHERE enrollment_no = ? AND book_id = ? AND borrow_date = ?
                ORDER BY id DESC LIMIT 1
            """, (enrollment, book_id, borrow_date))
            result = cursor.fetchone()
            
            if result:
                transaction_id = result[0]
                
                # Handle returned transactions
                if "returned" in status:
                    returned_days_ago = scenario.get("returned_days_ago", 0)
                    return_date = (today - timedelta(days=returned_days_ago)).strftime("%Y-%m-%d")
                    
                    # Calculate fine if late
                    due_date_obj = datetime.strptime(due_date, "%Y-%m-%d")
                    return_date_obj = datetime.strptime(return_date, "%Y-%m-%d")
                    days_late = max(0, (return_date_obj - due_date_obj).days)
                    fine = days_late * 5  # ₹5 per day
                    
                    # Return the book
                    cursor.execute("""
                        UPDATE transactions 
                        SET return_date = ?, fine = ?, status = 'returned'
                        WHERE id = ?
                    """, (return_date, fine, transaction_id))
                    
                    # Update book availability
                    cursor.execute("""
                        UPDATE books 
                        SET available_copies = available_copies + 1 
                        WHERE book_id = ?
                    """, (book_id,))
                    
                    conn.commit()
                    print(f"  ✓ Returned: {enrollment} - {book_id} (Fine: ₹{fine})")
                else:
                    print(f"  ✓ Issued: {enrollment} - {book_id} ({status})")
            
            conn.close()
        else:
            print(f"  ⚠ Failed: {enrollment} - {book_id} - {msg}")
    
    print(f"\n✅ Transactions created: {transactions_created}/{len(scenarios)}")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Demo Database Created Successfully!")
    print("=" * 60)
    print(f"\n📊 Summary:")
    print(f"  • Students: {students_added}")
    print(f"  • Books: {books_added}")
    print(f"  • Transactions: {transactions_created}")
    print(f"    - Active loans: {sum(1 for s in scenarios if s['status'] == 'active')}")
    print(f"    - Overdue: {sum(1 for s in scenarios if s['status'] == 'overdue')}")
    print(f"    - Returned: {sum(1 for s in scenarios if 'returned' in s['status'])}")
    print("\n💡 You can now test all features with this realistic data!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        create_demo_data()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
