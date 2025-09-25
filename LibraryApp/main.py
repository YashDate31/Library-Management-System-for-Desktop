#!/usr/bin/env python3
"""
Library of Computer Department Management System
Version v3.7_DEVELOPER_LOGIN - Developer branding on login + visible version label
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import sqlite3
import os
import sys
import pandas as pd
from tkinter import font
import webbrowser
import subprocess
import platform
try:
    from docx import Document
    from docx.shared import Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
except Exception:
    Document = None  # Will handle gracefully if not installed

# Calendar date picker support
try:
    from tkcalendar import DateEntry
except Exception:
    DateEntry = None  # Fallback to manual entry + dialog

# Add the current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database import Database

# ---------------------------------------------------------------------------
# Application Version (update this each time you create a new packaged build)
# ---------------------------------------------------------------------------
APP_VERSION = "v5.0_FINAL"
FINE_PER_DAY = 5  # monetary units per day late
# Fixed loan period (teacher requirement): exactly 7 days between borrow and due date
LOAN_PERIOD_DAYS = 7
# Simple password required to perform full data wipe (change as needed)
CLEAR_WIPE_PASSWORD = "clear123"  # EASY default; change for production use
# Admin login credentials (required at startup)
ADMIN_USERNAME = "gpa"
ADMIN_PASSWORD = "gpa123"

class LibraryApp:
    def __init__(self, root):
        self.root = root
        # Set window title with current version so user can verify build
        self.root.title(f"📚 Library of Computer Department {APP_VERSION}")
        self.root.geometry("1400x900")
        self.root.state('zoomed')  # Maximize window
        
        # Professional light color scheme (3 colors) - IMPROVED
        self.colors = {
            'primary': '#ffffff',      # Pure white (backgrounds)
            'secondary': '#2E86AB',    # Professional blue (buttons, accents)
            'accent': '#0F3460'        # Dark blue (text, headers)
        }
        
        self.root.configure(bg=self.colors['primary'])
        
        # Initialize database
        self.db = Database()

        # Notify user if calendar support missing
        if DateEntry is None:
            print("tkcalendar not installed - falling back to manual date entry dialog.")
        
        # Configure styles
        self.setup_styles()
        
        # Search/filter related variables
        self.student_search_var = tk.StringVar()
        self.student_year_filter = tk.StringVar(value="All")
        self.book_search_var = tk.StringVar()
        self.book_category_filter = tk.StringVar(value="All")
        self.record_search_var = tk.StringVar()
        self.record_type_filter = tk.StringVar(value="All")

        # Launch login interface
        self.create_login_interface()

    def setup_styles(self):
        """Configure ttk styles (restored after refactor)."""
        try:
            style = ttk.Style()
            # Try a modern theme if available
            for theme in ("clam", "vista", "default"):
                try:
                    style.theme_use(theme)
                    break
                except Exception:
                    continue

            # Treeview base
            style.configure(
                'Treeview',
                background='white',
                foreground='#222222',
                fieldbackground='white',
                rowheight=26,
                font=('Segoe UI', 10)
            )
            style.configure(
                'Treeview.Heading',
                font=('Segoe UI', 10, 'bold'),
                background=self.colors['secondary'],
                foreground='white'
            )
            style.map('Treeview', background=[('selected', '#cfe9ff')])

            # Buttons (ttk) - ensure consistent focus/hover colors if later used
            style.configure('TButton', font=('Segoe UI', 10, 'bold'))
        except Exception as e:
            # Fail silently – styling is not critical for functionality
            print(f"Style setup warning: {e}")
    def create_login_interface(self):
        """Render the login screen (simplified)"""
        for w in self.root.winfo_children():
            w.destroy()
        wrapper = tk.Frame(self.root, bg=self.colors['primary'])
        wrapper.pack(expand=True)
        card = tk.Frame(wrapper, bg='#3a5373', bd=0, relief='flat', padx=40, pady=30)
        card.pack()
        tk.Label(card, text="Admin Login", font=('Segoe UI', 18, 'bold'), bg='#3a5373', fg='white').pack(pady=(0,10))

        tk.Label(card, text="Username", font=('Segoe UI', 10, 'bold'), bg='#3a5373', fg='white').pack(anchor='w')
        user_entry = tk.Entry(card, font=('Segoe UI', 11), width=28, bg='#2b3e56', fg='white', insertbackground='white', relief='solid', bd=1)
        user_entry.pack(pady=(2,12), ipady=6)

        tk.Label(card, text="Password", font=('Segoe UI', 10, 'bold'), bg='#3a5373', fg='white').pack(anchor='w')
        pass_entry = tk.Entry(card, font=('Segoe UI', 11), show='*', width=28, bg='#2b3e56', fg='white', insertbackground='white', relief='solid', bd=1)
        pass_entry.pack(pady=(2,18), ipady=6)

        def do_login():
            username = user_entry.get().strip()
            password = pass_entry.get().strip()
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                self.create_main_interface()
            else:
                messagebox.showerror('Login Error','Invalid username or password!')

        login_btn = tk.Button(
            card,
            text='👨‍💻 Login',
            font=('Segoe UI',12,'bold'),
            bg='#00bcd4', fg='white', bd=0, relief='flat', cursor='hand2',
            command=do_login,
            activebackground='#0097a7', activeforeground='white'
        )
        login_btn.pack(fill=tk.X, ipady=8)

        def handle_enter(event):
            do_login()

        for e in (user_entry, pass_entry):
            e.bind('<Return>', handle_enter)
        self.root.bind('<Return>', handle_enter)
        user_entry.focus()
    
    def create_main_interface(self):
        """Create the main application interface"""
        # Clear root
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['primary'])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.create_header(main_container)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 20))
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_students_tab()
        self.create_books_tab()
        self.create_transactions_tab()
        self.create_records_tab()  # New records tab
        
        # Set focus to dashboard
        self.notebook.select(0)
        
        # Initial data load
        self.refresh_all_data()
    
    def create_header(self, parent):
        """Create application header"""
        header_frame = tk.Frame(parent, bg=self.colors['secondary'], height=90)
        header_frame.pack(fill=tk.X, padx=15, pady=(15, 0))
        header_frame.pack_propagate(False)
        
        # Add subtle shadow effect
        shadow_frame = tk.Frame(parent, bg='#d1d1d1', height=2)
        shadow_frame.pack(fill=tk.X, padx=15)
        
        # Logo and title container
        logo_title_frame = tk.Frame(header_frame, bg=self.colors['secondary'])
        logo_title_frame.pack(expand=True, fill=tk.BOTH, padx=25, pady=15)
        
        # Logo
        logo_frame = tk.Frame(logo_title_frame, bg='white', width=70, height=70)
        logo_frame.pack(side=tk.LEFT, padx=(0, 25))
        logo_frame.pack_propagate(False)
        
        logo_label = tk.Label(
            logo_frame,
            text="📚",
            font=('Segoe UI', 28, 'bold'),
            bg='white',
            fg=self.colors['secondary'],
            justify='center'
        )
        logo_label.pack(expand=True)
        
        # Title and subtitle
        title_frame = tk.Frame(logo_title_frame, bg=self.colors['secondary'])
        title_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        title_label = tk.Label(
            title_frame,
            text="Library of Computer Department",
            font=('Segoe UI', 20, 'bold'),
            bg=self.colors['secondary'],
            fg='white'
        )
        title_label.pack(anchor='w', pady=(15, 2))
        
        subtitle_label = tk.Label(
            title_frame,
            text="Comprehensive Book & Student Management System",
            font=('Segoe UI', 12),
            bg=self.colors['secondary'],
            fg='#b8d4f0'
        )
        subtitle_label.pack(anchor='w')
        
        # User info
        user_frame = tk.Frame(logo_title_frame, bg=self.colors['secondary'])
        user_frame.pack(side=tk.RIGHT, padx=(25, 0))
        
        user_label = tk.Label(
            user_frame,
            text="👨‍💻 Developer",
            font=('Segoe UI', 13, 'bold'),
            bg=self.colors['secondary'],
            fg='white'
        )
        user_label.pack(pady=(25, 2))
        user_label.config(cursor='hand2')
        user_label.bind('<Button-1>', lambda e: self.show_developer_info())

        # Version label (so you can visually confirm correct build)
        version_label = tk.Label(
            user_frame,
            text=f"Version: {APP_VERSION}",
            font=('Segoe UI', 9),
            bg=self.colors['secondary'],
            fg='#e0f2ff'
        )
        version_label.pack(pady=(0, 12))

        # Developer Info button
        dev_btn = tk.Button(
            user_frame,
            text="👨‍💻 Developer Info",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg=self.colors['secondary'],
            relief='flat',
            padx=20,
            pady=6,
            command=self.show_developer_info,
            cursor='hand2',
            activebackground='#f0f8ff',
            activeforeground=self.colors['secondary']
        )
        dev_btn.pack()
        # Danger zone: Clear All Data button (small, subtle)
        clear_btn = tk.Button(
            user_frame,
            text="🗑️ Clear All Data",
            font=('Segoe UI', 9, 'bold'),
            bg='#dc3545',
            fg='white',
            relief='flat',
            padx=14,
            pady=4,
            command=self.clear_all_data_ui,
            cursor='hand2',
            activebackground='#c82333',
            activeforeground='white'
        )
        clear_btn.pack(pady=(6,0))
    def show_developer_info(self):
        """Minimal developer info dialog (only 4 fields)"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Developer Info")
        dialog.configure(bg='white')
        dialog.resizable(False, False)
        dialog.geometry("320x210")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.update_idletasks()
        dialog.geometry(f"+{self.root.winfo_rootx()+360}+{self.root.winfo_rooty()+240}")
        header = tk.Label(dialog, text="👨‍💻 Developer", font=('Segoe UI',14,'bold'), bg='white', fg=self.colors['accent'])
        header.pack(pady=(14,6))
        body = tk.Frame(dialog, bg='white')
        body.pack(fill=tk.BOTH, expand=True, padx=24, pady=4)
        items = [("Name","Yash Vijay Date"),("Enrollment","24210270230"),("Branch","Computer Engineering"),("Year","2nd Year")]
        kf=('Segoe UI',10,'bold'); vf=('Segoe UI',10)
        for r,(k,v) in enumerate(items):
            tk.Label(body,text=f"{k}:",font=kf,bg='white',fg=self.colors['accent']).grid(row=r,column=0,sticky='w',padx=(0,10),pady=3)
            tk.Label(body,text=v,font=vf,bg='white',fg='#222').grid(row=r,column=1,sticky='w',pady=3)
        body.grid_columnconfigure(0,weight=0); body.grid_columnconfigure(1,weight=1)
        tk.Button(dialog,text='Close',font=('Segoe UI',10,'bold'),bg=self.colors['secondary'],fg='white',relief='flat',padx=16,pady=6,cursor='hand2',command=dialog.destroy,activebackground=self.colors['accent'],activeforeground='white').pack(pady=(4,14))

    def clear_all_data_ui(self):
        """UI handler to clear all data from database after confirmations"""
        from tkinter import messagebox, simpledialog
        # First confirmation
        if not messagebox.askyesno(
            "Confirm Data Wipe",
            "This will permanently remove ALL students, books and transaction records.\n\nAre you absolutely sure?",
            icon='warning'
        ):
            return
        # Password prompt (must match CLEAR_WIPE_PASSWORD)
        pwd = simpledialog.askstring(
            "Enter Wipe Password",
            "Enter password to continue (cancel to abort):",
            show='*'
        )
        if pwd is None:
            messagebox.showinfo("Cancelled", "Data wipe cancelled.")
            return
        if pwd.strip() != CLEAR_WIPE_PASSWORD:
            messagebox.showerror("Incorrect", "Wrong password. Data wipe aborted.")
            return
        # Second, stronger confirmation
        if not messagebox.askyesno(
            "Final Confirmation",
            "Last chance! This action cannot be undone. Proceed with complete wipe?",
            icon='warning'
        ):
            return
        try:
            success, msg = self.db.clear_all_data()
            if success:
                # Refresh UI tables
                try:
                    self.refresh_all_data()
                except Exception:
                    pass
                messagebox.showinfo("Data Cleared", "All data removed successfully.")
            else:
                messagebox.showerror("Error", msg or "Failed to clear data.")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")
    
    def create_dashboard_tab(self):
        """Create dashboard tab with statistics"""
        dashboard_frame = tk.Frame(self.notebook, bg=self.colors['primary'])
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        # Statistics cards container
        self.stats_container = tk.Frame(dashboard_frame, bg=self.colors['primary'])
        self.stats_container.pack(fill=tk.X, padx=20, pady=20)
        
        # Statistics cards
        self.create_stats_cards(self.stats_container)
        
        # Current Borrowed Books (Dashboard Table)
        borrowed_frame = tk.LabelFrame(
            dashboard_frame,
            text="📋 Currently Borrowed Books",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent'],
            padx=10,
            pady=10
        )
        borrowed_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        columns = ('Enrollment No', 'Student Name', 'Book ID', 'Book Name', 'Borrow Date', 'Due Date', 'Days Left')
        self.dashboard_borrowed_tree = ttk.Treeview(borrowed_frame, columns=columns, show='headings', height=12)
        for col in columns:
            self.dashboard_borrowed_tree.heading(col, text=col)
            self.dashboard_borrowed_tree.column(col, width=120 if col in ['Enrollment No', 'Book ID', 'Borrow Date', 'Due Date', 'Days Left'] else 200)

        v_scrollbar = ttk.Scrollbar(borrowed_frame, orient=tk.VERTICAL, command=self.dashboard_borrowed_tree.yview)
        h_scrollbar = ttk.Scrollbar(borrowed_frame, orient=tk.HORIZONTAL, command=self.dashboard_borrowed_tree.xview)
        self.dashboard_borrowed_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        self.dashboard_borrowed_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Populate dashboard borrowed books
        self.refresh_dashboard_borrowed()
    def refresh_dashboard_borrowed(self):
        """Refresh dashboard borrowed books table"""
        for item in self.dashboard_borrowed_tree.get_children():
            self.dashboard_borrowed_tree.delete(item)
        borrowed_books = self.db.get_borrowed_books()
        for record in borrowed_books:
            enrollment_no = record[0]
            student_name = record[1]
            book_id = record[4]
            book_name = record[5]
            borrow_date = record[7]
            due_date = record[8]
            # Calculate days left
            try:
                days_left = (datetime.strptime(due_date, '%Y-%m-%d') - datetime.now()).days
            except:
                days_left = ''
            self.dashboard_borrowed_tree.insert('', 'end', values=(enrollment_no, student_name, book_id, book_name, borrow_date, due_date, days_left))
    
    def create_stats_cards(self, parent):
        """Create statistics cards"""
        # Get statistics
        stats = self.get_library_statistics()
        
        cards_data = [
            ("📚 Total Books", stats['total_books'], self.colors['secondary']),
            ("✅ Available Books", stats['available_books'], '#28a745'),
            ("📖 Borrowed Books", stats['borrowed_books'], '#ffc107'),
            ("👥 Total Students", stats['total_students'], '#17a2b8')
        ]
        
        for i, (title, value, color) in enumerate(cards_data):
            card = tk.Frame(parent, bg='white', relief='raised', bd=2)
            card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15 if i < 3 else 0))
            
            # Icon/Title
            title_label = tk.Label(
                card,
                text=title,
                font=('Segoe UI', 12, 'bold'),
                bg='white',
                fg=self.colors['accent']
            )
            title_label.pack(pady=(15, 5))
            
            # Value
            value_label = tk.Label(
                card,
                text=str(value),
                font=('Segoe UI', 28, 'bold'),
                bg='white',
                fg=color
            )
            value_label.pack(pady=(0, 15))
    
    def get_library_statistics(self):
        """Get library statistics"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Total books
            cursor.execute("SELECT COUNT(*) FROM books")
            total_books = cursor.fetchone()[0]
            
            # Available books (sum of available_copies)
            cursor.execute("SELECT SUM(available_copies) FROM books")
            available_books = cursor.fetchone()[0] or 0
            
            # Borrowed books
            cursor.execute("SELECT COUNT(*) FROM borrow_records WHERE status = 'borrowed'")
            borrowed_books = cursor.fetchone()[0]
            
            # Total students (Computer department only)
            cursor.execute("SELECT COUNT(*) FROM students WHERE department = 'Computer'")
            total_students = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_books': total_books,
                'available_books': available_books,
                'borrowed_books': borrowed_books,
                'total_students': total_students
            }
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {
                'total_books': 0,
                'available_books': 0,
                'borrowed_books': 0,
                'total_students': 0
            }
    
    def create_students_tab(self):
        """Create students management tab"""
        students_frame = tk.Frame(self.notebook, bg=self.colors['primary'])
        self.notebook.add(students_frame, text="👥 Students")
        
        # Top frame for search and actions
        top_frame = tk.Frame(students_frame, bg=self.colors['primary'])
        top_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Search frame
        search_frame = tk.LabelFrame(
            top_frame,
            text="🔍 Search & Filter Students",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent']
        )
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Search controls
        search_controls = tk.Frame(search_frame, bg=self.colors['primary'])
        search_controls.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(search_controls, text="Search:", bg=self.colors['primary'], fg=self.colors['accent'], font=('Segoe UI', 10)).pack(side=tk.LEFT)
        search_entry = tk.Entry(search_controls, textvariable=self.student_search_var, font=('Segoe UI', 10), width=25)
        search_entry.pack(side=tk.LEFT, padx=(5, 15))
        
        tk.Label(search_controls, text="Year:", bg=self.colors['primary'], fg=self.colors['accent'], font=('Segoe UI', 10)).pack(side=tk.LEFT)
        year_combo = ttk.Combobox(search_controls, textvariable=self.student_year_filter, values=["All", "1st", "2nd", "3rd", "4th"], state="readonly", width=10)
        year_combo.pack(side=tk.LEFT, padx=5)
        year_combo.bind('<<ComboboxSelected>>', lambda e: self.search_students())
        
        # Actions frame
        actions_frame = tk.LabelFrame(
            top_frame,
            text="⚡ Actions",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent']
        )
        actions_frame.pack(side=tk.RIGHT)
        
        # Action buttons
        buttons_frame = tk.Frame(actions_frame, bg=self.colors['primary'])
        buttons_frame.pack(padx=10, pady=10)
        
        add_student_btn = tk.Button(
            buttons_frame,
            text="➕ Add Student",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['secondary'],
            fg='white',
            relief='flat',
            padx=15,
            pady=8,
            command=self.show_add_student_dialog,
            cursor='hand2'
        )
        add_student_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        import_students_btn = tk.Button(
            buttons_frame,
            text="📥 Import Excel",
            font=('Segoe UI', 10, 'bold'),
            bg='#6f42c1',
            fg='white',
            relief='flat',
            padx=15,
            pady=8,
            command=self.import_students_from_excel,
            cursor='hand2'
        )
        import_students_btn.pack(side=tk.LEFT, padx=5)
        
        # Students list
        students_list_frame = tk.LabelFrame(
            students_frame,
            text="📋 Students List",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent'],
            padx=10,
            pady=10
        )
        students_list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Students treeview
        columns = ('Enrollment No', 'Name', 'Email', 'Phone', 'Year')
        self.students_tree = ttk.Treeview(students_list_frame, columns=columns, show='headings', height=15)
        col_widths = {'Enrollment No': 120, 'Name': 150, 'Email': 180, 'Phone': 120, 'Year': 80}
        for col in columns:
            self.students_tree.heading(col, text=col)
            self.students_tree.column(col, width=col_widths[col])
        students_v_scrollbar = ttk.Scrollbar(students_list_frame, orient=tk.VERTICAL, command=self.students_tree.yview)
        students_h_scrollbar = ttk.Scrollbar(students_list_frame, orient=tk.HORIZONTAL, command=self.students_tree.xview)
        self.students_tree.configure(yscrollcommand=students_v_scrollbar.set, xscrollcommand=students_h_scrollbar.set)
        self.students_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        students_v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        students_h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Add double-click binding for delete option
        self.students_tree.bind('<Double-1>', self.on_student_double_click)
    
    def create_books_tab(self):
        """Create books management tab"""
        books_frame = tk.Frame(self.notebook, bg=self.colors['primary'])
        self.notebook.add(books_frame, text="📚 Books")
        
        # Top frame for search and actions
        top_frame = tk.Frame(books_frame, bg=self.colors['primary'])
        top_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Search frame
        search_frame = tk.LabelFrame(
            top_frame,
            text="🔍 Search & Filter Books",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent']
        )
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Search controls
        search_controls = tk.Frame(search_frame, bg=self.colors['primary'])
        search_controls.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(search_controls, text="Search:", bg=self.colors['primary'], fg=self.colors['accent'], font=('Segoe UI', 10)).pack(side=tk.LEFT)
        book_search_entry = tk.Entry(search_controls, textvariable=self.book_search_var, font=('Segoe UI', 10), width=25)
        book_search_entry.pack(side=tk.LEFT, padx=(5, 15))
        
        tk.Label(search_controls, text="Category:", bg=self.colors['primary'], fg=self.colors['accent'], font=('Segoe UI', 10)).pack(side=tk.LEFT)
        category_combo = ttk.Combobox(search_controls, textvariable=self.book_category_filter, 
                                    values=["All", "Technology", "Textbook", "Research"], state="readonly", width=12)
        category_combo.pack(side=tk.LEFT, padx=5)
        category_combo.bind('<<ComboboxSelected>>', lambda e: self.search_books())
        
        # Actions frame
        actions_frame = tk.LabelFrame(
            top_frame,
            text="⚡ Actions",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent']
        )
        actions_frame.pack(side=tk.RIGHT)
        
        # Action buttons
        buttons_frame = tk.Frame(actions_frame, bg=self.colors['primary'])
        buttons_frame.pack(padx=10, pady=10)
        
        add_book_btn = tk.Button(
            buttons_frame,
            text="➕ Add Book",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['secondary'],
            fg='white',
            relief='flat',
            padx=15,
            pady=8,
            command=self.show_add_book_dialog,
            cursor='hand2'
        )
        add_book_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        import_books_btn = tk.Button(
            buttons_frame,
            text="📥 Import Excel",
            font=('Segoe UI', 10, 'bold'),
            bg='#6f42c1',
            fg='white',
            relief='flat',
            padx=15,
            pady=8,
            command=self.import_books_from_excel,
            cursor='hand2'
        )
        import_books_btn.pack(side=tk.LEFT, padx=5)
        
        export_books_btn = tk.Button(
            buttons_frame,
            text="📊 Export to Excel",
            font=('Segoe UI', 10, 'bold'),
            bg='#28a745',
            fg='white',
            relief='flat',
            padx=15,
            pady=8,
            command=self.export_books_to_excel,
            cursor='hand2'
        )
        # Books list
        books_list_frame = tk.LabelFrame(
            books_frame,
            text="📚 Books Collection",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent'],
            padx=10,
            pady=10
        )
        books_list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Books treeview
        columns = ('Book ID', 'Title', 'Author', 'ISBN', 'Category', 'Total Copies', 'Available')
        self.books_tree = ttk.Treeview(books_list_frame, columns=columns, show='headings', height=15)
        
        # Define headings and widths
        column_widths = {'Book ID': 100, 'Title': 250, 'Author': 180, 'ISBN': 120, 
                        'Category': 100, 'Total Copies': 100, 'Available': 100}
        
        for col in columns:
            self.books_tree.heading(col, text=col)
            self.books_tree.column(col, width=column_widths[col])
        
        # Scrollbars
        books_v_scrollbar = ttk.Scrollbar(books_list_frame, orient=tk.VERTICAL, command=self.books_tree.yview)
        books_h_scrollbar = ttk.Scrollbar(books_list_frame, orient=tk.HORIZONTAL, command=self.books_tree.xview)
        self.books_tree.configure(yscrollcommand=books_v_scrollbar.set, xscrollcommand=books_h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.books_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        books_v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        books_h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Add double-click binding for delete option
        self.books_tree.bind('<Double-1>', self.on_book_double_click)
    
    def create_transactions_tab(self):
        """Create transactions tab with full-page scrolling (borrow + return + list)"""
        transactions_frame = tk.Frame(self.notebook, bg=self.colors['primary'])
        self.notebook.add(transactions_frame, text="📋 Transactions")

        # Outer canvas + single scrollbar for whole page
        outer_container = tk.Frame(transactions_frame, bg=self.colors['primary'])
        outer_container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(outer_container, bg=self.colors['primary'], highlightthickness=0)
        v_scroll = ttk.Scrollbar(outer_container, orient=tk.VERTICAL, command=canvas.yview)
        h_scroll = ttk.Scrollbar(outer_container, orient=tk.HORIZONTAL, command=canvas.xview)
        canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        # Horizontal scrollbar will be packed only if needed (dynamic)
        def _toggle_hbar():
            bbox = canvas.bbox('all')
            if not bbox:
                return
            content_width = bbox[2] - bbox[0]
            visible_width = canvas.winfo_width()
            if content_width > visible_width and not getattr(h_scroll, '_visible', False):
                h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
                h_scroll._visible = True
            elif content_width <= visible_width and getattr(h_scroll, '_visible', False):
                h_scroll.pack_forget()
                h_scroll._visible = False
        h_scroll._visible = False

        # Internal frame that will hold all sections
        main_container = tk.Frame(canvas, bg=self.colors['primary'])
        _mc_window = canvas.create_window((0, 0), window=main_container, anchor='nw')

        def _update_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox('all'))
            _toggle_hbar()
        main_container.bind('<Configure>', _update_scroll_region)

        # Also re-evaluate horizontal bar on canvas resize
        def _resize_content(event):
            # Match internal frame width to canvas width to remove empty right side
            canvas.itemconfig(_mc_window, width=canvas.winfo_width())
            _toggle_hbar()
        canvas.bind('<Configure>', _resize_content)

        # Mouse wheel scrolling (Windows/Linux)
        def _on_mousewheel(event):
            delta = -1 * (event.delta // 120) if event.delta else 0
            canvas.yview_scroll(delta, 'units')
        canvas.bind_all('<MouseWheel>', _on_mousewheel)
        
        # =================================================================
        # BORROW BOOK SECTION - Fixed UI Layout
        # =================================================================
        borrow_frame = tk.LabelFrame(
            main_container,
            text="📚 Borrow Book",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent'],
            padx=20,
            pady=20
        )
        borrow_frame.pack(fill=tk.X, expand=True, pady=(0, 25))
        
        # Borrow form container
        borrow_form = tk.Frame(borrow_frame, bg=self.colors['primary'])
        borrow_form.pack(fill=tk.X, padx=20, pady=10)
        
        # Row 1: Student and Book Input - Properly Spaced
        input_row = tk.Frame(borrow_form, bg=self.colors['primary'])
        input_row.pack(fill=tk.X, pady=(0, 20))
        
        # Student Enrollment Column
        student_col = tk.Frame(input_row, bg=self.colors['primary'])
        student_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 20))
        
        tk.Label(student_col, text="Student Enrollment No:", 
                font=('Segoe UI', 12, 'bold'), 
                bg=self.colors['primary'], 
                fg=self.colors['accent']).pack(anchor='w', pady=(0, 8))
        
        self.borrow_enrollment_entry = tk.Entry(student_col, 
                                              font=('Segoe UI', 12), 
                                              width=25, 
                                              relief='solid', 
                                              bd=2)
        self.borrow_enrollment_entry.pack(fill=tk.X, pady=(0, 8))
        self.borrow_enrollment_entry.bind('<KeyRelease>', lambda e: self.show_student_details('borrow'))

        # Student details display
        self.borrow_student_details = tk.Label(student_col, 
                                             text="", 
                                             font=('Segoe UI', 10), 
                                             bg=self.colors['primary'], 
                                             fg='#666666',
                                             wraplength=300)
        self.borrow_student_details.pack(anchor='w')
        
        # Book ID Column
        book_col = tk.Frame(input_row, bg=self.colors['primary'])
        book_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(20, 0))
        
        tk.Label(book_col, text="Book ID:", 
                font=('Segoe UI', 12, 'bold'), 
                bg=self.colors['primary'], 
                fg=self.colors['accent']).pack(anchor='w', pady=(0, 8))
        
        self.borrow_book_id_entry = tk.Entry(book_col, 
                                           font=('Segoe UI', 12), 
                                           width=25, 
                                           relief='solid', 
                                           bd=2)
        self.borrow_book_id_entry.pack(fill=tk.X, pady=(0, 8))
        self.borrow_book_id_entry.bind('<KeyRelease>', lambda e: self.show_book_details('borrow'))
        
        # Book details display
        self.borrow_book_details = tk.Label(book_col, 
                                          text="", 
                                          font=('Segoe UI', 10), 
                                          bg=self.colors['primary'], 
                                          fg='#666666',
                                          wraplength=300)
        self.borrow_book_details.pack(anchor='w')
        
        # Row 2: Borrow & Due Dates and Action Button - Better Layout
        action_row = tk.Frame(borrow_form, bg=self.colors['primary'])
        action_row.pack(fill=tk.X, pady=(15, 0))
        
        # Borrow Date Section (uses DateEntry if available)
        borrow_date_section = tk.Frame(action_row, bg=self.colors['primary'])
        borrow_date_section.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(borrow_date_section, text="Borrow Date:", font=('Segoe UI', 12, 'bold'), bg=self.colors['primary'], fg=self.colors['accent']).pack(anchor='w', pady=(0,8))
        borrow_date_input_frame = tk.Frame(borrow_date_section, bg=self.colors['primary'])
        borrow_date_input_frame.pack(anchor='w')
        if DateEntry:
            self.borrow_borrow_date_entry = DateEntry(borrow_date_input_frame, width=13, date_pattern='yyyy-mm-dd', state='readonly')
            self.borrow_borrow_date_entry.pack(side=tk.LEFT)
            # Auto-update due date when borrow date picked
            self.borrow_borrow_date_entry.bind('<<DateEntrySelected>>', self.on_borrow_date_changed)
        else:
            self.borrow_borrow_date_entry = tk.Entry(borrow_date_input_frame, font=('Segoe UI',12), width=15, relief='solid', bd=2)
            self.borrow_borrow_date_entry.pack(side=tk.LEFT)
            tk.Button(
                borrow_date_input_frame,
                text="📅",
                font=('Segoe UI', 14),
                bg=self.colors['secondary'],
                fg='white',
                relief='flat',
                padx=10,
                pady=6,
                command=lambda: self.show_date_picker(self.borrow_borrow_date_entry),
                cursor='hand2'
            ).pack(side=tk.LEFT, padx=(8,0))
            # Prevent manual typing; force picker
            self.borrow_borrow_date_entry.bind('<Key>', lambda e: 'break')

        # Due Date Section (DateEntry if available)
        date_section = tk.Frame(action_row, bg=self.colors['primary'])
        date_section.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(20,0))
        tk.Label(date_section, text="Due Date:", font=('Segoe UI', 12, 'bold'), bg=self.colors['primary'], fg=self.colors['accent']).pack(anchor='w', pady=(0,8))
        date_input_frame = tk.Frame(date_section, bg=self.colors['primary'])
        date_input_frame.pack(anchor='w')
        if DateEntry:
            self.borrow_due_date_entry = DateEntry(date_input_frame, width=13, date_pattern='yyyy-mm-dd', state='readonly')
            self.borrow_due_date_entry.pack(side=tk.LEFT)
            # Intercept any manual selection attempts
            self.borrow_due_date_entry.bind('<<DateEntrySelected>>', lambda e: self.on_due_date_attempt_change())
        else:
            self.borrow_due_date_entry = tk.Entry(date_input_frame, font=('Segoe UI', 12), width=15, relief='solid', bd=2)
            self.borrow_due_date_entry.pack(side=tk.LEFT)
            tk.Button(
                date_input_frame,
                text="📅",
                font=('Segoe UI', 14),
                bg=self.colors['secondary'],
                fg='white',
                relief='flat',
                padx=10,
                pady=6,
                command=lambda: self.show_date_picker(self.borrow_due_date_entry),
                cursor='hand2'
            ).pack(side=tk.LEFT, padx=(8,0))
            # Block manual typing; will be auto-set
            self.borrow_due_date_entry.bind('<Key>', lambda e: 'break')
        
        # Action Button Section - Right Side
        button_section = tk.Frame(action_row, bg=self.colors['primary'])
        button_section.pack(side=tk.RIGHT, padx=(20, 0))
        
        # Borrow button - Prominent and well-positioned
        borrow_btn = tk.Button(
            button_section,
            text="📚 Borrow Book",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['secondary'],
            fg='white',
            relief='flat',
            padx=30,
            pady=12,
            command=self.borrow_book,
            cursor='hand2'
        )
        borrow_btn.pack(pady=(25, 0))
        
        # Set default due date (exact 7-day loan period per requirement)
        from datetime import datetime, timedelta
        today_str = datetime.now().strftime('%Y-%m-%d')
        default_due = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        try:
            if DateEntry:
                self.borrow_borrow_date_entry.set_date(datetime.now())
                self.borrow_due_date_entry.set_date(datetime.now() + timedelta(days=7))
                # Ensure readonly state remains
                try:
                    self.borrow_borrow_date_entry.config(state='readonly')
                    self.borrow_due_date_entry.config(state='readonly')
                except Exception:
                    pass
            else:
                self.borrow_borrow_date_entry.delete(0, tk.END)
                self.borrow_borrow_date_entry.insert(0, today_str)
                self.borrow_due_date_entry.delete(0, tk.END)
                self.borrow_due_date_entry.insert(0, default_due)
        except Exception:
            pass
        
        # =================================================================
        # VISUAL SEPARATOR
        # =================================================================
        separator = tk.Frame(main_container, height=3, bg=self.colors['accent'])
        separator.pack(fill=tk.X, pady=30)
        
        # =================================================================
        # RETURN BOOK SECTION
        # =================================================================
        return_outer = tk.Frame(main_container, bg=self.colors['primary'], highlightthickness=0)
        return_outer.pack(fill=tk.X, pady=(0, 25))
        heading_bar = tk.Frame(return_outer, bg=self.colors['primary'])
        heading_bar.pack(fill=tk.X)
        heading_label = tk.Label(
            heading_bar,
            text="🔄 Return Book",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent']
        )
        heading_label.pack(anchor='w')
        # Return input row - directly in outer frame now
        return_input_row = tk.Frame(return_outer, bg=self.colors['primary'])
        return_input_row.pack(fill=tk.X, pady=(0, 20))
        
        # Student section
        return_student_col = tk.Frame(return_input_row, bg=self.colors['primary'])
        return_student_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 20))
        
        tk.Label(return_student_col, text="Student Enrollment No:", 
                font=('Segoe UI', 12, 'bold'), 
                bg=self.colors['primary'], 
                fg=self.colors['accent']).pack(anchor='w', pady=(0, 8))
        
        self.return_enrollment_entry = tk.Entry(return_student_col, 
                                              font=('Segoe UI', 12), 
                                              width=25, 
                                              relief='solid', 
                                              bd=2)
        self.return_enrollment_entry.pack(fill=tk.X, pady=(0, 8))
        self.return_enrollment_entry.bind('<KeyRelease>', lambda e: self.show_student_details('return'))
        
        self.return_student_details = tk.Label(return_student_col, 
                                             text="", 
                                             font=('Segoe UI', 10), 
                                             bg=self.colors['primary'], 
                                             fg='#666666',
                                             wraplength=300)
        self.return_student_details.pack(anchor='w')
        
        # Book section
        return_book_col = tk.Frame(return_input_row, bg=self.colors['primary'])
        return_book_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(20, 0))
        
        tk.Label(return_book_col, text="Book ID:", 
                font=('Segoe UI', 12, 'bold'), 
                bg=self.colors['primary'], 
                fg=self.colors['accent']).pack(anchor='w', pady=(0, 8))
        
        self.return_book_id_entry = tk.Entry(return_book_col, 
                                           font=('Segoe UI', 12), 
                                           width=25, 
                                           relief='solid', 
                                           bd=2)
        self.return_book_id_entry.pack(fill=tk.X, pady=(0, 8))
        self.return_book_id_entry.bind('<KeyRelease>', lambda e: self.show_book_details('return'))
        
        self.return_book_details = tk.Label(return_book_col, 
                                          text="", 
                                          font=('Segoe UI', 10), 
                                          bg=self.colors['primary'], 
                                          fg='#666666',
                                          wraplength=300)
        self.return_book_details.pack(anchor='w')
        
        # Return button - Centered and prominent
        return_button_frame = tk.Frame(return_outer, bg=self.colors['primary'])
        # Return date row
        return_date_row = tk.Frame(return_outer, bg=self.colors['primary'])
        return_date_row.pack(fill=tk.X, pady=(10, 5))
        tk.Label(return_date_row, text="Return Date:", font=('Segoe UI', 12, 'bold'), bg=self.colors['primary'], fg=self.colors['accent']).pack(side=tk.LEFT, padx=(0,8))
        if DateEntry:
            self.return_date_entry = DateEntry(return_date_row, width=13, date_pattern='yyyy-mm-dd', state='readonly')
            self.return_date_entry.pack(side=tk.LEFT)
            try:
                self.return_date_entry.set_date(datetime.now())
            except Exception:
                pass
        else:
            self.return_date_entry = tk.Entry(return_date_row, font=('Segoe UI', 12), width=15, relief='solid', bd=2)
            self.return_date_entry.pack(side=tk.LEFT)
            tk.Button(return_date_row, text="📅", font=('Segoe UI', 14), bg=self.colors['secondary'], fg='white', relief='flat', padx=10, pady=6, cursor='hand2', command=lambda: self.show_date_picker(self.return_date_entry)).pack(side=tk.LEFT, padx=(8,0))
            # Set default return date to today
            try:
                from datetime import datetime as _dt
                self.return_date_entry.delete(0, tk.END)
                self.return_date_entry.insert(0, _dt.now().strftime('%Y-%m-%d'))
            except Exception:
                pass
            self.return_date_entry.bind('<Key>', lambda e: 'break')
        return_button_frame.pack(pady=(10, 0))
        
        return_btn = tk.Button(
            return_button_frame,
            text="🔄 Return Book",
            font=('Segoe UI', 14, 'bold'),
            bg='#28a745',
            fg='white',
            relief='flat',
            padx=30,
            pady=12,
            command=self.return_book,
            cursor='hand2'
        )
        return_btn.pack()
        
        # =================================================================
        # CURRENTLY BORROWED BOOKS SECTION - Improved Layout
        # =================================================================
        borrowed_frame = tk.LabelFrame(
            main_container,
            text="📋 Currently Borrowed Books",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent'],
            padx=10,
            pady=10
        )
        borrowed_frame.pack(fill=tk.BOTH, expand=True, pady=(0,40))
        
        borrowed_columns = ('Student', 'Book ID', 'Book Title', 'Borrow Date', 'Due Date', 'Days Left')
        self.borrowed_tree = ttk.Treeview(borrowed_frame, columns=borrowed_columns, show='headings', height=10)
        borrowed_widths = {'Student': 150, 'Book ID': 100, 'Book Title': 250, 'Borrow Date': 120, 'Due Date': 120, 'Days Left': 100}
        
        for col in borrowed_columns:
            self.borrowed_tree.heading(col, text=col)
            self.borrowed_tree.column(col, width=borrowed_widths[col])
        
        borrowed_v_scrollbar = ttk.Scrollbar(borrowed_frame, orient=tk.VERTICAL, command=self.borrowed_tree.yview)
        borrowed_h_scrollbar = ttk.Scrollbar(borrowed_frame, orient=tk.HORIZONTAL, command=self.borrowed_tree.xview)
        self.borrowed_tree.configure(yscrollcommand=borrowed_v_scrollbar.set, xscrollcommand=borrowed_h_scrollbar.set)
        
        self.borrowed_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        borrowed_v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        borrowed_h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    # Commented out - no longer needed since we removed combobox autocomplete
    # def filter_student_suggestions(self, event, mode):
    #     """Filter student suggestions as user types"""
    #     try:
    #         current_text = event.widget.get().lower().strip()
    #         if len(current_text) < 1:  # Start filtering after 1 character
    #             return
    #         
    #         # Get all students
    #         students = self.db.get_students()
    #         # Filter students that match the current text (enrollment number or name)
    #         matching_students = []
    #         for s in students:
    #             enrollment = str(s[0]).lower()
    #             name = str(s[1]).lower()
    #             if current_text in enrollment or current_text in name:
    #                 matching_students.append(f"{s[0]} - {s[1]}")  # Format as "enrollment - name"
    #         
    #         # Update combobox values
    #         event.widget['values'] = matching_students[:10]  # Limit to 10 suggestions
    #         
    #         # Auto-open dropdown if there are matches
    #         if matching_students and len(current_text) >= 1:
    #             event.widget.event_generate('<Down>')
    #             
    #     except Exception as e:
    #         print(f"Error filtering student suggestions: {e}")
    # 
    # def filter_book_suggestions(self, event, mode):
    #     """Filter book suggestions as user types"""
    #     try:
    #         current_text = event.widget.get().lower().strip()
    #         if len(current_text) < 1:  # Start filtering after 1 character
    #             return
    #         
    #         # Get all books
    #         books = self.db.get_books()
    #         # Filter books that match the current text (book ID or title)
    #         matching_books = []
    #         for b in books:
    #             book_id = str(b[0]).lower()
    #             title = str(b[1]).lower()
    #             if current_text in book_id or current_text in title:
    #                 matching_books.append(f"{b[0]} - {b[1]}")  # Format as "ID - title"
    #         
    #         # Update combobox values
    #         event.widget['values'] = matching_books[:10]  # Limit to 10 suggestions
    #         
    #         # Auto-open dropdown if there are matches
    #         if matching_books and len(current_text) >= 1:
    #             event.widget.event_generate('<Down>')
    #             
    #     except Exception as e:
    #         print(f"Error filtering book suggestions: {e}")
    
    def show_student_details(self, mode):
        """Show student details below enrollment field in transactions tab"""
        if mode == 'borrow':
            enrollment_no = self.borrow_enrollment_entry.get().strip()
        else:
            enrollment_no = self.return_enrollment_entry.get().strip()
        
        if not enrollment_no:
            details = ""
        else:
            try:
                students = self.db.get_students()
                student = next((s for s in students if str(s[1]) == enrollment_no), None)
                if student:
                    details = f"Name: {student[2]} | Email: {student[3]} | Phone: {student[4]} | Year: {student[6]}"
                else:
                    details = "Student not found."
            except Exception as e:
                details = "Error loading student data."
                
        if mode == 'borrow':
            self.borrow_student_details.config(text=details)
        else:
            self.return_student_details.config(text=details)
    
    def show_book_details(self, mode):
        """Show book details when book ID is entered"""
        if mode == 'borrow':
            book_id = self.borrow_book_id_entry.get().strip()
        else:
            book_id = self.return_book_id_entry.get().strip()
        
        if not book_id:
            details = ""
        else:
            try:
                books = self.db.get_books()
                book = next((b for b in books if str(b[1]) == book_id), None)
                if book:
                    details = f"Title: {book[2]} | Author: {book[3]} | Available: {book[7]}"
                else:
                    details = "Book not found."
            except Exception as e:
                details = "Error loading book data."
                
        # Update the appropriate book details label
        if mode == 'borrow':
            self.borrow_book_details.config(text=details)
        else:
            self.return_book_details.config(text=details)
    
    def on_student_double_click(self, event):
        """Handle double-click on student to show delete option"""
        item = self.students_tree.selection()[0] if self.students_tree.selection() else None
        if not item:
            return

        student_data = self.students_tree.item(item, 'values')
        if not student_data:
            return

        enrollment_no = student_data[0]
        student_name = student_data[1]

        # Default placeholders
        branch = "(branch unknown)"
        year = "(year unknown)"

        try:
            # Use search term to narrow results
            candidates = self.db.get_students(enrollment_no)
            for s in candidates:
                # Expected schema: (enrollment_no, name, email, phone, department, year)
                if len(s) >= 6 and str(s[0]) == str(enrollment_no):
                    branch = s[4] or branch
                    year = s[5] or year
                    break
        except Exception:
            pass

        confirm_text = (
            f"Delete this student?\n\n"
            f"Name: {student_name}\n"
            f"Branch: {branch}\n"
            f"Year: {year}"
        )

        result = messagebox.askyesno(
            "Delete Student",
            confirm_text,
            icon='warning'
        )

        if result:
            success, message = self.db.delete_student(enrollment_no)
            if success:
                try:
                    self.refresh_students()
                    # Also refresh dashboard statistics so counts update immediately
                    self.refresh_dashboard()
                except Exception:
                    pass
                messagebox.showinfo("Success", "Student deleted successfully.")
            else:
                messagebox.showerror("Error", message or "Failed to delete student.")

    def on_book_double_click(self, event):
        """Handle double-click on book to show delete option"""
        item = self.books_tree.selection()[0] if self.books_tree.selection() else None
        if not item:
            return
        book_data = self.books_tree.item(item, 'values')
        if not book_data:
            return
        book_id = book_data[0]
        book_title = book_data[1]
        result = messagebox.askyesno(
            "Delete Book",
            f"Delete this book?\n\nID: {book_id}\nTitle: {book_title}",
            icon='warning'
        )
        if result:
            success, message = self.db.delete_book(book_id)
            if success:
                try:
                    self.refresh_books()
                    # Refresh dashboard statistics to reflect updated totals
                    self.refresh_dashboard()
                except Exception:
                    pass
                messagebox.showinfo("Success", "Book deleted successfully.")
            else:
                messagebox.showerror("Error", message or "Failed to delete book.")
        
    # ...existing code...
        # ...existing code...
        # ...existing code...
    
    def create_records_tab(self):
        """Create comprehensive records tab"""
        records_frame = tk.Frame(self.notebook, bg=self.colors['primary'])
        self.notebook.add(records_frame, text="📊 Records")
        
        # Top frame for search, filters and actions
        top_frame = tk.Frame(records_frame, bg=self.colors['primary'])
        top_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Search and filter frame
        search_filter_frame = tk.LabelFrame(
            top_frame,
            text="🔍 Search & Filter Records",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent']
        )
        search_filter_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Search controls
        search_controls = tk.Frame(search_filter_frame, bg=self.colors['primary'])
        search_controls.pack(fill=tk.X, padx=10, pady=10)
        
        # Row 1: Search and type filter
        row1 = tk.Frame(search_controls, bg=self.colors['primary'])
        row1.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(row1, text="Search:", bg=self.colors['primary'], fg=self.colors['accent'], font=('Segoe UI', 10)).pack(side=tk.LEFT)
        record_search_entry = tk.Entry(row1, textvariable=self.record_search_var, font=('Segoe UI', 10), width=25)
        record_search_entry.pack(side=tk.LEFT, padx=(5, 15))
        
        tk.Label(row1, text="Type:", bg=self.colors['primary'], fg=self.colors['accent'], font=('Segoe UI', 10)).pack(side=tk.LEFT)
        type_combo = ttk.Combobox(row1, textvariable=self.record_type_filter, 
                                 values=["All", "Borrowed", "Returned", "Overdue"], state="readonly", width=12)
        type_combo.pack(side=tk.LEFT, padx=5)
        type_combo.bind('<<ComboboxSelected>>', lambda e: self.search_records())
        
        # Row 2: Date filters
        row2 = tk.Frame(search_controls, bg=self.colors['primary'])
        row2.pack(fill=tk.X)
        
        tk.Label(row2, text="From Date:", bg=self.colors['primary'], fg=self.colors['accent'], font=('Segoe UI', 10)).pack(side=tk.LEFT)
        if DateEntry:
            self.record_from_date = DateEntry(row2, width=11, date_pattern='yyyy-mm-dd')
            self.record_from_date.pack(side=tk.LEFT, padx=(5, 15))
        else:
            self.record_from_date = tk.Entry(row2, font=('Segoe UI', 10), width=12)
            self.record_from_date.pack(side=tk.LEFT, padx=(5, 15))
        
        tk.Label(row2, text="To Date:", bg=self.colors['primary'], fg=self.colors['accent'], font=('Segoe UI', 10)).pack(side=tk.LEFT)
        if DateEntry:
            self.record_to_date = DateEntry(row2, width=11, date_pattern='yyyy-mm-dd')
            self.record_to_date.pack(side=tk.LEFT, padx=(5, 15))
        else:
            self.record_to_date = tk.Entry(row2, font=('Segoe UI', 10), width=12)
            self.record_to_date.pack(side=tk.LEFT, padx=(5, 15))
        
        filter_btn = tk.Button(
            row2,
            text="🔍 Filter",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['secondary'],
            fg='white',
            relief='flat',
            padx=10,
            pady=5,
            command=self.search_records,
            cursor='hand2'
        )
        filter_btn.pack(side=tk.LEFT, padx=5)
        
        clear_filter_btn = tk.Button(
            row2,
            text="🗑️ Clear",
            font=('Segoe UI', 9, 'bold'),
            bg='#6c757d',
            fg='white',
            relief='flat',
            padx=10,
            pady=5,
            command=self.clear_record_filters,
            cursor='hand2'
        )
        clear_filter_btn.pack(side=tk.LEFT, padx=5)
        
        # Actions frame
        actions_frame = tk.LabelFrame(
            top_frame,
            text="⚡ Actions",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent']
        )
        actions_frame.pack(side=tk.RIGHT)
        
        # Action buttons
        buttons_frame = tk.Frame(actions_frame, bg=self.colors['primary'])
        buttons_frame.pack(padx=10, pady=10)
        
        export_records_btn = tk.Button(
            buttons_frame,
            text="📊 Export Records",
            font=('Segoe UI', 10, 'bold'),
            bg='#28a745',
            fg='white',
            relief='flat',
            padx=15,
            pady=8,
            command=self.export_records_to_excel,
            cursor='hand2'
        )
        export_records_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        share_records_btn = tk.Button(
            buttons_frame,
            text="📤 Share Data",
            font=('Segoe UI', 10, 'bold'),
            bg='#6f42c1',
            fg='white',
            relief='flat',
            padx=15,
            pady=8,
            command=self.share_data_dialog,
            cursor='hand2'
        )
        share_records_btn.pack(side=tk.LEFT, padx=5)

        # New: Overdue notice letter generation button
        overdue_letter_btn = tk.Button(
            buttons_frame,
            text="📄 Overdue Letter (Word)",
            font=('Segoe UI', 10, 'bold'),
            bg='#d35400',
            fg='white',
            relief='flat',
            padx=15,
            pady=8,
            command=self.export_overdue_notice_letter_word,
            cursor='hand2'
        )
        overdue_letter_btn.pack(side=tk.LEFT, padx=5)
        # Optional Excel version button retained for users wanting spreadsheet format
        # Excel overdue letter button removed per user request (Word only)
        
        # Records list
        records_list_frame = tk.LabelFrame(
            records_frame,
            text="📋 Complete Transaction Records",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent'],
            padx=10,
            pady=10
        )
        records_list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Records treeview
        record_columns = ('Enrollment No', 'Student Name', 'Book ID', 'Book Title', 'Borrow Date', 'Due Date', 'Return Date', 'Status', 'Fine')
        self.records_tree = ttk.Treeview(records_list_frame, columns=record_columns, show='headings', height=15)
        record_widths = {'Enrollment No': 120, 'Student Name': 150, 'Book ID': 100, 'Book Title': 200, 'Borrow Date': 100, 'Due Date': 100, 'Return Date': 100, 'Status': 80, 'Fine': 80}
        for col in record_columns:
            self.records_tree.heading(col, text=col)
            self.records_tree.column(col, width=record_widths[col])
        # Scrollbars for records
        records_v_scrollbar = ttk.Scrollbar(records_list_frame, orient=tk.VERTICAL, command=self.records_tree.yview)
        records_h_scrollbar = ttk.Scrollbar(records_list_frame, orient=tk.HORIZONTAL, command=self.records_tree.xview)
        self.records_tree.configure(yscrollcommand=records_v_scrollbar.set, xscrollcommand=records_h_scrollbar.set)
        # Pack records treeview and scrollbars
        self.records_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        records_v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        records_h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def show_date_picker(self, entry_widget):
        """Show a simple date picker dialog"""
        from tkinter import simpledialog
        
        # Create a simple date input dialog
        date_str = simpledialog.askstring(
            "Select Date",
            "Enter date (YYYY-MM-DD):",
            initialvalue=entry_widget.get() or datetime.now().strftime('%Y-%m-%d')
        )
        
        if date_str:
            try:
                # Validate date format
                datetime.strptime(date_str, '%Y-%m-%d')
                entry_widget.delete(0, tk.END)
                entry_widget.insert(0, date_str)
            except ValueError:
                messagebox.showerror("Error", "Invalid date format! Please use YYYY-MM-DD")
    
    def show_add_student_dialog(self):
        """Show add student dialog with Computer department default"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Student")
        dialog.geometry("500x400")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 100, self.root.winfo_rooty() + 100))
        
        # Title
        title_label = tk.Label(
            dialog,
            text="👥 Add New Student",
            font=('Segoe UI', 16, 'bold'),
            bg='white',
            fg=self.colors['accent']
        )
        title_label.pack(pady=(20, 30))
        
        # Form frame
        form_frame = tk.Frame(dialog, bg='white')
        form_frame.pack(expand=True, padx=40)
        
        # Form fields
        fields = [
            ("Enrollment No:", "enrollment"),
            ("Full Name:", "name"),
            ("Email:", "email"),
            ("Phone:", "phone"),
            ("Year:", "year")
        ]
        
        entries = {}
        
        for i, (label_text, field_name) in enumerate(fields):
            # Label
            label = tk.Label(
                form_frame,
                text=label_text,
                font=('Segoe UI', 11, 'bold'),
                bg='white',
                fg=self.colors['accent']
            )
            label.grid(row=i, column=0, sticky='w', pady=(0, 15), padx=(0, 20))
            
            # Entry or Combobox
            if field_name == "year":
                entry = ttk.Combobox(
                    form_frame,
                    values=["1st", "2nd", "3rd", "4th"],
                    font=('Segoe UI', 11),
                    width=25,
                    state="readonly"
                )
                entry.set("1st")  # Default to 1st year
            else:
                entry = tk.Entry(
                    form_frame,
                    font=('Segoe UI', 11),
                    width=30,
                    relief='solid',
                    bd=2
                )
            
            entry.grid(row=i, column=1, pady=(0, 15))
            entries[field_name] = entry
        
        # Department info (read-only, always Computer)
        dept_label = tk.Label(
            form_frame,
            text="Department:",
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg=self.colors['accent']
        )
        dept_label.grid(row=len(fields), column=0, sticky='w', pady=(0, 15), padx=(0, 20))
        
        dept_value = tk.Label(
            form_frame,
            text="Computer (Default)",
            font=('Segoe UI', 11),
            bg='white',
            fg=self.colors['secondary']
        )
        dept_value.grid(row=len(fields), column=1, sticky='w', pady=(0, 15))
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg='white')
        btn_frame.pack(pady=20)
        
        def save_student():
            # Validate fields
            if not all([entries['enrollment'].get(), entries['name'].get()]):
                messagebox.showerror("Error", "Enrollment No and Name are required!")
                return
            
            # Add student with Computer department default
            success, message = self.db.add_student(
                entries['enrollment'].get(),
                entries['name'].get(),
                entries['email'].get(),
                entries['phone'].get(),
                "Computer",  # Always Computer department
                entries['year'].get()
            )
            
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                self.refresh_students()
                # Refresh dashboard so total student count updates immediately
                try:
                    self.refresh_dashboard()
                except Exception:
                    pass
            else:
                messagebox.showerror("Error", message)
        
        save_btn = tk.Button(
            btn_frame,
            text="💾 Save Student",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['secondary'],
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            command=save_student,
            cursor='hand2'
        )
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = tk.Button(
            btn_frame,
            text="❌ Cancel",
            font=('Segoe UI', 12, 'bold'),
            bg='#6c757d',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            command=dialog.destroy,
            cursor='hand2'
        )
        cancel_btn.pack(side=tk.LEFT)
        
        # Focus on first field
        entries['enrollment'].focus()
    
    def show_add_book_dialog(self):
        """Show add book dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Book")
        dialog.geometry("500x450")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 100, self.root.winfo_rooty() + 100))
        
        # Title
        title_label = tk.Label(
            dialog,
            text="📚 Add New Book",
            font=('Segoe UI', 16, 'bold'),
            bg='white',
            fg=self.colors['accent']
        )
        title_label.pack(pady=(20, 30))
        
        # Form frame
        form_frame = tk.Frame(dialog, bg='white')
        form_frame.pack(expand=True, padx=40)
        
        # Form fields
        fields = [
            ("Book ID:", "book_id"),
            ("Title:", "title"),
            ("Author:", "author"),
            ("ISBN:", "isbn"),
            ("Category:", "category"),
            ("Total Copies:", "copies")
        ]
        
        entries = {}
        
        for i, (label_text, field_name) in enumerate(fields):
            # Label
            label = tk.Label(
                form_frame,
                text=label_text,
                font=('Segoe UI', 11, 'bold'),
                bg='white',
                fg=self.colors['accent']
            )
            label.grid(row=i, column=0, sticky='w', pady=(0, 15), padx=(0, 20))
            
            # Entry or Combobox
            if field_name == "category":
                entry = ttk.Combobox(
                    form_frame,
                    values=["Technology", "Textbook", "Research"],
                    font=('Segoe UI', 11),
                    width=25,
                    state="readonly"
                )
                entry.set("Technology")  # Default category
            else:
                entry = tk.Entry(
                    form_frame,
                    font=('Segoe UI', 11),
                    width=30,
                    relief='solid',
                    bd=2
                )
                if field_name == "copies":
                    entry.insert(0, "1")  # Default to 1 copy
            
            entry.grid(row=i, column=1, pady=(0, 15))
            entries[field_name] = entry
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg='white')
        btn_frame.pack(pady=20)
        
        def save_book():
            # Validate required fields
            required_fields = ['book_id', 'title']
            for field in required_fields:
                if not entries[field].get().strip():
                    messagebox.showerror("Error", f"{field.replace('_', ' ').title()} is required!")
                    return
            # Validate copies
            try:
                copies = int(entries['copies'].get())
                if copies <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "Total copies must be a positive number!")
                return
            # Add book
            success, message = self.db.add_book(
                entries['book_id'].get().strip(),
                entries['title'].get().strip(),
                entries['author'].get().strip(),
                entries['isbn'].get().strip(),
                entries['category'].get(),
                copies
            )
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                # Refresh books view
                self.refresh_books()
                # Update dashboard statistics
                self.refresh_dashboard()
            else:
                messagebox.showerror("Error", message)
        
        save_btn = tk.Button(
            btn_frame,
            text="💾 Save Book",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['secondary'],
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            command=save_book,
            cursor='hand2'
        )
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = tk.Button(
            btn_frame,
            text="❌ Cancel",
            font=('Segoe UI', 12, 'bold'),
            bg='#6c757d',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            command=dialog.destroy,
            cursor='hand2'
        )
        cancel_btn.pack(side=tk.LEFT)
        
        # Focus on first field
        entries['book_id'].focus()
    
    def borrow_book(self):
        """Handle book borrowing"""
        enrollment_text = self.borrow_enrollment_entry.get().strip()
        book_text = self.borrow_book_id_entry.get().strip()
        borrow_date = self.borrow_borrow_date_entry.get().strip()
        due_date = self.borrow_due_date_entry.get().strip()
        
        if not all([enrollment_text, book_text, borrow_date, due_date]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        # Extract enrollment number (before " - " if formatted, otherwise use as is)
        enrollment_no = enrollment_text.split(' - ')[0] if ' - ' in enrollment_text else enrollment_text
        
        # Extract book ID (before " - " if formatted, otherwise use as is)
        book_id = book_text.split(' - ')[0] if ' - ' in book_text else book_text
        
        # Validate date format (borrow & due)
        try:
            from datetime import datetime, timedelta
            datetime.strptime(borrow_date, '%Y-%m-%d')
            datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Invalid date format! Please use YYYY-MM-DD")
            return
        # Ensure due >= borrow
        from datetime import datetime as _dt
        if _dt.strptime(due_date, '%Y-%m-%d') < _dt.strptime(borrow_date, '%Y-%m-%d'):
            messagebox.showerror("Error", "Due date cannot be before borrow date")
            return

        # UI-side validation for allowed range: 1..LOAN_PERIOD_DAYS days from borrow
        try:
            bd_obj = datetime.strptime(borrow_date, '%Y-%m-%d')
            dd_obj = datetime.strptime(due_date, '%Y-%m-%d')
            diff_days = (dd_obj - bd_obj).days
            if not (1 <= diff_days <= LOAN_PERIOD_DAYS):
                messagebox.showerror(
                    "Invalid Due Date",
                    f"Due date must be between 1 and {LOAN_PERIOD_DAYS} days after the borrow date."
                )
                return
        except Exception:
            pass

        success, message = self.db.borrow_book(enrollment_no, book_id, borrow_date, due_date)
        
        if success:
            # Determine if late and show punishment popup if overdue
            late_popup_shown = False
            try:
                conn = self.db.get_connection()
                cur = conn.cursor()
                cur.execute("""
                    SELECT br.due_date, br.return_date
                    FROM borrow_records br
                    WHERE br.enrollment_no = ? AND br.book_id = ? AND br.status = 'returned'
                    ORDER BY br.id DESC LIMIT 1
                """, (enrollment_no, book_id))
                row = cur.fetchone()
                conn.close()
                if row:
                    due_date_val, return_date_val = row
                    from datetime import datetime as _dt
                    try:
                        dd = _dt.strptime(due_date_val, '%Y-%m-%d').date()
                        rd = _dt.strptime(return_date_val, '%Y-%m-%d').date()
                        if rd > dd:
                            overdue_days = (rd - dd).days
                            fine_amount = overdue_days * FINE_PER_DAY
                            messagebox.showwarning(
                                "Late Return",
                                f"You failed to return the book on time.\n\nDue Date: {due_date_val}\nReturn Date: {return_date_val}\nOverdue Days: {overdue_days}\nFine: {fine_amount} units\n\nYou are punished for late submission!"
                            )
                            late_popup_shown = True
                    except Exception:
                        pass
            except Exception:
                pass
            if not late_popup_shown:
                messagebox.showinfo("Success", message)
            # Clear fields
            self.borrow_enrollment_entry.delete(0, tk.END)
            self.borrow_book_id_entry.delete(0, tk.END)
            # Reset due date to default (suggest max window of 7 days)
            today_str = datetime.now().strftime('%Y-%m-%d')
            self.borrow_borrow_date_entry.delete(0, tk.END)
            self.borrow_borrow_date_entry.insert(0, today_str)
            self.borrow_due_date_entry.delete(0, tk.END)
            # Suggest 7-day period by default; user may change to 1..7 days
            default_due = (datetime.now() + timedelta(days=LOAN_PERIOD_DAYS)).strftime('%Y-%m-%d')
            self.borrow_due_date_entry.insert(0, default_due)

            # Clear student and book details
            self.borrow_student_details.config(text="")
            self.borrow_book_details.config(text="")

            # Refresh views
            self.refresh_borrowed()
            self.refresh_books()
            self.refresh_dashboard()
            self.refresh_records()
        else:
            messagebox.showerror("Error", message)
    
    def return_book(self):
        """Handle book return"""
        enrollment_text = self.return_enrollment_entry.get().strip()
        book_text = self.return_book_id_entry.get().strip()
        
        if not all([enrollment_text, book_text]):
            messagebox.showerror("Error", "Both Enrollment No and Book ID are required!")
            return
        
        # Extract enrollment number (before " - " if formatted, otherwise use as is)
        enrollment_no = enrollment_text.split(' - ')[0] if ' - ' in enrollment_text else enrollment_text
        
        # Extract book ID (before " - " if formatted, otherwise use as is)
        book_id = book_text.split(' - ')[0] if ' - ' in book_text else book_text
        
        # Get optional return date from UI
        return_date_input = getattr(self, 'return_date_entry', None)
        user_return_date = return_date_input.get().strip() if return_date_input else None
        if user_return_date == '':
            user_return_date = None

        success, message = self.db.return_book(enrollment_no, book_id, user_return_date)
        
        if success:
            messagebox.showinfo("Success", message)
            # Late return fine popup
            try:
                conn = self.db.get_connection()
                cur = conn.cursor()
                cur.execute("""
                    SELECT due_date, return_date FROM borrow_records
                    WHERE enrollment_no=? AND book_id=?
                    ORDER BY id DESC LIMIT 1
                """, (enrollment_no, book_id))
                row = cur.fetchone()
                conn.close()
                if row and row[0] and row[1]:
                    from datetime import datetime as _dt
                    due_dt = _dt.strptime(row[0], '%Y-%m-%d')
                    ret_dt = _dt.strptime(row[1], '%Y-%m-%d')
                    days_late = (ret_dt - due_dt).days
                    if days_late > 0:
                        fine_amount = days_late * FINE_PER_DAY
                        messagebox.showwarning(
                            "Late Return",
                            f"This book is returned {days_late} day(s) late.\nFine: Rs {fine_amount}"
                        )
            except Exception as e:
                print(f"Late return fine computation failed: {e}")
            # Clear fields
            self.return_enrollment_entry.delete(0, tk.END)
            self.return_book_id_entry.delete(0, tk.END)
            
            # Clear student details and return date (reset to today for convenience)
            self.return_student_details.config(text="")
            if return_date_input:
                return_date_input.delete(0, tk.END)
                return_date_input.insert(0, datetime.now().strftime('%Y-%m-%d'))
            
            # Refresh views
            self.refresh_borrowed()
            self.refresh_books()
            self.refresh_dashboard()
            self.refresh_records()
        else:
            messagebox.showerror("Error", message)
    
    def import_students_from_excel(self):
        """Import students from Excel file (append; skip invalid or duplicate)."""
        file_path = filedialog.askopenfilename(
            title="Select Students Excel file",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if not file_path:
            return
        try:
            df = pd.read_excel(file_path)
            # Normalize columns
            df.columns = df.columns.str.lower().str.replace(' ', '_')
            # Accept some synonyms
            column_map = {
                'enrollment': 'enrollment_no',
                'enrollmentno': 'enrollment_no',
                'enrollment_number': 'enrollment_no'
            }
            df.rename(columns={k: v for k, v in column_map.items() if k in df.columns}, inplace=True)
            required = ['enrollment_no', 'name']
            missing = [c for c in required if c not in df.columns]
            if missing:
                messagebox.showerror("Error", f"Missing required columns: {', '.join(missing)}")
                return
            added = 0
            skipped = 0
            duplicate = 0
            errors = 0
            error_list = []
            for idx, row in df.iterrows():
                row_no = idx + 2
                try:
                    enrollment = str(row.get('enrollment_no', '')).strip()
                    name = str(row.get('name', '')).strip()
                    email = str(row.get('email', '')).strip()
                    phone = str(row.get('phone', '')).strip()
                    department = str(row.get('department', 'Computer')).strip() or 'Computer'
                    year = str(row.get('year', '2nd Year')).strip() or '2nd Year'
                    if not enrollment or not name or enrollment.lower() == 'nan' or name.lower() == 'nan':
                        skipped += 1
                        continue
                    success, message = self.db.add_student(enrollment, name, email, phone, department, year)
                    if success:
                        added += 1
                    else:
                        # Determine if it's duplicate vs generic error
                        if 'exists' in message.lower() or 'duplicate' in message.lower():
                            duplicate += 1
                        else:
                            errors += 1
                            error_list.append(f"Row {row_no}: {message}")
                except Exception as e:
                    errors += 1
                    error_list.append(f"Row {row_no}: {e}")
            summary = (
                f"Import completed!\n\nAdded: {added}\nDuplicates: {duplicate}\n"
                f"Skipped (missing enrollment/name): {skipped}\nErrors: {errors}"
            )
            if error_list:
                summary += "\n\nFirst few errors:\n" + "\n".join(error_list[:5])
                if len(error_list) > 5:
                    summary += f"\n... and {len(error_list) - 5} more errors."
            messagebox.showinfo("Import Results", summary)
            if added or duplicate:
                self.refresh_students()
                self.refresh_dashboard()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import Excel file: {e}")
    def search_students(self):
        """Search and filter students"""
        search_term = self.student_search_var.get().lower()
        year_filter = self.student_year_filter.get()
        
        # Get all students from database
        try:
            students = self.db.get_students()
            
            # Filter students
            filtered_students = []
            for student in students:
                # Apply search term filter
                if search_term:
                    student_text = f"{student[0]} {student[1]} {student[2]} {student[3]}".lower()
                    if search_term not in student_text:
                        continue
                
                # Apply year filter
                if year_filter != "All":
                    if student[4] != year_filter:  # Year is at index 4
                        continue
                
                filtered_students.append(student)
            
            # Populate the tree with filtered results
            self.populate_students_tree(filtered_students)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error searching students: {str(e)}")
    
    def search_books(self):
        """Search and filter books"""
        try:
            # Check if books tree exists
            if hasattr(self, 'books_tree'):
                # Get all books from database
                books = self.db.get_books()
                # For now, just populate all books - you can add filtering later
                self.populate_books_tree(books)
        except Exception as e:
            print(f"Error searching books: {str(e)}")
    
    def search_records(self):
        """Search and filter records"""
        search_term = self.record_search_var.get().lower()
        type_filter = self.record_type_filter.get()
        from_date = self.record_from_date.get()
        to_date = self.record_to_date.get()
        
        records = self.get_all_records()
        
        # Filter records
        filtered_records = []
        for record in records:
            # record: (enroll, name, book_id, title, borrow_date, due_date, return_date, status, fine)
            status_val = record[7]
            fine_val = record[8]
            if type_filter != "All":
                if type_filter == "Overdue":
                    if fine_val == '0':
                        continue
                else:
                    if status_val.lower() != type_filter.lower():
                        continue
            
            # Apply search filter
            if search_term:
                if not any(search_term in str(field).lower() for field in record):
                    continue
            
            # Apply date filters
            if from_date:
                try:
                    record_date = datetime.strptime(record[4], '%Y-%m-%d')  # borrow_date index 4
                    from_date_obj = datetime.strptime(from_date, '%Y-%m-%d')
                    if record_date < from_date_obj:
                        continue
                except ValueError:
                    pass
            
            if to_date:
                try:
                    record_date = datetime.strptime(record[4], '%Y-%m-%d')
                    to_date_obj = datetime.strptime(to_date, '%Y-%m-%d')
                    if record_date > to_date_obj:
                        continue
                except ValueError:
                    pass
            
            filtered_records.append(record)
        
        self.populate_records_tree(filtered_records)
    
    def clear_record_filters(self):
        """Clear all record filters"""
        self.record_search_var.set("")
        self.record_type_filter.set("All")
        self.record_from_date.delete(0, tk.END)
        self.record_to_date.delete(0, tk.END)
        self.search_records()
    
    def refresh_all_data(self):
        """Refresh all data in the application"""
        self.refresh_dashboard()
        self.refresh_students()
        self.refresh_books()
        self.refresh_borrowed()
        self.refresh_records()
    
    def refresh_dashboard(self):
        """Refresh dashboard statistics"""
        # Refresh dashboard borrowed books
        if hasattr(self, 'dashboard_borrowed_tree'):
            self.refresh_dashboard_borrowed()
        
        # Refresh statistics cards if they exist
        if hasattr(self, 'stats_container'):
            # Clear existing stats
            for widget in self.stats_container.winfo_children():
                widget.destroy()
            # Recreate stats cards
            self.create_stats_cards(self.stats_container)
    
    def refresh_students(self):
        """Refresh students list"""
        self.search_students()  # This will apply current filters
    
    def refresh_books(self):
        """Refresh books list"""
        self.search_books()  # This will apply current filters
    
    def refresh_borrowed(self):
        """Refresh borrowed books list"""
        borrowed = self.db.get_borrowed_books()
        self.populate_borrowed_tree(borrowed)
    
    def refresh_records(self):
        """Refresh records list"""
        self.search_records()  # This will apply current filters
    
    def populate_students_tree(self, students):
        """Populate students treeview"""
        if hasattr(self, 'students_tree'):
            for item in self.students_tree.get_children():
                self.students_tree.delete(item)
            
            for student in students:
                # Display only relevant fields (exclude department as it's always Computer)
                display_data = (student[1], student[2], student[3], student[4], student[6])  # Enrollment, Name, Email, Phone, Year
                self.students_tree.insert('', 'end', values=display_data)
    
    def populate_books_tree(self, books):
        """Populate books treeview"""
        if hasattr(self, 'books_tree'):
            for item in self.books_tree.get_children():
                self.books_tree.delete(item)
            
            for book in books:
                # Display all book fields
                display_data = (book[1], book[2], book[3], book[4], book[5], book[6], book[7])  # All except id
                self.books_tree.insert('', 'end', values=display_data)
    
    def populate_borrowed_tree(self, borrowed):
        """Populate borrowed books treeview with enhanced data
        Expected order from get_borrowed_books():
        (enrollment_no, student_name, department, year, book_id, title, author, borrow_date, due_date)
        """
        if hasattr(self, 'borrowed_tree'):
            for item in self.borrowed_tree.get_children():
                self.borrowed_tree.delete(item)
            
            for record in borrowed:
                # record indexes mapping
                enrollment_no = record[0]
                student_name = record[1]
                book_id = record[4]
                book_title = record[5]
                borrow_date = record[7]
                due_date_val = record[8]
                # Calculate days left
                try:
                    from datetime import datetime as _dt
                    due_date = _dt.strptime(due_date_val, '%Y-%m-%d').date()
                    today = _dt.now().date()
                    delta = (due_date - today).days
                    if delta < 0:
                        days_left_str = f"Overdue {abs(delta)}d"
                        tag = 'overdue'
                    elif delta == 0:
                        days_left_str = 'Due Today'
                        tag = ''
                    else:
                        days_left_str = f"{delta}d left"
                        tag = ''
                except Exception:
                    days_left_str = 'N/A'
                    tag = ''
                display_data = (student_name, book_id, book_title, borrow_date, due_date_val, days_left_str)
                self.borrowed_tree.insert('', 'end', values=display_data, tags=(tag,))
            try:
                self.borrowed_tree.tag_configure('overdue', background='#ffe6e6', foreground='#b30000')
            except Exception:
                pass
    
    def populate_activities_tree(self, activities):
        """Populate recent activities treeview"""
        if hasattr(self, 'activities_tree'):
            for item in self.activities_tree.get_children():
                self.activities_tree.delete(item)
            
            for activity in activities:
                self.activities_tree.insert('', 'end', values=activity)
    
    def populate_records_tree(self, records):
        """Populate records treeview"""
        if hasattr(self, 'records_tree'):
            for item in self.records_tree.get_children():
                self.records_tree.delete(item)
            
            for record in records:
                # record: (..., status, fine)
                *base, status, fine = record
                fine_is_num = False
                if isinstance(fine, str):
                    try:
                        fine_val_num = int(fine)
                        fine_is_num = True
                    except ValueError:
                        fine_val_num = fine
                else:
                    fine_val_num = fine
                    fine_is_num = True
                fine_display = f"{fine_val_num} (Late)" if fine_is_num and isinstance(fine_val_num, int) and fine_val_num > 0 else str(fine_val_num)
                tag = 'late' if (fine_is_num and isinstance(fine_val_num, int) and fine_val_num > 0) else ''
                self.records_tree.insert('', 'end', values=(*base, status, fine_display), tags=(tag,))
            try:
                self.records_tree.tag_configure('late', background='#fff3cd')
            except Exception:
                pass
    
    def get_student_name(self, enrollment_no):
        """Get student name by enrollment number"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM students WHERE enrollment_no = ?", (enrollment_no,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else enrollment_no
        except:
            return enrollment_no
    
    def get_book_title(self, book_id):
        """Get book title by book ID"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT title FROM books WHERE book_id = ?", (book_id,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else book_id
        except:
            return book_id
    
    def get_recent_activities(self):
        """Get recent activities for dashboard"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Get recent borrow/return activities
            cursor.execute("""
                SELECT 
                    CASE WHEN return_date IS NULL THEN 'Borrow' ELSE 'Return' END as type,
                    s.name as student_name,
                    b.title as book_title,
                    CASE WHEN return_date IS NULL THEN borrow_date ELSE return_date END as activity_date,
                    status
                FROM borrow_records br
                JOIN students s ON br.enrollment_no = s.enrollment_no
                JOIN books b ON br.book_id = b.book_id
                ORDER BY br.id DESC
                LIMIT 20
            """)
            
            activities = cursor.fetchall()
            conn.close()
            return activities
        except Exception as e:
            print(f"Error getting recent activities: {e}")
            return []
    
    def get_all_records(self):
        """Get all transaction records"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            # Return enrollment_no and book_id explicitly for correct display
            cursor.execute("""
                SELECT 
                    br.enrollment_no,
                    s.name as student_name,
                    br.book_id,
                    b.title as book_title,
                    br.borrow_date,
                    br.due_date,
                    COALESCE(br.return_date, 'Not returned') as return_date,
                    br.status,
                    CASE 
                        WHEN br.status = 'borrowed' AND date('now') > br.due_date 
                        THEN CAST(julianday('now') - julianday(br.due_date) AS INT)
                        ELSE 0 
                    END as days_overdue
                FROM borrow_records br
                JOIN students s ON br.enrollment_no = s.enrollment_no
                JOIN books b ON br.book_id = b.book_id
                ORDER BY br.id DESC
            """)
            
            records = cursor.fetchall()
            conn.close()
            
            # Format records for display
            formatted_records = []
            from datetime import datetime as _dt
            today = _dt.now().date()
            for rec in records:
                (enroll, student_name, book_id, title, borrow_date, due_date, return_date, status, days_overdue) = rec
                # Determine effective overdue days & fine
                try:
                    due_d = _dt.strptime(due_date, '%Y-%m-%d').date()
                except Exception:
                    due_d = None
                fine = 0
                if status == 'borrowed':
                    # still out; overdue based on today
                    if due_d and today > due_d:
                        overdue_days = (today - due_d).days
                        fine = overdue_days * FINE_PER_DAY
                else:
                    # returned; compute late based on return_date
                    try:
                        ret_d = _dt.strptime(return_date, '%Y-%m-%d').date()
                        if due_d and ret_d > due_d:
                            overdue_days = (ret_d - due_d).days
                            fine = overdue_days * FINE_PER_DAY
                    except Exception:
                        pass
                # Keep fine as numeric for downstream display logic
                formatted_records.append((enroll, student_name, book_id, title, borrow_date, due_date, return_date, status, fine))
            return formatted_records
        except Exception as e:
            print(f"Error getting records: {e}")
            return []

    # ------------------------------------------------------------------
    # Date auto update helpers
    # ------------------------------------------------------------------
    def on_borrow_date_changed(self, event=None):
        """When borrow date changes, suggest due date = borrow + LOAN_PERIOD_DAYS (max),
        but allow user to choose 1..LOAN_PERIOD_DAYS days range."""
        try:
            from datetime import datetime as _dt, timedelta
            borrow_str = self.borrow_borrow_date_entry.get()
            bd = _dt.strptime(borrow_str, '%Y-%m-%d')
            new_due = (bd + timedelta(days=LOAN_PERIOD_DAYS)).strftime('%Y-%m-%d')
            if DateEntry:
                try:
                    self.borrow_due_date_entry.config(state='normal')
                except Exception:
                    pass
                try:
                    self.borrow_due_date_entry.set_date(_dt.strptime(new_due, '%Y-%m-%d'))
                except Exception:
                    self.borrow_due_date_entry.delete(0, tk.END)
                    self.borrow_due_date_entry.insert(0, new_due)
                try:
                    self.borrow_due_date_entry.config(state='readonly')
                except Exception:
                    pass
            else:
                self.borrow_due_date_entry.delete(0, tk.END)
                self.borrow_due_date_entry.insert(0, new_due)
        except Exception as e:
            print(f"Auto due date update failed: {e}")

    def on_due_date_attempt_change(self):
        """Validate due-date change: must be within 1..LOAN_PERIOD_DAYS days of borrow date."""
        try:
            from datetime import datetime as _dt
            bd = _dt.strptime(self.borrow_borrow_date_entry.get(), '%Y-%m-%d')
            dd = _dt.strptime(self.borrow_due_date_entry.get(), '%Y-%m-%d')
            diff = (dd - bd).days
            if not (1 <= diff <= LOAN_PERIOD_DAYS):
                messagebox.showerror(
                    "Invalid Due Date",
                    f"Due date must be between 1 and {LOAN_PERIOD_DAYS} days after the borrow date."
                )
                # Re-suggest maximum allowed
                from datetime import timedelta
                suggested = (bd + timedelta(days=LOAN_PERIOD_DAYS)).strftime('%Y-%m-%d')
                try:
                    self.borrow_due_date_entry.config(state='normal')
                    self.borrow_due_date_entry.delete(0, tk.END)
                    self.borrow_due_date_entry.insert(0, suggested)
                finally:
                    try:
                        self.borrow_due_date_entry.config(state='readonly')
                    except Exception:
                        pass
        except Exception:
            pass
    
    def export_students_dialog(self):
        """Show export students dialog with year selection"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Export Students to Excel")
        dialog.geometry("400x300")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 200, self.root.winfo_rooty() + 200))
        
        # Title
        title_label = tk.Label(
            dialog,
            text="📊 Export Students",
            font=('Segoe UI', 16, 'bold'),
            bg='white',
            fg=self.colors['accent']
        )
        title_label.pack(pady=(20, 30))
        
        # Options frame
        options_frame = tk.Frame(dialog, bg='white')
        options_frame.pack(expand=True, padx=40)
        
        # Year selection
        year_label = tk.Label(
            options_frame,
            text="Select Year to Export:",
            font=('Segoe UI', 12, 'bold'),
            bg='white',
            fg=self.colors['accent']
        )
        year_label.pack(pady=(0, 10))
        
        year_var = tk.StringVar(value="All")
        year_frame = tk.Frame(options_frame, bg='white')
        year_frame.pack(pady=(0, 20))
        
        years = ["All", "1st", "2nd", "3rd", "4th"]
        for year in years:
            rb = tk.Radiobutton(
                year_frame,
                text=year,
                variable=year_var,
                value=year,
                font=('Segoe UI', 11),
                bg='white',
                fg=self.colors['accent']
            )
            rb.pack(anchor='w')
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg='white')
        btn_frame.pack(pady=20)
        
        def export_data():
            selected_year = year_var.get()
            self.export_students_to_excel(selected_year)
            dialog.destroy()
        
        export_btn = tk.Button(
            btn_frame,
            text="📊 Export to Excel",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['secondary'],
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            command=export_data,
            cursor='hand2'
        )
        export_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = tk.Button(
            btn_frame,
            text="❌ Cancel",
            font=('Segoe UI', 12, 'bold'),
            bg='#6c757d',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            command=dialog.destroy,
            cursor='hand2'
        )
        cancel_btn.pack(side=tk.LEFT)
    
    def export_students_to_excel(self, year_filter="All"):
        """Export students to Excel with year filter"""
        try:
            students = self.db.get_students()
            
            # Filter by Computer department and year
            filtered_students = []
            for student in students:
                if student[5] == "Computer":  # Department filter
                    if year_filter == "All" or student[6] == year_filter:  # Year filter
                        filtered_students.append({
                            'Enrollment No': student[1],
                            'Name': student[2],
                            'Email': student[3],
                            'Phone': student[4],
                            'Department': student[5],
                            'Year': student[6]
                        })
            
            if not filtered_students:
                messagebox.showwarning("Warning", f"No students found for year: {year_filter}")
                return
            
            # Create DataFrame
            df = pd.DataFrame(filtered_students)
            
            # Save to file
            filename = f"students_{year_filter}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                # Tkinter option is 'initialfile' (not 'initialname')
                initialfile=filename
            )
            
            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Success", f"Students data exported to {file_path}")
                
                # Ask if user wants to open the file
                if messagebox.askyesno("Open File", "Do you want to open the exported file?"):
                    self.open_file(file_path)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export students: {str(e)}")
    
    def export_books_to_excel(self):
        """Export books to Excel"""
        try:
            books = self.db.get_books()
            
            # Filter Computer department books
            filtered_books = []
            for book in books:
                # Defensive validation: check for missing Book ID or Title (should not happen due to enforced validation)
                invalid_rows = []
                for b in books:
                    # Assuming schema: (id, book_id, title, author, isbn, category, total_copies, available_copies)
                    try:
                        book_id_val = str(b[1]).strip()
                        title_val = str(b[2]).strip()
                        if not book_id_val or not title_val:
                            invalid_rows.append(b)
                    except Exception:
                        invalid_rows.append(b)
                if invalid_rows:
                    if not messagebox.askyesno(
                        "Validation Warning",
                        f"Detected {len(invalid_rows)} book record(s) with missing Book ID or Title. Continue export?"
                    ):
                        return
                if book[5] in ["Technology", "Textbook", "Research"]:
                    filtered_books.append({
                        'Book ID': book[1],
                        'Title': book[2],
                        'Author': book[3],
                        'ISBN': book[4],
                        'Category': book[5],
                        'Total Copies': book[6],
                        'Available Copies': book[7],
                        'Date Added': book[8]
                    })
            
            if not filtered_books:
                messagebox.showwarning("Warning", "No books found to export!")
                return
            
            # Create DataFrame
            df = pd.DataFrame(filtered_books)
            
            # Save to file
            filename = f"books_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                # Correct parameter name
                initialfile=filename
            )
            
            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Success", f"Books data exported to {file_path}")
                
                # Ask if user wants to open the file
                if messagebox.askyesno("Open File", "Do you want to open the exported file?"):
                    self.open_file(file_path)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export books: {str(e)}")
    
    def export_records_to_excel(self):
        """Export records to Excel"""
        try:
            # Instead of exporting ALL records from DB, export only what user currently sees
            # in the Records tab (i.e., after filters/search applied). This gives a true
            # "filtered export" matching on‑screen data.
            if not hasattr(self, 'records_tree'):
                messagebox.showerror("Error", "Records view not initialized yet.")
                return

            visible_records = []
            for item_id in self.records_tree.get_children():
                vals = self.records_tree.item(item_id, 'values')
                # Expecting 9-tuple: (Enrollment No, Student Name, Book ID, Book Title, Borrow Date, Due Date, Return Date, Status, Fine)
                visible_records.append(vals)

            if not visible_records:
                messagebox.showwarning("Warning", "No filtered records to export (the list is empty)!")
                return

            # Build DataFrame with the same column ordering used in the tree
            df = pd.DataFrame(visible_records, columns=[
                'Enrollment No', 'Student Name', 'Book ID', 'Book Title', 'Borrow Date',
                'Due Date', 'Return Date', 'Status', 'Fine'
            ])

            # (Optional future enhancement) Could add metadata sheet with applied filters.
            # For now keep it simple per request: export exactly what is visible.
            
            # Save to file
            filename = f"records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                # Correct parameter name
                initialfile=filename
            )
            
            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Success", f"Records data exported to {file_path}")
                
                # Ask if user wants to open the file
                if messagebox.askyesno("Open File", "Do you want to open the exported file?"):
                    self.open_file(file_path)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export records: {str(e)}")

    # ------------------------------------------------------------------
    # Overdue Notice Letter Export
    # ------------------------------------------------------------------
    def get_current_overdue_records(self):
        """Return list of overdue (currently borrowed and past due date) records.
        Each record tuple: (Enrollment No, Student Name, Book ID, Book Title, Borrow Date, Due Date, Return Date, Status, Fine)
        """
        overdue = []
        try:
            all_records = self.get_all_records()
            today = datetime.now().date()
            from datetime import datetime as _dt
            for rec in all_records:
                enroll, name, book_id, title, borrow_date, due_date, return_date, status, fine = rec
                if status == 'borrowed':
                    try:
                        due_d = _dt.strptime(due_date, '%Y-%m-%d').date()
                        if due_d < today:
                            days_overdue = (today - due_d).days
                            overdue.append({
                                'Enrollment No': enroll,
                                'Student Name': name,
                                'Book ID': book_id,
                                'Book Title': title,
                                'Borrow Date': borrow_date,
                                'Due Date': due_date,
                                'Days Overdue': days_overdue,
                                'Accrued Fine': int(days_overdue) * FINE_PER_DAY
                            })
                    except Exception:
                        continue
            return overdue
        except Exception as e:
            print(f"Overdue fetch error: {e}")
            return []

    def export_overdue_notice_letter(self):
        """Generate overdue notice as Excel (.xlsx) + plain text (.txt) letter.
        Excel sheet contains letter heading, body, table of overdue books, and closing with signature.
        """
        try:
            overdue = self.get_current_overdue_records()
            if not overdue:
                messagebox.showinfo("Overdue Notice", "There are currently no overdue borrowed books.")
                return

            today_str = datetime.now().strftime('%Y-%m-%d')
            ref_code = f"Library/Overdue/{datetime.now().strftime('%Y%m%d')}"

            body_lines = [
                "GOVERNMENT POLYTECHNIC AWASARI (Kh)",
                "Library of Computer Department",
                "", f"Date: {today_str}", f"Ref: {ref_code}", "",
                "Subject: Submission of Overdue Library Books",
                "", "Dear Students,", "",
                "The following students are hereby notified to immediately submit the listed library books that are now overdue.",
                f"A fine of Rs {FINE_PER_DAY} per day has accrued (or will continue to accrue) until the books are returned.",
                "Failure to comply today will trigger disciplinary action per departmental policy.",
                "", "Overdue Book List:", ""
            ]

            df = pd.DataFrame(overdue)
            base_filename = f"overdue_notice_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                initialfile=base_filename + '.xlsx'
            )
            if not file_path:
                return

            try:
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    sheet_name = 'Overdue Notice'
                    startrow = len(body_lines) + 1
                    df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=startrow)
                    ws = writer.book[sheet_name]
                    for idx, line in enumerate(body_lines, start=1):
                        ws.cell(row=idx, column=1, value=line)
                    for col_idx, col_name in enumerate(df.columns, start=1):
                        max_len = max(len(str(col_name)), *(len(str(v)) for v in df[col_name].astype(str)))
                        ws.column_dimensions[chr(64+col_idx)].width = min(max_len + 2, 50)
                    closing_start = startrow + len(df) + 3
                    closing_lines = [
                        "", "You are directed to return the above books without further delay.",
                        "Punishment Clause: Continued non-compliance after 3 days from this notice will result in suspension of borrowing privileges for one month and a formal report to the Academic Coordinator.",
                        "", "Regards,", "", "__________________________", "Librarian", "Library of Computer Department",
                        "Government Polytechnic Awasari (Kh)"
                    ]
                    for offset, line in enumerate(closing_lines):
                        ws.cell(row=closing_start + offset, column=1, value=line)
            except Exception as e:
                messagebox.showwarning("Excel Write Warning", f"Excel formatting fallback due to: {e}\nCreating plain text letter only.")

            # Create companion text letter
            try:
                txt_path = os.path.splitext(file_path)[0] + '.txt'
                cols = list(df.columns)
                col_widths = [max(len(c), *(len(str(v)) for v in df[c].astype(str))) for c in cols]
                def fmt_row(row_vals):
                    return "  ".join(str(v).ljust(w) for v, w in zip(row_vals, col_widths))
                table_lines = [fmt_row(cols), fmt_row(['-'*w for w in col_widths])] + [fmt_row(df.iloc[i]) for i in range(len(df))]
                closing_text = [
                    "", "You are directed to return the above books without further delay.",
                    "Punishment Clause: Continued non-compliance after 3 days from this notice will result in suspension of borrowing privileges for one month and a formal report to the Academic Coordinator.",
                    "", "Regards,", "", "__________________________", "Librarian", "Library of Computer Department", "Government Polytechnic Awasari (Kh)"
                ]
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write("\n".join(body_lines + table_lines + closing_text))
            except Exception as e:
                print(f"Text companion creation failed: {e}")

            messagebox.showinfo("Overdue Notice", f"Overdue notice letter exported:\n{file_path}")
            if messagebox.askyesno("Open File", "Open the Excel letter now?"):
                self.open_file(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate overdue notice: {e}")

    def export_overdue_notice_letter_word(self):
        """Generate the overdue notice as a formatted Microsoft Word (.docx) document.
        Provides proper headings, paragraphs, table, punishment clause, and signature block.
        Offers to also create Excel/text version afterward.
        """
        try:
            overdue = self.get_current_overdue_records()
            if not overdue:
                messagebox.showinfo("Overdue Notice", "There are currently no overdue borrowed books.")
                return
            if Document is None:
                messagebox.showerror(
                    "Dependency Missing",
                    "python-docx is not installed. Please install it (pip install python-docx) and try again."
                )
                return
            today_str = datetime.now().strftime('%Y-%m-%d')
            ref_code = f"Library/Overdue/{datetime.now().strftime('%Y%m%d')}"
            base_filename = f"overdue_notice_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".docx",
                filetypes=[("Word Document", "*.docx")],
                initialfile=base_filename + '.docx'
            )
            if not file_path:
                return

            doc = Document()
            def add_center(text, bold=True, size=16):
                p = doc.add_paragraph()
                run = p.add_run(text)
                run.bold = bold
                run.font.size = Pt(size)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER

            add_center("GOVERNMENT POLYTECHNIC AWASARI (Kh)", True, 18)
            add_center("Library of Computer Department", True, 16)
            meta_p = doc.add_paragraph()
            meta_p.add_run(f"Date: {today_str}\nRef: {ref_code}")
            subj = doc.add_paragraph()
            run_subj = subj.add_run("Subject: Submission of Overdue Library Books")
            run_subj.bold = True
            body_paras = [
                "Dear Students,",
                "The following students are hereby notified to immediately submit the listed library books that are now overdue.",
                f"A fine of Rs {FINE_PER_DAY} per day has accrued (or will continue to accrue) until the books are returned.",
                "Failure to comply today will trigger disciplinary action per departmental policy.",
                "Overdue Book List:"
            ]
            for line in body_paras:
                doc.add_paragraph(line)

            columns = ["Enrollment No", "Student Name", "Book ID", "Book Title", "Borrow Date", "Due Date", "Days Overdue", "Accrued Fine"]
            table = doc.add_table(rows=1, cols=len(columns))
            hdr = table.rows[0].cells
            for i, col in enumerate(columns):
                hdr[i].text = col
            for rec in overdue:
                row = table.add_row().cells
                row[0].text = str(rec['Enrollment No'])
                row[1].text = str(rec['Student Name'])
                row[2].text = str(rec['Book ID'])
                row[3].text = str(rec['Book Title'])
                row[4].text = str(rec['Borrow Date'])
                row[5].text = str(rec['Due Date'])
                row[6].text = str(rec['Days Overdue'])
                row[7].text = str(rec['Accrued Fine'])

            doc.add_paragraph()
            clause = doc.add_paragraph()
            clause.add_run(
                "You are directed to return the above books without further delay.\n"
                "Punishment Clause: Continued non-compliance after 3 days from this notice will result in suspension "
                "of borrowing privileges for one month and a formal report to the Academic Coordinator."
            )
            doc.add_paragraph()
            doc.add_paragraph("Regards,")
            doc.add_paragraph()
            doc.add_paragraph("__________________________")
            doc.add_paragraph("Librarian")
            doc.add_paragraph("Library of Computer Department")
            doc.add_paragraph("Government Polytechnic Awasari (Kh)")

            doc.save(file_path)
            messagebox.showinfo("Overdue Notice", f"Word overdue notice exported:\n{file_path}")
            if messagebox.askyesno("Open File", "Open the Word letter now?"):
                self.open_file(file_path)
            # Excel/text companion removed per user request
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate Word overdue notice: {e}")
    
    def import_books_from_excel(self):
        """Import books from Excel file"""
        file_path = filedialog.askopenfilename(
            title="Select Excel file to import",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            df = pd.read_excel(file_path)
            
            # Only strictly required columns now (per request): book_id and title
            required_columns = ['book_id', 'title']
            
            # Check if required columns exist (case insensitive)
            df.columns = df.columns.str.lower().str.replace(' ', '_')
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                messagebox.showerror("Error", f"Excel file must contain columns: {', '.join(required_columns)}")
                return
            
            # Import books with mandatory validation for book_id and title
            success_count = 0
            error_count = 0
            skipped_count = 0
            errors = []
            
            for index, row in df.iterrows():
                row_no = index + 2  # Account for header row in Excel display
                try:
                    raw_book_id = str(row.get('book_id', '')).strip()
                    raw_title = str(row.get('title', '')).strip()
                    if not raw_book_id or not raw_title or raw_book_id.lower() == 'nan' or raw_title.lower() == 'nan':
                        skipped_count += 1
                        continue  # Mandatory fields missing
                    # Copies parsing
                    try:
                        copies_val = int(row.get('total_copies', 1))
                        if copies_val <= 0:
                            copies_val = 1
                    except Exception:
                        copies_val = 1
                    success, message = self.db.add_book(
                        raw_book_id,
                        raw_title,
                        str(row.get('author', '')).strip(),
                        str(row.get('isbn', '')).strip(),
                        str(row.get('category', 'Technology')).strip() or 'Technology',
                        copies_val
                    )
                    if success:
                        success_count += 1
                    else:
                        error_count += 1
                        errors.append(f"Row {row_no}: {message}")
                except Exception as e:
                    error_count += 1
                    errors.append(f"Row {row_no}: {str(e)}")
            
            # Show results (include skipped)
            result_message = (
                "Import completed!\n\n"
                f"Added: {success_count}\n"
                f"Errors: {error_count}\n"
                f"Skipped (missing Book ID/Title): {skipped_count}"
            )
            if errors:
                result_message += f"\n\nFirst few errors:\n" + "\n".join(errors[:5])
                if len(errors) > 5:
                    result_message += f"\n... and {len(errors) - 5} more errors."
            messagebox.showinfo("Import Results", result_message)
            
            if success_count > 0:
                self.refresh_books()
                self.refresh_dashboard()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import Excel file: {str(e)}")
    
    def share_data_dialog(self):
        """Show data sharing dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Share Library Data")
        dialog.geometry("500x400")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 200, self.root.winfo_rooty() + 200))
        
        # Title
        title_label = tk.Label(
            dialog,
            text="📤 Share Library Data",
            font=('Segoe UI', 16, 'bold'),
            bg='white',
            fg=self.colors['accent']
        )
        title_label.pack(pady=(20, 30))
        
        # Instructions
        info_label = tk.Label(
            dialog,
            text="Export data to Excel and share via email, WhatsApp, or other platforms:",
            font=('Segoe UI', 11),
            bg='white',
            fg=self.colors['accent'],
            wraplength=400
        )
        info_label.pack(pady=(0, 20))
        
        # Buttons frame
        buttons_frame = tk.Frame(dialog, bg='white')
        buttons_frame.pack(expand=True)
        
        # Data type buttons
        data_types = [
            ("📊 Dashboard Summary", self.export_dashboard_summary),
            ("👥 Students Data", self.export_students_dialog),
            ("📚 Books Data", self.export_books_to_excel),
            ("📋 Transaction Records", self.export_records_to_excel)
        ]
        
        for text, command in data_types:
            btn = tk.Button(
                buttons_frame,
                text=text,
                font=('Segoe UI', 12, 'bold'),
                bg=self.colors['secondary'],
                fg='white',
                relief='flat',
                padx=20,
                pady=15,
                command=lambda cmd=command: [cmd(), dialog.destroy()],
                cursor='hand2',
                width=25
            )
            btn.pack(pady=10)
        
        # Close button
        close_btn = tk.Button(
            dialog,
            text="❌ Close",
            font=('Segoe UI', 12, 'bold'),
            bg='#6c757d',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            command=dialog.destroy,
            cursor='hand2'
        )
        close_btn.pack(pady=20)
    
    def export_dashboard_summary(self):
        """Export dashboard summary to Excel"""
        try:
            # Get statistics
            stats = self.get_library_statistics()
            
            # Get recent activities
            activities = self.get_recent_activities()
            
            # Create summary data
            summary_data = {
                'Library Statistics': [
                    ['Metric', 'Value'],
                    ['Total Books', stats['total_books']],
                    ['Available Books', stats['available_books']],
                    ['Borrowed Books', stats['borrowed_books']],
                    ['Total Students', stats['total_students']],
                    ['Generated On', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
                ]
            }
            
            # Save to file
            filename = f"dashboard_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                # Correct parameter name
                initialfile=filename
            )
            
            if file_path:
                with pd.ExcelWriter(file_path) as writer:
                    # Write statistics
                    stats_df = pd.DataFrame(summary_data['Library Statistics'][1:], 
                                          columns=summary_data['Library Statistics'][0])
                    stats_df.to_excel(writer, sheet_name='Statistics', index=False)
                    
                    # Write recent activities
                    if activities:
                        activities_df = pd.DataFrame(activities, columns=[
                            'Type', 'Student', 'Book', 'Date', 'Status'
                        ])
                        activities_df.to_excel(writer, sheet_name='Recent Activities', index=False)
                
                messagebox.showinfo("Success", f"Dashboard summary exported to {file_path}")
                
                # Ask if user wants to open the file
                if messagebox.askyesno("Open File", "Do you want to open the exported file?"):
                    self.open_file(file_path)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export dashboard summary: {str(e)}")
    
    def open_file(self, file_path):
        """Open file with default application"""
        try:
            if platform.system() == 'Windows':
                os.startfile(file_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', file_path])
            else:  # Linux
                subprocess.run(['xdg-open', file_path])
        except Exception as e:
            print(f"Failed to open file: {e}")

# Main application entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()