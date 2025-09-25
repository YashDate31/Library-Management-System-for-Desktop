import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from database import Database
import base64

class LibraryManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Academic Library Management System")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f8f9fa')
        
        # Initialize database
        self.db = Database()
        
        # Create main frame
        self.main_frame = tk.Frame(root, bg='#f8f9fa')
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
        """Create enhanced application header with logo"""
        header_frame = tk.Frame(self.main_frame, bg='#2c3e50', height=100)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        header_frame.pack_propagate(False)
        
        # Logo and title container
        logo_title_frame = tk.Frame(header_frame, bg='#2c3e50')
        logo_title_frame.pack(expand=True, fill=tk.BOTH)
        
        # Create logo (using text-based logo for simplicity)
        logo_frame = tk.Frame(logo_title_frame, bg='#3498db', width=80, height=80)
        logo_frame.pack(side=tk.LEFT, padx=20, pady=10)
        logo_frame.pack_propagate(False)
        
        # Logo text
        logo_label = tk.Label(
            logo_frame,
            text="📚\nLMS",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#3498db',
            justify=tk.CENTER
        )
        logo_label.pack(expand=True)
        
        # Title and subtitle
        title_frame = tk.Frame(logo_title_frame, bg='#2c3e50')
        title_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10)
        
        title_label = tk.Label(
            title_frame, 
            text="Academic Library Management System", 
            font=('Arial', 28, 'bold'),
            fg='white', 
            bg='#2c3e50'
        )
        title_label.pack(anchor='w', pady=(15, 0))
        
        subtitle_label = tk.Label(
            title_frame, 
            text="Streamlined Student & Book Management Solution", 
            font=('Arial', 12),
            fg='#ecf0f1', 
            bg='#2c3e50'
        )
        subtitle_label.pack(anchor='w')
        
        # Current date/time
        datetime_label = tk.Label(
            logo_title_frame,
            text=datetime.now().strftime("%B %d, %Y\n%I:%M %p"),
            font=('Arial', 11),
            fg='#bdc3c7',
            bg='#2c3e50',
            justify=tk.CENTER
        )
        datetime_label.pack(side=tk.RIGHT, padx=20, pady=10)
    
    def create_navigation_bar(self):
        """Create professional navigation bar"""
        nav_frame = tk.Frame(self.main_frame, bg='#34495e', height=50)
        nav_frame.pack(fill=tk.X, pady=(0, 15))
        nav_frame.pack_propagate(False)
        
        # Navigation buttons
        nav_buttons = [
            ("🏠 Dashboard", self.show_dashboard, '#e74c3c'),
            ("👥 Students", self.show_students, '#27ae60'),
            ("📚 Books", self.show_books, '#3498db'),
            ("📋 Transactions", self.show_transactions, '#f39c12'),
            ("📊 Reports", self.show_reports, '#9b59b6')
        ]
        
        for text, command, color in nav_buttons:
            btn = tk.Button(
                nav_frame,
                text=text,
                command=command,
                bg=color,
                fg='white',
                font=('Arial', 11, 'bold'),
                bd=0,
                padx=20,
                pady=10,
                cursor='hand2'
            )
            btn.pack(side=tk.LEFT, padx=2, pady=5)
    
    def create_content_area(self):
        """Create main content area"""
        self.content_frame = tk.Frame(self.main_frame, bg='#f8f9fa')
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
    
    def show_books(self):
        """Show books view"""
        if self.current_view == 'books':
            return
        self.current_view = 'books'
        self.clear_content()
        self.create_books_view()
    
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
        """Create dashboard view"""
        # Title
        title_frame = tk.Frame(self.content_frame, bg='#f8f9fa')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            title_frame, 
            text="📊 Library Dashboard", 
            font=('Arial', 20, 'bold'),
            bg='#f8f9fa',
            fg='#2c3e50'
        ).pack(side=tk.LEFT)
        
        # Stats cards
        stats_frame = tk.Frame(self.content_frame, bg='#f8f9fa')
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Get statistics
        students = self.db.get_students()
        books = self.db.get_books()
        borrowed = self.db.get_borrowed_books()
        
        stats = [
            ("Total Students", len(students), '#27ae60'),
            ("Total Books", len(books), '#3498db'),
            ("Books Borrowed", len(borrowed), '#e74c3c'),
            ("Available Books", sum(book[6] for book in books), '#f39c12')
        ]
        
        for title, value, color in stats:
            card = tk.Frame(stats_frame, bg=color, width=200, height=100)
            card.pack(side=tk.LEFT, padx=10, fill=tk.Y)
            card.pack_propagate(False)
            
            tk.Label(card, text=str(value), font=('Arial', 24, 'bold'), fg='white', bg=color).pack(expand=True)
            tk.Label(card, text=title, font=('Arial', 12), fg='white', bg=color).pack()
        
        # Currently borrowed books
        tk.Label(
            self.content_frame, 
            text="� Currently Borrowed Books", 
            font=('Arial', 16, 'bold'),
            bg='#f8f9fa',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(20, 10))
        
        # Borrowed books list
        list_frame = tk.Frame(self.content_frame, bg='white', relief=tk.RIDGE, bd=1)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('Enrollment No', 'Student Name', 'Dept', 'Year', 'Book ID', 'Title', 'Author', 'Borrow Date', 'Due Date')
        self.borrowed_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.borrowed_tree.heading(col, text=col)
            self.borrowed_tree.column(col, width=120)
        
        # Scrollbar
        borrowed_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.borrowed_tree.yview)
        self.borrowed_tree.configure(yscrollcommand=borrowed_scroll.set)
        
        self.borrowed_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        borrowed_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        self.refresh_borrowed()
    
    def create_students_view(self):
        """Create students management view"""
        # Title and controls
        title_frame = tk.Frame(self.content_frame, bg='#f8f9fa')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            title_frame, 
            text="👥 Student Management", 
            font=('Arial', 20, 'bold'),
            bg='#f8f9fa',
            fg='#2c3e50'
        ).pack(side=tk.LEFT)
        
        # Controls frame
        controls_frame = tk.Frame(self.content_frame, bg='white', relief=tk.RIDGE, bd=1)
        controls_frame.pack(fill=tk.X, padx=0, pady=(0, 10))
        
        # Search and add
        search_frame = tk.Frame(controls_frame, bg='white')
        search_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(search_frame, text="🔍 Search Students:", font=('Arial', 12, 'bold'), bg='white').pack(side=tk.LEFT)
        self.student_search_var = tk.StringVar()
        self.student_search_var.trace('w', lambda *args: self.search_students())
        search_entry = tk.Entry(search_frame, textvariable=self.student_search_var, width=40, font=('Arial', 11))
        search_entry.pack(side=tk.LEFT, padx=(10, 0))
        
        add_btn = tk.Button(
            search_frame, 
            text="➕ Add New Student", 
            command=self.show_add_student_dialog,
            bg='#27ae60', 
            fg='white', 
            font=('Arial', 11, 'bold'),
            padx=20,
            cursor='hand2'
        )
        add_btn.pack(side=tk.RIGHT, padx=10)
        
        # Students list
        list_frame = tk.Frame(self.content_frame, bg='white', relief=tk.RIDGE, bd=1)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Enrollment No', 'Name', 'Email', 'Phone', 'Department', 'Year', 'Date Registered')
        self.students_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=18)
        
        for col in columns:
            self.students_tree.heading(col, text=col)
            self.students_tree.column(col, width=140)
        
        students_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.students_tree.yview)
        self.students_tree.configure(yscrollcommand=students_scroll.set)
        
        self.students_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        students_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        self.students_tree.bind("<Button-3>", self.show_student_context_menu)
        self.refresh_students()
    
    def create_books_tab(self):
        """Create books management tab"""
        books_frame = ttk.Frame(self.notebook)
        self.notebook.add(books_frame, text="📖 Books")
        
        # Top frame for controls
        controls_frame = tk.Frame(books_frame, bg='white', relief=tk.RIDGE, bd=1)
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Search frame
        search_frame = tk.Frame(controls_frame, bg='white')
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(search_frame, text="Search Books:", font=('Arial', 10, 'bold'), bg='white').pack(side=tk.LEFT)
        self.book_search_var = tk.StringVar()
        self.book_search_var.trace('w', lambda *args: self.search_books())
        search_entry = tk.Entry(search_frame, textvariable=self.book_search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=(10, 0))
        
        # Add book button
        add_btn = tk.Button(
            search_frame, 
            text="➕ Add New Book", 
            command=self.show_add_book_dialog,
            bg='#3498db', 
            fg='white', 
            font=('Arial', 9, 'bold')
        )
        add_btn.pack(side=tk.RIGHT, padx=10)
        
        # Books list
        list_frame = tk.Frame(books_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview for books
        columns = ('ID', 'Book ID', 'Title', 'Author', 'Category', 'Total', 'Available')
        self.books_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.books_tree.heading(col, text=col)
            self.books_tree.column(col, width=150)
        
        # Scrollbar
        books_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.books_tree.yview)
        self.books_tree.configure(yscrollcommand=books_scroll.set)
        
        self.books_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        books_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Context menu for books
        self.books_tree.bind("<Button-3>", self.show_book_context_menu)
    
    def create_borrow_tab(self):
        """Create borrowing/returning tab"""
        borrow_frame = ttk.Frame(self.notebook)
        self.notebook.add(borrow_frame, text="📋 Borrow/Return")
        
        # Split into two sections
        paned = ttk.PanedWindow(borrow_frame, orient=tk.VERTICAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Borrow section
        borrow_section = tk.Frame(paned, bg='white', relief=tk.RIDGE, bd=1)
        paned.add(borrow_section, weight=1)
        
        tk.Label(borrow_section, text="📤 Borrow Book", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        borrow_form = tk.Frame(borrow_section, bg='white')
        borrow_form.pack(padx=20, pady=10)
        
        # Borrow form fields
        tk.Label(borrow_form, text="Student ID:", bg='white').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.borrow_student_id = tk.Entry(borrow_form, width=20)
        self.borrow_student_id.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(borrow_form, text="Book ID:", bg='white').grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.borrow_book_id = tk.Entry(borrow_form, width=20)
        self.borrow_book_id.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(borrow_form, text="Due Date:", bg='white').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.due_date = tk.Entry(borrow_form, width=20)
        self.due_date.grid(row=1, column=1, padx=5, pady=5)
        
        # Set default due date (14 days from now)
        default_due = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        self.due_date.insert(0, default_due)
        
        borrow_btn = tk.Button(
            borrow_form, 
            text="📤 Borrow Book", 
            command=self.borrow_book,
            bg='#e74c3c', 
            fg='white', 
            font=('Arial', 10, 'bold')
        )
        borrow_btn.grid(row=1, column=2, columnspan=2, padx=20, pady=10)
        
        # Return section
        return_section = tk.Frame(paned, bg='white', relief=tk.RIDGE, bd=1)
        paned.add(return_section, weight=1)
        
        tk.Label(return_section, text="📥 Return Book", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        return_form = tk.Frame(return_section, bg='white')
        return_form.pack(padx=20, pady=10)
        
        # Return form fields
        tk.Label(return_form, text="Student ID:", bg='white').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.return_student_id = tk.Entry(return_form, width=20)
        self.return_student_id.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(return_form, text="Book ID:", bg='white').grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.return_book_id = tk.Entry(return_form, width=20)
        self.return_book_id.grid(row=0, column=3, padx=5, pady=5)
        
        return_btn = tk.Button(
            return_form, 
            text="📥 Return Book", 
            command=self.return_book,
            bg='#27ae60', 
            fg='white', 
            font=('Arial', 10, 'bold')
        )
        return_btn.grid(row=0, column=4, padx=20, pady=10)
    
    def create_dashboard_tab(self):
        """Create dashboard tab"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        # Title
        tk.Label(
            dashboard_frame, 
            text="📊 Currently Borrowed Books", 
            font=('Arial', 16, 'bold')
        ).pack(pady=10)
        
        # Borrowed books list
        list_frame = tk.Frame(dashboard_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('Student ID', 'Student Name', 'Book ID', 'Title', 'Author', 'Borrow Date', 'Due Date')
        self.borrowed_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.borrowed_tree.heading(col, text=col)
            self.borrowed_tree.column(col, width=150)
        
        # Scrollbar
        borrowed_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.borrowed_tree.yview)
        self.borrowed_tree.configure(yscrollcommand=borrowed_scroll.set)
        
        self.borrowed_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        borrowed_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Refresh button
        refresh_btn = tk.Button(
            dashboard_frame, 
            text="🔄 Refresh", 
            command=self.refresh_all_data,
            bg='#9b59b6', 
            fg='white', 
            font=('Arial', 10, 'bold')
        )
        refresh_btn.pack(pady=10)
    
    def show_add_student_dialog(self):
        """Show add student dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Student")
        dialog.geometry("500x450")
        dialog.resizable(False, False)
        dialog.configure(bg='white')
        
        # Center the dialog
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog on screen
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (450 // 2)
        dialog.geometry(f"500x450+{x}+{y}")
        
        # Form fields
        tk.Label(dialog, text="👤 Add New Student", font=('Arial', 16, 'bold'), bg='white', fg='#2c3e50').pack(pady=15)
        
        form_frame = tk.Frame(dialog, bg='white')
        form_frame.pack(padx=30, pady=20)
        
        # Enrollment Number
        tk.Label(form_frame, text="Enrollment No:", bg='white', font=('Arial', 11, 'bold')).grid(row=0, column=0, sticky='w', pady=8)
        enrollment_entry = tk.Entry(form_frame, width=35, font=('Arial', 11))
        enrollment_entry.grid(row=0, column=1, pady=8, padx=(15, 0))
        
        # Name
        tk.Label(form_frame, text="Full Name:", bg='white', font=('Arial', 11, 'bold')).grid(row=1, column=0, sticky='w', pady=8)
        name_entry = tk.Entry(form_frame, width=35, font=('Arial', 11))
        name_entry.grid(row=1, column=1, pady=8, padx=(15, 0))
        
        # Email
        tk.Label(form_frame, text="Email:", bg='white', font=('Arial', 11, 'bold')).grid(row=2, column=0, sticky='w', pady=8)
        email_entry = tk.Entry(form_frame, width=35, font=('Arial', 11))
        email_entry.grid(row=2, column=1, pady=8, padx=(15, 0))
        
        # Phone
        tk.Label(form_frame, text="Phone:", bg='white', font=('Arial', 11, 'bold')).grid(row=3, column=0, sticky='w', pady=8)
        phone_entry = tk.Entry(form_frame, width=35, font=('Arial', 11))
        phone_entry.grid(row=3, column=1, pady=8, padx=(15, 0))
        
        # Department
        tk.Label(form_frame, text="Department:", bg='white', font=('Arial', 11, 'bold')).grid(row=4, column=0, sticky='w', pady=8)
        department_entry = ttk.Combobox(form_frame, width=33, font=('Arial', 11), values=[
            "Computer Science", "Information Technology", "Electronics", "Mechanical", 
            "Civil", "Electrical", "Chemical", "Biotechnology", "Mathematics", "Physics", 
            "Chemistry", "English", "Business Administration", "Other"
        ])
        department_entry.grid(row=4, column=1, pady=8, padx=(15, 0))
        
        # Year
        tk.Label(form_frame, text="Academic Year:", bg='white', font=('Arial', 11, 'bold')).grid(row=5, column=0, sticky='w', pady=8)
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
                self.refresh_students()
            else:
                messagebox.showerror("Error", message)
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg='white')
        btn_frame.pack(pady=30, side=tk.BOTTOM)
        
        save_btn = tk.Button(btn_frame, text="💾 Save Student", command=save_student, bg='#27ae60', fg='white', width=15, height=2, font=('Arial', 11, 'bold'))
        save_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = tk.Button(btn_frame, text="❌ Cancel", command=dialog.destroy, bg='#e74c3c', fg='white', width=15, height=2, font=('Arial', 11, 'bold'))
        cancel_btn.pack(side=tk.LEFT, padx=10)
    
    def show_add_book_dialog(self):
        """Show add book dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Book")
        dialog.geometry("450x450")
        dialog.resizable(False, False)
        dialog.configure(bg='white')
        
        # Center the dialog
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog on screen
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (450 // 2)
        dialog.geometry(f"450x450+{x}+{y}")
        
        # Form fields
        tk.Label(dialog, text="Add New Book", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        form_frame = tk.Frame(dialog, bg='white')
        form_frame.pack(padx=20, pady=20)
        
        tk.Label(form_frame, text="Book ID:", bg='white').grid(row=0, column=0, sticky='w', pady=5)
        book_id_entry = tk.Entry(form_frame, width=30)
        book_id_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        tk.Label(form_frame, text="Title:", bg='white').grid(row=1, column=0, sticky='w', pady=5)
        title_entry = tk.Entry(form_frame, width=30)
        title_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        tk.Label(form_frame, text="Author:", bg='white').grid(row=2, column=0, sticky='w', pady=5)
        author_entry = tk.Entry(form_frame, width=30)
        author_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        tk.Label(form_frame, text="ISBN:", bg='white').grid(row=3, column=0, sticky='w', pady=5)
        isbn_entry = tk.Entry(form_frame, width=30)
        isbn_entry.grid(row=3, column=1, pady=5, padx=(10, 0))
        
        tk.Label(form_frame, text="Category:", bg='white').grid(row=4, column=0, sticky='w', pady=5)
        category_entry = tk.Entry(form_frame, width=30)
        category_entry.grid(row=4, column=1, pady=5, padx=(10, 0))
        
        tk.Label(form_frame, text="Total Copies:", bg='white').grid(row=5, column=0, sticky='w', pady=5)
        copies_entry = tk.Entry(form_frame, width=30)
        copies_entry.grid(row=5, column=1, pady=5, padx=(10, 0))
        copies_entry.insert(0, "1")
        
        def save_book():
            if not book_id_entry.get() or not title_entry.get() or not author_entry.get():
                messagebox.showerror("Error", "Book ID, Title and Author are required!")
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
                self.refresh_books()
            else:
                messagebox.showerror("Error", message)
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg='white')
        btn_frame.pack(pady=30, side=tk.BOTTOM)
        
        save_btn = tk.Button(btn_frame, text="💾 Save", command=save_book, bg='#3498db', fg='white', width=12, height=2, font=('Arial', 10, 'bold'))
        save_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = tk.Button(btn_frame, text="❌ Cancel", command=dialog.destroy, bg='#e74c3c', fg='white', width=12, height=2, font=('Arial', 10, 'bold'))
        cancel_btn.pack(side=tk.LEFT, padx=10)
    
    def borrow_book(self):
        """Handle book borrowing"""
        student_id = self.borrow_student_id.get()
        book_id = self.borrow_book_id.get()
        due_date = self.due_date.get()
        
        if not student_id or not book_id or not due_date:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        success, message = self.db.borrow_book(student_id, book_id, due_date)
        
        if success:
            messagebox.showinfo("Success", message)
            self.borrow_student_id.delete(0, tk.END)
            self.borrow_book_id.delete(0, tk.END)
            # Reset due date to 14 days from now
            self.due_date.delete(0, tk.END)
            default_due = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
            self.due_date.insert(0, default_due)
            self.refresh_all_data()
        else:
            messagebox.showerror("Error", message)
    
    def return_book(self):
        """Handle book returning"""
        student_id = self.return_student_id.get()
        book_id = self.return_book_id.get()
        
        if not student_id or not book_id:
            messagebox.showerror("Error", "Student ID and Book ID are required!")
            return
        
        success, message = self.db.return_book(student_id, book_id)
        
        if success:
            messagebox.showinfo("Success", message)
            self.return_student_id.delete(0, tk.END)
            self.return_book_id.delete(0, tk.END)
            self.refresh_all_data()
        else:
            messagebox.showerror("Error", message)
    
    def search_students(self):
        """Search students"""
        search_term = self.student_search_var.get()
        students = self.db.get_students(search_term)
        self.populate_students_tree(students)
    
    def search_books(self):
        """Search books"""
        search_term = self.book_search_var.get()
        books = self.db.get_books(search_term)
        self.populate_books_tree(books)
    
    def refresh_students(self):
        """Refresh students list"""
        students = self.db.get_students()
        self.populate_students_tree(students)
    
    def refresh_books(self):
        """Refresh books list"""
        books = self.db.get_books()
        self.populate_books_tree(books)
    
    def refresh_borrowed(self):
        """Refresh borrowed books list"""
        borrowed = self.db.get_borrowed_books()
        self.populate_borrowed_tree(borrowed)
    
    def refresh_all_data(self):
        """Refresh all data"""
        self.refresh_students()
        self.refresh_books()
        self.refresh_borrowed()
    
    def populate_students_tree(self, students):
        """Populate students treeview"""
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        for student in students:
            self.students_tree.insert('', 'end', values=student)
    
    def populate_books_tree(self, books):
        """Populate books treeview"""
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        
        for book in books:
            self.books_tree.insert('', 'end', values=book)
    
    def populate_borrowed_tree(self, borrowed):
        """Populate borrowed books treeview"""
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
        student_id = item['values'][1]  # Student ID is in column 1
        
        if messagebox.askyesno("Confirm", f"Delete student {student_id}?"):
            success, message = self.db.delete_student(student_id)
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