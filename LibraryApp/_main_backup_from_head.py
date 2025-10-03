
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
from database import Database
import pandas as pd

class LibraryManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("≡ƒôÜ Library Management System v2.4.0")
        self.root.geometry("1400x800")
        self.root.configure(bg='#1a1a2e')  # Modern dark background

        # Show admin login first
        self.show_login()

    def show_login(self):
        # Modern login with gradient background
        self.login_frame = tk.Frame(self.root, bg='#1a1a2e')
        self.login_frame.pack(expand=True, fill=tk.BOTH)
        
        # Create central login card with modern styling
        login_card = tk.Frame(self.login_frame, bg='#16213e', relief=tk.FLAT, bd=0)
        login_card.place(relx=0.5, rely=0.5, anchor='center', width=450, height=420)
        
        # Modern title with gradient effect
        title_frame = tk.Frame(login_card, bg='#16213e')
        title_frame.pack(pady=(30, 20))
        
        tk.Label(
            title_frame, 
            text="≡ƒöÉ Admin Login", 
            font=("Segoe UI", 24, "bold"), 
            bg="#16213e", 
            fg="#00d4ff"
        ).pack()
        
        tk.Label(
            title_frame, 
            text="Library Management System", 
            font=("Segoe UI", 12), 
            bg="#16213e", 
            fg="#8892b0"
        ).pack(pady=(5, 0))
        
        # Modern form with sleek inputs
        form = tk.Frame(login_card, bg="#16213e")
        form.pack(pady=20, padx=40)
        
        # Username field
        tk.Label(
            form, 
            text="Username", 
            font=("Segoe UI", 11, "bold"), 
            bg="#16213e", 
            fg="#ccd6f6"
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        username_entry = tk.Entry(
            form, 
            font=("Segoe UI", 12), 
            width=25,
            bg="#0f1419",
            fg="#ccd6f6",
            insertbackground="#00d4ff",
            bd=0,
            relief=tk.FLAT
        )
        username_entry.grid(row=1, column=0, pady=(0, 15), ipady=8)
        
        # Password field
        tk.Label(
            form, 
            text="Password", 
            font=("Segoe UI", 11, "bold"), 
            bg="#16213e", 
            fg="#ccd6f6"
        ).grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        password_entry = tk.Entry(
            form, 
            font=("Segoe UI", 12), 
            show="*", 
            width=25,
            bg="#0f1419",
            fg="#ccd6f6",
            insertbackground="#00d4ff",
            bd=0,
            relief=tk.FLAT
        )
        password_entry.grid(row=3, column=0, pady=(0, 25), ipady=8)

        def do_login():
            if username_entry.get() == "gpa" and password_entry.get() == "gpa123":
                self.login_frame.destroy()
                self.load_main_app()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")

        # Modern login button with gradient effect
        login_btn = tk.Button(
            form, 
            text="≡ƒÜÇ Login", 
            font=("Segoe UI", 12, "bold"), 
            bg="#00d4ff", 
            fg="#0f1419", 
            width=20,
            bd=0,
            relief=tk.FLAT,
            cursor='hand2',
            activebackground="#0099cc",
            activeforeground="#ffffff",
            command=do_login
        )
        login_btn.grid(row=4, column=0, pady=20, ipady=8)

    def load_main_app(self):
        # Initialize database
        self.db = Database()
        # Create main frame with modern dark theme
        self.main_frame = tk.Frame(self.root, bg='#1a1a2e')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        # Create enhanced header with logo
        self.create_enhanced_header()
        # Create navigation bar
        self.create_navigation_bar()
        # Create content area
        self.create_content_area()
        # Load initial data
        self.refresh_all_data()
    
    def create_enhanced_header(self):
        """Create modern enhanced application header with gradient styling"""
        header_frame = tk.Frame(
            self.main_frame, 
            bg='#16213e', 
            height=100, 
            relief=tk.FLAT, 
            bd=0
        )
        header_frame.pack(fill=tk.X, pady=(0, 15))
        header_frame.pack_propagate(False)
        
        # Logo and title container with modern styling
        logo_title_frame = tk.Frame(header_frame, bg='#16213e')
        logo_title_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        
        # Modern logo with sleek design
        logo_frame = tk.Frame(logo_title_frame, bg='#00d4ff', width=80, height=80)
        logo_frame.pack(side=tk.LEFT, padx=(0, 20))
        logo_frame.pack_propagate(False)
        
        # Sleek logo
        logo_label = tk.Label(
            logo_frame,
            text="∩┐╜",
            font=('Segoe UI', 32, 'bold'),
            fg='#0f1419',
            bg='#00d4ff',
            justify=tk.CENTER
        )
        logo_label.pack(expand=True)
        
        # Modern title and subtitle
        title_frame = tk.Frame(logo_title_frame, bg='#16213e')
        title_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        title_label = tk.Label(
            title_frame, 
            text="Library Management System", 
            font=('Segoe UI', 26, 'bold'),
            fg='#ccd6f6', 
            bg='#16213e'
        )
        title_label.pack(anchor='w', pady=(20, 5))
        
        subtitle_label = tk.Label(
            title_frame, 
            text="Advanced Student & Book Management Solution", 
            font=('Segoe UI', 11),
            fg='#8892b0', 
            bg='#16213e'
        )
        subtitle_label.pack(anchor='w')
        
        # Modern developer info with sleek styling
        dev_info_frame = tk.Frame(logo_title_frame, bg='#16213e')
        dev_info_frame.pack(side=tk.RIGHT, padx=20)
        
        # Modern developer button
        dev_btn = tk.Button(
            dev_info_frame,
            text="≡ƒæ¿ΓÇì≡ƒÆ╗ Developer",
            font=('Segoe UI', 10, 'bold'),
            bg='#64ffda',
            fg='#0f1419',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2',
            relief=tk.FLAT,
            activebackground='#4fd3b8',
            activeforeground='#0f1419',
            command=self.show_dev_info
        )
        dev_btn.pack()
    
    def show_dev_info(self):
        """Show developer information"""
        messagebox.showinfo(
            "Developer Information",
            "≡ƒæ¿ΓÇì≡ƒÆ╗ Developer: Yash Vijay Date\n"
            "≡ƒåö Enrollment No: 24210270230\n"
            "≡ƒÄô Branch: Computer Department\n"
            "≡ƒôÜ Year: 2nd Year\n\n"
            "≡ƒÆ╛ Database: SQLite (Persistent Storage)\n"
            "≡ƒöº Built with: Python & Tkinter\n"
            "≡ƒôà Version: v2.4.0"
        )
    
    def create_navigation_bar(self):
        """Create modern navigation bar with sleek styling"""
        nav_frame = tk.Frame(
            self.main_frame, 
            bg='#16213e', 
            height=60, 
            relief=tk.FLAT, 
            bd=0
        )
        nav_frame.pack(fill=tk.X, pady=(0, 15))
        nav_frame.pack_propagate(False)
        
        # Modern navigation buttons with vibrant colors
        nav_buttons = [
            ("≡ƒÅá Dashboard", self.show_dashboard, '#ff6b6b'),
            ("≡ƒæÑ Students", self.show_students, '#4ecdc4'),
            ("≡ƒôÜ Books", self.show_books, '#45b7d1'),
            ("≡ƒôï Transactions", self.show_transactions, '#f9ca24')
        ]
        
        button_container = tk.Frame(nav_frame, bg='#16213e')
        button_container.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        
        for text, command, color in nav_buttons:
            btn = tk.Button(
                button_container,
                text=text,
                command=command,
                bg=color,
                fg='#0f1419',
                font=('Segoe UI', 12, 'bold'),
                bd=0,
                padx=25,
                pady=12,
                cursor='hand2',
                relief=tk.FLAT,
                activebackground='#ffffff',
                activeforeground='#0f1419'
            )
            btn.pack(side=tk.LEFT, padx=8)
    
    def create_content_area(self):
        """Create main content area with modern styling"""
        self.content_frame = tk.Frame(self.main_frame, bg='#1a1a2e')
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Start with dashboard
        self.current_view = None
        self.show_dashboard()
    
    def clear_content(self):
        """Clear current content"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Show dashboard view"""
        if self.current_view == 'dashboard':
            return
        self.current_view = 'dashboard'
        self.clear_content()
        self.create_dashboard_view()
    
    def show_students(self):
        """Show students view"""
        if self.current_view == 'students':
            return
        self.current_view = 'students'
        self.clear_content()
        self.create_students_view()
        # Add modern history button
        history_btn = tk.Button(
            self.content_frame, 
            text="≡ƒôè Show Student History", 
            bg='#ff6b6b', 
            fg='#ffffff', 
            font=('Segoe UI', 11, 'bold'),
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2',
            relief=tk.FLAT,
            command=self.show_student_history
        )
        history_btn.pack(anchor='ne', padx=20, pady=10)
    
    def show_books(self):
        """Show books view"""
        if self.current_view == 'books':
            return
        self.current_view = 'books'
        self.clear_content()
        self.create_books_view()
        # Add modern history button
        history_btn = tk.Button(
            self.content_frame, 
            text="≡ƒôè Show Book History", 
            bg='#ff6b6b', 
            fg='#ffffff', 
            font=('Segoe UI', 11, 'bold'),
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2',
            relief=tk.FLAT,
            command=self.show_book_history
        )
        history_btn.pack(anchor='ne', padx=20, pady=10)
    
    def show_book_history(self):
        # Show all borrow/return history for books with modern styling
        history_win = tk.Toplevel(self.root)
        history_win.title("≡ƒôÜ Book Borrow/Return History")
        history_win.geometry("1000x650")
        history_win.configure(bg='#1a1a2e')
        
        # Modern title
        title_label = tk.Label(
            history_win,
            text="≡ƒôÜ Book Transaction History",
            font=('Segoe UI', 18, 'bold'),
            bg='#1a1a2e',
            fg='#ccd6f6'
        )
        title_label.pack(pady=15)
        
        # Modern tree container
        tree_container = tk.Frame(history_win, bg='#16213e')
        tree_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        tree = ttk.Treeview(
            tree_container, 
            columns=("Book ID", "Title", "Enrollment No", "Student Name", "Borrow Date", "Return Date"), 
            show='headings', 
            height=25
        )
        
        for col in ("Book ID", "Title", "Enrollment No", "Student Name", "Borrow Date", "Return Date"):
            tree.heading(col, text=col)
            tree.column(col, width=140)
        
        tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Get history from db
        for record in self.db.get_book_history():
            tree.insert('', 'end', values=record)
    def show_student_history(self):
        # Show all borrow/return history for students with modern styling
        history_win = tk.Toplevel(self.root)
        history_win.title("≡ƒæÑ Student Borrow/Return History")
        history_win.geometry("1000x650")
        history_win.configure(bg='#1a1a2e')
        
        # Modern title
        title_label = tk.Label(
            history_win,
            text="≡ƒæÑ Student Transaction History",
            font=('Segoe UI', 18, 'bold'),
            bg='#1a1a2e',
            fg='#ccd6f6'
        )
        title_label.pack(pady=15)
        
        # Modern tree container
        tree_container = tk.Frame(history_win, bg='#16213e')
        tree_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        tree = ttk.Treeview(
            tree_container, 
            columns=("Enrollment No", "Student Name", "Book ID", "Title", "Borrow Date", "Return Date"), 
            show='headings', 
            height=25
        )
        
        for col in ("Enrollment No", "Student Name", "Book ID", "Title", "Borrow Date", "Return Date"):
            tree.heading(col, text=col)
            tree.column(col, width=140)
        
        tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Get history from db
        for record in self.db.get_student_history():
            tree.insert('', 'end', values=record)
    
    def show_transactions(self):
        """Show transactions view"""
        if self.current_view == 'transactions':
            return
        self.current_view = 'transactions'
        self.clear_content()
        self.create_transactions_view()
    
    def show_reports(self):
        """Show reports view"""
        if self.current_view == 'reports':
            return
        self.current_view = 'reports'
        self.clear_content()
        self.create_reports_view()
    
    def create_dashboard_view(self):
        """Create modern dashboard view with sleek cards"""
        # Modern title
        title_frame = tk.Frame(self.content_frame, bg='#1a1a2e')
        title_frame.pack(fill=tk.X, pady=(0, 25))
        
        tk.Label(
            title_frame, 
            text="≡ƒôè Library Dashboard", 
            font=('Segoe UI', 22, 'bold'),
            bg='#1a1a2e',
            fg='#ccd6f6'
        ).pack(side=tk.LEFT)
        
        # Modern stats cards container
        stats_container = tk.Frame(self.content_frame, bg='#1a1a2e')
        stats_container.pack(fill=tk.X, pady=(0, 30))
        
        # Get statistics
        students = self.db.get_students()
        books = self.db.get_books()
        borrowed = self.db.get_borrowed_books()
        
        stats = [
            ("Total Students", len(students), '#ff6b6b', '≡ƒæÑ'),
            ("Total Books", len(books), '#4ecdc4', '≡ƒôÜ'),
            ("Books Borrowed", len(borrowed), '#ffa726', '≡ƒôñ'),
            ("Available Books", sum(book[6] for book in books) if books else 0, '#26de81', 'Γ£à')
        ]
        
        for title, value, color, icon in stats:
            # Modern card with sleek design
            card_container = tk.Frame(stats_container, bg='#1a1a2e')
            card_container.pack(side=tk.LEFT, padx=15, fill=tk.BOTH, expand=True)
            
            card = tk.Frame(
                card_container, 
                bg='#16213e', 
                relief=tk.FLAT, 
                bd=0,
                width=250, 
                height=120
            )
            card.pack(fill=tk.BOTH, expand=True)
            card.pack_propagate(False)
            
            # Card content with modern layout
            content_frame = tk.Frame(card, bg='#16213e')
            content_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=15)
            
            # Icon and value row
            top_row = tk.Frame(content_frame, bg='#16213e')
            top_row.pack(fill=tk.X)
            
            tk.Label(
                top_row, 
                text=icon, 
                font=('Segoe UI', 24), 
                fg=color, 
                bg='#16213e'
            ).pack(side=tk.LEFT)
            
            tk.Label(
                top_row, 
                text=str(value), 
                font=('Segoe UI', 28, 'bold'), 
                fg='#ccd6f6', 
                bg='#16213e'
            ).pack(side=tk.RIGHT)
            
            # Title row
            tk.Label(
                content_frame, 
                text=title, 
                font=('Segoe UI', 11, 'bold'), 
                fg='#8892b0', 
                bg='#16213e'
            ).pack(anchor='w', side=tk.BOTTOM)
        
        # Modern section title
        tk.Label(
            self.content_frame, 
            text="≡ƒôï Currently Borrowed Books", 
            font=('Segoe UI', 18, 'bold'),
            bg='#1a1a2e',
            fg='#ccd6f6'
        ).pack(anchor='w', pady=(20, 15))
        
        # Modern list container
        list_container = tk.Frame(self.content_frame, bg='#16213e', relief=tk.FLAT, bd=0)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        columns = ('Enrollment No', 'Student Name', 'Dept', 'Year', 'Book ID', 'Title', 'Author', 'Borrow Date', 'Due Date')
        self.borrowed_tree = ttk.Treeview(list_container, columns=columns, show='headings', height=15)
        
        # Modern treeview styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', 
                       background='#0f1419',
                       foreground='#ccd6f6',
                       fieldbackground='#0f1419',
                       borderwidth=0,
                       relief='flat')
        style.configure('Treeview.Heading',
                       background='#16213e',
                       foreground='#ccd6f6',
                       borderwidth=0,
                       relief='flat')
        
        for col in columns:
            self.borrowed_tree.heading(col, text=col)
            self.borrowed_tree.column(col, width=120)
        
        # Modern scrollbar
        borrowed_scroll = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.borrowed_tree.yview)
        self.borrowed_tree.configure(yscrollcommand=borrowed_scroll.set)
        
        self.borrowed_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        borrowed_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=15)
        
        self.refresh_borrowed()
    
    def create_students_view(self):
        """Create modern students management view"""
        # Modern title and controls
        title_frame = tk.Frame(self.content_frame, bg='#1a1a2e')
        title_frame.pack(fill=tk.X, pady=(0, 25))
        
        tk.Label(
            title_frame, 
            text="≡ƒæÑ Student Management", 
            font=('Segoe UI', 22, 'bold'),
            bg='#1a1a2e',
            fg='#ccd6f6'
        ).pack(side=tk.LEFT)
        
        # Modern controls frame
        controls_frame = tk.Frame(self.content_frame, bg='#16213e', relief=tk.FLAT, bd=0)
        controls_frame.pack(fill=tk.X, padx=0, pady=(0, 15))
        
        # Modern search and add section
        search_frame = tk.Frame(controls_frame, bg='#16213e')
        search_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(
            search_frame, 
            text="≡ƒöì Search Students:", 
            font=('Segoe UI', 12, 'bold'), 
            bg='#16213e',
            fg='#ccd6f6'
        ).pack(side=tk.LEFT)
        
        self.student_search_var = tk.StringVar()
        self.student_search_var.trace('w', lambda *args: self.search_students())
        search_entry = tk.Entry(
            search_frame, 
            textvariable=self.student_search_var, 
            width=40, 
            font=('Segoe UI', 11),
            bg='#0f1419',
            fg='#ccd6f6',
            insertbackground='#00d4ff',
            bd=0,
            relief=tk.FLAT
        )
        search_entry.pack(side=tk.LEFT, padx=(15, 0), ipady=5)
        
        # Modern buttons with vibrant colors
        add_btn = tk.Button(
            search_frame, 
            text="Γ₧ò Add New Student", 
            command=self.show_add_student_dialog,
            bg='#4ecdc4', 
            fg='#0f1419', 
            font=('Segoe UI', 11, 'bold'),
            padx=20,
            pady=8,
            cursor='hand2',
            relief=tk.FLAT,
            bd=0,
            activebackground='#26de81',
            activeforeground='#0f1419'
        )
        add_btn.pack(side=tk.RIGHT, padx=10)
        
        import_btn = tk.Button(
            search_frame, 
            text="≡ƒôè Import from Excel", 
            command=self.import_students_excel,
            bg='#a55eea', 
            fg='#ffffff', 
            font=('Segoe UI', 11, 'bold'),
            padx=20,
            pady=8,
            cursor='hand2',
            relief=tk.FLAT,
            bd=0,
            activebackground='#8854d0',
            activeforeground='#ffffff'
        )
        import_btn.pack(side=tk.RIGHT, padx=10)
        
        # Modern students list container
        list_container = tk.Frame(self.content_frame, bg='#16213e', relief=tk.FLAT, bd=0)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Enrollment No', 'Name', 'Email', 'Phone', 'Department', 'Year', 'Date Registered')
        self.students_tree = ttk.Treeview(list_container, columns=columns, show='headings', height=18)
        
        for col in columns:
            self.students_tree.heading(col, text=col)
            self.students_tree.column(col, width=140)
        
        students_scroll = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.students_tree.yview)
        self.students_tree.configure(yscrollcommand=students_scroll.set)
        
        self.students_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        students_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=15)
        
        self.students_tree.bind("<Button-3>", self.show_student_context_menu)
        # Only show Computer department students
        students = [s for s in self.db.get_students() if s[5] == "Computer"]
        self.populate_students_tree(students)
    
    def create_books_view(self):
        """Create modern books management view"""
        # Modern title and controls
        title_frame = tk.Frame(self.content_frame, bg='#1a1a2e')
        title_frame.pack(fill=tk.X, pady=(0, 25))
        
        tk.Label(
            title_frame, 
            text="≡ƒôÜ Book Management", 
            font=('Segoe UI', 22, 'bold'),
            bg='#1a1a2e',
            fg='#ccd6f6'
        ).pack(side=tk.LEFT)
        
        # Modern controls frame
        controls_frame = tk.Frame(self.content_frame, bg='#16213e', relief=tk.FLAT, bd=0)
        controls_frame.pack(fill=tk.X, padx=0, pady=(0, 15))
        
        # Modern search and add section
        search_frame = tk.Frame(controls_frame, bg='#16213e')
        search_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(
            search_frame, 
            text="≡ƒöì Search Books:", 
            font=('Segoe UI', 12, 'bold'), 
            bg='#16213e',
            fg='#ccd6f6'
        ).pack(side=tk.LEFT)
        
        self.book_search_var = tk.StringVar()
        self.book_search_var.trace('w', lambda *args: self.search_books())
        search_entry = tk.Entry(
            search_frame, 
            textvariable=self.book_search_var, 
            width=40, 
            font=('Segoe UI', 11),
            bg='#0f1419',
            fg='#ccd6f6',
            insertbackground='#00d4ff',
            bd=0,
            relief=tk.FLAT
        )
        search_entry.pack(side=tk.LEFT, padx=(15, 0), ipady=5)
        
        # Modern buttons
        add_btn = tk.Button(
            search_frame, 
            text="Γ₧ò Add New Book", 
            command=self.show_add_book_dialog,
            bg='#45b7d1', 
            fg='#0f1419', 
            font=('Segoe UI', 11, 'bold'),
            padx=20,
            pady=8,
            cursor='hand2',
            relief=tk.FLAT,
            bd=0,
            activebackground='#3498db',
            activeforeground='#0f1419'
        )
        add_btn.pack(side=tk.RIGHT, padx=10)
        
        import_btn = tk.Button(
            search_frame, 
            text="≡ƒôè Import from Excel", 
            command=self.import_books_excel,
            bg='#a55eea', 
            fg='#ffffff', 
            font=('Segoe UI', 11, 'bold'),
            padx=20,
            pady=8,
            cursor='hand2',
            relief=tk.FLAT,
            bd=0,
            activebackground='#8854d0',
            activeforeground='#ffffff'
        )
        import_btn.pack(side=tk.RIGHT, padx=10)
        
        # Modern books list container
        list_container = tk.Frame(self.content_frame, bg='#16213e', relief=tk.FLAT, bd=0)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Book ID', 'Title', 'Author', 'Category', 'Total Copies', 'Available')
        self.books_tree = ttk.Treeview(list_container, columns=columns, show='headings', height=18)
        
        for col in columns:
            self.books_tree.heading(col, text=col)
            self.books_tree.column(col, width=140)
        
        books_scroll = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.books_tree.yview)
        self.books_tree.configure(yscrollcommand=books_scroll.set)
        
        self.books_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        books_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=15)
        
        self.books_tree.bind("<Button-3>", self.show_book_context_menu)
        # Only show Computer department books (category Technology/Textbook/Research)
        books = [b for b in self.db.get_books() if b[5] in ["Technology", "Textbook", "Research"]]
        self.populate_books_tree(books)
    
    def create_transactions_view(self):
        """Create modern transactions view for borrowing/returning"""
        # Modern title
        title_frame = tk.Frame(self.content_frame, bg='#1a1a2e')
        title_frame.pack(fill=tk.X, pady=(0, 25))
        
        tk.Label(
            title_frame, 
            text="≡ƒôï Book Transactions", 
            font=('Segoe UI', 22, 'bold'),
            bg='#1a1a2e',
            fg='#ccd6f6'
        ).pack(side=tk.LEFT)
        
        # Split into two modern sections
        paned = ttk.PanedWindow(self.content_frame, orient=tk.VERTICAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Modern borrow section
        borrow_section = tk.Frame(paned, bg='#16213e', relief=tk.FLAT, bd=0)
        paned.add(borrow_section, weight=1)
        
        tk.Label(
            borrow_section, 
            text="≡ƒôñ Borrow Book", 
            font=('Segoe UI', 18, 'bold'), 
            bg='#16213e', 
            fg='#ccd6f6'
        ).pack(pady=20)
        
        borrow_form = tk.Frame(borrow_section, bg='#16213e')
        borrow_form.pack(padx=40, pady=20)
        
        # Student enrollment with modern styling
        tk.Label(
            borrow_form, 
            text="Student Enrollment No:", 
            bg='#16213e', 
            font=('Segoe UI', 12, 'bold'),
            fg='#ccd6f6'
        ).grid(row=0, column=0, sticky='w', padx=10, pady=10)
        
        # Modern enrollment entry frame
        enrollment_frame = tk.Frame(borrow_form, bg='#16213e')
        enrollment_frame.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        
        self.borrow_enrollment_no = tk.Entry(
            enrollment_frame, 
            width=25, 
            font=('Segoe UI', 11),
            bg='#0f1419',
            fg='#ccd6f6',
            insertbackground='#00d4ff',
            bd=0,
            relief=tk.FLAT
        )
        self.borrow_enrollment_no.pack(ipady=5)
        
        # Suggestion listbox for enrollment (hidden - suggestions disabled)
        # self.enrollment_suggestion_box = tk.Listbox(
        #     enrollment_frame, 
        #     width=25, 
        #     height=4, 
        #     font=('Segoe UI', 10),
        #     bg='#0f1419',
        #     fg='#ccd6f6',
        #     selectbackground='#00d4ff',
        #     bd=0,
        #     relief=tk.FLAT
        # )
        
        # Student details display with modern styling
        self.borrow_student_details = tk.Label(
            borrow_form, 
            text="", 
            bg='#16213e', 
            font=('Segoe UI', 10, 'italic'), 
            fg='#4ecdc4', 
            wraplength=300
        )
        self.borrow_student_details.grid(row=1, column=0, columnspan=2, sticky='w', padx=10, pady=5)
        
        # Book ID with modern styling
        tk.Label(
            borrow_form, 
            text="Book ID:", 
            bg='#16213e', 
            font=('Segoe UI', 12, 'bold'),
            fg='#ccd6f6'
        ).grid(row=0, column=2, sticky='w', padx=10, pady=10)
        
        # Modern book entry frame
        book_frame = tk.Frame(borrow_form, bg='#16213e')
        book_frame.grid(row=0, column=3, padx=10, pady=10, sticky='w')
        
        self.borrow_book_id = tk.Entry(
            book_frame, 
            width=25, 
            font=('Segoe UI', 11),
            bg='#0f1419',
            fg='#ccd6f6',
            insertbackground='#00d4ff',
            bd=0,
            relief=tk.FLAT
        )
        self.borrow_book_id.pack(ipady=5)
        
        # Suggestion listbox for book ID (hidden - suggestions disabled)
        # self.book_suggestion_box = tk.Listbox(
        #     book_frame, 
        #     width=25, 
        #     height=4, 
        #     font=('Segoe UI', 10),
        #     bg='#0f1419',
        #     fg='#ccd6f6',
        #     selectbackground='#00d4ff',
        #     bd=0,
        #     relief=tk.FLAT
        # )
        
        # Book details display
        self.borrow_book_details = tk.Label(
            borrow_form, 
            text="", 
            bg='#16213e', 
            font=('Segoe UI', 10, 'italic'), 
            fg='#45b7d1', 
            wraplength=300
        )
        self.borrow_book_details.grid(row=1, column=2, columnspan=2, sticky='w', padx=10, pady=5)
        
        # Due date with modern styling
        tk.Label(
            borrow_form, 
            text="Due Date:", 
            bg='#16213e', 
            font=('Segoe UI', 12, 'bold'),
            fg='#ccd6f6'
        ).grid(row=2, column=0, sticky='w', padx=10, pady=10)
        
        self.due_date = tk.Entry(
            borrow_form, 
            width=25, 
            font=('Segoe UI', 11),
            bg='#0f1419',
            fg='#ccd6f6',
            insertbackground='#00d4ff',
            bd=0,
            relief=tk.FLAT
        )
        self.due_date.grid(row=2, column=1, padx=10, pady=10, ipady=5)
        
        # Set default due date (14 days from now)
        default_due = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        self.due_date.insert(0, default_due)
        
        # Modern borrow button
        borrow_btn = tk.Button(
            borrow_form, 
            text="≡ƒôñ Borrow Book", 
            command=self.borrow_book,
            bg='#f9ca24', 
            fg='#0f1419', 
            font=('Segoe UI', 12, 'bold'),
            padx=25,
            pady=12,
            relief=tk.FLAT,
            bd=0,
            cursor='hand2',
            activebackground='#f39c12',
            activeforeground='#0f1419'
        )
        borrow_btn.grid(row=2, column=2, columnspan=2, padx=20, pady=15)
        
        # Bind events for borrow form (suggestions removed)
        # self.borrow_enrollment_no.bind('<KeyRelease>', self.show_enrollment_suggestions)
        # self.enrollment_suggestion_box.bind('<<ListboxSelect>>', self.select_enrollment_suggestion)
        # self.borrow_book_id.bind('<KeyRelease>', self.show_book_suggestions)
        # self.book_suggestion_box.bind('<<ListboxSelect>>', self.select_book_suggestion)
        
        # Modern return section
        return_section = tk.Frame(paned, bg='#16213e', relief=tk.FLAT, bd=0)
        paned.add(return_section, weight=1)
        
        tk.Label(
            return_section, 
            text="≡ƒôÑ Return Book", 
            font=('Segoe UI', 18, 'bold'), 
            bg='#16213e', 
            fg='#ccd6f6'
        ).pack(pady=20)
        
        return_form = tk.Frame(return_section, bg='#16213e')
        return_form.pack(padx=40, pady=20)
        
        # Return form - Student enrollment with modern styling
        tk.Label(
            return_form, 
            text="Student Enrollment No:", 
            bg='#16213e', 
            font=('Segoe UI', 12, 'bold'),
            fg='#ccd6f6'
        ).grid(row=0, column=0, sticky='w', padx=10, pady=10)
        
        # Modern return enrollment entry frame
        return_enrollment_frame = tk.Frame(return_form, bg='#16213e')
        return_enrollment_frame.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        
        self.return_enrollment_no = tk.Entry(
            return_enrollment_frame, 
            width=25, 
            font=('Segoe UI', 11),
            bg='#0f1419',
            fg='#ccd6f6',
            insertbackground='#00d4ff',
            bd=0,
            relief=tk.FLAT
        )
        self.return_enrollment_no.pack(ipady=5)
        
        # Suggestion listbox for return enrollment (hidden - suggestions disabled)
        # self.return_enrollment_suggestion_box = tk.Listbox(
        #     return_enrollment_frame, 
        #     width=25, 
        #     height=4, 
        #     font=('Segoe UI', 10),
        #     bg='#0f1419',
        #     fg='#ccd6f6',
        #     selectbackground='#00d4ff',
        #     bd=0,
        #     relief=tk.FLAT
        # )
        
        # Return form - Book ID with modern styling
        tk.Label(
            return_form, 
            text="Book ID:", 
            bg='#16213e', 
            font=('Segoe UI', 12, 'bold'),
            fg='#ccd6f6'
        ).grid(row=0, column=2, sticky='w', padx=10, pady=10)
        
        # Modern return book entry frame
        return_book_frame = tk.Frame(return_form, bg='#16213e')
        return_book_frame.grid(row=0, column=3, padx=10, pady=10, sticky='w')
        
        self.return_book_id = tk.Entry(
            return_book_frame, 
            width=25, 
            font=('Segoe UI', 11),
            bg='#0f1419',
            fg='#ccd6f6',
            insertbackground='#00d4ff',
            bd=0,
            relief=tk.FLAT
        )
        self.return_book_id.pack(ipady=5)
        
        # Suggestion listbox for return book ID (hidden - suggestions disabled)
        # self.return_book_suggestion_box = tk.Listbox(
        #     return_book_frame, 
        #     width=25, 
        #     height=4, 
        #     font=('Segoe UI', 10),
        #     bg='#0f1419',
        #     fg='#ccd6f6',
        #     selectbackground='#00d4ff',
        #     bd=0,
        #     relief=tk.FLAT
        # )
        
        # Return details display
        self.return_details = tk.Label(
            return_form, 
            text="", 
            bg='#16213e', 
            font=('Segoe UI', 10, 'italic'), 
            fg='#ff6b6b', 
            wraplength=600
        )
        self.return_details.grid(row=1, column=0, columnspan=4, sticky='w', padx=10, pady=5)
        
        # Modern return button
        return_btn = tk.Button(
            return_form, 
            text="≡ƒôÑ Return Book", 
            command=self.return_book,
            bg='#4ecdc4', 
            fg='#0f1419', 
            font=('Segoe UI', 12, 'bold'),
            padx=25,
            pady=12,
            relief=tk.FLAT,
            bd=0,
            cursor='hand2',
            activebackground='#26de81',
            activeforeground='#0f1419'
        )
        return_btn.grid(row=2, column=1, columnspan=2, padx=20, pady=15)
        
        # Bind events for return form (suggestions removed)
        # self.return_enrollment_no.bind('<KeyRelease>', self.show_return_enrollment_suggestions)
        # self.return_enrollment_suggestion_box.bind('<<ListboxSelect>>', self.select_return_enrollment_suggestion)
        self.return_book_id.bind('<KeyRelease>', self.show_return_book_suggestions)
        self.return_book_suggestion_box.bind('<<ListboxSelect>>', self.select_return_book_suggestion)
    
    def create_reports_view(self):
        """Create reports view"""
        # Title
        title_frame = tk.Frame(self.content_frame, bg='#f8f9fa')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            title_frame, 
            text="≡ƒôè Library Reports", 
            font=('Arial', 20, 'bold'),
            bg='#f8f9fa',
            fg='#2c3e50'
        ).pack(side=tk.LEFT)
        
        # Reports content
        reports_frame = tk.Frame(self.content_frame, bg='#fff5f5', relief=tk.RIDGE, bd=1)
        reports_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        tk.Label(
            reports_frame, 
            text="≡ƒôê Detailed Reports Coming Soon!", 
            font=('Arial', 18, 'bold'),
            bg='#fff5f5',
            fg='#7f8c8d'
        ).pack(expand=True)
        
        tk.Label(
            reports_frame, 
            text="This section will include:\nΓÇó Student borrowing history\nΓÇó Most popular books\nΓÇó Overdue reports\nΓÇó Department-wise statistics", 
            font=('Arial', 14),
            bg='#fff5f5',
            fg='#95a5a6',
            justify=tk.LEFT
        ).pack(expand=True)
    
    def show_add_student_dialog(self):
        """Show add student dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Student")
        dialog.geometry("500x450")
        dialog.resizable(False, False)
        dialog.configure(bg='#fff5f5')
        
        # Center the dialog
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog on screen
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (450 // 2)
        dialog.geometry(f"500x450+{x}+{y}")
        
        # Form fields
        tk.Label(dialog, text="≡ƒæñ Add New Student", font=('Arial', 16, 'bold'), bg='#fff5f5', fg='#2c3e50').pack(pady=15)
        
        form_frame = tk.Frame(dialog, bg='#fff5f5')
        form_frame.pack(padx=30, pady=20)
        
        # Enrollment Number
        tk.Label(form_frame, text="Enrollment No:", bg='#fff5f5', font=('Arial', 11, 'bold')).grid(row=0, column=0, sticky='w', pady=8)
        enrollment_entry = tk.Entry(form_frame, width=35, font=('Arial', 11))
        enrollment_entry.grid(row=0, column=1, pady=8, padx=(15, 0))
        
        # Name
        tk.Label(form_frame, text="Full Name:", bg='#fff5f5', font=('Arial', 11, 'bold')).grid(row=1, column=0, sticky='w', pady=8)
        name_entry = tk.Entry(form_frame, width=35, font=('Arial', 11))
        name_entry.grid(row=1, column=1, pady=8, padx=(15, 0))
        
        # Email
        tk.Label(form_frame, text="Email:", bg='#fff5f5', font=('Arial', 11, 'bold')).grid(row=2, column=0, sticky='w', pady=8)
        email_entry = tk.Entry(form_frame, width=35, font=('Arial', 11))
        email_entry.grid(row=2, column=1, pady=8, padx=(15, 0))
        
        # Phone
        tk.Label(form_frame, text="Phone:", bg='#fff5f5', font=('Arial', 11, 'bold')).grid(row=3, column=0, sticky='w', pady=8)
        phone_entry = tk.Entry(form_frame, width=35, font=('Arial', 11))
        phone_entry.grid(row=3, column=1, pady=8, padx=(15, 0))
        
        # Department
        tk.Label(form_frame, text="Department:", bg='#fff5f5', font=('Arial', 11, 'bold')).grid(row=4, column=0, sticky='w', pady=8)
        department_entry = ttk.Combobox(form_frame, width=33, font=('Arial', 11), values=[
            "Mechanical", "Civil", "Electrical", "IT", "E&TC", "Computer", "Automobile"
        ])
        department_entry.grid(row=4, column=1, pady=8, padx=(15, 0))
        
        # Year
        tk.Label(form_frame, text="Academic Year:", bg='#fff5f5', font=('Arial', 11, 'bold')).grid(row=5, column=0, sticky='w', pady=8)
        year_entry = ttk.Combobox(form_frame, width=33, font=('Arial', 11), values=[
            "1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year", "Graduate", "Post Graduate"
        ])
        year_entry.grid(row=5, column=1, pady=8, padx=(15, 0))
        
        def save_student():
            if not enrollment_entry.get() or not name_entry.get():
                messagebox.showerror("Error", "Enrollment Number and Name are required!")
                return
            
            if not department_entry.get():
                messagebox.showerror("Error", "Please select a department!")
                return
                
            if not year_entry.get():
                messagebox.showerror("Error", "Please select academic year!")
                return
            
            success, message = self.db.add_student(
                enrollment_entry.get(),
                name_entry.get(),
                email_entry.get(),
                phone_entry.get(),
                department_entry.get(),
                year_entry.get()
            )
            
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                # Force refresh the students view
                self.refresh_students()
                # Update the dashboard as well
                if hasattr(self, 'borrowed_tree'):
                    self.refresh_borrowed()
                # Force UI update
                self.root.update_idletasks()
            else:
                messagebox.showerror("Error", message)
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg='#fff5f5')
        btn_frame.pack(pady=30, side=tk.BOTTOM)
        
        save_btn = tk.Button(btn_frame, text="≡ƒÆ╛ Save Student", command=save_student, bg='#28a745', fg='white', width=15, height=2, font=('Segoe UI', 11, 'bold'), relief=tk.FLAT, cursor='hand2')
        save_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = tk.Button(btn_frame, text="Γ¥î Cancel", command=dialog.destroy, bg='#dc3545', fg='white', width=15, height=2, font=('Segoe UI', 11, 'bold'), relief=tk.FLAT, cursor='hand2')
        cancel_btn.pack(side=tk.LEFT, padx=10)
    
    def show_add_book_dialog(self):
        """Show add book dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Book")
        dialog.geometry("500x450")
        dialog.resizable(False, False)
        dialog.configure(bg='#fff5f5')
        
        # Center the dialog
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog on screen
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (450 // 2)
        dialog.geometry(f"500x450+{x}+{y}")
        
        # Form fields
        tk.Label(dialog, text="≡ƒôÜ Add New Book", font=('Arial', 16, 'bold'), bg='#fff5f5', fg='#2c3e50').pack(pady=15)
        
        form_frame = tk.Frame(dialog, bg='#fff5f5')
        form_frame.pack(padx=30, pady=20)
        
        tk.Label(form_frame, text="Book ID:", bg='#fff5f5', font=('Arial', 11, 'bold')).grid(row=0, column=0, sticky='w', pady=8)
        book_id_entry = tk.Entry(form_frame, width=35, font=('Arial', 11))
        book_id_entry.grid(row=0, column=1, pady=8, padx=(15, 0))
        
        tk.Label(form_frame, text="Title:", bg='#fff5f5', font=('Arial', 11, 'bold')).grid(row=1, column=0, sticky='w', pady=8)
        title_entry = tk.Entry(form_frame, width=35, font=('Arial', 11))
        title_entry.grid(row=1, column=1, pady=8, padx=(15, 0))
        
        tk.Label(form_frame, text="Author:", bg='#fff5f5', font=('Arial', 11, 'bold')).grid(row=2, column=0, sticky='w', pady=8)
        author_entry = tk.Entry(form_frame, width=35, font=('Arial', 11))
        author_entry.grid(row=2, column=1, pady=8, padx=(15, 0))
        
        tk.Label(form_frame, text="ISBN:", bg='#fff5f5', font=('Arial', 11, 'bold')).grid(row=3, column=0, sticky='w', pady=8)
        isbn_entry = tk.Entry(form_frame, width=35, font=('Arial', 11))
        isbn_entry.grid(row=3, column=1, pady=8, padx=(15, 0))
        
        tk.Label(form_frame, text="Category:", bg='#fff5f5', font=('Arial', 11, 'bold')).grid(row=4, column=0, sticky='w', pady=8)
        category_entry = ttk.Combobox(form_frame, width=33, font=('Arial', 11), values=[
            "Fiction", "Non-Fiction", "Science", "Technology", "Mathematics", "History", 
            "Biography", "Reference", "Textbook", "Research", "Other"
        ])
        category_entry.grid(row=4, column=1, pady=8, padx=(15, 0))
        
        tk.Label(form_frame, text="Total Copies:", bg='#fff5f5', font=('Arial', 11, 'bold')).grid(row=5, column=0, sticky='w', pady=8)
        copies_entry = tk.Entry(form_frame, width=35, font=('Arial', 11))
        copies_entry.grid(row=5, column=1, pady=8, padx=(15, 0))
        copies_entry.insert(0, "1")
        
        def save_book():
            if not book_id_entry.get() or not title_entry.get():
                messagebox.showerror("Error", "Book ID and Title are required!")
                return
            
            try:
                copies = int(copies_entry.get())
                if copies <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "Total copies must be a positive number!")
                return
            
            success, message = self.db.add_book(
                book_id_entry.get(),
                title_entry.get(),
                author_entry.get(),
                isbn_entry.get(),
                category_entry.get(),
                copies
            )
            
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                # Force refresh the books view
                self.refresh_books()
                # Update the dashboard as well
                if hasattr(self, 'borrowed_tree'):
                    self.refresh_borrowed()
                # Force UI update
                self.root.update_idletasks()
            else:
                messagebox.showerror("Error", message)
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg='#fff5f5')
        btn_frame.pack(pady=30, side=tk.BOTTOM)
        
        save_btn = tk.Button(btn_frame, text="≡ƒÆ╛ Save Book", command=save_book, bg='#17a2b8', fg='white', width=15, height=2, font=('Segoe UI', 11, 'bold'), relief=tk.FLAT, cursor='hand2')
        save_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = tk.Button(btn_frame, text="Γ¥î Cancel", command=dialog.destroy, bg='#dc3545', fg='white', width=15, height=2, font=('Segoe UI', 11, 'bold'), relief=tk.FLAT, cursor='hand2')
        cancel_btn.pack(side=tk.LEFT, padx=10)
    
    def show_enrollment_suggestions(self, event):
        """Show enrollment number suggestions for borrow form"""
        typed = self.borrow_enrollment_no.get()
        if len(typed) < 1:
            self.enrollment_suggestion_box.pack_forget()
            return
            
        # Get Computer department students matching the typed text
        students = [s for s in self.db.get_students() if s[5] == "Computer" and typed.lower() in s[1].lower()]
        
        self.enrollment_suggestion_box.delete(0, tk.END)
        for student in students:
            display_text = f"{student[1]} - {student[2]}"  # Enrollment - Name
            self.enrollment_suggestion_box.insert(tk.END, display_text)
        
        if students and typed:
            self.enrollment_suggestion_box.pack(pady=(5, 0))
        else:
            self.enrollment_suggestion_box.pack_forget()
    
    def select_enrollment_suggestion(self, event):
        """Select enrollment from suggestions for borrow form"""
        selection = self.enrollment_suggestion_box.curselection()
        if selection:
            selected_text = self.enrollment_suggestion_box.get(selection[0])
            enrollment = selected_text.split(" - ")[0]  # Extract enrollment number
            
            self.borrow_enrollment_no.delete(0, tk.END)
            self.borrow_enrollment_no.insert(0, enrollment)
            self.enrollment_suggestion_box.pack_forget()
            
            # Auto-fill student details
            student = next((s for s in self.db.get_students() if s[1] == enrollment), None)
            if student:
                self.borrow_student_details.config(text=f"Γ£ô Student: {student[2]} | Department: {student[5]} | Year: {student[6]}")
            else:
                self.borrow_student_details.config(text="")
    
    def show_book_suggestions(self, event):
        """Show book ID suggestions for borrow form"""
        typed = self.borrow_book_id.get()
        if len(typed) < 1:
            self.book_suggestion_box.pack_forget()
            return
            
        # Get available books matching the typed text
        books = self.db.get_books()
        available_books = [b for b in books if b[6] > 0 and typed.lower() in b[1].lower()]  # Available copies > 0
        
        self.book_suggestion_box.delete(0, tk.END)
        for book in available_books:
            display_text = f"{book[1]} - {book[2]}"  # Book ID - Title
            self.book_suggestion_box.insert(tk.END, display_text)
        
        if available_books and typed:
            self.book_suggestion_box.pack(pady=(5, 0))
        else:
            self.book_suggestion_box.pack_forget()
    
    def select_book_suggestion(self, event):
        """Select book from suggestions for borrow form"""
        selection = self.book_suggestion_box.curselection()
        if selection:
            selected_text = self.book_suggestion_box.get(selection[0])
            book_id = selected_text.split(" - ")[0]  # Extract book ID
            
            self.borrow_book_id.delete(0, tk.END)
            self.borrow_book_id.insert(0, book_id)
            self.book_suggestion_box.pack_forget()
            
            # Auto-fill book details
            book = next((b for b in self.db.get_books() if b[1] == book_id), None)
            if book:
                self.borrow_book_details.config(text=f"Γ£ô Book: {book[2]} | Author: {book[3]} | Available: {book[6]} copies")
            else:
                self.borrow_book_details.config(text="")
    
    def show_return_enrollment_suggestions(self, event):
        """Show enrollment suggestions for return form (only students with borrowed books)"""
        typed = self.return_enrollment_no.get()
        if len(typed) < 1:
            self.return_enrollment_suggestion_box.pack_forget()
            return
            
        # Get students who have borrowed books
        borrowed_books = self.db.get_borrowed_books()
        students_with_books = list(set([b[0] for b in borrowed_books]))  # Unique enrollment numbers
        students = [s for s in self.db.get_students() if s[1] in students_with_books and typed.lower() in s[1].lower()]
        
        self.return_enrollment_suggestion_box.delete(0, tk.END)
        for student in students:
            display_text = f"{student[1]} - {student[2]}"
            self.return_enrollment_suggestion_box.insert(tk.END, display_text)
        
        if students and typed:
            self.return_enrollment_suggestion_box.pack(pady=(5, 0))
        else:
            self.return_enrollment_suggestion_box.pack_forget()
    
    def select_return_enrollment_suggestion(self, event):
        """Select enrollment from suggestions for return form"""
        selection = self.return_enrollment_suggestion_box.curselection()
        if selection:
            selected_text = self.return_enrollment_suggestion_box.get(selection[0])
            enrollment = selected_text.split(" - ")[0]
            
            self.return_enrollment_no.delete(0, tk.END)
            self.return_enrollment_no.insert(0, enrollment)
            self.return_enrollment_suggestion_box.pack_forget()
            
            # Show borrowed books for this student
            borrowed_books = [b for b in self.db.get_borrowed_books() if b[0] == enrollment]
            if borrowed_books:
                book_list = ", ".join([f"{b[4]} ({b[5]})" for b in borrowed_books])
                self.return_details.config(text=f"Γ£ô Borrowed Books: {book_list}")
            else:
                self.return_details.config(text="No borrowed books found for this student")
    
    def show_return_book_suggestions(self, event):
        """Show book suggestions for return form (only borrowed books)"""
        typed = self.return_book_id.get()
        enrollment = self.return_enrollment_no.get()
        
        if len(typed) < 1:
            self.return_book_suggestion_box.pack_forget()
            return
        
        # Get borrowed books for the specific student or all if no student selected
        borrowed_books = self.db.get_borrowed_books()
        if enrollment:
            borrowed_books = [b for b in borrowed_books if b[0] == enrollment and typed.lower() in b[4].lower()]
        else:
            borrowed_books = [b for b in borrowed_books if typed.lower() in b[4].lower()]
        
        self.return_book_suggestion_box.delete(0, tk.END)
        for book in borrowed_books:
            display_text = f"{book[4]} - {book[5]}"  # Book ID - Title
            self.return_book_suggestion_box.insert(tk.END, display_text)
        
        if borrowed_books and typed:
            self.return_book_suggestion_box.pack(pady=(5, 0))
        else:
            self.return_book_suggestion_box.pack_forget()
    
    def select_return_book_suggestion(self, event):
        """Select book from suggestions for return form"""
        selection = self.return_book_suggestion_box.curselection()
        if selection:
            selected_text = self.return_book_suggestion_box.get(selection[0])
            book_id = selected_text.split(" - ")[0]
            
            self.return_book_id.delete(0, tk.END)
            self.return_book_id.insert(0, book_id)
            self.return_book_suggestion_box.pack_forget()
            
            # Show return details
            enrollment = self.return_enrollment_no.get()
            borrowed_books = [b for b in self.db.get_borrowed_books() if b[0] == enrollment and b[4] == book_id]
            if borrowed_books:
                book = borrowed_books[0]
                self.return_details.config(text=f"Γ£ô Returning: {book[5]} | Borrowed on: {book[7]} | Due: {book[8]}")
            else:
                self.return_details.config(text="Book not found in borrowed list")
    
    def borrow_book(self):
        """Handle book borrowing with improved validation"""
        enrollment_no = self.borrow_enrollment_no.get().strip()
        book_id = self.borrow_book_id.get().strip()
        due_date = self.due_date.get().strip()
        
        if not enrollment_no or not book_id or not due_date:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        # Validate student exists and is from Computer department
        student = next((s for s in self.db.get_students() if s[1] == enrollment_no and s[5] == "Computer"), None)
        if not student:
            messagebox.showerror("Error", "Student not found or not from Computer department!")
            return
        
        # Validate book exists and is available
        book = next((b for b in self.db.get_books() if b[1] == book_id), None)
        if not book:
            messagebox.showerror("Error", "Book not found!")
            return
        
        if book[6] <= 0:  # Available copies
            messagebox.showerror("Error", "Book is not available for borrowing!")
            return
        
        success, message = self.db.borrow_book(enrollment_no, book_id, due_date)
        
        if success:
            messagebox.showinfo("Success", f"Book borrowed successfully!\n\nStudent: {student[2]}\nBook: {book[2]}\nDue Date: {due_date}")
            # Clear form
            self.borrow_enrollment_no.delete(0, tk.END)
            self.borrow_book_id.delete(0, tk.END)
            self.borrow_student_details.config(text="")
            self.borrow_book_details.config(text="")
            # Reset due date to 14 days from now
            self.due_date.delete(0, tk.END)
            default_due = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
            self.due_date.insert(0, default_due)
            self.refresh_all_data()
        else:
            messagebox.showerror("Error", message)
    
    def return_book(self):
        """Handle book returning with improved validation"""
        enrollment_no = self.return_enrollment_no.get().strip()
        book_id = self.return_book_id.get().strip()
        
        if not enrollment_no or not book_id:
            messagebox.showerror("Error", "Enrollment Number and Book ID are required!")
            return
        
        # Validate that the book is actually borrowed by this student
        borrowed_books = [b for b in self.db.get_borrowed_books() if b[0] == enrollment_no and b[4] == book_id]
        if not borrowed_books:
            messagebox.showerror("Error", "This book is not borrowed by this student!")
            return
        
        success, message = self.db.return_book(enrollment_no, book_id)
        
        if success:
            book_details = borrowed_books[0]
            messagebox.showinfo("Success", f"Book returned successfully!\n\nStudent: {book_details[1]}\nBook: {book_details[5]}\nBorrowed on: {book_details[7]}")
            # Clear form
            self.return_enrollment_no.delete(0, tk.END)
            self.return_book_id.delete(0, tk.END)
            self.return_details.config(text="")
            self.refresh_all_data()
        else:
            messagebox.showerror("Error", message)
    
    def import_students_excel(self):
        """Import students from Excel file"""
        file_path = filedialog.askopenfilename(
            title="Select Excel file to import students",
            filetypes=[("Excel files", "*.xlsx"), ("Excel files", "*.xls"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            # Show instructions dialog
            instruction_msg = (
                "≡ƒôï Excel Import Instructions:\n\n"
                "MANDATORY COLUMNS (required):\n"
                "ΓÇó enrollment_no (or Enrollment No) - REQUIRED Γ£ô\n"
                "ΓÇó name (or Name) - REQUIRED Γ£ô\n\n"
                "OPTIONAL COLUMNS:\n"
                "ΓÇó email (or Email)\n"
                "ΓÇó phone (or Phone)\n"
                "ΓÇó department (or Department)\n"
                "ΓÇó year (or Year)\n\n"
                "The first row should contain column headers.\n"
                "Do you want to continue?"
            )
            
            if not messagebox.askyesno("Import Instructions", instruction_msg):
                return
            
            # Read Excel file
            df = pd.read_excel(file_path, engine='openpyxl')
            
            # Normalize column names (handle different naming conventions)
            df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('no', 'no')
            
            # Map common column variations
            column_mapping = {
                'enrollment_no': 'enrollment_no',
                'enrollmentno': 'enrollment_no',
                'enrollment': 'enrollment_no',
                'roll_no': 'enrollment_no',
                'student_name': 'name',
                'full_name': 'name',
                'student_email': 'email',
                'email_id': 'email',
                'phone_number': 'phone',
                'mobile': 'phone',
                'contact': 'phone',
                'dept': 'department',
                'branch': 'department',
                'academic_year': 'year',
                'class': 'year'
            }
            
            # Apply column mapping
            for old_name, new_name in column_mapping.items():
                if old_name in df.columns:
                    df = df.rename(columns={old_name: new_name})
            
            # Check required columns
            required_columns = ['enrollment_no', 'name']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                messagebox.showerror(
                    "Missing Columns", 
                    f"Required columns missing: {', '.join(missing_columns)}\n\n"
                    f"Available columns: {', '.join(df.columns)}"
                )
                return
            
            # Process data
            success_count = 0
            error_count = 0
            error_details = []
            
            for index, row in df.iterrows():
                try:
                    enrollment_no = str(row.get('enrollment_no', '')).strip()
                    name = str(row.get('name', '')).strip()
                    email = str(row.get('email', '')).strip()
                    phone = str(row.get('phone', '')).strip()
                    department = str(row.get('department', 'Computer')).strip()
                    year = str(row.get('year', '1st Year')).strip()
                    
                    # Skip empty rows
                    if not enrollment_no or not name:
                        continue
                    
                    # Add student to database
                    success, message = self.db.add_student(
                        enrollment_no, name, email, phone, department, year
                    )
                    
                    if success:
                        success_count += 1
                    else:
                        error_count += 1
                        error_details.append(f"Row {index + 2}: {message}")
                        
                except Exception as e:
                    error_count += 1
                    error_details.append(f"Row {index + 2}: {str(e)}")
            
            # Refresh the students view
            self.refresh_students()
            
            # Show results
            result_msg = f"Γ£à Import completed!\n\n"
            result_msg += f"≡ƒôè Successfully imported: {success_count} students\n"
            
            if error_count > 0:
                result_msg += f"ΓÜá∩╕Å Errors encountered: {error_count}\n\n"
                if error_details:
                    result_msg += "Error details:\n" + "\n".join(error_details[:5])
                    if len(error_details) > 5:
                        result_msg += f"\n... and {len(error_details) - 5} more errors"
            
            messagebox.showinfo("Import Results", result_msg)
            
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import Excel file:\n\n{str(e)}")
    
    def import_books_excel(self):
        """Import books from Excel file"""
        file_path = filedialog.askopenfilename(
            title="Select Excel file to import books",
            filetypes=[("Excel files", "*.xlsx"), ("Excel files", "*.xls"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            # Show instructions dialog
            instruction_msg = (
                "≡ƒôï Excel Import Instructions:\n\n"
                "MANDATORY COLUMNS (required):\n"
                "ΓÇó book_id (or Book ID) - REQUIRED Γ£ô\n"
                "ΓÇó title (or Title) - REQUIRED Γ£ô\n\n"
                "OPTIONAL COLUMNS:\n"
                "ΓÇó author (or Author)\n"
                "ΓÇó isbn (or ISBN)\n"
                "ΓÇó category (or Category)\n"
                "ΓÇó total_copies (or Total Copies) - defaults to 1\n\n"
                "The first row should contain column headers.\n"
                "Do you want to continue?"
            )
            
            if not messagebox.askyesno("Import Instructions", instruction_msg):
                return
            
            # Read Excel file
            df = pd.read_excel(file_path, engine='openpyxl')
            
            # Normalize column names
            df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('no', 'no')
            
            # Map common column variations
            column_mapping = {
                'book_id': 'book_id',
                'bookid': 'book_id',
                'id': 'book_id',
                'book_title': 'title',
                'book_name': 'title',
                'book_author': 'author',
                'author_name': 'author',
                'isbn_no': 'isbn',
                'isbn_number': 'isbn',
                'book_category': 'category',
                'subject': 'category',
                'copies': 'total_copies',
                'quantity': 'total_copies',
                'no_of_copies': 'total_copies'
            }
            
            # Apply column mapping
            for old_name, new_name in column_mapping.items():
                if old_name in df.columns:
                    df = df.rename(columns={old_name: new_name})
            
            # Check required columns
            required_columns = ['book_id', 'title', 'author']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                messagebox.showerror(
                    "Missing Columns", 
                    f"Required columns missing: {', '.join(missing_columns)}\n\n"
                    f"Available columns: {', '.join(df.columns)}"
                )
                return
            
            # Process data
            success_count = 0
            error_count = 0
            error_details = []
            
            for index, row in df.iterrows():
                try:
                    book_id = str(row.get('book_id', '')).strip()
                    title = str(row.get('title', '')).strip()
                    author = str(row.get('author', '')).strip()
                    isbn = str(row.get('isbn', '')).strip()
                    category = str(row.get('category', 'Technology')).strip()
                    
                    # Handle total_copies
                    try:
                        total_copies = int(row.get('total_copies', 1))
                        if total_copies <= 0:
                            total_copies = 1
                    except (ValueError, TypeError):
                        total_copies = 1
                    
                    # Skip empty rows
                    if not book_id or not title or not author:
                        continue
                    
                    # Add book to database
                    success, message = self.db.add_book(
                        book_id, title, author, isbn, category, total_copies
                    )
                    
                    if success:
                        success_count += 1
                    else:
                        error_count += 1
                        error_details.append(f"Row {index + 2}: {message}")
                        
                except Exception as e:
                    error_count += 1
                    error_details.append(f"Row {index + 2}: {str(e)}")
            
            # Refresh the books view
            self.refresh_books()
            
            # Show results
            result_msg = f"Γ£à Import completed!\n\n"
            result_msg += f"≡ƒôè Successfully imported: {success_count} books\n"
            
            if error_count > 0:
                result_msg += f"ΓÜá∩╕Å Errors encountered: {error_count}\n\n"
                if error_details:
                    result_msg += "Error details:\n" + "\n".join(error_details[:5])
                    if len(error_details) > 5:
                        result_msg += f"\n... and {len(error_details) - 5} more errors"
            
            messagebox.showinfo("Import Results", result_msg)
            
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import Excel file:\n\n{str(e)}")
    
    def search_students(self):
        """Search students"""
        search_term = self.student_search_var.get()
        students = self.db.get_students(search_term)
        # Only show Computer department students
        filtered_students = [s for s in students if s[5] == "Computer"]
        self.populate_students_tree(filtered_students)
    
    def search_books(self):
        """Search books"""
        search_term = self.book_search_var.get()
        books = self.db.get_books(search_term)
        # Only show Computer department books (category Technology/Textbook/Research)
        filtered_books = [b for b in books if b[5] in ["Technology", "Textbook", "Research"]]
        self.populate_books_tree(filtered_books)
    
    def refresh_students(self):
        """Refresh students list"""
        students = self.db.get_students()
        # Only show Computer department students
        if hasattr(self, 'students_tree'):
            filtered_students = [s for s in students if s[5] == "Computer"]
            self.populate_students_tree(filtered_students)
    
    def refresh_books(self):
        """Refresh books list"""
        books = self.db.get_books()
        # Only show Computer department books (category Technology/Textbook/Research)
        if hasattr(self, 'books_tree'):
            filtered_books = [b for b in books if b[5] in ["Technology", "Textbook", "Research"]]
            self.populate_books_tree(filtered_books)
    
    def refresh_borrowed(self):
        """Refresh borrowed books list"""
        borrowed = self.db.get_borrowed_books()
        self.populate_borrowed_tree(borrowed)
    
    def refresh_all_data(self):
        """Refresh all data"""
        if hasattr(self, 'students_tree'):
            self.refresh_students()
        if hasattr(self, 'books_tree'):
            self.refresh_books()
        if hasattr(self, 'borrowed_tree'):
            self.refresh_borrowed()
    
    def populate_students_tree(self, students):
        """Populate students treeview"""
        if hasattr(self, 'students_tree'):
            for item in self.students_tree.get_children():
                self.students_tree.delete(item)
            
            for student in students:
                self.students_tree.insert('', 'end', values=student)
    
    def populate_books_tree(self, books):
        """Populate books treeview"""
        if hasattr(self, 'books_tree'):
            for item in self.books_tree.get_children():
                self.books_tree.delete(item)
            
            for book in books:
                self.books_tree.insert('', 'end', values=book)
    
    def populate_borrowed_tree(self, borrowed):
        """Populate borrowed books treeview"""
        if hasattr(self, 'borrowed_tree'):
            for item in self.borrowed_tree.get_children():
                self.borrowed_tree.delete(item)
            
            for record in borrowed:
                self.borrowed_tree.insert('', 'end', values=record)
    
    def show_student_context_menu(self, event):
        """Show context menu for students"""
        selection = self.students_tree.selection()
        if not selection:
            return
        
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="Delete Student", command=self.delete_selected_student)
        context_menu.add_command(label="Export Students", command=self.export_students)
        context_menu.add_command(label="Import Students", command=self.import_students)
        
        def export_students():
            import csv
            students = [s for s in self.db.get_students() if s[5] == "Computer"]
            with open("students_export.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Enrollment No", "Name", "Email", "Phone", "Department", "Year", "Date Registered"])
                writer.writerows(students)
            messagebox.showinfo("Export", "Students exported to students_export.csv")
        
        def import_students():
            import csv
            from tkinter import filedialog
            file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
            if not file_path:
                return
            with open(file_path, "r") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    self.db.add_student(*row[1:7])
            self.refresh_students()
            messagebox.showinfo("Import", "Students imported successfully.")
        
        # Bind the functions to the menu
        context_menu.entryconfig("Export Students", command=export_students)
        context_menu.entryconfig("Import Students", command=import_students)
            
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
    
    def show_book_context_menu(self, event):
        """Show context menu for books"""
        selection = self.books_tree.selection()
        if not selection:
            return
        
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="Delete Book", command=self.delete_selected_book)
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
    
    def delete_selected_student(self):
        """Delete selected student"""
        selection = self.students_tree.selection()
        if not selection:
            return
        
        item = self.students_tree.item(selection[0])
        enrollment_no = item['values'][1]  # Enrollment No is in column 1
        
        if messagebox.askyesno("Confirm", f"Delete student {enrollment_no}?"):
            success, message = self.db.delete_student(enrollment_no)
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_students()
            else:
                messagebox.showerror("Error", message)
    
    def delete_selected_book(self):
        """Delete selected book"""
        selection = self.books_tree.selection()
        if not selection:
            return
        
        item = self.books_tree.item(selection[0])
        book_id = item['values'][1]  # Book ID is in column 1
        
        if messagebox.askyesno("Confirm", f"Delete book {book_id}?"):
            success, message = self.db.delete_book(book_id)
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_books()
            else:
                messagebox.showerror("Error", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementApp(root)
    root.mainloop()
