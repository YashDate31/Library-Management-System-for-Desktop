import sqlite3
import os
import sys
from datetime import datetime
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not available, assume env vars are set by system or not needed (local mode)
    pass

# Try importing psycopg2 for PostgreSQL support
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False
    psycopg2 = None
    RealDictCursor = None




class PostgresRow:
    """Wrapper for Postgres dict rows to support both index and key access (like sqlite3.Row)"""
    def __init__(self, data):
        self._data = data
        self._values = list(data.values())
    
    def __getitem__(self, item):
        if isinstance(item, int):
            return self._values[item]
        return self._data[item]
    
    def keys(self):
        return self._data.keys()
    
    def __iter__(self):
        # sqlite3.Row iterates over values
        return iter(self._values)

class PostgresCursorWrapper:
    """
    Wrapper to make psycopg2 cursor behave like sqlite3 cursor.
    - Replaces '?' placeholders with '%s' safely for this specific application context.
    - Supports row_factory style access (dict-like)
    """
    def __init__(self, cursor):
        self.cursor = cursor
        self.rowcount = -1

    def execute(self, sql, params=None):
        # Convert SQLite '?' placeholders to Postgres '%s'
        # NOTE: This is a basic string replacement. It assumes '?' is ONLY used as a placeholder.
        # In a generic library, this would be unsafe (e.g., "SELECT 'Where is he?'").
        # For this Application, we verify that no static SQL contains '?' literals.
        pg_sql = sql.replace('?', '%s')
        
        try:
            if params:
                self.cursor.execute(pg_sql, params)
            else:
                self.cursor.execute(pg_sql)
            self.rowcount = self.cursor.rowcount
            return self.cursor
        except Exception as e:
            # Log error for debugging
            print(f"SQL Error in PostgresWrapper: {e}")
            print(f"Query: {pg_sql}")
            raise e

    def fetchone(self):
        row = self.cursor.fetchone()
        return PostgresRow(row) if row else None

    def fetchall(self):
        rows = self.cursor.fetchall()
        return [PostgresRow(row) for row in rows] if rows else []
        
    def close(self):
        self.cursor.close()

class PostgresConnectionWrapper:
    """Wrapper for Postgres connection to mimic sqlite3 connection"""
    def __init__(self, conn):
        self.conn = conn
    
    def cursor(self):
        return PostgresCursorWrapper(self.conn.cursor(cursor_factory=RealDictCursor))
    
    def commit(self):
        self.conn.commit()
    
    def close(self):
        self.conn.close()
        
    def execute(self, sql, params=None):
        # Shortcut execute support
        cursor = self.cursor()
        cursor.execute(sql, params)
        return cursor


