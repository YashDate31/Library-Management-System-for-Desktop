# ===============================================================================
# FRESH BUILD SCRIPT - Library Management System v4.0
# Creates everything from scratch - database, UI, all features
# ===============================================================================

Write-Host "🚀 Building Fresh Library Management System v4.0" -ForegroundColor Cyan
Write-Host "Creating all files from scratch..." -ForegroundColor White
Write-Host ""

# Navigate to LibraryApp directory
Set-Location "LibraryApp"

Write-Host "📝 Step 1: Creating database.py..." -ForegroundColor Yellow

# Create database.py
@'
import sqlite3
import os
import sys
from datetime import datetime

class Database:
    def __init__(self):
        """Initialize database with fresh, clean structure"""
        # Create database in current directory
        if hasattr(sys, '_MEIPASS'):
            # Running as PyInstaller executable
            self.db_path = os.path.join(os.path.dirname(sys.executable), 'library.db')
        else:
            # Running as script
            self.db_path = os.path.join(os.path.dirname(__file__), 'library.db')
        
        print(f"📊 Database location: {self.db_path}")
        self.init_database()
        self.add_sample_data_if_empty()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database with clean tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Students table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                enrollment_no TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                department TEXT DEFAULT 'Computer',
                year TEXT,
                date_registered DATE DEFAULT CURRENT_DATE
            )
        ''')
        
        # Books table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT,
                category TEXT,
                total_copies INTEGER DEFAULT 1,
                available_copies INTEGER DEFAULT 1,
                date_added DATE DEFAULT CURRENT_DATE
            )
        ''')
        
        # Borrow records table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS borrow_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                enrollment_no TEXT NOT NULL,
                book_id TEXT NOT NULL,
                borrow_date DATE NOT NULL,
                due_date DATE NOT NULL,
                return_date DATE,
                status TEXT DEFAULT 'borrowed',
                FOREIGN KEY (enrollment_no) REFERENCES students (enrollment_no),
                FOREIGN KEY (book_id) REFERENCES books (book_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database tables created successfully!")
    
    def add_student(self, enrollment_no, name, email='', phone='', department='Computer', year=''):
        """Add new student"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO students (enrollment_no, name, email, phone, department, year)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (enrollment_no, name, email, phone, department, year))
            conn.commit()
            return True, "Student added successfully"
        except sqlite3.IntegrityError:
            return False, "Enrollment Number already exists"
        except Exception as e:
            return False, f"Error: {str(e)}"
        finally:
            conn.close()
    
    def add_book(self, book_id, title, author, isbn='', category='', total_copies=1):
        """Add new book"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO books (book_id, title, author, isbn, category, total_copies, available_copies)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (book_id, title, author, isbn, category, total_copies, total_copies))
            conn.commit()
            return True, "Book added successfully"
        except sqlite3.IntegrityError:
            return False, "Book ID already exists"
        except Exception as e:
            return False, f"Error: {str(e)}"
        finally:
            conn.close()
    
    def borrow_book(self, enrollment_no, book_id, due_date):
        """Record book borrowing"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Check if book is available
            cursor.execute('SELECT available_copies FROM books WHERE book_id = ?', (book_id,))
            result = cursor.fetchone()
            if not result or result[0] <= 0:
                return False, "Book not available"
            
            # Check if student exists
            cursor.execute('SELECT id FROM students WHERE enrollment_no = ?', (enrollment_no,))
            if not cursor.fetchone():
                return False, "Student not found"
            
            # Add borrow record
            borrow_date = datetime.now().strftime('%Y-%m-%d')
            cursor.execute('''
                INSERT INTO borrow_records (enrollment_no, book_id, borrow_date, due_date)
                VALUES (?, ?, ?, ?)
            ''', (enrollment_no, book_id, borrow_date, due_date))
            
            # Update available copies
            cursor.execute('''
                UPDATE books SET available_copies = available_copies - 1 
                WHERE book_id = ?
            ''', (book_id,))
            
            conn.commit()
            return True, "Book borrowed successfully"
        except Exception as e:
            return False, f"Error: {str(e)}"
        finally:
            conn.close()
    
    def return_book(self, enrollment_no, book_id):
        """Record book return"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Update borrow record
            return_date = datetime.now().strftime('%Y-%m-%d')
            cursor.execute('''
                UPDATE borrow_records 
                SET return_date = ?, status = 'returned'
                WHERE enrollment_no = ? AND book_id = ? AND status = 'borrowed'
            ''', (return_date, enrollment_no, book_id))
            
            if cursor.rowcount == 0:
                return False, "No active borrowing record found"
            
            # Update available copies
            cursor.execute('''
                UPDATE books SET available_copies = available_copies + 1 
                WHERE book_id = ?
            ''', (book_id,))
            
            conn.commit()
            return True, "Book returned successfully"
        except Exception as e:
            return False, f"Error: {str(e)}"
        finally:
            conn.close()
    
    def get_students(self, search_term=''):
        """Get students list"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if search_term:
            cursor.execute('''
                SELECT * FROM students 
                WHERE enrollment_no LIKE ? OR name LIKE ? OR email LIKE ?
            ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        else:
            cursor.execute('SELECT * FROM students')
        result = cursor.fetchall()
        conn.close()
        return result
    
    def get_books(self, search_term=''):
        """Get books list"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if search_term:
            cursor.execute('''
                SELECT * FROM books 
                WHERE book_id LIKE ? OR title LIKE ? OR author LIKE ?
            ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        else:
            cursor.execute('SELECT * FROM books')
        result = cursor.fetchall()
        conn.close()
        return result
    
    def get_borrowed_books(self):
        """Get currently borrowed books"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT br.enrollment_no, s.name, s.department, s.year, br.book_id, b.title, b.author, 
                   br.borrow_date, br.due_date
            FROM borrow_records br
            JOIN students s ON br.enrollment_no = s.enrollment_no
            JOIN books b ON br.book_id = b.book_id
            WHERE br.status = 'borrowed'
            ORDER BY br.due_date
        ''')
        result = cursor.fetchall()
        conn.close()
        return result
    
    def delete_student(self, enrollment_no):
        """Delete student"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Check if student has borrowed books
            cursor.execute('''
                SELECT COUNT(*) FROM borrow_records 
                WHERE enrollment_no = ? AND status = 'borrowed'
            ''', (enrollment_no,))
            if cursor.fetchone()[0] > 0:
                return False, "Cannot delete student with borrowed books"
            
            cursor.execute('DELETE FROM students WHERE enrollment_no = ?', (enrollment_no,))
            if cursor.rowcount == 0:
                return False, "Student not found"
            
            conn.commit()
            return True, "Student deleted successfully"
        except Exception as e:
            return False, f"Error: {str(e)}"
        finally:
            conn.close()
    
    def delete_book(self, book_id):
        """Delete book"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Check if book is borrowed
            cursor.execute('''
                SELECT COUNT(*) FROM borrow_records 
                WHERE book_id = ? AND status = 'borrowed'
            ''', (book_id,))
            if cursor.fetchone()[0] > 0:
                return False, "Cannot delete book that is currently borrowed"
            
            cursor.execute('DELETE FROM books WHERE book_id = ?', (book_id,))
            if cursor.rowcount == 0:
                return False, "Book not found"
            
            conn.commit()
            return True, "Book deleted successfully"
        except Exception as e:
            return False, f"Error: {str(e)}"
        finally:
            conn.close()
    
    def add_sample_data_if_empty(self):
        """Add sample data if database is empty"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Check if any data exists
            cursor.execute('SELECT COUNT(*) FROM students')
            student_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM books')
            book_count = cursor.fetchone()[0]
            
            # Add sample data only if database is empty
            if student_count == 0 and book_count == 0:
                # Sample students
                sample_students = [
                    ('24210270230', 'Yash Vijay Date', 'yash@example.com', '9876543210', 'Computer', '2nd Year'),
                    ('24210270231', 'John Doe', 'john@example.com', '9876543211', 'Computer', '3rd Year'),
                    ('24210270232', 'Jane Smith', 'jane@example.com', '9876543212', 'Computer', '1st Year'),
                ]
                
                for student in sample_students:
                    cursor.execute('''
                        INSERT INTO students (enrollment_no, name, email, phone, department, year)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', student)
                
                # Sample books
                sample_books = [
                    ('B001', 'Introduction to Programming', 'John Smith', '978-0123456789', 'Technology', 5, 5),
                    ('B002', 'Database Systems', 'Mary Johnson', '978-0987654321', 'Technology', 3, 3),
                    ('B003', 'Engineering Mathematics', 'Robert Brown', '978-0456789123', 'Mathematics', 4, 4),
                    ('B004', 'Data Structures', 'Alice Wilson', '978-0789123456', 'Technology', 2, 2),
                ]
                
                for book in sample_books:
                    cursor.execute('''
                        INSERT INTO books (book_id, title, author, isbn, category, total_copies, available_copies)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', book)
                
                conn.commit()
                print("✅ Sample data added to database")
                
        except Exception as e:
            print(f"❌ Error adding sample data: {str(e)}")
        finally:
            conn.close()
'@ | Out-File -FilePath "database.py" -Encoding UTF8

Write-Host "✅ database.py created!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Step 2: Creating requirements.txt..." -ForegroundColor Yellow

# Create requirements.txt
@'
tkinter
pandas>=1.5.0
openpyxl>=3.0.0
pyinstaller>=5.0.0
'@ | Out-File -FilePath "requirements.txt" -Encoding UTF8

Write-Host "✅ requirements.txt created!" -ForegroundColor Green
Write-Host ""

Write-Host "🎯 Fresh project structure created successfully!" -ForegroundColor Green
Write-Host "📁 Files created:" -ForegroundColor White
Write-Host "  • database.py (complete SQLite database layer)" -ForegroundColor Gray
Write-Host "  • requirements.txt (Python dependencies)" -ForegroundColor Gray
Write-Host ""
Write-Host "⏭️  Next: Run BUILD_MAIN_APP.ps1 to create the UI and complete the app" -ForegroundColor Yellow