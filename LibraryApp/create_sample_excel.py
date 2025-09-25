import pandas as pd
import os

def create_sample_excel_files():
    """Create sample Excel files for students and books import"""
    
    # Sample Students Data with mandatory columns (enrollment_no and name)
    students_data = {
        'enrollment_no': [
            '24210270230',
            '24210270231', 
            '24210270232',
            '24210270233',
            '24210270234'
        ],
        'name': [
            'Yash Vijay Date',
            'Rohit Kumar Sharma',
            'Priya Singh Patel',
            'Arjun Reddy Nair', 
            'Sneha Anil Gupta'
        ],
        'email': [
            'yash.date@example.com',
            'rohit.sharma@example.com',
            'priya.patel@example.com',
            'arjun.nair@example.com',
            'sneha.gupta@example.com'
        ],
        'phone': [
            '9876543210',
            '9876543211',
            '9876543212',
            '9876543213',
            '9876543214'
        ],
        'department': [
            'Computer',
            'Computer', 
            'Computer',
            'Computer',
            'Computer'
        ],
        'year': [
            '2nd Year',
            '1st Year',
            '3rd Year',
            '2nd Year',
            '4th Year'
        ]
    }
    
    # Sample Books Data with mandatory columns (book_id and title)
    books_data = {
        'book_id': [
            'CS001',
            'CS002',
            'CS003', 
            'CS004',
            'CS005'
        ],
        'title': [
            'Introduction to Python Programming',
            'Data Structures and Algorithms',
            'Database Management Systems',
            'Computer Networks Fundamentals',
            'Software Engineering Principles'
        ],
        'author': [
            'John Smith',
            'Alice Johnson',
            'Robert Brown',
            'Emily Davis',
            'Michael Wilson'
        ],
        'isbn': [
            '978-0123456789',
            '978-0123456790',
            '978-0123456791',
            '978-0123456792',
            '978-0123456793'
        ],
        'category': [
            'Technology',
            'Technology',
            'Technology',
            'Technology',
            'Technology'
        ],
        'total_copies': [
            5,
            3,
            7,
            4,
            6
        ]
    }
    
    # Create DataFrames
    students_df = pd.DataFrame(students_data)
    books_df = pd.DataFrame(books_data)
    
    # Save to Excel files
    students_file = 'sample_students.xlsx'
    books_file = 'sample_books.xlsx'
    
    students_df.to_excel(students_file, index=False, engine='openpyxl')
    books_df.to_excel(books_file, index=False, engine='openpyxl')
    
    print("✅ Sample Excel files created successfully!")
    print(f"📄 Students file: {os.path.abspath(students_file)}")
    print(f"📄 Books file: {os.path.abspath(books_file)}")
    print()
    print("📋 Students Excel Structure:")
    print("- enrollment_no (MANDATORY)")
    print("- name (MANDATORY)")
    print("- email (optional)")
    print("- phone (optional)")
    print("- department (optional)")
    print("- year (optional)")
    print()
    print("📚 Books Excel Structure:")
    print("- book_id (MANDATORY)")
    print("- title (MANDATORY)")
    print("- author (optional)")
    print("- isbn (optional)")
    print("- category (optional)")
    print("- total_copies (optional, defaults to 1)")

if __name__ == "__main__":
    create_sample_excel_files()