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
                academic_year TEXT,
                FOREIGN KEY (enrollment_no) REFERENCES students (enrollment_no),
                FOREIGN KEY (book_id) REFERENCES books (book_id)
            )
        ''')
        
        # Create promotion_history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS promotion_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                enrollment_no TEXT NOT NULL,
                student_name TEXT NOT NULL,
                old_year TEXT NOT NULL,
                new_year TEXT NOT NULL,
                letter_number TEXT,
                academic_year TEXT,
                promotion_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (enrollment_no) REFERENCES students (enrollment_no)
            )
        ''')
        
        # Create academic_years table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS academic_years (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year_name TEXT UNIQUE NOT NULL,
                start_date DATE,
                end_date DATE,
                is_active INTEGER DEFAULT 0,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    
    def update_student(self, enrollment_no, name, email='', phone='', department='', year=''):
        """Update an existing student's information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Check if student exists
            cursor.execute("SELECT id FROM students WHERE enrollment_no = ?", (enrollment_no,))
            if not cursor.fetchone():
                return False, "Student not found"
            
            # Update student information
            cursor.execute('''
                UPDATE students 
                SET name=?, email=?, phone=?, department=?, year=?
                WHERE enrollment_no=?
            ''', (name, email, phone, department, year, enrollment_no))
            conn.commit()
            return True, "Student updated successfully"
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
    
    def update_book(self, book_id, title, author, isbn='', category='', total_copies=1):
        """Update an existing book's information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Check if book exists
            cursor.execute("SELECT available_copies, total_copies FROM books WHERE book_id = ?", (book_id,))
            result = cursor.fetchone()
            if not result:
                return False, "Book not found"
            
            old_available, old_total = result
            
            # Calculate new available copies maintaining the difference
            borrowed_count = old_total - old_available
            new_available = total_copies - borrowed_count
            
            # Prevent setting total copies less than borrowed count
            if new_available < 0:
                return False, f"Cannot set total copies to {total_copies}. {borrowed_count} copies are currently borrowed."
            
            # Update book information
            cursor.execute('''
                UPDATE books 
                SET title=?, author=?, isbn=?, category=?, total_copies=?, available_copies=?
                WHERE book_id=?
            ''', (title, author, isbn, category, total_copies, new_available, book_id))
            conn.commit()
            return True, "Book updated successfully"
        except Exception as e:
            return False, f"Error: {str(e)}"
        finally:
            conn.close()
    
    def borrow_book(self, enrollment_no, book_id, borrow_date, due_date):
        """Record a book borrowing with academic year tracking.
        borrow_date: string YYYY-MM-DD (user-selected or default today)
        due_date: string YYYY-MM-DD
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Check student's eligibility: Pass Out students cannot borrow
            cursor.execute('SELECT year FROM students WHERE enrollment_no = ?', (enrollment_no,))
            srow = cursor.fetchone()
            if not srow:
                return False, "Student not found"
            year_val = (srow[0] or '').strip().lower()
            if year_val in ("pass out", "passout"):
                return False, "Pass Out students cannot borrow books"

            # Check if book is available
            cursor.execute('SELECT available_copies FROM books WHERE book_id = ?', (book_id,))
            result = cursor.fetchone()
            if not result or result[0] <= 0:
                return False, "Book not available"
            
            # Student existence implicitly checked above
            
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

            # Get active academic year
            academic_year = self.get_active_academic_year()

            # Add borrow record using provided borrow_date and academic year
            cursor.execute('''
                INSERT INTO borrow_records (enrollment_no, book_id, borrow_date, due_date, academic_year)
                VALUES (?, ?, ?, ?, ?)
            ''', (enrollment_no, book_id, borrow_date, due_date, academic_year))
            
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
        """Get list of students with optional search - newest first"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if search_term:
            cursor.execute('''
                SELECT * FROM students 
                WHERE enrollment_no LIKE ? OR name LIKE ? OR email LIKE ? OR department LIKE ?
                ORDER BY id DESC
            ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        else:
            cursor.execute('SELECT * FROM students ORDER BY id DESC')
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

    def get_next_book_id(self):
        """Generate next book ID automatically as simple numbers (1, 2, 3, etc.)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Get all existing Book IDs
            cursor.execute('SELECT book_id FROM books')
            all_ids = cursor.fetchall()
            
            # Extract numeric IDs
            numeric_ids = []
            for row in all_ids:
                try:
                    numeric_ids.append(int(row[0]))
                except:
                    pass
            
            # Find the smallest available number starting from 1
            if not numeric_ids:
                return "1"
            
            # Sort and find first gap
            numeric_ids.sort()
            for i in range(1, max(numeric_ids) + 2):
                if i not in numeric_ids:
                    return str(i)
            
            return str(max(numeric_ids) + 1)
        except:
            return "1"
        finally:
            conn.close()
    
    def add_promotion_history(self, enrollment_no, student_name, old_year, new_year, letter_number, academic_year):
        """Add a record to promotion history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO promotion_history (enrollment_no, student_name, old_year, new_year, letter_number, academic_year)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (enrollment_no, student_name, old_year, new_year, letter_number, academic_year))
            conn.commit()
            return True, "Promotion recorded"
        except Exception as e:
            return False, f"Error: {str(e)}"
        finally:
            conn.close()
    
    def get_promotion_history(self):
        """Get all promotion history records"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT enrollment_no, student_name, old_year, new_year, letter_number, 
                       academic_year, promotion_date
                FROM promotion_history
                ORDER BY promotion_date DESC
            ''')
            return cursor.fetchall()
        except:
            return []
        finally:
            conn.close()
    
    def undo_last_promotion(self):
        """Undo the last promotion activity (revert ALL students promoted in the last batch)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Get the most recent promotion date/time
            cursor.execute('''
                SELECT promotion_date
                FROM promotion_history
                ORDER BY promotion_date DESC
                LIMIT 1
            ''')
            last_promo_time = cursor.fetchone()
            
            if not last_promo_time:
                return False, "No promotion to undo"
            
            last_time = last_promo_time[0]
            
            # Get ALL promotion records from that batch (same timestamp)
            cursor.execute('''
                SELECT enrollment_no, old_year, new_year
                FROM promotion_history
                WHERE promotion_date = ?
            ''', (last_time,))
            
            all_last_promos = cursor.fetchall()
            
            if not all_last_promos:
                return False, "No promotion records found"
            
            # Revert all students from that promotion
            count = 0
            for enrollment_no, old_year, new_year in all_last_promos:
                cursor.execute('''
                    UPDATE students
                    SET year = ?
                    WHERE enrollment_no = ?
                ''', (old_year, enrollment_no))
                count += 1
            
            # Delete all promotion records from that batch
            cursor.execute('''
                DELETE FROM promotion_history
                WHERE promotion_date = ?
            ''', (last_time,))
            
            conn.commit()
            return True, f"Undone promotion for {count} student(s) from last activity"
        except Exception as e:
            return False, f"Error: {str(e)}"
        finally:
            conn.close()
    
    def create_academic_year(self, year_name):
        """Create a new academic year"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Deactivate all other academic years
            cursor.execute('UPDATE academic_years SET is_active = 0')
            
            # Insert new academic year as active
            cursor.execute('''
                INSERT INTO academic_years (year_name, is_active)
                VALUES (?, 1)
            ''', (year_name,))
            conn.commit()
            return True, f"Academic year {year_name} created"
        except sqlite3.IntegrityError:
            # Year already exists, just activate it
            cursor.execute('''
                UPDATE academic_years SET is_active = 1 WHERE year_name = ?
            ''', (year_name,))
            cursor.execute('''
                UPDATE academic_years SET is_active = 0 WHERE year_name != ?
            ''', (year_name,))
            conn.commit()
            return True, f"Academic year {year_name} activated"
        except Exception as e:
            return False, f"Error: {str(e)}"
        finally:
            conn.close()
    
    def get_active_academic_year(self):
        """Get the current active academic year"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT year_name FROM academic_years WHERE is_active = 1 LIMIT 1')
            result = cursor.fetchone()
            return result[0] if result else None
        except:
            return None
        finally:
            conn.close()
    
    def get_all_academic_years(self):
        """Get all academic years"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT year_name FROM academic_years ORDER BY created_date DESC')
            return [row[0] for row in cursor.fetchall()]
        except:
            return []
        finally:
            conn.close()


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