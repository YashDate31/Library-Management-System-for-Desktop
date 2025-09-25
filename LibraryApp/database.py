import sqlite3
import os
import sys
from datetime import datetime

class Database:
    def __init__(self):
        # Create database in a persistent location
        # For executable, use the directory where the executable is located
        if hasattr(sys, '_MEIPASS'):
            # Running as PyInstaller executable
            self.db_path = os.path.join(os.path.dirname(sys.executable), 'library.db')
        else:
            # Running as script
            self.db_path = os.path.join(os.path.dirname(__file__), 'library.db')
        
        print(f"Database will be created at: {self.db_path}")
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create students table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
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
        
        # Create books table
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
        
        # Create borrow_records table
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
        
    # No automatic sample data insertion (clean production build)
    
    def add_student(self, enrollment_no, name, email='', phone='', department='', year=''):
        """Add a new student to the database"""
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
    
    def remove_student(self, enrollment_no):
        """Remove a student from the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Check if student has any borrowed books
            cursor.execute("SELECT COUNT(*) FROM borrow_records WHERE enrollment_no = ? AND status = 'borrowed'", (enrollment_no,))
            borrowed_count = cursor.fetchone()[0]
            
            if borrowed_count > 0:
                return False, "Cannot remove student with borrowed books. Please return all books first."
            
            # Check if student exists
            cursor.execute("SELECT name FROM students WHERE enrollment_no = ?", (enrollment_no,))
            student = cursor.fetchone()
            if not student:
                return False, "Student not found"
            
            student_name = student[0]
            
            # Remove student
            cursor.execute("DELETE FROM students WHERE enrollment_no = ?", (enrollment_no,))
            conn.commit()
            
            if cursor.rowcount > 0:
                return True, f"Student '{student_name}' removed successfully"
            else:
                return False, "Failed to remove student"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
        finally:
            conn.close()
    
    def add_book(self, book_id, title, author, isbn='', category='', total_copies=1):
        """Add a new book to the database"""
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
    
    def borrow_book(self, enrollment_no, book_id, borrow_date, due_date):
        """Record a book borrowing.
        borrow_date: string YYYY-MM-DD (user-selected or default today)
        due_date: string YYYY-MM-DD
        """
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
            
            # Validate provided dates and enforce exactly 7-day loan period
            try:
                bd_obj = datetime.strptime(borrow_date, '%Y-%m-%d')
                dd_obj = datetime.strptime(due_date, '%Y-%m-%d')
                diff_days = (dd_obj - bd_obj).days
                if diff_days < 0:
                    return False, "Due date cannot be before borrow date"
                if diff_days != 7:
                    return False, "Loan period must be exactly 7 days (teacher requirement)"
            except ValueError:
                return False, "Invalid date format (expected YYYY-MM-DD)"

            # Add borrow record using provided borrow_date
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
    
    def return_book(self, enrollment_no, book_id, return_date=None):
        """Record a book return.
        return_date: optional string YYYY-MM-DD; if None uses today.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if return_date is None or not return_date.strip():
                return_date = datetime.now().strftime('%Y-%m-%d')
            # Validate date format
            try:
                datetime.strptime(return_date, '%Y-%m-%d')
            except ValueError:
                return False, "Invalid return date format"
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
        """Get list of students with optional search"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if search_term:
            cursor.execute('''
                SELECT * FROM students 
                WHERE enrollment_no LIKE ? OR name LIKE ? OR email LIKE ? OR department LIKE ?
            ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        else:
            cursor.execute('SELECT * FROM students')
        result = cursor.fetchall()
        conn.close()
        return result
    
    def get_books(self, search_term=''):
        """Get list of books with optional search"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if search_term:
            cursor.execute('''
                SELECT * FROM books 
                WHERE book_id LIKE ? OR title LIKE ? OR author LIKE ? OR category LIKE ?
            ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        else:
            cursor.execute('SELECT * FROM books')
        result = cursor.fetchall()
        conn.close()
        return result
    
    def get_borrowed_books(self):
        """Get list of currently borrowed books"""
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
        """Delete a student"""
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
        """Delete a book"""
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
    
    # Removed add_sample_data_if_empty to keep production database empty on first run

    def clear_all_data(self):
        """Completely remove all students, books and borrow records.
        Returns (success: bool, message: str).
        Order matters due to foreign key references: borrow_records first, then books & students.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Disable foreign key constraints temporarily (just in case)
            try:
                cursor.execute('PRAGMA foreign_keys = OFF;')
            except Exception:
                pass

            cursor.execute('DELETE FROM borrow_records')
            cursor.execute('DELETE FROM books')
            cursor.execute('DELETE FROM students')
            conn.commit()
            return True, "All data cleared successfully"
        except Exception as e:
            return False, f"Error clearing data: {e}"
        finally:
            try:
                cursor.execute('PRAGMA foreign_keys = ON;')
            except Exception:
                pass
            conn.close()