class Database:
    def __init__(self):
        # Check if we should use Cloud DB (PostgreSQL)
        # Only if psycopg2 is available AND DATABASE_URL is set
        self.database_url = os.getenv('DATABASE_URL')
        self.use_cloud = POSTGRES_AVAILABLE and bool(self.database_url)
        
        self.db_path = ""
        
        if self.use_cloud:
            print(f"Database: Using Cloud PostgreSQL")
        else:
            # Fallback to local SQLite
            # Create database in a persistent location
            # For executable, use the directory where the executable is located
            if hasattr(sys, '_MEIPASS'):
                # Running as PyInstaller executable
                self.db_path = os.path.join(os.path.dirname(sys.executable), 'library.db')
            else:
                # Running as script
                self.db_path = os.path.join(os.path.dirname(__file__), 'library.db')
            
            print(f"Database: Using Local SQLite at {self.db_path}")
            
        self.init_database()
    
    def get_connection(self):
        if self.use_cloud:
            try:
                conn = psycopg2.connect(self.database_url)
                return PostgresConnectionWrapper(conn)
            except Exception as e:
                print(f"Cloud DB Connection Failed: {e}. Falling back to clean State if possible, or erroring.")
                # We might want to fallback? But 'Hybrid' implies syncing.
                # For this request, "If DATABASE_URL is missing, fall back". 
                # If present but fails, we usually error out.
                raise e
        else:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            # Enforce foreign keys for SQLite (Postgres does this by default)
            conn.execute('PRAGMA foreign_keys = ON')
            return conn
    
    def create_table_safe(self, cursor, table_name, pg_sql, sqlite_sql):
        """Execute appropriate CREATE TABLE based on backend"""
        if self.use_cloud:
            try:
                cursor.execute(pg_sql)
            except Exception as e:
                # Postgres might throw error if valid table exists but we try to create it?
                # IF NOT EXISTS should handle it.
                print(f"Warning creating table {table_name}: {e}")
        else:
            cursor.execute(sqlite_sql)
            
    def init_database(self):
        """Initialize the database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create tables
        self.create_table_safe(cursor, 'students', '''
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                enrollment_no TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                department TEXT,
                year TEXT,
                date_registered DATE DEFAULT CURRENT_DATE
            )
        ''', sqlite_sql='''
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
        
        self.create_table_safe(cursor, 'books', '''
             CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                book_id TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT,
                category TEXT,
                total_copies INTEGER DEFAULT 1,
                available_copies INTEGER DEFAULT 1,
                date_added DATE DEFAULT CURRENT_DATE
            )
        ''', sqlite_sql='''
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
        
        self.create_table_safe(cursor, 'transactions', '''
            CREATE TABLE IF NOT EXISTS transactions (
                id SERIAL PRIMARY KEY,
                enrollment_no TEXT NOT NULL,
                book_id TEXT NOT NULL,
                borrow_date DATE NOT NULL,
                due_date DATE NOT NULL,
                return_date DATE,
                fine INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                FOREIGN KEY (enrollment_no) REFERENCES students(enrollment_no),
                FOREIGN KEY (book_id) REFERENCES books(book_id)
            )
        ''', sqlite_sql='''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                enrollment_no TEXT NOT NULL,
                book_id TEXT NOT NULL,
                borrow_date DATE NOT NULL,
                due_date DATE NOT NULL,
                return_date DATE,
                fine INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                FOREIGN KEY (enrollment_no) REFERENCES students(enrollment_no),
                FOREIGN KEY (book_id) REFERENCES books(book_id)
            )
        ''')

        # borrow_records (active system)
        self.create_table_safe(cursor, 'borrow_records', '''
             CREATE TABLE IF NOT EXISTS borrow_records (
                id SERIAL PRIMARY KEY,
                enrollment_no TEXT NOT NULL,
                book_id TEXT NOT NULL,
                borrow_date DATE NOT NULL,
                due_date DATE NOT NULL,
                return_date DATE,
                status TEXT DEFAULT 'borrowed',
                fine INTEGER DEFAULT 0,
                academic_year TEXT,
                FOREIGN KEY (enrollment_no) REFERENCES students (enrollment_no) ON DELETE RESTRICT ON UPDATE CASCADE,
                FOREIGN KEY (book_id) REFERENCES books (book_id) ON DELETE RESTRICT ON UPDATE CASCADE
            )
        ''', sqlite_sql='''
             CREATE TABLE IF NOT EXISTS borrow_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                enrollment_no TEXT NOT NULL,
                book_id TEXT NOT NULL,
                borrow_date DATE NOT NULL,
                due_date DATE NOT NULL,
                return_date DATE,
                status TEXT DEFAULT 'borrowed',
                fine INTEGER DEFAULT 0,
                academic_year TEXT,
                FOREIGN KEY (enrollment_no) REFERENCES students (enrollment_no) ON DELETE RESTRICT ON UPDATE CASCADE,
                FOREIGN KEY (book_id) REFERENCES books (book_id) ON DELETE RESTRICT ON UPDATE CASCADE
            )
        ''')
        
        self.create_table_safe(cursor, 'promotion_history', '''
            CREATE TABLE IF NOT EXISTS promotion_history (
                id SERIAL PRIMARY KEY,
                enrollment_no TEXT NOT NULL,
                student_name TEXT NOT NULL,
                old_year TEXT NOT NULL,
                new_year TEXT NOT NULL,
                letter_number TEXT,
                academic_year TEXT,
                promotion_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (enrollment_no) REFERENCES students (enrollment_no) ON DELETE RESTRICT ON UPDATE CASCADE
            )
        ''', sqlite_sql='''
            CREATE TABLE IF NOT EXISTS promotion_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                enrollment_no TEXT NOT NULL,
                student_name TEXT NOT NULL,
                old_year TEXT NOT NULL,
                new_year TEXT NOT NULL,
                letter_number TEXT,
                academic_year TEXT,
                promotion_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (enrollment_no) REFERENCES students (enrollment_no) ON DELETE RESTRICT ON UPDATE CASCADE
            )
        ''')

        self.create_table_safe(cursor, 'academic_years', '''
             CREATE TABLE IF NOT EXISTS academic_years (
                id SERIAL PRIMARY KEY,
                year_name TEXT UNIQUE NOT NULL,
                start_date DATE,
                end_date DATE,
                is_active INTEGER DEFAULT 0,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''', sqlite_sql='''
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
        
        # Migration: Add fine column if it doesn't exist
        # Migration: Add fine column if it doesn't exist (SQLite specific logic usually, but let's check basic columns)
        # For Cloud DB, we assume schema is managed or initially created correct. 
        # But if we need to migrate schema on existing Cloud DB, we check too.
        
        # Check column existence safely
        has_fine = False
        try:
            if self.use_cloud:
                # Postgres check
                cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='borrow_records' AND column_name='fine'")
                if cursor.fetchone():
                    has_fine = True
            else:
                # SQLite check
                cursor.execute("PRAGMA table_info(borrow_records)")
                columns = [col[1] for col in cursor.fetchall()]
                if 'fine' in columns:
                    has_fine = True

            if not has_fine:
                cursor.execute("ALTER TABLE borrow_records ADD COLUMN fine INTEGER DEFAULT 0")
                conn.commit()
                print("Migration: Added 'fine' column to borrow_records table")

        except Exception as e:
            print(f"Migration check warning: {e}")

        
        conn.close()
        
    # No automatic sample data insertion (clean production build)
    
    def add_student(self, enrollment_no, name, email='', phone='', department='', year=''):
        """Add a new student to the database"""
        # Validate required fields
        if not enrollment_no or not enrollment_no.strip():
            return False, "Enrollment number is required"
        if not name or not name.strip():
            return False, "Student name is required"
        
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
    
    def add_book(self, book_id, title, author='', isbn='', category='', total_copies=1):
        """Add a new book to the database"""
        # Validate required fields
        if not book_id or not book_id.strip():
            return False, "Book ID is required"
        if not title or not title.strip():
            return False, "Book title is required"
        # Author is optional - no validation needed
        
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
            
            # Check max books per student limit (enforced at database level for consistency)
            cursor.execute("SELECT COUNT(*) FROM borrow_records WHERE enrollment_no = ? AND status = 'borrowed'", (enrollment_no,))
            current_books = cursor.fetchone()[0]
            # Note: max_books limit is enforced in UI layer with configurable settings
            # Database allows up to reasonable limit (e.g., 20) for flexibility
            if current_books >= 20:
                return False, f"Maximum borrow limit reached ({current_books} books currently borrowed)"
            
            # Student existence implicitly checked above
            
            # Validate provided dates
            try:
                bd_obj = datetime.strptime(borrow_date, '%Y-%m-%d')
                dd_obj = datetime.strptime(due_date, '%Y-%m-%d')
                diff_days = (dd_obj - bd_obj).days
                if diff_days < 0:
                    return False, "Due date cannot be before borrow date"
                if diff_days < 1 or diff_days > 30:
                    return False, "Loan period must be between 1 and 30 days"
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
            
            # Notify waitlist - get book title for notification
            cursor.execute('SELECT title FROM books WHERE book_id = ?', (book_id,))
            book_row = cursor.fetchone()
            if book_row:
                book_title = book_row[0]
                self._notify_waitlist(book_id, book_title)
            
            return True, "Book returned successfully"
        except Exception as e:
            return False, f"Error: {str(e)}"
        finally:
            conn.close()
    
    def _notify_waitlist(self, book_id, book_title):
        """Notify first person on waitlist when book becomes available."""
        import sqlite3
        import os
        
        # Connect to portal.db
        portal_db_path = os.path.join(os.path.dirname(__file__), 'Web-Extension', 'portal.db')
        if not os.path.exists(portal_db_path):
            return
        
        try:
            portal_conn = sqlite3.connect(portal_db_path)
            portal_conn.row_factory = sqlite3.Row
            portal_cursor = portal_conn.cursor()
            
            # Get first person on waitlist who hasn't been notified
            portal_cursor.execute("""
                SELECT id, enrollment_no, book_title 
                FROM book_waitlist 
                WHERE book_id = ? AND notified = 0 
                ORDER BY created_at ASC 
                LIMIT 1
            """, (book_id,))
            
            waitlist_entry = portal_cursor.fetchone()
            if not waitlist_entry:
                portal_conn.close()
                return
            
            waitlist_id = waitlist_entry['id']
            enrollment_no = waitlist_entry['enrollment_no']
            
            # Create notification
            portal_cursor.execute("""
                INSERT INTO user_notifications (enrollment_no, type, title, message, link)
                VALUES (?, 'system', ?, ?, ?)
            """, (
                enrollment_no,
                'Book Available',
                f'"{book_title}" is now available for borrowing!',
                f'/catalogue'
            ))
            
            # Mark as notified
            portal_cursor.execute("""
                UPDATE book_waitlist SET notified = 1 WHERE id = ?
            """, (waitlist_id,))
            
            portal_conn.commit()
            portal_conn.close()
            
            print(f"Notified {enrollment_no} about available book: {book_title}")
            
        except Exception as e:
            print(f"Error notifying waitlist: {e}")
    
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

    def get_student_by_enrollment(self, enrollment_no):
        """Get specific student details by enrollment number"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM students WHERE enrollment_no = ?', (enrollment_no,))
            return cursor.fetchone()
        except:
            return None
        finally:
            conn.close()

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

    def get_book_by_id(self, book_id):
        """Get specific book details by Book ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM books WHERE book_id = ?', (book_id,))
            return cursor.fetchone()
        except:
            return None
        finally:
            conn.close()
    
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
    
    # Alias for backward compatibility
    def remove_book(self, book_id):
        """Alias for delete_book for backward compatibility"""
        return self.delete_book(book_id)
    
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
    
    def verify_data_integrity(self):
        """Verify and fix data integrity issues - CODD's Rules enforcement"""
        conn = self.get_connection()
        cursor = conn.cursor()
        issues_found = []
        issues_fixed = []
        
        try:
            # 1. Check for orphaned borrow_records (student doesn't exist)
            cursor.execute("""
                SELECT DISTINCT br.enrollment_no 
                FROM borrow_records br 
                LEFT JOIN students s ON br.enrollment_no = s.enrollment_no 
                WHERE s.enrollment_no IS NULL
            """)
            orphaned_students = cursor.fetchall()
            if orphaned_students:
                issues_found.append(f"Found {len(orphaned_students)} orphaned borrow records with non-existent students")
            
            # 2. Check for orphaned borrow_records (book doesn't exist)
            cursor.execute("""
                SELECT DISTINCT br.book_id 
                FROM borrow_records br 
                LEFT JOIN books b ON br.book_id = b.book_id 
                WHERE b.book_id IS NULL
            """)
            orphaned_books = cursor.fetchall()
            if orphaned_books:
                issues_found.append(f"Found {len(orphaned_books)} orphaned borrow records with non-existent books")
            
            # 3. Verify available_copies consistency with actual borrow_records
            cursor.execute("SELECT book_id, total_copies, available_copies FROM books")
            books = cursor.fetchall()
            
            for book in books:
                book_id = book['book_id']
                total = book['total_copies']
                available = book['available_copies']
                
                # Count actual borrowed copies
                cursor.execute("SELECT COUNT(*) FROM borrow_records WHERE book_id = ? AND status = 'borrowed'", (book_id,))
                actual_borrowed = cursor.fetchone()[0]
                calculated_available = total - actual_borrowed
                
                if available != calculated_available:
                    issues_found.append(f"Book {book_id}: Database shows {available} available, but should be {calculated_available}")
                    # Fix it
                    cursor.execute("UPDATE books SET available_copies = ? WHERE book_id = ?", (calculated_available, book_id))
                    issues_fixed.append(f"Fixed available_copies for book {book_id}: {available} -> {calculated_available}")
            
            # 4. Check for duplicate student enrollment numbers
            cursor.execute("""
                SELECT enrollment_no, COUNT(*) as count 
                FROM students 
                GROUP BY enrollment_no 
                HAVING COUNT(*) > 1
            """)
            duplicates = cursor.fetchall()
            if duplicates:
                issues_found.append(f"Found {len(duplicates)} duplicate enrollment numbers")
            
            # 5. Check for duplicate book IDs
            cursor.execute("""
                SELECT book_id, COUNT(*) as count 
                FROM books 
                GROUP BY book_id 
                HAVING COUNT(*) > 1
            """)
            dup_books = cursor.fetchall()
            if dup_books:
                issues_found.append(f"Found {len(dup_books)} duplicate book IDs")
            
            # 6. Check for invalid status values in borrow_records
            cursor.execute("""
                SELECT COUNT(*) FROM borrow_records 
                WHERE status NOT IN ('borrowed', 'returned')
            """)
            invalid_status = cursor.fetchone()[0]
            if invalid_status > 0:
                issues_found.append(f"Found {invalid_status} borrow records with invalid status")
            
            # 7. Check for books with negative available_copies
            cursor.execute("SELECT book_id, available_copies FROM books WHERE available_copies < 0")
            negative_books = cursor.fetchall()
            if negative_books:
                for book in negative_books:
                    issues_found.append(f"Book {book['book_id']} has negative available_copies: {book['available_copies']}")
            
            # 8. Check for books where available_copies > total_copies
            cursor.execute("SELECT book_id, total_copies, available_copies FROM books WHERE available_copies > total_copies")
            over_available = cursor.fetchall()
            if over_available:
                for book in over_available:
                    issues_found.append(f"Book {book['book_id']}: available ({book['available_copies']}) > total ({book['total_copies']})")
            
            conn.commit()
            
            return {
                'status': 'ok' if not issues_found else 'issues_found',
                'issues': issues_found,
                'fixes_applied': issues_fixed,
                'total_issues': len(issues_found),
                'total_fixes': len(issues_fixed)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'issues': issues_found,
                'fixes_applied': issues_fixed
            }
        finally:
            conn.close()