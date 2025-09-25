#!/usr/bin/env python3
"""
Library of Computer Department Management System
Version 3.0.0 - Complete redesign with light, professional UI
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

# Add the current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database import Database

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Library of Computer Department v3.0.0")
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
        
        # Configure styles
        self.setup_styles()
        
        # Search variables
        self.student_search_var = tk.StringVar()
        self.book_search_var = tk.StringVar()
        self.record_search_var = tk.StringVar()
        
        # Filter variables
        self.book_category_filter = tk.StringVar(value="All")
        self.record_type_filter = tk.StringVar(value="All")
        self.student_year_filter = tk.StringVar(value="All")
        
        # Trace search variables
        self.student_search_var.trace('w', lambda *args: self.search_students())
        self.book_search_var.trace('w', lambda *args: self.search_books())
        self.record_search_var.trace('w', lambda *args: self.search_records())
        
        # Create login interface
        self.create_login_interface()
    
    def setup_styles(self):
        """Setup ttk styles for consistent theming"""
        style = ttk.Style()
        
        # Configure ttk styles
        style.theme_use('clam')
        
        # Notebook (tab) style
        style.configure('TNotebook', 
                       background=self.colors['primary'],
                       borderwidth=0)
        style.configure('TNotebook.Tab', 
                       background=self.colors['primary'],
                       foreground=self.colors['accent'],
                       padding=[20, 10],
                       font=('Segoe UI', 11, 'bold'))
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['secondary']),
                            ('active', '#5ba0f2')],
                 foreground=[('selected', 'white'),
                            ('active', 'white')])
        
        # Treeview style
        style.configure('Treeview',
                       background=self.colors['primary'],
                       foreground=self.colors['accent'],
                       fieldbackground=self.colors['primary'],
                       font=('Segoe UI', 10))
        style.configure('Treeview.Heading',
                       background=self.colors['secondary'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'))
        
        # Button style
        style.configure('Action.TButton',
                       background=self.colors['secondary'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(15, 8))
        style.map('Action.TButton',
                 background=[('active', '#5ba0f2')])
        
        # Entry style
        style.configure('TEntry',
                       fieldbackground=self.colors['primary'],
                       borderwidth=2,
                       relief='solid',
                       bordercolor=self.colors['secondary'])
        
        # Combobox style
        style.configure('TCombobox',
                       fieldbackground=self.colors['primary'],
                       borderwidth=2,
                       relief='solid',
                       bordercolor=self.colors['secondary'])
    
    def create_login_interface(self):
        """Create modern login interface matching the provided image"""
        # Clear root
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container with dark blue background like in image
        main_container = tk.Frame(self.root, bg='#2b3e56')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Center frame
        center_frame = tk.Frame(main_container, bg='#2b3e56')
        center_frame.pack(expand=True, fill=tk.BOTH)
        
        # Login card exactly like in the image
        login_card = tk.Frame(center_frame, bg='#3a5373', relief=tk.FLAT, bd=0)
        login_card.place(relx=0.5, rely=0.5, anchor='center', width=400, height=350)
        
        # Title section
        title_frame = tk.Frame(login_card, bg='#3a5373')
        title_frame.pack(pady=(30, 10))
        
        # Lock icon with "Admin Login" text exactly like in image
        tk.Label(
            title_frame, 
            text="🔐 Admin Login", 
            font=("Segoe UI", 20, "bold"), 
            bg="#3a5373", 
            fg="#00bcd4"  # Cyan color like in image
        ).pack()
        
        # Subtitle exactly like in image
        tk.Label(
            title_frame, 
            text="Library Management System", 
            font=("Segoe UI", 11), 
            bg="#3a5373", 
            fg="#8fa5b8"  # Light gray like in image
        ).pack(pady=(5, 0))
        
        # Form fields
        form = tk.Frame(login_card, bg="#3a5373")
        form.pack(pady=20, padx=40)
        
        # Username label and field exactly like in image
        tk.Label(
            form, 
            text="Username", 
            font=("Segoe UI", 10, "bold"), 
            bg="#3a5373", 
            fg="#ffffff"
        ).pack(anchor='w', pady=(0, 5))
        
        username_entry = tk.Entry(
            form, 
            font=("Segoe UI", 11), 
            width=30,
            bg="#2b3e56",  # Dark background like in image
            fg="#ffffff",
            insertbackground="#00bcd4",
            bd=1,
            relief=tk.SOLID
        )
        username_entry.pack(pady=(0, 15), ipady=8)
        username_entry.insert(0, "gpa")  # Default username like in image
        
        # Password label and field exactly like in image
        tk.Label(
            form, 
            text="Password", 
            font=("Segoe UI", 10, "bold"), 
            bg="#3a5373", 
            fg="#ffffff"
        ).pack(anchor='w', pady=(0, 5))
        
        password_entry = tk.Entry(
            form, 
            font=("Segoe UI", 11), 
            show="*", 
            width=30,
            bg="#2b3e56",  # Dark background like in image
            fg="#ffffff",
            insertbackground="#00bcd4",
            bd=1,
            relief=tk.SOLID
        )
        password_entry.pack(pady=(0, 20), ipady=8)
        password_entry.insert(0, "gpa123")  # Default password

        # Login function with correct credentials
        def login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            if username == "gpa" and password == "gpa123":
                self.create_main_interface()
            else:
                messagebox.showerror("Login Error", "Invalid username or password!")

        # Login button exactly like in image - cyan, full width
        login_btn = tk.Button(
            form, 
            text="� Login", 
            font=("Segoe UI", 12, "bold"), 
            bg="#00bcd4",  # Cyan like in image
            fg="#ffffff", 
            bd=0,
            relief=tk.FLAT,
            cursor='hand2',
            activebackground="#00acc1",
            activeforeground="#ffffff",
            command=login
        )
        login_btn.pack(fill=tk.X, pady=(10, 0), ipady=12)  # Full width like in image
        
        # Enter key binding
        def handle_enter(event):
            login()
        self.root.bind('<Return>', handle_enter)
        username_entry.bind('<Return>', handle_enter)
        password_entry.bind('<Return>', handle_enter)
        
        # Set focus
        username_entry.focus()
        username_entry.select_range(0, tk.END)
    
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
            text="👤 Administrator",
            font=('Segoe UI', 13, 'bold'),
            bg=self.colors['secondary'],
            fg='white'
        )
        user_label.pack(pady=(25, 15))

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
    def show_developer_info(self):
        """Show developer information dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Developer Information")
        dialog.geometry("400x350")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.grab_set()

        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 300, self.root.winfo_rooty() + 200))

        title_label = tk.Label(
            dialog,
            text="👨‍💻 Developer Information",
            font=('Segoe UI', 16, 'bold'),
            bg='white',
            fg=self.colors['accent']
        )
        title_label.pack(pady=(20, 10))

        info_text = (
            "🎓 Student Developer Information\n\n"
            "Name: Yash\n"
            "Enrollment: [Your Enrollment Number]\n"
            "Branch: Computer Engineering\n"
            "Year: 2nd Year\n\n"
            "📱 Application Details:\n"
            "App: Library of Computer Department v3.1\n"
            "Type: Student Management System\n"
            "Framework: Python + Tkinter\n\n"
            "✨ Special thanks to Computer Department faculty\n"
            "for guidance and support in this project."
        )
        info_label = tk.Label(
            dialog,
            text=info_text,
            font=('Segoe UI', 12),
            bg='white',
            fg=self.colors['accent'],
            justify='left'
        )
        info_label.pack(pady=(0, 20), padx=20)

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
        close_btn.pack(pady=10)
    
    def create_dashboard_tab(self):
        """Create dashboard tab with statistics"""
        dashboard_frame = tk.Frame(self.notebook, bg=self.colors['primary'])
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        # Statistics cards container
        stats_container = tk.Frame(dashboard_frame, bg=self.colors['primary'])
        stats_container.pack(fill=tk.X, padx=20, pady=20)
        
        # Statistics cards
        self.create_stats_cards(stats_container)
        
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
    
    def create_transactions_tab(self):
        """Create transactions tab with improved layout"""
        transactions_frame = tk.Frame(self.notebook, bg=self.colors['primary'])
        self.notebook.add(transactions_frame, text="📋 Transactions")
        
        # Main container with proper spacing
        main_container = tk.Frame(transactions_frame, bg=self.colors['primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Borrow Book Section
        borrow_frame = tk.LabelFrame(
            main_container,
            text="📖 Borrow Book",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent'],
            padx=15,
            pady=15
        )
        borrow_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Borrow form
        borrow_form = tk.Frame(borrow_frame, bg=self.colors['primary'])
        borrow_form.pack(fill=tk.X)
        
        # Row 1
        row1 = tk.Frame(borrow_form, bg=self.colors['primary'])
        row1.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(row1, text="Student Enrollment No:", font=('Segoe UI', 11, 'bold'), 
                bg=self.colors['primary'], fg=self.colors['accent']).pack(side=tk.LEFT)
        # Autocomplete Combobox for student enrollment
        try:
            students = self.db.get_students()
            student_list = [str(s[0]) for s in students]  # Use enrollment numbers (first column)
        except:
            student_list = []
        
        self.borrow_enrollment_combo = ttk.Combobox(row1, font=('Segoe UI', 11), width=20, values=student_list)
        self.borrow_enrollment_combo.pack(side=tk.LEFT, padx=(10, 30))
        self.borrow_enrollment_combo.bind('<<ComboboxSelected>>', lambda e: self.show_student_details('borrow'))
        # Enable autocomplete behavior
        self.borrow_enrollment_combo.bind('<KeyRelease>', lambda e: self.filter_student_suggestions(e, 'borrow'))

        # Student details label
        self.borrow_student_details = tk.Label(row1, text="", font=('Segoe UI', 10), bg=self.colors['primary'], fg=self.colors['accent'])
        self.borrow_student_details.pack(side=tk.LEFT, padx=(0, 30))
        
        tk.Label(row1, text="Book ID:", font=('Segoe UI', 11, 'bold'), 
                bg=self.colors['primary'], fg=self.colors['accent']).pack(side=tk.LEFT)
        
        # Autocomplete Combobox for book ID
        try:
            books = self.db.get_books()
            book_list = [str(b[0]) for b in books]  # Use book IDs (first column)
        except:
            book_list = []
        
        self.borrow_book_id_combo = ttk.Combobox(row1, font=('Segoe UI', 11), width=20, values=book_list)
        self.borrow_book_id_combo.pack(side=tk.LEFT, padx=(10, 30))
        self.borrow_book_id_combo.bind('<KeyRelease>', lambda e: self.filter_book_suggestions(e, 'borrow'))
        
        # Row 2
        row2 = tk.Frame(borrow_form, bg=self.colors['primary'])
        row2.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(row2, text="Due Date:", font=('Segoe UI', 11, 'bold'), 
                bg=self.colors['primary'], fg=self.colors['accent']).pack(side=tk.LEFT)
        
        # Date frame
        date_frame = tk.Frame(row2, bg=self.colors['primary'])
        date_frame.pack(side=tk.LEFT, padx=(10, 30))
        
        self.borrow_due_date_entry = tk.Entry(date_frame, font=('Segoe UI', 11), width=15, relief='solid', bd=2)
        self.borrow_due_date_entry.pack(side=tk.LEFT)
        
        # Calendar button
        calendar_btn = tk.Button(
            date_frame,
            text="📅",
            font=('Segoe UI', 11),
            bg=self.colors['secondary'],
            fg='white',
            relief='flat',
            padx=8,
            pady=5,
            command=lambda: self.show_date_picker(self.borrow_due_date_entry),
            cursor='hand2'
        )
        calendar_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Set default due date (2 weeks from today)
        from datetime import datetime, timedelta
        default_due = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        self.borrow_due_date_entry.insert(0, default_due)
        
        # Borrow button
        borrow_btn = tk.Button(
            row2,
            text="📖 Borrow Book",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['secondary'],
            fg='white',
            relief='flat',
            padx=25,
            pady=10,
            command=self.borrow_book,
            cursor='hand2'
        )
        borrow_btn.pack(side=tk.LEFT, padx=(20, 0))
        
        # Separator
        separator = tk.Frame(main_container, height=2, bg=self.colors['accent'])
        separator.pack(fill=tk.X, pady=20)
        
        # Return Book Section
        return_frame = tk.LabelFrame(
            main_container,
            text="📚 Return Book",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent'],
            padx=15,
            pady=15
        )
        return_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Return form
        return_row = tk.Frame(return_frame, bg=self.colors['primary'])
        return_row.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(return_row, text="Student Enrollment No:", font=('Segoe UI', 11, 'bold'), 
                bg=self.colors['primary'], fg=self.colors['accent']).pack(side=tk.LEFT)
        
        try:
            students = self.db.get_students()
            student_list = [str(s[0]) for s in students]  # Use enrollment numbers (first column)
        except:
            student_list = []
        
        self.return_enrollment_combo = ttk.Combobox(return_row, font=('Segoe UI', 11), width=20, values=student_list)
        self.return_enrollment_combo.pack(side=tk.LEFT, padx=(10, 30))
        self.return_enrollment_combo.bind('<<ComboboxSelected>>', lambda e: self.show_student_details('return'))
        # Enable autocomplete behavior
        self.return_enrollment_combo.bind('<KeyRelease>', lambda e: self.filter_student_suggestions(e, 'return'))
        
        # Student details label for return
        self.return_student_details = tk.Label(return_row, text="", font=('Segoe UI', 10), bg=self.colors['primary'], fg=self.colors['accent'])
        self.return_student_details.pack(side=tk.LEFT, padx=(0, 30))
        
        tk.Label(return_row, text="Book ID:", font=('Segoe UI', 11, 'bold'), 
                bg=self.colors['primary'], fg=self.colors['accent']).pack(side=tk.LEFT)
        
        # Autocomplete Combobox for book ID in return
        try:
            books = self.db.get_books()
            book_list = [str(b[0]) for b in books]  # Use book IDs (first column)
        except:
            book_list = []
        
        self.return_book_id_combo = ttk.Combobox(return_row, font=('Segoe UI', 11), width=20, values=book_list)
        self.return_book_id_combo.pack(side=tk.LEFT, padx=(10, 20))
        self.return_book_id_combo.bind('<KeyRelease>', lambda e: self.filter_book_suggestions(e, 'return'))
        
        # Return button
        return_btn = tk.Button(
            return_row,
            text="📚 Return Book",
            font=('Segoe UI', 12, 'bold'),
            bg='#28a745',
            fg='white',
            relief='flat',
            padx=25,
            pady=10,
            command=self.return_book,
            cursor='hand2'
        )
        return_btn.pack(side=tk.LEFT, padx=(20, 0))
        
        # Borrowed Books Section
        borrowed_frame = tk.LabelFrame(
            main_container,
            text="📋 Currently Borrowed Books",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent'],
            padx=10,
            pady=10
        )
        borrowed_frame.pack(fill=tk.BOTH, expand=True)
        
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
    
    def filter_student_suggestions(self, event, mode):
        """Filter student suggestions as user types"""
        try:
            current_text = event.widget.get().lower().strip()
            if len(current_text) < 1:  # Start filtering after 1 character
                return
            
            # Get all students
            students = self.db.get_students()
            # Filter students that match the current text (enrollment number or name)
            matching_students = []
            for s in students:
                enrollment = str(s[0]).lower()
                name = str(s[1]).lower()
                if current_text in enrollment or current_text in name:
                    matching_students.append(f"{s[0]} - {s[1]}")  # Format as "enrollment - name"
            
            # Update combobox values
            event.widget['values'] = matching_students[:10]  # Limit to 10 suggestions
            
            # Auto-open dropdown if there are matches
            if matching_students and len(current_text) >= 1:
                event.widget.event_generate('<Down>')
                
        except Exception as e:
            print(f"Error filtering student suggestions: {e}")
    
    def filter_book_suggestions(self, event, mode):
        """Filter book suggestions as user types"""
        try:
            current_text = event.widget.get().lower().strip()
            if len(current_text) < 1:  # Start filtering after 1 character
                return
            
            # Get all books
            books = self.db.get_books()
            # Filter books that match the current text (book ID or title)
            matching_books = []
            for b in books:
                book_id = str(b[0]).lower()
                title = str(b[1]).lower()
                if current_text in book_id or current_text in title:
                    matching_books.append(f"{b[0]} - {b[1]}")  # Format as "ID - title"
            
            # Update combobox values
            event.widget['values'] = matching_books[:10]  # Limit to 10 suggestions
            
            # Auto-open dropdown if there are matches
            if matching_books and len(current_text) >= 1:
                event.widget.event_generate('<Down>')
                
        except Exception as e:
            print(f"Error filtering book suggestions: {e}")
    
    def show_student_details(self, mode):
        """Show student details below enrollment field in transactions tab"""
        if mode == 'borrow':
            enrollment_no = self.borrow_enrollment_combo.get()
        else:
            enrollment_no = self.return_enrollment_combo.get()
        
        try:
            students = self.db.get_students()
            student = next((s for s in students if str(s[0]) == enrollment_no), None)
            if student:
                details = f"Name: {student[1]} | Email: {student[2]} | Phone: {student[3]} | Year: {student[4]}"
            else:
                details = "Student not found."
        except Exception as e:
            details = "Error loading student data."
            
        if mode == 'borrow':
            self.borrow_student_details.config(text=details)
        else:
            self.return_student_details.config(text=details)
        
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
        self.record_from_date = tk.Entry(row2, font=('Segoe UI', 10), width=12)
        self.record_from_date.pack(side=tk.LEFT, padx=(5, 15))
        
        tk.Label(row2, text="To Date:", bg=self.colors['primary'], fg=self.colors['accent'], font=('Segoe UI', 10)).pack(side=tk.LEFT)
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
        record_columns = ('Enrollment No', 'Student Name', 'Book ID', 'Book Title', 'Borrow Date', 'Due Date', 'Return Date', 'Status')
        self.records_tree = ttk.Treeview(records_list_frame, columns=record_columns, show='headings', height=15)
        record_widths = {'Enrollment No': 120, 'Student Name': 150, 'Book ID': 100, 'Book Title': 200, 'Borrow Date': 100, 'Due Date': 100, 'Return Date': 100, 'Status': 80}
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
        enrollment_text = self.borrow_enrollment_combo.get().strip()
        book_text = self.borrow_book_id_combo.get().strip()
        due_date = self.borrow_due_date_entry.get().strip()
        
        if not all([enrollment_text, book_text, due_date]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        # Extract enrollment number (before " - " if formatted, otherwise use as is)
        enrollment_no = enrollment_text.split(' - ')[0] if ' - ' in enrollment_text else enrollment_text
        
        # Extract book ID (before " - " if formatted, otherwise use as is)
        book_id = book_text.split(' - ')[0] if ' - ' in book_text else book_text
        
        # Validate date format
        try:
            from datetime import datetime, timedelta
            datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Invalid date format! Please use YYYY-MM-DD")
            return
        
        success, message = self.db.borrow_book(enrollment_no, book_id, due_date)
        
        if success:
            messagebox.showinfo("Success", message)
            # Clear fields
            self.borrow_enrollment_combo.set('')
            self.borrow_book_id_combo.set('')
            # Reset due date to default (2 weeks from today)
            self.borrow_due_date_entry.delete(0, tk.END)
            default_due = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
            self.borrow_due_date_entry.insert(0, default_due)
            
            # Clear student details
            self.borrow_student_details.config(text="")
            
            # Refresh views
            self.refresh_borrowed()
            self.refresh_books()
            self.refresh_dashboard()
            self.refresh_records()
        else:
            messagebox.showerror("Error", message)
    
    def return_book(self):
        """Handle book return"""
        enrollment_text = self.return_enrollment_combo.get().strip()
        book_text = self.return_book_id_combo.get().strip()
        
        if not all([enrollment_text, book_text]):
            messagebox.showerror("Error", "Both Enrollment No and Book ID are required!")
            return
        
        # Extract enrollment number (before " - " if formatted, otherwise use as is)
        enrollment_no = enrollment_text.split(' - ')[0] if ' - ' in enrollment_text else enrollment_text
        
        # Extract book ID (before " - " if formatted, otherwise use as is)
        book_id = book_text.split(' - ')[0] if ' - ' in book_text else book_text
        
        success, message = self.db.return_book(enrollment_no, book_id)
        
        if success:
            messagebox.showinfo("Success", message)
            # Clear fields
            self.return_enrollment_combo.set('')
            self.return_book_id_combo.set('')
            
            # Clear student details
            self.return_student_details.config(text="")
            
            # Refresh views
            self.refresh_borrowed()
            self.refresh_books()
            self.refresh_dashboard()
            self.refresh_records()
        else:
            messagebox.showerror("Error", message)
    
    def import_students_from_excel(self):
        """Import students from Excel file, keep only one student in DB"""
        file_path = filedialog.askopenfilename(
            title="Select Excel file to import",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if not file_path:
            return
        try:
            df = pd.read_excel(file_path)
            # Only keep first row
            if df.empty:
                messagebox.showerror("Error", "Excel file is empty.")
                return
            df.columns = df.columns.str.lower().str.replace(' ', '_')
            required_columns = ['enrollment_no', 'name', 'year']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                messagebox.showerror("Error", f"Missing required columns: {', '.join(missing_columns)}")
                return
            # Remove all students first
            for student in self.db.get_students():
                self.db.remove_student(student[1])
            # Add only the first student
            row = df.iloc[0]
            success, message = self.db.add_student(
                str(row['enrollment_no']),
                str(row['name']),
                str(row.get('email', '')),
                str(row.get('phone', '')),
                str(row.get('department', 'Computer')),
                str(row.get('year', ''))
            )
            if success:
                messagebox.showinfo("Import Result", "Student imported and replaced successfully.")
            else:
                messagebox.showerror("Import Error", message)
            self.refresh_students()
            self.refresh_dashboard()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import Excel file: {str(e)}")
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
            # Apply type filter
            if type_filter != "All":
                if type_filter == "Overdue" and record[7] == "0":  # Days overdue
                    continue
                elif type_filter != "Overdue" and record[6] != type_filter.lower():  # Status
                    continue
            
            # Apply search filter
            if search_term:
                if not any(search_term in str(field).lower() for field in record):
                    continue
            
            # Apply date filters
            if from_date:
                try:
                    record_date = datetime.strptime(record[3], '%Y-%m-%d')
                    from_date_obj = datetime.strptime(from_date, '%Y-%m-%d')
                    if record_date < from_date_obj:
                        continue
                except ValueError:
                    pass
            
            if to_date:
                try:
                    record_date = datetime.strptime(record[3], '%Y-%m-%d')
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
        if hasattr(self, 'activities_tree'):
            # Refresh recent activities
            activities = self.get_recent_activities()
            self.populate_activities_tree(activities)
    
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
        """Populate borrowed books treeview with enhanced data"""
        if hasattr(self, 'borrowed_tree'):
            for item in self.borrowed_tree.get_children():
                self.borrowed_tree.delete(item)
            
            for record in borrowed:
                # Calculate days left
                try:
                    due_date = datetime.strptime(record[4], '%Y-%m-%d')
                    today = datetime.now()
                    days_left = (due_date - today).days
                    if days_left < 0:
                        days_left_str = f"{abs(days_left)} overdue"
                    else:
                        days_left_str = str(days_left)
                except:
                    days_left_str = "N/A"
                
                # Get student name and book title
                student_name = self.get_student_name(record[1])
                book_title = self.get_book_title(record[2])
                
                display_data = (student_name, record[2], book_title, record[3], record[4], days_left_str)
                self.borrowed_tree.insert('', 'end', values=display_data)
    
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
                self.records_tree.insert('', 'end', values=record)
    
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
            
            cursor.execute("""
                SELECT 
                    br.id,
                    s.name as student_name,
                    b.title as book_title,
                    br.borrow_date,
                    br.due_date,
                    br.return_date,
                    br.status,
                    CASE 
                        WHEN br.status = 'borrowed' AND date('now') > br.due_date 
                        THEN julianday('now') - julianday(br.due_date)
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
            for record in records:
                formatted_record = list(record)
                # Format return date
                if not formatted_record[5]:
                    formatted_record[5] = "Not returned"
                # Format days overdue
                if formatted_record[7] > 0:
                    formatted_record[7] = f"{int(formatted_record[7])}"
                else:
                    formatted_record[7] = "0"
                
                formatted_records.append(tuple(formatted_record))
            
            return formatted_records
        except Exception as e:
            print(f"Error getting records: {e}")
            return []
    
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
                initialname=filename
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
                initialname=filename
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
            records = self.get_all_records()
            
            if not records:
                messagebox.showwarning("Warning", "No records found to export!")
                return
            
            # Create DataFrame
            df = pd.DataFrame(records, columns=[
                'Record ID', 'Student Name', 'Book Title', 'Borrow Date', 
                'Due Date', 'Return Date', 'Status', 'Days Overdue'
            ])
            
            # Save to file
            filename = f"records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                initialname=filename
            )
            
            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Success", f"Records data exported to {file_path}")
                
                # Ask if user wants to open the file
                if messagebox.askyesno("Open File", "Do you want to open the exported file?"):
                    self.open_file(file_path)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export records: {str(e)}")
    
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
            
            # Expected columns
            required_columns = ['book_id', 'title', 'author', 'isbn', 'category', 'total_copies']
            
            # Check if required columns exist (case insensitive)
            df.columns = df.columns.str.lower().str.replace(' ', '_')
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                messagebox.showerror("Error", f"Missing required columns: {', '.join(missing_columns)}")
                return
            
            # Import books
            success_count = 0
            error_count = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    success, message = self.db.add_book(
                        str(row['book_id']),
                        str(row['title']),
                        str(row['author']),
                        str(row.get('isbn', '')),
                        str(row.get('category', 'Technology')),
                        int(row.get('total_copies', 1))
                    )
                    
                    if success:
                        success_count += 1
                    else:
                        error_count += 1
                        errors.append(f"Row {index + 2}: {message}")
                        
                except Exception as e:
                    error_count += 1
                    errors.append(f"Row {index + 2}: {str(e)}")
            
            # Show results
            result_message = f"Import completed!\n\nSuccessful: {success_count}\nErrors: {error_count}"
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
                initialname=filename
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