#!/usr/bin/env python3
"""
Demo Data Generator for Library Management System
Creates 100+ students and 40+ books with realistic data for comprehensive testing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import Database
from datetime import datetime, timedelta
import random

def create_demo_data():
    """Create comprehensive demo data for testing all features"""
    db = Database()
    print("=" * 60)
    print("CREATING DEMO DATA FOR LIBRARY MANAGEMENT SYSTEM")
    print("=" * 60)
    
    # ========== STUDENTS DATA (110 students) ==========
    print("\n[1/4] Adding 110 Students...")
    
    # First names pool
    first_names_male = [
        "Aarav", "Arjun", "Aditya", "Aryan", "Sai", "Vihaan", "Krishna", "Vivaan",
        "Atharv", "Aayush", "Dhruv", "Shaurya", "Reyansh", "Kian", "Advait",
        "Vedant", "Om", "Pranav", "Arnav", "Ayaan", "Kartik", "Rohan", "Harsh",
        "Ishaan", "Parth", "Dev", "Tanish", "Aadhya", "Rudra", "Samar"
    ]
    
    first_names_female = [
        "Aadhya", "Ananya", "Diya", "Pari", "Saanvi", "Aaradhya", "Navya", "Myra",
        "Aanya", "Sara", "Kiara", "Riya", "Isha", "Avni", "Anaya", "Prisha",
        "Siya", "Shanaya", "Vanya", "Zara", "Anika", "Kavya", "Nidhi", "Shriya",
        "Tara", "Ishita", "Jiya", "Rhea", "Palak", "Simran"
    ]
    
    # Last names pool
    last_names = [
        "Sharma", "Patel", "Singh", "Kumar", "Desai", "Reddy", "Shah", "Joshi",
        "Verma", "Gupta", "Mehta", "Kulkarni", "Rao", "Nair", "Iyer", "Pillai",
        "Chopra", "Malhotra", "Kapoor", "Khan", "Agarwal", "Bansal", "Saxena",
        "Pandey", "Mishra", "Sinha", "Chaudhary", "Thakur", "Bose", "Das",
        "Ghosh", "Mukherjee", "Chatterjee", "Roy", "Sen", "Dutta", "Bhatt",
        "Trivedi", "Jain", "Arora"
    ]
    
    # Divisions
    divisions = ["A", "B", "C"]
    
    students_added = 0
    students_skipped = 0
    
    # Generate 110 students across three years
    enrollment_counter = 24210270001
    
    for year_name, year_count in [("1st Year", 40), ("2nd Year", 40), ("3rd Year", 30)]:
        for i in range(year_count):
            # Randomly choose gender and name
            if random.random() > 0.5:
                name = f"{random.choice(first_names_male)} {random.choice(last_names)}"
            else:
                name = f"{random.choice(first_names_female)} {random.choice(last_names)}"
            
            enrollment_no = str(enrollment_counter)
            email = f"{name.lower().replace(' ', '.')}@student.gpa.edu" if random.random() > 0.3 else ""
            phone = f"9{random.randint(100000000, 999999999)}" if random.random() > 0.2 else ""
            department = "Computer"
            
            success, message = db.add_student(enrollment_no, name, email, phone, department, year_name)
            if success:
                students_added += 1
            else:
                students_skipped += 1
            
            enrollment_counter += 1
    
    print(f"   ✓ Added: {students_added} students")
    print(f"   ✗ Skipped: {students_skipped} students (duplicates)")
    
    # ========== BOOKS DATA (45 books) ==========
    print("\n[2/4] Adding 45 Books...")
    
    books_data = [
        # Core CS Books (8)
        ("1", "Introduction to Algorithms", "Thomas H. Cormen", "978-0262033848", "Core CS", 5),
        ("2", "Computer Networks", "Andrew S. Tanenbaum", "978-0132126953", "Core CS", 4),
        ("3", "Operating System Concepts", "Abraham Silberschatz", "978-1118063330", "Core CS", 4),
        ("4", "Database System Concepts", "Abraham Silberschatz", "978-0078022159", "Core CS", 3),
        ("5", "Data Structures and Algorithms", "Narasimha Karumanchi", "978-8193245279", "Core CS", 5),
        ("6", "Theory of Computation", "Michael Sipser", "978-1133187790", "Core CS", 3),
        ("7", "Computer Organization and Design", "David A. Patterson", "978-0124077263", "Core CS", 3),
        ("8", "Discrete Mathematics", "Kenneth H. Rosen", "978-0073383095", "Core CS", 4),
        
        # Programming Books (10)
        ("9", "Python Crash Course", "Eric Matthes", "978-1593279288", "Programming", 6),
        ("10", "Clean Code", "Robert C. Martin", "978-0132350884", "Programming", 4),
        ("11", "Head First Java", "Kathy Sierra", "978-0596009205", "Programming", 5),
        ("12", "Effective Java", "Joshua Bloch", "978-0134685991", "Programming", 3),
        ("13", "C Programming Language", "Brian W. Kernighan", "978-0131103627", "Programming", 4),
        ("14", "JavaScript: The Good Parts", "Douglas Crockford", "978-0596517748", "Programming", 3),
        ("15", "Design Patterns", "Erich Gamma", "978-0201633612", "Programming", 3),
        ("16", "The Pragmatic Programmer", "David Thomas", "978-0135957059", "Programming", 4),
        ("17", "Code Complete", "Steve McConnell", "978-0735619678", "Programming", 3),
        ("18", "Python for Data Analysis", "Wes McKinney", "978-1491957660", "Programming", 4),
        
        # Web Development (6)
        ("19", "HTML and CSS: Design and Build Websites", "Jon Duckett", "978-1118008189", "Web Development", 5),
        ("20", "Learning Web Design", "Jennifer Robbins", "978-1491960202", "Web Development", 4),
        ("21", "Node.js Design Patterns", "Mario Casciaro", "978-1839214110", "Web Development", 3),
        ("22", "React Up and Running", "Stoyan Stefanov", "978-1492051466", "Web Development", 3),
        ("23", "Full Stack Development", "Nitin Pandit", "978-9389845426", "Web Development", 4),
        ("24", "RESTful Web APIs", "Leonard Richardson", "978-1449358068", "Web Development", 2),
        
        # Database Books (4)
        ("25", "SQL in 10 Minutes", "Ben Forta", "978-0135182796", "Database", 5),
        ("26", "MongoDB: The Definitive Guide", "Shannon Bradshaw", "978-1491954461", "Database", 3),
        ("27", "Learning MySQL", "Seyed Tahaghoghi", "978-0596008642", "Database", 4),
        ("28", "Database Design and Relational Theory", "C.J. Date", "978-1449328016", "Database", 2),
        
        # AI/ML Books (5)
        ("29", "Hands-On Machine Learning", "Aurélien Géron", "978-1492032649", "AI/ML", 4),
        ("30", "Deep Learning", "Ian Goodfellow", "978-0262035613", "AI/ML", 3),
        ("31", "Pattern Recognition and Machine Learning", "Christopher Bishop", "978-0387310732", "AI/ML", 2),
        ("32", "Artificial Intelligence: A Modern Approach", "Stuart Russell", "978-0134610993", "AI/ML", 3),
        ("33", "Python Machine Learning", "Sebastian Raschka", "978-1789955750", "AI/ML", 4),
        
        # Networking Books (3)
        ("34", "Computer Networking: A Top-Down Approach", "James Kurose", "978-0133594140", "Networking", 4),
        ("35", "TCP/IP Illustrated", "W. Richard Stevens", "978-0201633467", "Networking", 2),
        ("36", "Network Security Essentials", "William Stallings", "978-0134527338", "Networking", 3),
        
        # Software Engineering (4)
        ("37", "Software Engineering", "Ian Sommerville", "978-0133943030", "Software Engineering", 4),
        ("38", "The Mythical Man-Month", "Frederick Brooks", "978-0201835953", "Software Engineering", 3),
        ("39", "Continuous Delivery", "Jez Humble", "978-0321601919", "Software Engineering", 2),
        ("40", "Agile Software Development", "Robert C. Martin", "978-0135974445", "Software Engineering", 3),
        
        # Project Guides (3)
        ("41", "Project Management for IT", "Joseph Phillips", "978-1259861536", "Project Guides", 3),
        ("42", "Final Year Project Guide", "Dr. R.K. Sharma", "978-8193456789", "Project Guides", 5),
        ("43", "Research Methodology", "C.R. Kothari", "978-8122427806", "Project Guides", 4),
        
        # Competitive Programming (2)
        ("44", "Competitive Programming 3", "Steven Halim", "978-5800083125", "Competitive Programming", 2),
        ("45", "Cracking the Coding Interview", "Gayle Laakmann", "978-0984782857", "Competitive Programming", 4),
    ]
    
    books_added = 0
    books_skipped = 0
    
    for book_id, title, author, isbn, category, copies in books_data:
        success, message = db.add_book(book_id, title, author, isbn, category, copies)
        if success:
            books_added += 1
        else:
            books_skipped += 1
    
    print(f"   ✓ Added: {books_added} books")
    print(f"   ✗ Skipped: {books_skipped} books (duplicates)")
    
    # ========== TRANSACTIONS (60 borrow records) ==========
    print("\n[3/4] Creating 60 Transaction Records...")
    
    # Get all students and books
    students = db.get_students()
    books = db.get_books()
    
    transactions_created = 0
    transactions_returned = 0
    
    # Create varied transactions
    for i in range(60):
        # Pick random student and book
        student = random.choice(students)
        book = random.choice(books)
        
        enrollment_no = student[1]  # enrollment_no
        book_id = book[1]  # book_id
        
        # Varied borrow dates (past 90 days)
        days_ago = random.randint(1, 90)
        borrow_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        due_date = (datetime.now() - timedelta(days=days_ago) + timedelta(days=7)).strftime('%Y-%m-%d')
        
        # Try to borrow
        success, message = db.borrow_book(enrollment_no, book_id, borrow_date, due_date)
        
        if success:
            transactions_created += 1
            
            # Return 40% of books (some on time, some late)
            if random.random() < 0.4:
                # Calculate return date (some overdue, some on time)
                if random.random() < 0.3:  # 30% overdue
                    return_days_late = random.randint(1, 10)
                    return_date = (datetime.strptime(due_date, '%Y-%m-%d') + timedelta(days=return_days_late)).strftime('%Y-%m-%d')
                else:  # 70% on time or early
                    return_days_early = random.randint(0, 6)
                    return_date = (datetime.strptime(due_date, '%Y-%m-%d') - timedelta(days=return_days_early)).strftime('%Y-%m-%d')
                
                return_success, return_message = db.return_book(enrollment_no, book_id, return_date)
                if return_success:
                    transactions_returned += 1
    
    print(f"   ✓ Created: {transactions_created} borrow transactions")
    print(f"   ✓ Returned: {transactions_returned} books")
    print(f"   → Active: {transactions_created - transactions_returned} books currently borrowed")
    
    # ========== ACADEMIC YEAR ==========
    print("\n[4/4] Setting up Academic Year...")
    
    current_year = datetime.now().year
    academic_year = f"{current_year}-{current_year + 1}"
    success, message = db.create_academic_year(academic_year)
    
    if success:
        print(f"   ✓ Active Academic Year: {academic_year}")
    else:
        print(f"   ⚠ Academic Year: {message}")
    
    # ========== SUMMARY ==========
    print("\n" + "=" * 60)
    print("DEMO DATA CREATION COMPLETE!")
    print("=" * 60)
    
    # Get final statistics
    all_students = db.get_students()
    all_books = db.get_books()
    all_borrowed = db.get_borrowed_books()
    
    print(f"\n📊 FINAL STATISTICS:")
    print(f"   Students: {len(all_students)}")
    print(f"   Books: {len(all_books)} titles")
    
    # Count total copies
    total_copies = sum(book[6] for book in all_books)  # book[6] is total_copies
    available_copies = sum(book[7] for book in all_books)  # book[7] is available_copies
    print(f"   Total Book Copies: {total_copies}")
    print(f"   Available Copies: {available_copies}")
    print(f"   Currently Borrowed: {len(all_borrowed)}")
    
    # Count students by year
    year_1 = len([s for s in all_students if s[6] == "1st Year"])
    year_2 = len([s for s in all_students if s[6] == "2nd Year"])
    year_3 = len([s for s in all_students if s[6] == "3rd Year"])
    pass_out = len([s for s in all_students if s[6] == "Pass Out"])
    
    print(f"\n   Year-wise Distribution:")
    print(f"   • 1st Year: {year_1}")
    print(f"   • 2nd Year: {year_2}")
    print(f"   • 3rd Year: {year_3}")
    print(f"   • Pass Out: {pass_out}")
    
    print("\n✅ Demo data is ready for comprehensive testing!")
    print("\n💡 You can now test:")
    print("   - Search & Filter (100+ students)")
    print("   - Book availability tracking")
    print("   - Transaction management")
    print("   - Overdue detection & fines")
    print("   - Email notifications (add emails to test)")
    print("   - Analytics & charts")
    print("   - Student promotion")
    print("   - Excel import/export")
    print("   - All CRUD operations")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    print("\n⚠️  WARNING: This will add demo data to your database!")
    print("   Make sure you have a backup if needed.\n")
    
    response = input("Do you want to proceed? (yes/no): ").strip().lower()
    
    if response in ['yes', 'y']:
        create_demo_data()
    else:
        print("\n❌ Operation cancelled.")
