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
from io import BytesIO

# Optional: Word export support
try:
    from docx import Document
    from docx.shared import Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
except Exception:
    Document = None

# Calendar date picker support
try:
    from tkcalendar import DateEntry
except Exception:
    DateEntry = None

# Matplotlib for charts and analysis
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except Exception:
    MATPLOTLIB_AVAILABLE = False
    print("matplotlib not available - Analysis tab will show installation prompt")

# Advanced Excel export support
try:
    import xlsxwriter
    XLSXWRITER_AVAILABLE = True
except Exception:
    XLSXWRITER_AVAILABLE = False

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
        # Set window title (remove version as requested)
        self.root.title("📚 Library of Computer Department")
        self.root.geometry("1400x900")
        self.root.state('zoomed')  # Maximize window
        
        # Professional light color scheme (3 colors) - IMPROVED
        self.colors = {
            'primary': '#ffffff',      # Pure white (backgrounds)
            'secondary': '#2E86AB',    # Professional blue (buttons, accents)
            'accent': '#0F3460',       # Dark blue (text, headers)
            'text': '#333333'          # Dark gray text
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
        """Render the login screen with college branding"""
        for w in self.root.winfo_children():
            w.destroy()

        root = self.root
        root.configure(bg=self.colors['primary'])

        wrapper = tk.Frame(root, bg=self.colors['primary'])
        wrapper.pack(fill=tk.BOTH, expand=True)

        # Small top spacer so content is nearer the top-middle
        tk.Frame(wrapper, height=40, bg=self.colors['primary']).pack(fill=tk.X)

        # Top branding area: logo + titles
        branding = tk.Frame(wrapper, bg=self.colors['primary'])
        branding.pack(pady=(0, 10))

        # Logo (reuse same file as main header if present).
        # When running as EXE, images are in the PyInstaller temp dir (sys._MEIPASS).
        logo_path = None
        try:
            from PIL import Image, ImageTk
            if hasattr(sys, '_MEIPASS'):
                base_dir = sys._MEIPASS
            else:
                base_dir = os.path.dirname(__file__)
            for candidate in ("logo.png", "college_logo.png", "college_logo.jpg"):
                p = os.path.join(base_dir, candidate)
                if os.path.exists(p):
                    logo_path = p
                    break
            if logo_path:
                img = Image.open(logo_path)
                img.thumbnail((96, 96), Image.Resampling.LANCZOS)
                self.login_logo_photo = ImageTk.PhotoImage(img)
                tk.Label(branding, image=self.login_logo_photo, bg=self.colors['primary']).pack(pady=(0, 8))
            else:
                raise FileNotFoundError
        except Exception:
            tk.Label(
                branding,
                text="📚",
                font=('Segoe UI', 40, 'bold'),
                bg=self.colors['primary'],
                fg=self.colors['secondary']
            ).pack(pady=(0, 8))

        # College name (big title)
        tk.Label(
            branding,
            text="Government Polytechnic Awasari (Kh)",
            font=('Segoe UI', 24, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent']
        ).pack()

        # Department / app name (subtitle)
        tk.Label(
            branding,
            text="Library of Computer Department",
            font=('Segoe UI', 14),
            bg=self.colors['primary'],
            fg='#666666'
        ).pack(pady=(6, 0))

        # Login card with subtle shadow
        card_outer = tk.Frame(wrapper, bg=self.colors['primary'])
        card_outer.pack(pady=(16, 0))

        shadow = tk.Frame(card_outer, bg='#d0d7e2')
        shadow.pack(padx=2, pady=2)

        card = tk.Frame(shadow, bg='#3a5373', bd=0, relief='flat', padx=50, pady=36)
        card.pack()

        tk.Label(card, text="Admin Login", font=('Segoe UI', 20, 'bold'), bg='#3a5373', fg='white').pack(pady=(0,14))

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
            # If entries no longer exist (e.g., after login), ignore
            try:
                if not (user_entry.winfo_exists() and pass_entry.winfo_exists()):
                    return 'break'
            except Exception:
                return 'break'
            do_login()
            return 'break'  # Stop propagation (avoid duplicate triggers)
        # Bind to the login card so it's automatically cleaned up when the login UI is destroyed
        card.bind('<Return>', handle_enter)
        user_entry.focus()
    
    def create_main_interface(self):
        """Create the main application interface"""
        # Remove any leftover global key bindings from the login screen
        try:
            self.root.unbind('<Return>')
        except Exception:
            pass
        # Clear root
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['primary'])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.create_header(main_container)
        
        # Create notebook for tabs with larger tab sizes
        self.notebook = ttk.Notebook(main_container)
        
        # Configure notebook style for larger tabs
        style = ttk.Style()
        style.configure('TNotebook.Tab', 
                       padding=[20, 12],  # Increased padding for larger tabs
                       font=('Segoe UI', 11, 'bold'))  # Larger font
        
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 20))
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_students_tab()
        self.create_books_tab()
        self.create_transactions_tab()
        self.create_records_tab()  # New records tab
        self.create_analysis_tab()  # New analysis tab with charts
        
        # Set focus to dashboard
        self.notebook.select(0)
        
        # Initial data load
        self.refresh_all_data()
    
    def create_header(self, parent):
        """Create application header"""
        # Slightly taller header to avoid any text clipping
        header_frame = tk.Frame(parent, bg=self.colors['secondary'], height=120)
        header_frame.pack(fill=tk.X, padx=0, pady=(0, 0))
        header_frame.pack_propagate(False)

        # Add subtle shadow effect
        shadow_frame = tk.Frame(parent, bg='#d1d1d1', height=2)
        shadow_frame.pack(fill=tk.X, padx=15)

        # Logo and title container
        logo_title_frame = tk.Frame(header_frame, bg=self.colors['secondary'])
        # Reduce vertical padding so content fits comfortably
        logo_title_frame.pack(expand=True, fill=tk.BOTH, padx=25, pady=10)
        # Use grid inside this frame for precise alignment (logo | title | actions)
        logo_title_frame.grid_columnconfigure(0, weight=0)
        logo_title_frame.grid_columnconfigure(1, weight=1)
        logo_title_frame.grid_columnconfigure(2, weight=0)
        logo_title_frame.grid_rowconfigure(0, weight=1)

        # Logo - Proper size
        logo_frame = tk.Frame(logo_title_frame, bg='white', width=80, height=80)
        logo_frame.grid(row=0, column=0, sticky='w', padx=(0, 20))
        logo_frame.pack_propagate(False)

        # Try to load college logo image, fallback to emoji
        try:
            from PIL import Image, ImageTk
            import os
            # First check for logo.png, then college_logo.png, then college_logo.jpg
            logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
            if not os.path.exists(logo_path):
                logo_path = os.path.join(os.path.dirname(__file__), 'college_logo.png')
            if not os.path.exists(logo_path):
                logo_path = os.path.join(os.path.dirname(__file__), 'college_logo.jpg')

            if os.path.exists(logo_path):
                # Load original image and preserve its rectangular aspect ratio
                img = Image.open(logo_path)
                # Fit within 78x78 box while maintaining aspect ratio
                max_size = (78, 78)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(img)

                logo_label = tk.Label(
                    logo_frame,
                    image=self.logo_photo,
                    bg='white'
                )
            else:
                raise FileNotFoundError("Logo file not found")
        except Exception:
            # Fallback to emoji if image loading fails
            logo_label = tk.Label(
                logo_frame,
                text="📚",
                font=('Segoe UI', 32, 'bold'),
                bg='white',
                fg=self.colors['secondary'],
                justify='center'
            )
        logo_label.pack(expand=True)

        # Title - Single line header with proper spacing
        title_frame = tk.Frame(logo_title_frame, bg=self.colors['secondary'])
        title_frame.grid(row=0, column=1, sticky='nsew')
        # Center the title vertically in its cell
        title_frame.grid_rowconfigure(0, weight=1)
        title_frame.grid_columnconfigure(0, weight=1)

        # Get current active academic year
        active_year = self.db.get_active_academic_year()
        if not active_year:
            active_year = "2025-2026"  # Default fallback
        
        # Convert format from "2025-2026" to "25-26"
        if "-" in active_year:
            years = active_year.split("-")
            if len(years) == 2:
                # Extract last 2 digits of each year
                year1 = years[0][-2:]  # "2025" -> "25"
                year2 = years[1][-2:]  # "2026" -> "26"
                display_year = f"{year1}-{year2}"
            else:
                display_year = active_year
        else:
            display_year = active_year
        
        # Title with academic year - GPA'S Library of Computer Department
        main_title_label = tk.Label(
            title_frame,
            text=f"GPA'S Library of Computer Department",
            font=('Segoe UI', 26, 'bold'),  # Increased from 22 to 26
            bg=self.colors['secondary'],
            fg='white',
            anchor='w'
        )
        # Use grid so it vertically centers without extra padding
        main_title_label.grid(row=0, column=0, sticky='w', padx=(0, 0), pady=0)
        
        # Academic year label (smaller size) - store as instance variable for updates
        self.academic_year_label = tk.Label(
            title_frame,
            text=f"Academic Year: {display_year}",
            font=('Segoe UI', 16, 'bold'),  # Decreased from 22 to 16
            bg=self.colors['secondary'],
            fg='#FFD700',  # Gold color for emphasis
            anchor='w'
        )
        self.academic_year_label.grid(row=1, column=0, sticky='w', padx=(0, 0), pady=(5, 0))

        # User info
        user_frame = tk.Frame(logo_title_frame, bg=self.colors['secondary'])
        user_frame.grid(row=0, column=2, sticky='e', padx=(25, 0))
        
        # Top-right row: Developer label + inline Promote link
        user_top_row = tk.Frame(user_frame, bg=self.colors['secondary'])
        user_top_row.pack(anchor='e', pady=(18, 2))
        user_label = tk.Label(
            user_top_row,
            text="👨‍💻 Developer",
            font=('Segoe UI', 13, 'bold'),
            bg=self.colors['secondary'],
            fg='white',
            cursor='hand2'
        )
        user_label.pack(side=tk.LEFT)
        user_label.bind('<Button-1>', lambda e: self.show_developer_info())
        promote_btn_hdr = tk.Button(
            user_top_row,
            text="⬆️ Promote Student Years…",
            font=('Segoe UI', 10, 'bold'),
            bg='#0d6efd',
            fg='white',
            relief='flat',
            padx=10,
            pady=2,
            cursor='hand2',
            activebackground='#0b5ed7',
            activeforeground='white',
            command=self._prompt_and_promote
        )
        promote_btn_hdr.pack(side=tk.LEFT, padx=(10, 0))
        # Removed version label and duplicate Developer Info button as requested

    # Removed "Clear All Data" button from header as requested
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
        """Clear all demo/user data with a confirmation prompt."""
        if not messagebox.askyesno("Confirm", "Remove ALL students, books and records? This cannot be undone."):
            return
        ok, msg = self.db.clear_all_data()
        if ok:
            messagebox.showinfo("Done", msg)
            self.refresh_all_data()
        else:
            messagebox.showerror("Error", msg)

    def _prompt_and_promote(self):
        """Prompt for password and, if correct, promote student years.
        Required password: gpa123
        """
        from tkinter import simpledialog
        pwd = simpledialog.askstring("Authentication Required", "Enter password to promote students:", show='*')
        if pwd is None:
            return
        if pwd.strip() != 'gpa123':
            messagebox.showerror("Access Denied", "Incorrect password. Promotion aborted.")
            return
        self.promote_student_years()

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
        
        # Current Issued Books (Dashboard Table)
        borrowed_frame = tk.LabelFrame(
            dashboard_frame,
            text="📋 Currently Issued Books",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent'],
            padx=10,
            pady=10
        )
        borrowed_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        columns = ('Enrollment No', 'Student Name', 'Book ID', 'Book Name', 'Issue Date', 'Due Date', 'Days Left')
        self.dashboard_borrowed_tree = ttk.Treeview(borrowed_frame, columns=columns, show='headings', height=12)
        for col in columns:
            self.dashboard_borrowed_tree.heading(col, text=col)
            self.dashboard_borrowed_tree.column(col, width=120 if col in ['Enrollment No', 'Book ID', 'Issue Date', 'Due Date', 'Days Left'] else 200)

        v_scrollbar = ttk.Scrollbar(borrowed_frame, orient=tk.VERTICAL, command=self.dashboard_borrowed_tree.yview)
        h_scrollbar = ttk.Scrollbar(borrowed_frame, orient=tk.HORIZONTAL, command=self.dashboard_borrowed_tree.xview)
        self.dashboard_borrowed_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        self.dashboard_borrowed_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Populate dashboard issued books
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
            ("📖 Issued Books", stats['borrowed_books'], '#ffc107'),
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
        # Live search while typing
        search_entry.bind('<KeyRelease>', lambda e: self.search_students())
        
        tk.Label(search_controls, text="Year:", bg=self.colors['primary'], fg=self.colors['accent'], font=('Segoe UI', 10)).pack(side=tk.LEFT)
        # Include 'Pass Out' instead of '4th' for final year
        year_combo = ttk.Combobox(search_controls, textvariable=self.student_year_filter, values=["All", "1st", "2nd", "3rd", "Pass Out"], state="readonly", width=10)
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
        # Live book search while typing
        book_search_entry.bind('<KeyRelease>', lambda e: self.search_books())
        
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

        # Mouse wheel scrolling (Windows/Linux) with Shift for horizontal
        def _tx_units(delta):
            return -1 if delta > 0 else (1 if delta < 0 else 0)
        # Handlers when bound directly to the scrollable canvas/main container
        def _tx_vwheel(event):
            u = _tx_units(event.delta)
            if u:
                canvas.yview_scroll(u, 'units')
            return 'break'
        def _tx_hwheel(event):
            u = _tx_units(event.delta)
            if u:
                canvas.xview_scroll(u, 'units')
            return 'break'
        # Child-binding variants: scroll page but don't cancel widget defaults
        def _tx_vwheel_child(event):
            u = _tx_units(getattr(event, 'delta', 0))
            if u:
                canvas.yview_scroll(u, 'units')
            # no return => allow widget default if any
        def _tx_hwheel_child(event):
            u = _tx_units(getattr(event, 'delta', 0))
            if u:
                canvas.xview_scroll(u, 'units')
            # no return => allow widget default if any
        canvas.bind('<MouseWheel>', _tx_vwheel)
        canvas.bind('<Shift-MouseWheel>', _tx_hwheel)
        main_container.bind('<MouseWheel>', _tx_vwheel)
        main_container.bind('<Shift-MouseWheel>', _tx_hwheel)
        # Pointer-scoped global binds while cursor is over the Transactions tab
        def _enter_tx(_e=None):
            try:
                transactions_frame.bind_all('<MouseWheel>', _tx_vwheel, add='+')
                transactions_frame.bind_all('<Shift-MouseWheel>', _tx_hwheel, add='+')
            except Exception:
                pass
        def _leave_tx(_e=None):
            try:
                transactions_frame.unbind_all('<MouseWheel>')
                transactions_frame.unbind_all('<Shift-MouseWheel>')
            except Exception:
                pass
        transactions_frame.bind('<Enter>', _enter_tx)
        transactions_frame.bind('<Leave>', _leave_tx)
        # Focus canvas when pointer enters so wheel events target it
        canvas.bind('<Enter>', lambda e: canvas.focus_set())
        main_container.bind('<Enter>', lambda e: canvas.focus_set())
        # Linux-style wheel events fallback
        def _tx_btn4(_e=None):
            canvas.yview_scroll(-1, 'units'); return 'break'
        def _tx_btn5(_e=None):
            canvas.yview_scroll(1, 'units'); return 'break'
        canvas.bind('<Button-4>', _tx_btn4)
        canvas.bind('<Button-5>', _tx_btn5)

        # Recursively bind wheel events to children so hovering any element scrolls the page
        def _bind_wheel_recursive(widget):
            try:
                # Skip Treeview to avoid double-scrolling its own content
                if isinstance(widget, ttk.Treeview):
                    return
            except Exception:
                pass
            try:
                widget.bind('<MouseWheel>', _tx_vwheel_child, add='+')
                widget.bind('<Shift-MouseWheel>', _tx_hwheel_child, add='+')
            except Exception:
                pass
            for child in getattr(widget, 'winfo_children', lambda: [])():
                _bind_wheel_recursive(child)

        # Defer binding until content is populated; schedule after idle
        try:
            widget_ref = main_container
            widget_ref.after(200, lambda: _bind_wheel_recursive(widget_ref))
        except Exception:
            pass
        
        # =================================================================
        # ISSUE BOOK SECTION - Fixed UI Layout
        # =================================================================
        borrow_frame = tk.LabelFrame(
            main_container,
            text="📚 Issue Book",
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
        
    # Row 2: Issue & Due Dates and Action Button - Better Layout
        action_row = tk.Frame(borrow_form, bg=self.colors['primary'])
        action_row.pack(fill=tk.X, pady=(15, 0))
        
        # Issue Date Section (uses DateEntry if available)
        borrow_date_section = tk.Frame(action_row, bg=self.colors['primary'])
        borrow_date_section.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(borrow_date_section, text="Issue Date:", font=('Segoe UI', 12, 'bold'), bg=self.colors['primary'], fg=self.colors['accent']).pack(anchor='w', pady=(0,8))
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
        
        # Issue button - Prominent and well-positioned
        borrow_btn = tk.Button(
            button_section,
            text="📚 Issue Book",
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
        # CURRENTLY ISSUED BOOKS SECTION - Improved Layout
        # =================================================================
        borrowed_frame = tk.LabelFrame(
            main_container,
            text="📋 Currently Issued Books",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent'],
            padx=10,
            pady=10
        )
        borrowed_frame.pack(fill=tk.BOTH, expand=True, pady=(0,40))
        
        borrowed_columns = ('Student', 'Book ID', 'Book Title', 'Issue Date', 'Due Date', 'Days Left')
        self.borrowed_tree = ttk.Treeview(borrowed_frame, columns=borrowed_columns, show='headings', height=10)
        borrowed_widths = {'Student': 150, 'Book ID': 100, 'Book Title': 250, 'Issue Date': 120, 'Due Date': 120, 'Days Left': 100}
        
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
                                  values=["All", "Issued", "Returned", "Overdue"], state="readonly", width=12)
        type_combo.pack(side=tk.LEFT, padx=5)
        type_combo.bind('<<ComboboxSelected>>', lambda e: self.search_records())
        
        # Row 2: Date filters and Academic Year
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
        
        # Academic Year filter
        tk.Label(row2, text="Academic Year:", bg=self.colors['primary'], fg=self.colors['accent'], font=('Segoe UI', 10)).pack(side=tk.LEFT)
        self.record_academic_year_var = tk.StringVar(value="All")
        
        # Get academic years from database and convert format
        academic_years_raw = self.db.get_all_academic_years()
        academic_years = ["All"]
        for year in academic_years_raw:
            # Convert format from "2025-2026" to "25-26"
            if "-" in year:
                years = year.split("-")
                if len(years) == 2:
                    year1 = years[0][-2:]  # "2025" -> "25"
                    year2 = years[1][-2:]  # "2026" -> "26"
                    academic_years.append(f"{year1}-{year2}")
                else:
                    academic_years.append(year)
            else:
                academic_years.append(year)
        
        academic_year_combo = ttk.Combobox(row2, textvariable=self.record_academic_year_var, 
                                          values=academic_years, state="readonly", width=15)
        academic_year_combo.pack(side=tk.LEFT, padx=(5, 15))
        academic_year_combo.bind('<<ComboboxSelected>>', lambda e: self.search_records())
        
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
        
        # Row 3: Quick date filters
        row3 = tk.Frame(search_controls, bg=self.colors['primary'])
        row3.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(row3, text="Quick Filter:", bg=self.colors['primary'], fg=self.colors['accent'], font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        
        def filter_last_days(days):
            """Filter records for last N days"""
            from datetime import datetime, timedelta
            today = datetime.now()
            from_date = (today - timedelta(days=days)).strftime('%Y-%m-%d')
            to_date = today.strftime('%Y-%m-%d')
            
            # Set date fields
            if DateEntry:
                self.record_from_date.set_date(today - timedelta(days=days))
                self.record_to_date.set_date(today)
            else:
                self.record_from_date.delete(0, tk.END)
                self.record_from_date.insert(0, from_date)
                self.record_to_date.delete(0, tk.END)
                self.record_to_date.insert(0, to_date)
            
            # Apply filter
            self.search_records()
        
        last_7_btn = tk.Button(
            row3,
            text="📅 Last 7 Days",
            font=('Segoe UI', 9),
            bg='#17a2b8',
            fg='white',
            relief='flat',
            padx=10,
            pady=5,
            command=lambda: filter_last_days(7),
            cursor='hand2'
        )
        last_7_btn.pack(side=tk.LEFT, padx=2)
        
        last_15_btn = tk.Button(
            row3,
            text="📅 Last 15 Days",
            font=('Segoe UI', 9),
            bg='#17a2b8',
            fg='white',
            relief='flat',
            padx=10,
            pady=5,
            command=lambda: filter_last_days(15),
            cursor='hand2'
        )
        last_15_btn.pack(side=tk.LEFT, padx=2)
        
        last_30_btn = tk.Button(
            row3,
            text="📅 Last 30 Days",
            font=('Segoe UI', 9),
            bg='#17a2b8',
            fg='white',
            relief='flat',
            padx=10,
            pady=5,
            command=lambda: filter_last_days(30),
            cursor='hand2'
        )
        last_30_btn.pack(side=tk.LEFT, padx=2)
        
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
        
        # Tip label for double-click feature
        tip_frame = tk.Frame(actions_frame, bg=self.colors['primary'])
        tip_frame.pack(padx=10, pady=(0, 10))
        
        tip_label = tk.Label(
            tip_frame,
            text="💡 Tip: Double-click on overdue student to send letter",
            font=('Segoe UI', 9, 'italic'),
            bg='#fff3cd',
            fg='#856404',
            relief='solid',
            bd=1,
            padx=10,
            pady=5
        )
        tip_label.pack()
        
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
        record_columns = ('Enrollment No', 'Student Name', 'Book ID', 'Book Title', 'Issue Date', 'Due Date', 'Return Date', 'Status', 'Fine')
        self.records_tree = ttk.Treeview(records_list_frame, columns=record_columns, show='headings', height=15)
        record_widths = {'Enrollment No': 120, 'Student Name': 150, 'Book ID': 100, 'Book Title': 200, 'Issue Date': 100, 'Due Date': 100, 'Return Date': 100, 'Status': 80, 'Fine': 80}
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

        # Free scrolling in Records: vertical and Shift+Wheel horizontal, pointer-scoped
        def _rec_units(delta):
            return -1 if delta > 0 else (1 if delta < 0 else 0)
        def _records_vwheel(event):
            u = _rec_units(event.delta)
            if u:
                self.records_tree.yview_scroll(u, 'units')
            return 'break'
        def _records_hwheel(event):
            u = _rec_units(event.delta)
            if u:
                self.records_tree.xview_scroll(u, 'units')
            return 'break'
        self.records_tree.bind('<MouseWheel>', _records_vwheel)
        self.records_tree.bind('<Shift-MouseWheel>', _records_hwheel)
        
        # Bind double-click event for sending overdue letter
        self.records_tree.bind('<Double-1>', self.on_record_double_click)

        # Initial population of records (avoid empty first view)
        try:
            self.clear_record_filters()  # resets inputs and calls search_records
        except Exception:
            # Fallback: directly populate with all records
            try:
                self.populate_records_tree(self.get_all_records())
            except Exception:
                pass
    
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
        dialog.geometry("500x500")
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
        
        # Auto-generate checkbox variable
        auto_gen_var = tk.BooleanVar(value=False)
        
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
                entry.grid(row=i, column=1, pady=(0, 15))
            elif field_name == "book_id":
                # Book ID entry with auto-generate option
                id_frame = tk.Frame(form_frame, bg='white')
                book_id_entry = tk.Entry(
                    id_frame,
                    font=('Segoe UI', 11),
                    width=30,
                    relief='solid',
                    bd=2
                )
                book_id_entry.pack(side=tk.TOP, fill=tk.X)
                
                def toggle_auto_gen():
                    if auto_gen_var.get():
                        next_id = self.db.get_next_book_id()
                        book_id_entry.delete(0, tk.END)
                        book_id_entry.insert(0, next_id)
                        book_id_entry.config(state='readonly')
                    else:
                        book_id_entry.config(state='normal')
                        book_id_entry.delete(0, tk.END)
                
                auto_check = tk.Checkbutton(
                    id_frame,
                    text="Auto-generate Book ID",
                    variable=auto_gen_var,
                    command=toggle_auto_gen,
                    font=('Segoe UI', 9),
                    bg='white',
                    fg=self.colors['text']
                )
                auto_check.pack(side=tk.TOP, anchor='w', pady=(3, 0))
                
                id_frame.grid(row=i, column=1, pady=(0, 15))
                entry = book_id_entry  # Store the actual entry widget
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
                    entry.config(validate='key', validatecommand=(dialog.register(lambda P: P.isdigit() or P == ""), '%P'))
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
            # Check Book ID uniqueness
            book_id_val = entries['book_id'].get().strip()
            if book_id_val:
                # Query database for existing Book ID
                conn = self.db.get_connection()
                cur = conn.cursor()
                cur.execute('SELECT COUNT(*) FROM books WHERE book_id = ?', (book_id_val,))
                exists = cur.fetchone()[0]
                conn.close()
                if exists:
                    messagebox.showerror("Error", f"Book ID '{book_id_val}' already exists! Please use a unique Book ID.")
                    return
            # Add book
            success, message = self.db.add_book(
                book_id_val,
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
        
        # Enforce: Pass Out students cannot borrow (UI-side quick check)
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT year FROM students WHERE enrollment_no = ?", (enrollment_no,))
            row = cur.fetchone()
            conn.close()
            if not row:
                messagebox.showerror("Error", "Student not found!")
                return
            year_val = (row[0] or '').strip().lower()
            if year_val in ("pass out", "passout"):
                messagebox.showerror("Not Allowed", "Pass Out students cannot borrow books.")
                return
        except Exception:
            # If the check fails unexpectedly, continue to DB enforcement which also validates
            pass

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
            messagebox.showerror("Error", "Due date cannot be before issue date")
            return

        # UI-side validation for allowed range: 1..LOAN_PERIOD_DAYS days from borrow
        try:
            bd_obj = datetime.strptime(borrow_date, '%Y-%m-%d')
            dd_obj = datetime.strptime(due_date, '%Y-%m-%d')
            diff_days = (dd_obj - bd_obj).days
            if not (1 <= diff_days <= LOAN_PERIOD_DAYS):
                messagebox.showerror(
                    "Invalid Due Date",
                    f"Due date must be between 1 and {LOAN_PERIOD_DAYS} days after the issue date."
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

            # DB students columns:
            # (id, enrollment_no, name, email, phone, department, year, date_registered)
            filtered_students = []
            for s in students:
                if search_term:
                    text = f"{s[1]} {s[2]} {s[3]} {s[4]} {s[6]} {s[5]}".lower()
                    if search_term not in text:
                        continue
                if year_filter != "All":
                    if (s[6] or '').strip() != year_filter:
                        continue
                filtered_students.append(s)

            self.populate_students_tree(filtered_students)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error searching students: {str(e)}")
    
    def search_books(self):
        """Search and filter books"""
        try:
            if hasattr(self, 'books_tree'):
                term = (self.book_search_var.get() or '').strip()
                category = self.book_category_filter.get()
                # Fetch from DB with optional LIKE filtering when term present
                books = self.db.get_books(term)
                # DB books columns:
                # (id, book_id, title, author, isbn, category, total_copies, available_copies, date_added)
                filtered = []
                for b in books:
                    if category and category != 'All':
                        if (b[5] or '').strip() != category:
                            continue
                    filtered.append(b)
                self.populate_books_tree(filtered)
        except Exception as e:
            print(f"Error searching books: {str(e)}")
    
    def search_records(self):
        """Search and filter records including academic year"""
        search_term = self.record_search_var.get().lower()
        type_filter = self.record_type_filter.get()
        from_date = self.record_from_date.get()
        to_date = self.record_to_date.get()
        academic_year_filter = self.record_academic_year_var.get() if hasattr(self, 'record_academic_year_var') else "All"
        
        records = self.get_all_records()
        
        # Filter records
        filtered_records = []
        for record in records:
            # record: (enroll, name, book_id, title, borrow_date, due_date, return_date, status, fine, academic_year)
            status_val = record[7]
            fine_val = record[8]
            academic_year_val = record[9] if len(record) > 9 else 'N/A'
            
            # Apply type filter
            if type_filter != "All":
                if type_filter == "Overdue":
                    # Overdue means fine > 0
                    if fine_val == 0 or fine_val == '0':
                        continue
                elif type_filter == "Issued":
                    # Issued means status is 'borrowed'
                    if status_val.lower() != 'borrowed':
                        continue
                elif type_filter == "Returned":
                    # Returned means status is 'returned'
                    if status_val.lower() != 'returned':
                        continue
            
            # Apply academic year filter
            if academic_year_filter != "All":
                # Convert database format to display format for comparison
                display_academic_year = academic_year_val
                if academic_year_val and "-" in academic_year_val:
                    years = academic_year_val.split("-")
                    if len(years) == 2:
                        year1 = years[0][-2:]  # "2025" -> "25"
                        year2 = years[1][-2:]  # "2026" -> "26"
                        display_academic_year = f"{year1}-{year2}"
                
                if display_academic_year != academic_year_filter:
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
        if hasattr(self, 'record_academic_year_var'):
            self.record_academic_year_var.set("All")
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
        
        # Refresh academic year display
        self.refresh_academic_year_display()
        
        # Auto-refresh Analysis tab charts when data changes
        if hasattr(self, 'notebook') and hasattr(self, 'refresh_analysis'):
            try:
                self.refresh_analysis()
            except Exception:
                pass
    
    def refresh_academic_year_display(self):
        """Refresh the academic year display in the header"""
        try:
            if hasattr(self, 'academic_year_label'):
                active_year = self.db.get_active_academic_year()
                if not active_year:
                    active_year = "2025-2026"  # Default fallback
                
                # Convert format from "2025-2026" to "25-26"
                if "-" in active_year:
                    years = active_year.split("-")
                    if len(years) == 2:
                        # Extract last 2 digits of each year
                        year1 = years[0][-2:]  # "2025" -> "25"
                        year2 = years[1][-2:]  # "2026" -> "26"
                        display_year = f"{year1}-{year2}"
                    else:
                        display_year = active_year
                else:
                    display_year = active_year
                
                self.academic_year_label.config(text=f"Academic Year: {display_year}")
                # Force the GUI to update
                self.academic_year_label.update_idletasks()
        except Exception as e:
            pass  # Silently fail if label doesn't exist yet
    
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
                # Map DB tuple to UI columns
                # Enrollment No, Name, Email, Phone, Year
                display_data = (student[1], student[2], student[3], student[4], student[6])
                self.students_tree.insert('', 'end', values=display_data)
    
    def populate_books_tree(self, books):
        """Populate books treeview"""
        if hasattr(self, 'books_tree'):
            for item in self.books_tree.get_children():
                self.books_tree.delete(item)
            
            for book in books:
                # Map DB tuple to UI columns: (Book ID, Title, Author, ISBN, Category, Total, Available)
                display_data = (book[1], book[2], book[3], book[4], book[5], book[6], book[7])
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
                # Add "Rs" prefix and "(Late)" suffix for overdue records
                if fine_is_num and isinstance(fine_val_num, int) and fine_val_num > 0:
                    fine_display = f"Rs {fine_val_num} (Late)"
                else:
                    fine_display = f"Rs {fine_val_num}" if fine_is_num else str(fine_val_num)
                tag = 'late' if (fine_is_num and isinstance(fine_val_num, int) and fine_val_num > 0) else ''
                self.records_tree.insert('', 'end', values=(*base, status, fine_display), tags=(tag,))
            try:
                self.records_tree.tag_configure('late', background='#fff3cd')
            except Exception:
                pass
    
    def on_record_double_click(self, event):
        """Handle double-click on record to send overdue letter"""
        selection = self.records_tree.selection()
        if not selection:
            return
        
        # Get the selected record data
        item = self.records_tree.item(selection[0])
        values = item['values']
        
        if not values or len(values) < 9:
            return
        
        # Extract record details
        enrollment_no = values[0]
        student_name = values[1]
        book_id = values[2]
        book_title = values[3]
        issue_date = values[4]
        due_date = values[5]
        return_date = values[6]
        status = values[7]
        fine_info = str(values[8])
        
        # Extract fine amount to check if overdue
        fine_amount = 0
        try:
            # Remove "Rs", "(Late)", and other text to get the number
            fine_str = fine_info.replace('Rs', '').replace('(Late)', '').strip()
            fine_amount = int(fine_str)
        except:
            fine_amount = 0
        
        # Check if this is an overdue record (borrowed + fine > 0)
        if status.lower() == 'borrowed' and fine_amount > 0:
            # Show dialog to confirm sending letter
            response = messagebox.askyesno(
                "Send Overdue Letter",
                f"Send overdue letter to:\n\n"
                f"Student: {student_name}\n"
                f"Enrollment: {enrollment_no}\n"
                f"Book: {book_title}\n"
                f"Fine: {fine_info}\n\n"
                f"Generate Word document?",
                icon='question'
            )
            
            if response:
                self.generate_overdue_letter(
                    enrollment_no, student_name, book_id, 
                    book_title, issue_date, due_date, fine_info
                )
        else:
            messagebox.showinfo(
                "Not Overdue",
                "This record is not overdue. Letters can only be sent for overdue borrowed books.",
                icon='info'
            )
    
    def generate_overdue_letter(self, enrollment_no, student_name, book_id, book_title, issue_date, due_date, fine_info):
        """Generate overdue letter as Word document"""
        if not Document:
            messagebox.showerror("Error", "python-docx is not installed. Cannot generate Word document.")
            return
        
        try:
            # Calculate days overdue
            from datetime import datetime as _dt
            due_d = _dt.strptime(due_date, '%Y-%m-%d')
            today = _dt.now()
            days_overdue = (today.date() - due_d.date()).days
            
            # Extract fine amount
            fine_amount = 0
            try:
                fine_str = fine_info.replace('(Late)', '').strip()
                fine_amount = int(fine_str)
            except:
                fine_amount = days_overdue * FINE_PER_DAY
            
            # Create Word document
            doc = Document()
            
            # Add logo at the top if available
            logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
            if os.path.exists(logo_path):
                try:
                    logo_para = doc.add_paragraph()
                    logo_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    logo_run = logo_para.add_run()
                    logo_run.add_picture(logo_path, width=Pt(80))
                except Exception as e:
                    print(f"Could not add logo: {e}")
            
            # Add institutional header with colors
            def add_colored_header(text, size, rgb_color):
                from docx.shared import RGBColor
                p = doc.add_paragraph()
                run = p.add_run(text)
                run.bold = True
                run.font.size = Pt(size)
                run.font.color.rgb = RGBColor(*rgb_color)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                return p
            
            # Three-line header with gradient colors
            add_colored_header("Government Polytechnic Awasari (Kh)", 20, (31, 71, 136))
            add_colored_header("Departmental Library", 16, (46, 92, 138))
            add_colored_header("Computer Department", 14, (54, 95, 145))
            
            # Add separator line
            sep_para = doc.add_paragraph("_" * 70)
            sep_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            doc.add_paragraph()  # Spacing
            
            # Add date
            date_para = doc.add_paragraph()
            date_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            date_run = date_para.add_run(f"Date: {today.strftime('%B %d, %Y')}")
            date_run.font.size = Pt(11)
            
            doc.add_paragraph()  # Spacing
            
            # Add subject
            subject = doc.add_paragraph()
            subject_run = subject.add_run('Subject: Overdue Book Notice')
            subject_run.bold = True
            subject_run.font.size = Pt(12)
            subject.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            doc.add_paragraph()  # Spacing
            
            # Recipient details
            to_para = doc.add_paragraph()
            to_run = to_para.add_run(f'To,\n{student_name}\nEnrollment No: {enrollment_no}')
            to_run.font.size = Pt(11)
            
            doc.add_paragraph()  # Spacing
            
            # Body of letter
            body = doc.add_paragraph()
            body_text = (
                f"Dear {student_name},\n\n"
                f"This is to inform you that the following book borrowed from the Library of Computer Department "
                f"is overdue and needs to be returned immediately.\n\n"
            )
            body_run = body.add_run(body_text)
            body_run.font.size = Pt(11)
            
            # Book details table
            doc.add_paragraph('Book Details:', style='Heading 2')
            table = doc.add_table(rows=5, cols=2)
            table.style = 'Light Grid Accent 1'
            
            table.cell(0, 0).text = 'Book ID:'
            table.cell(0, 1).text = str(book_id)
            table.cell(1, 0).text = 'Book Title:'
            table.cell(1, 1).text = book_title
            table.cell(2, 0).text = 'Issue Date:'
            table.cell(2, 1).text = issue_date
            table.cell(3, 0).text = 'Due Date:'
            table.cell(3, 1).text = due_date
            table.cell(4, 0).text = 'Days Overdue:'
            table.cell(4, 1).text = str(days_overdue)
            
            doc.add_paragraph()  # Spacing
            
            # Fine details
            fine_para = doc.add_paragraph()
            fine_run = fine_para.add_run(
                f"As per library rules, a fine of ₹{FINE_PER_DAY} per day is applicable for overdue books.\n"
                f"Your current fine amount is: ₹{fine_amount}\n\n"
            )
            fine_run.font.size = Pt(11)
            fine_run.bold = True
            
            # Request
            request_para = doc.add_paragraph()
            request_text = (
                "You are hereby requested to return the book to the library at the earliest and clear the pending fine. "
                "Failure to do so may result in restrictions on future borrowing privileges.\n\n"
                "Please contact the library desk for any queries or clarifications.\n\n"
            )
            request_run = request_para.add_run(request_text)
            request_run.font.size = Pt(11)
            
            # Closing
            doc.add_paragraph()  # Spacing
            closing = doc.add_paragraph()
            closing_text = "Thank you for your cooperation.\n\nYours sincerely,\n\n"
            closing_run = closing.add_run(closing_text)
            closing_run.font.size = Pt(11)
            
            # Signature
            doc.add_paragraph()
            doc.add_paragraph("__________________________")
            signature = doc.add_paragraph()
            signature_run = signature.add_run('Librarian')
            signature_run.font.size = Pt(11)
            signature_run.bold = True
            
            dept1 = doc.add_paragraph()
            dept1.add_run('Departmental Library').font.size = Pt(10)
            dept2 = doc.add_paragraph()
            dept2.add_run('Computer Department').font.size = Pt(10)
            dept3 = doc.add_paragraph()
            dept3.add_run('Government Polytechnic Awasari (Kh)').font.size = Pt(10)
            
            # Save the document
            default_filename = f"Overdue_Letter_{enrollment_no}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
            filepath = filedialog.asksaveasfilename(
                defaultextension=".docx",
                filetypes=[("Word Document", "*.docx")],
                initialfile=default_filename,
                title="Save Overdue Letter"
            )
            
            if filepath:
                doc.save(filepath)
                messagebox.showinfo(
                    "Success", 
                    f"Overdue letter generated successfully!\n\nSaved to:\n{filepath}",
                    icon='info'
                )
                
                # Ask if user wants to open the document
                if messagebox.askyesno("Open Document", "Do you want to open the document now?"):
                    try:
                        if platform.system() == 'Windows':
                            os.startfile(filepath)
                        elif platform.system() == 'Darwin':  # macOS
                            subprocess.call(['open', filepath])
                        else:  # Linux
                            subprocess.call(['xdg-open', filepath])
                    except Exception as e:
                        messagebox.showwarning("Warning", f"Document saved but couldn't open automatically.\nError: {e}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate overdue letter.\n\nError: {e}")
    
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
        """Get all transaction records including academic year"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            # Return enrollment_no, book_id, and academic_year explicitly for correct display
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
                    END as days_overdue,
                    COALESCE(br.academic_year, 'N/A') as academic_year
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
                (enroll, student_name, book_id, title, borrow_date, due_date, return_date, status, days_overdue, academic_year) = rec
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
                # Keep fine as numeric for downstream display logic, add academic_year
                formatted_records.append((enroll, student_name, book_id, title, borrow_date, due_date, return_date, status, fine, academic_year))
            return formatted_records
        except Exception as e:
            print(f"Error getting records: {e}")
            return []

    # ------------------------------------------------------------------
    # Date auto update helpers
    # ------------------------------------------------------------------
    def on_borrow_date_changed(self, event=None):
        """When issue date changes, suggest due date = issue + LOAN_PERIOD_DAYS (max),
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
        """Validate due-date change: must be within 1..LOAN_PERIOD_DAYS days of issue date."""
        try:
            from datetime import datetime as _dt
            bd = _dt.strptime(self.borrow_borrow_date_entry.get(), '%Y-%m-%d')
            dd = _dt.strptime(self.borrow_due_date_entry.get(), '%Y-%m-%d')
            diff = (dd - bd).days
            if not (1 <= diff <= LOAN_PERIOD_DAYS):
                messagebox.showerror(
                    "Invalid Due Date",
                    f"Due date must be between 1 and {LOAN_PERIOD_DAYS} days after the issue date."
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
        years = ["All", "1st", "2nd", "3rd", "Pass Out"]
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
        
        # Auto-update years option
        auto_update_var = tk.BooleanVar(value=True)
        auto_cb = tk.Checkbutton(
            options_frame,
            text="Auto-update years to current academic year before export",
            variable=auto_update_var,
            bg='white', fg=self.colors['accent'], selectcolor='white', anchor='w', justify='left', wraplength=320
        )
        auto_cb.pack(fill=tk.X, pady=(0, 10))

        # Buttons
        btn_frame = tk.Frame(dialog, bg='white')
        btn_frame.pack(pady=20)
        
        def export_data():
            selected_year = year_var.get()
            self.export_students_to_excel(selected_year, auto_update=auto_update_var.get())
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
    
    def export_students_to_excel(self, year_filter="All", auto_update=True):
        """Export students to Excel with year filter.
        If auto_update is True, compute current year (1st..3rd) based on date_registered and an academic rollover on July 1.
        """
        try:
            students = self.db.get_students()
            
            # Filter by Computer department and year
            filtered_students = []
            for student in students:
                if student[5] == "Computer":  # Department filter
                    # Compute effective year label if requested
                    eff_year = student[6]
                    if auto_update:
                        try:
                            eff_year = self._compute_current_year_label(student[7], student[6])
                        except Exception:
                            eff_year = student[6]
                    if year_filter == "All" or eff_year == year_filter:
                        filtered_students.append({
                            'Enrollment No': student[1],
                            'Name': student[2],
                            'Email': student[3],
                            'Phone': student[4],
                            'Department': student[5],
                            'Year': eff_year,
                            'Registered': student[7]
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
                # Add header then table using openpyxl for styling flexibility
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    sheet = 'Students'
                    # Write institutional header first
                    header_end_row = 6  # New enhanced header takes 6 rows
                    df.to_excel(writer, sheet_name=sheet, index=False, startrow=header_end_row)
                    ws = writer.book[sheet]
                    # Write enhanced header
                    self._write_excel_header_openpyxl(ws, start_row=1)
                    # Apply enhanced auto-adjust with styling
                    self._auto_adjust_column_width(ws)
                messagebox.showinfo("Success", f"Students data exported to {file_path}")
                
                # Ask if user wants to open the file
                if messagebox.askyesno("Open File", "Do you want to open the exported file?"):
                    self.open_file(file_path)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export students: {str(e)}")

    # ---------------------- Academic Year Helpers ----------------------
    def _compute_current_year_label(self, date_registered, stored_year_label):
        """Return current year label ('1st','2nd','3rd') based on date_registered and today's date.
        Assumptions: 3-year course; academic year rolls over on July 1. Falls back to stored label if missing date.
        """
        try:
            from datetime import datetime as _dt
            if not date_registered:
                return stored_year_label or '1st'
            d = _dt.strptime(str(date_registered), '%Y-%m-%d').date()
            today = _dt.now().date()
            def acad_index(x):
                return x.year if (x.month, x.day) >= (7, 1) else x.year - 1
            promotions = max(0, acad_index(today) - acad_index(d))
            base = 1
            map_to_num = {'1st': 1, '2nd': 2, '3rd': 3, 'First':1, 'Second':2, 'Third':3}
            if stored_year_label in map_to_num:
                base = map_to_num[stored_year_label]
            progressed = base + promotions
            if progressed >= 4:
                return 'Pass Out'
            new_num = min(max(progressed, 1), 3)
            return {1:'1st',2:'2nd',3:'3rd'}[new_num]
        except Exception:
            return stored_year_label or '1st'

    def export_all_students_direct(self):
        """Direct export of students with year selection for Share Data function"""
        # Create year selection dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Export Students - Select Year")
        dialog.geometry("450x550")  # Increased height significantly
        dialog.configure(bg='#f8f9fa')  # Light gray background
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 180, self.root.winfo_rooty() + 100))
        
        # Main container with border
        main_frame = tk.Frame(
            dialog, 
            bg='white', 
            relief='ridge', 
            bd=2,
            padx=25,
            pady=20
        )
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Title with icon
        title_frame = tk.Frame(main_frame, bg='white')
        title_frame.pack(pady=(0, 20))
        
        title_label = tk.Label(
            title_frame,
            text="📊 Export Students Data",
            font=('Segoe UI', 18, 'bold'),
            bg='white',
            fg=self.colors['accent']
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(
            title_frame,
            text="Select which year students to export:",
            font=('Segoe UI', 12),
            bg='white',
            fg='#6c757d'
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Year selection container with background
        selection_frame = tk.Frame(
            main_frame, 
            bg='#f8f9fa',
            relief='solid',
            bd=1,
            padx=20,
            pady=15
        )
        selection_frame.pack(fill='x', pady=(0, 20))
        
        year_var = tk.StringVar(value="All")
        
        # Year options with better styling
        year_options = [
            ("📚 All Students", "All", "#4285f4"),
            ("🥇 1st Year", "1st", "#34a853"), 
            ("🥈 2nd Year", "2nd", "#fbbc04"),
            ("🥉 3rd Year", "3rd", "#ea4335"),
            ("🎓 Pass Out", "Pass Out", "#9333ea")
        ]
        
        for i, (text, value, color) in enumerate(year_options):
            rb = tk.Radiobutton(
                selection_frame,
                text=text,
                variable=year_var,
                value=value,
                font=('Segoe UI', 12, 'bold'),
                bg='#f8f9fa',
                fg=color,
                selectcolor='white',
                activebackground='#f8f9fa',
                activeforeground=color,
                relief='flat',
                padx=10,
                pady=6
            )
            rb.pack(anchor='w', pady=4)
        
        # Buttons container - FIXED positioning at bottom
        btn_container = tk.Frame(main_frame, bg='white')
        btn_container.pack(side='bottom', pady=(20, 0))
        
        def perform_export():
            selected_year = year_var.get()
            dialog.destroy()
            self._export_students_by_year(selected_year)
        
        # Export button with gradient-like styling
        export_btn = tk.Button(
            btn_container,
            text="📊 Export to Excel",
            font=('Segoe UI', 12, 'bold'),
            bg='#28a745',
            fg='white',
            relief='flat',
            padx=25,
            pady=12,
            command=perform_export,
            cursor='hand2',
            activebackground='#218838',
            activeforeground='white'
        )
        export_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Cancel button
        cancel_btn = tk.Button(
            btn_container,
            text="❌ Cancel",
            font=('Segoe UI', 12, 'bold'),
            bg='#dc3545',
            fg='white',
            relief='flat',
            padx=25,
            pady=12,
            command=dialog.destroy,
            cursor='hand2',
            activebackground='#c82333',
            activeforeground='white'
        )
        cancel_btn.pack(side=tk.LEFT)
        
        # Add hover effects
        def on_enter_export(e):
            export_btn.configure(bg='#218838')
        
        def on_leave_export(e):
            export_btn.configure(bg='#28a745')
            
        def on_enter_cancel(e):
            cancel_btn.configure(bg='#c82333')
        
        def on_leave_cancel(e):
            cancel_btn.configure(bg='#dc3545')
        
        export_btn.bind("<Enter>", on_enter_export)
        export_btn.bind("<Leave>", on_leave_export)
        cancel_btn.bind("<Enter>", on_enter_cancel)
        cancel_btn.bind("<Leave>", on_leave_cancel)

    def _export_students_by_year(self, year_filter):
        """Helper function to export students filtered by year"""
        try:
            students = self.db.get_students()
            
            # Filter by Computer department and selected year
            filtered_students = []
            for student in students:
                if student[5] == "Computer":  # Department filter
                    # Check year filter
                    if year_filter == "All" or student[6] == year_filter:
                        filtered_students.append({
                            'Enrollment No': student[1],
                            'Name': student[2],
                            'Email': student[3],
                            'Phone': student[4],
                            'Department': student[5],
                            'Year': student[6],
                            'Registered': student[7]
                        })
            
            if not filtered_students:
                messagebox.showwarning("Warning", f"No students found for {year_filter}!")
                return
            
            # Create DataFrame
            df = pd.DataFrame(filtered_students)
            
            # Save to file
            year_suffix = year_filter if year_filter != "All" else "all_years"
            filename = f"students_{year_suffix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                initialfile=filename
            )
            
            if file_path:
                # Add professional header and formatting
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    sheet_name = f'Students_{year_filter}' if year_filter != "All" else 'All_Students'
                    header_end_row = 6  # Enhanced header takes 6 rows
                    df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=header_end_row)
                    ws = writer.book[sheet_name]
                    # Write enhanced header
                    self._write_excel_header_openpyxl(ws, start_row=1)
                    # Apply enhanced auto-adjust with styling
                    self._auto_adjust_column_width(ws)
                    
                messagebox.showinfo("Success", f"{year_filter} students data exported to {file_path}")
                
                # Ask if user wants to open the file
                if messagebox.askyesno("Open File", "Do you want to open the exported file?"):
                    self.open_file(file_path)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export students: {str(e)}")

    def promote_student_years(self):
        """Enhanced promotion with letter number, academic year creation, and history tracking"""
        # Create promotion dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Promote Student Years")
        dialog.geometry("600x500")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 100, self.root.winfo_rooty() + 100))
        
        # Title
        title_label = tk.Label(
            dialog,
            text="🎓 Promote Student Years",
            font=('Segoe UI', 16, 'bold'),
            bg='white',
            fg=self.colors['accent']
        )
        title_label.pack(pady=(20, 10))
        
        # Info text
        info_label = tk.Label(
            dialog,
            text="This will promote: 1st→2nd, 2nd→3rd, 3rd→Pass Out",
            font=('Segoe UI', 10),
            bg='white',
            fg=self.colors['text']
        )
        info_label.pack(pady=(0, 20))
        
        # Form frame
        form_frame = tk.Frame(dialog, bg='white')
        form_frame.pack(expand=True, padx=40)
        
        # Letter Number field
        letter_label = tk.Label(
            form_frame,
            text="Letter Number:",
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg=self.colors['accent']
        )
        letter_label.grid(row=0, column=0, sticky='w', pady=(0, 15), padx=(0, 20))
        
        letter_entry = tk.Entry(
            form_frame,
            font=('Segoe UI', 11),
            width=30,
            relief='solid',
            bd=2
        )
        letter_entry.grid(row=0, column=1, pady=(0, 15))
        
        letter_hint = tk.Label(
            form_frame,
            text="(Can contain letters, numbers, and symbols)",
            font=('Segoe UI', 8, 'italic'),
            bg='white',
            fg='#666'
        )
        letter_hint.grid(row=1, column=1, sticky='w', pady=(0, 15))
        
        # Academic Year field
        year_label = tk.Label(
            form_frame,
            text="Academic Year:",
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg=self.colors['accent']
        )
        year_label.grid(row=2, column=0, sticky='w', pady=(0, 15), padx=(0, 20))
        
        # Auto-suggest NEXT academic year for teacher convenience
        current_year = datetime.now().year
        # If we're in July-December, suggest next year
        # If we're in January-June, suggest current year
        if datetime.now().month >= 7:  # July onwards = next academic year
            suggested_year = f"{current_year + 1}-{current_year + 2}"
        else:  # January-June = current academic year
            suggested_year = f"{current_year}-{current_year + 1}"
        
        # Get all academic years from database
        all_academic_years = self.db.get_all_academic_years()
        
        # Create a list with suggested year first, then existing years
        year_options = []
        if suggested_year not in all_academic_years:
            year_options.append(suggested_year)
        year_options.extend(all_academic_years)
        
        # Also add next few years for convenience
        for i in range(1, 4):
            future_year = f"{current_year + i}-{current_year + i + 1}"
            if future_year not in year_options:
                year_options.append(future_year)
        
        # Create combobox for academic year selection
        year_entry = ttk.Combobox(
            form_frame,
            font=('Segoe UI', 11),
            width=28,
            values=year_options,
            state='normal'  # Allow typing custom years
        )
        year_entry.set(suggested_year)
        year_entry.grid(row=2, column=1, pady=(0, 15))
        
        year_hint = tk.Label(
            form_frame,
            text=f"(Suggested: {suggested_year} - You can type custom year)",
            font=('Segoe UI', 8, 'italic'),
            bg='white',
            fg='#666'
        )
        year_hint.grid(row=3, column=1, sticky='w', pady=(0, 20))
        
        # Buttons frame
        btn_frame = tk.Frame(dialog, bg='white')
        btn_frame.pack(pady=20)
        
        def perform_promotion():
            letter_number = letter_entry.get().strip()
            academic_year = year_entry.get().strip()
            
            if not letter_number:
                messagebox.showerror("Error", "Letter Number is required!")
                return
            
            if not academic_year:
                messagebox.showerror("Error", "Academic Year is required!")
                return
            
            # Confirm promotion
            if not messagebox.askyesno(
                "Confirm Promotion",
                f"This will promote all students with:\n\nLetter Number: {letter_number}\nAcademic Year: {academic_year}\n\nProceed?"
            ):
                return
            
            def _norm(label: str) -> str:
                if not label:
                    return '1st'
                s = str(label).strip().lower()
                if s in ('1st', 'first', 'first year', '1', 'i', 'fy', 'f.y', 'f.y.', 'fe', 'fe year'):
                    return '1st'
                if s in ('2nd', 'second', 'second year', '2', 'ii', 'sy', 's.y', 's.y.'):
                    return '2nd'
                if s in ('3rd', 'third', 'third year', '3', 'iii', 'ty', 't.y', 't.y.'):
                    return '3rd'
                if 'pass' in s:
                    return 'Pass Out'
                return label

            def _promote_once(label: str) -> str:
                l = _norm(label)
                return {'1st': '2nd', '2nd': '3rd', '3rd': 'Pass Out'}.get(l, l)

            try:
                # Create/activate academic year
                self.db.create_academic_year(academic_year)
                
                conn = self.db.get_connection()
                cur = conn.cursor()
                cur.execute('SELECT enrollment_no, name, year FROM students')
                rows = cur.fetchall()
                c_12 = c_23 = c_3p = c_skip = 0
                
                # Collect promotion records
                promotion_records = []
                
                for en, name, yr in rows:
                    new = _promote_once(yr)
                    if new != yr:
                        cur.execute('UPDATE students SET year=? WHERE enrollment_no=?', (new, en))
                        # Store promotion data for later insertion
                        promotion_records.append((en, name, yr, new, letter_number, academic_year))
                        
                        if _norm(yr) == '1st' and new == '2nd':
                            c_12 += 1
                        elif _norm(yr) == '2nd' and new == '3rd':
                            c_23 += 1
                        elif _norm(yr) == '3rd' and new == 'Pass Out':
                            c_3p += 1
                    else:
                        c_skip += 1
                
                conn.commit()
                conn.close()
                
                # Now add all promotion history records (after closing the main connection)
                for record in promotion_records:
                    self.db.add_promotion_history(*record)
                
                total = c_12 + c_23 + c_3p
                msg = (
                    f"Promotion Complete!\n\n"
                    f"Updated Year for {total} student(s).\n\n"
                    f"1st → 2nd: {c_12}\n"
                    f"2nd → 3rd: {c_23}\n"
                    f"3rd → Pass Out: {c_3p}\n"
                    f"Unchanged: {c_skip}\n\n"
                    f"Letter Number: {letter_number}\n"
                    f"Academic Year: {academic_year}"
                )
                messagebox.showinfo("Success", msg)
                dialog.destroy()
                
                try:
                    self.refresh_students()
                    self.refresh_dashboard()
                except Exception:
                    pass
                    
            except Exception as e:
                messagebox.showerror("Error", f"Promotion failed: {e}")
        
        def undo_last():
            """Undo the last promotion"""
            if messagebox.askyesno("Confirm Undo", "Undo the last promotion? This will revert the most recent promotion action."):
                success, message = self.db.undo_last_promotion()
                if success:
                    messagebox.showinfo("Success", message)
                    try:
                        self.refresh_students()
                        self.refresh_dashboard()
                    except Exception:
                        pass
                else:
                    messagebox.showerror("Error", message)
        
        def view_history():
            """View promotion history"""
            self.show_promotion_history_dialog()
        
        # Promote button
        promote_btn = tk.Button(
            btn_frame,
            text="🎓 Promote Students",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['accent'],
            fg='white',
            command=perform_promotion,
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        promote_btn.pack(side=tk.LEFT, padx=5)
        
        # Undo button
        undo_btn = tk.Button(
            btn_frame,
            text="↩️ Undo Last",
            font=('Segoe UI', 11),
            bg='#FF9800',
            fg='white',
            command=undo_last,
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        undo_btn.pack(side=tk.LEFT, padx=5)
        
        # History button
        history_btn = tk.Button(
            btn_frame,
            text="📜 History",
            font=('Segoe UI', 11),
            bg=self.colors['secondary'],
            fg='white',
            command=view_history,
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        history_btn.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        cancel_btn = tk.Button(
            btn_frame,
            text="❌ Cancel",
            font=('Segoe UI', 11),
            bg='#666',
            fg='white',
            command=dialog.destroy,
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def show_promotion_history_dialog(self):
        """Show promotion history summary (Letter Number, Date, Time, Student Count)"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Promotion History")
        dialog.geometry("800x600")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Title
        title_label = tk.Label(
            dialog,
            text="📜 Promotion History Summary",
            font=('Segoe UI', 16, 'bold'),
            bg='white',
            fg=self.colors['accent']
        )
        title_label.pack(pady=(20, 10))
        
        # Tree frame
        tree_frame = tk.Frame(dialog, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        h_scroll = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        
        # Treeview - Simplified columns
        columns = ('Letter Number', 'Date', 'Time', '1st→2nd', '2nd→3rd', '3rd→Pass Out', 'Total Students')
        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=v_scroll.set,
            xscrollcommand=h_scroll.set,
            height=15
        )
        
        v_scroll.config(command=tree.yview)
        h_scroll.config(command=tree.xview)
        
        # Configure columns
        column_widths = [150, 100, 80, 80, 80, 100, 100]
        for col, width in zip(columns, column_widths):
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor='center')
        
        # Grid layout
        tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Load and process data
        history = self.db.get_promotion_history()
        
        # Group by promotion date/time and letter number
        from collections import defaultdict
        grouped = defaultdict(lambda: {'1st→2nd': 0, '2nd→3rd': 0, '3rd→Pass Out': 0, 'letter': '', 'datetime': ''})
        
        for record in history:
            # record: (enrollment_no, student_name, old_year, new_year, letter_number, academic_year, promotion_date)
            old_year = record[2]
            new_year = record[3]
            letter_num = record[4]
            promo_datetime = record[6]
            
            key = (letter_num, promo_datetime)
            grouped[key]['letter'] = letter_num
            grouped[key]['datetime'] = promo_datetime
            
            # Count transitions
            if old_year == '1st' and new_year == '2nd':
                grouped[key]['1st→2nd'] += 1
            elif old_year == '2nd' and new_year == '3rd':
                grouped[key]['2nd→3rd'] += 1
            elif old_year == '3rd' and new_year == 'Pass Out':
                grouped[key]['3rd→Pass Out'] += 1
        
        # Display grouped data
        summary_data = []
        for key, data in grouped.items():
            try:
                # Parse datetime
                dt = datetime.strptime(data['datetime'], '%Y-%m-%d %H:%M:%S')
                date_str = dt.strftime('%Y-%m-%d')
                time_str = dt.strftime('%H:%M:%S')
            except:
                date_str = data['datetime']
                time_str = ''
            
            total = data['1st→2nd'] + data['2nd→3rd'] + data['3rd→Pass Out']
            
            row = (
                data['letter'],
                date_str,
                time_str,
                data['1st→2nd'],
                data['2nd→3rd'],
                data['3rd→Pass Out'],
                total
            )
            summary_data.append(row)
            tree.insert('', 'end', values=row)
        
        # Button frame
        btn_frame = tk.Frame(dialog, bg='white')
        btn_frame.pack(pady=20)
        
        def download_history():
            """Download promotion history summary as Excel file"""
            if not summary_data:
                messagebox.showinfo("Info", "No promotion history to download")
                return
            
            try:
                # Create DataFrame
                df = pd.DataFrame(summary_data, columns=columns)
                
                # Save to file
                filename = f"promotion_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[("Excel files", "*.xlsx")],
                    initialfile=filename
                )
                
                if file_path:
                    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                        sheet = 'Promotion Summary'
                        df.to_excel(writer, sheet_name=sheet, index=False, startrow=4)
                        ws = writer.book[sheet]
                        self._write_excel_header_openpyxl(ws, start_row=1)
                        self._auto_adjust_column_width(ws)
                    
                    messagebox.showinfo("Success", f"Promotion history exported to {file_path}")
                    
                    if messagebox.askyesno("Open File", "Do you want to open the exported file?"):
                        self.open_file(file_path)
                        
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
        
        # Download button
        download_btn = tk.Button(
            btn_frame,
            text="📥 Download History",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['accent'],
            fg='white',
            command=download_history,
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        download_btn.pack(side=tk.LEFT, padx=5)
        
        # Close button
        close_btn = tk.Button(
            btn_frame,
            text="❌ Close",
            font=('Segoe UI', 11),
            bg='#666',
            fg='white',
            command=dialog.destroy,
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        close_btn.pack(side=tk.LEFT, padx=5)
    
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
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    sheet = 'Books'
                    header_end_row = 6  # Enhanced header takes 6 rows
                    df.to_excel(writer, sheet_name=sheet, index=False, startrow=header_end_row)
                    ws = writer.book[sheet]
                    self._write_excel_header_openpyxl(ws, start_row=1)
                    # Apply enhanced auto-adjust with styling
                    self._auto_adjust_column_width(ws)
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
                # Tree has 9 columns: (Enrollment No, Student Name, Book ID, Book Title, Issue Date, Due Date, Return Date, Status, Fine)
                # Convert tuple to list to ensure we have exactly 9 columns
                record_list = list(vals)
                if len(record_list) > 9:
                    # If more columns, trim to 9
                    record_list = record_list[:9]
                elif len(record_list) < 9:
                    # If fewer columns, pad with empty strings
                    record_list.extend([''] * (9 - len(record_list)))
                visible_records.append(tuple(record_list))

            if not visible_records:
                messagebox.showwarning("Warning", "No filtered records to export (the list is empty)!")
                return

            # Build DataFrame with the same column ordering used in the tree
            df = pd.DataFrame(visible_records, columns=[
                'Enrollment No', 'Student Name', 'Book ID', 'Book Title', 'Issue Date',
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
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    sheet = 'Records'
                    header_end_row = 6  # Enhanced header takes 6 rows
                    df.to_excel(writer, sheet_name=sheet, index=False, startrow=header_end_row)
                    ws = writer.book[sheet]
                    self._write_excel_header_openpyxl(ws, start_row=1)
                    # Apply enhanced auto-adjust with styling
                    self._auto_adjust_column_width(ws)
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
        """Return list of overdue (currently issued and past due date) records.
        Each record dict with: Enrollment No, Student Name, Book ID, Book Title, Issue Date, Due Date, Days Overdue, Accrued Fine
        """
        overdue = []
        try:
            all_records = self.get_all_records()
            today = datetime.now().date()
            from datetime import datetime as _dt
            for rec in all_records:
                # Now handling 10 fields (with academic_year at the end)
                if len(rec) >= 9:
                    enroll, name, book_id, title, borrow_date, due_date, return_date, status, fine = rec[:9]
                    # If there's a 10th field, it's academic_year (we don't need it here)
                    
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
                                    'Issue Date': borrow_date,
                                    'Due Date': due_date,
                                    'Days Overdue': days_overdue,
                                    'Accrued Fine': int(days_overdue) * FINE_PER_DAY
                                })
                        except Exception as e:
                            print(f"Error processing overdue record: {e}")
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
                messagebox.showinfo("Overdue Notice", "There are currently no overdue issued books.")
                return

            today_str = datetime.now().strftime('%Y-%m-%d')
            ref_code = f"Library/Overdue/{datetime.now().strftime('%Y%m%d')}"

            body_lines = [
                "Government Polytechnic Awasari (Kh)",
                "Computer Department",
                "Department of Library",
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
                    
                    # Add institutional header with logo first
                    ws = writer.book.create_sheet(sheet_name)
                    header_rows = self._write_excel_header_openpyxl(ws, start_row=1)
                    
                    # Add date and ref below header
                    current_row = header_rows + 1
                    ws.cell(row=current_row, column=1, value=f"Date: {today_str}")
                    ws.cell(row=current_row + 1, column=1, value=f"Ref: {ref_code}")
                    current_row += 3
                    
                    # Add subject and body text
                    from openpyxl.styles import Font
                    ws.cell(row=current_row, column=1, value="Subject: Submission of Overdue Library Books").font = Font(bold=True)
                    current_row += 2
                    ws.cell(row=current_row, column=1, value="Dear Students,")
                    current_row += 2
                    ws.cell(row=current_row, column=1, value="The following students are hereby notified to immediately submit the listed library books that are now overdue.")
                    current_row += 1
                    ws.cell(row=current_row, column=1, value=f"A fine of Rs {FINE_PER_DAY} per day has accrued (or will continue to accrue) until the books are returned.")
                    current_row += 1
                    ws.cell(row=current_row, column=1, value="Failure to comply today will trigger disciplinary action per departmental policy.")
                    current_row += 2
                    ws.cell(row=current_row, column=1, value="Overdue Book List:").font = Font(bold=True)
                    current_row += 2
                    
                    # Write table data
                    startrow = current_row
                    df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=startrow)
                    
                    # Auto-adjust columns for the table
                    self._auto_adjust_column_width(ws)
                    
                    # Add closing text
                    closing_start = startrow + len(df) + 3
                    closing_lines = [
                        "", "You are directed to return the above books without further delay.",
                        "Punishment Clause: Continued non-compliance after 3 days from this notice will result in suspension of borrowing privileges for one month and a formal report to the Academic Coordinator.",
                        "", "Regards,", "", "__________________________", "Librarian", "Departmental Library",
                        "Computer Department", "Government Polytechnic Awasari (Kh)"
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
                    "", "Regards,", "", "__________________________", "Librarian", "Department of Library", "Computer Department", "Government Polytechnic Awasari (Kh)"
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
                messagebox.showinfo("Overdue Notice", "There are currently no overdue issued books.")
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
            
            # Add logo at the top if available
            logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
            if os.path.exists(logo_path):
                try:
                    # Add logo centered at top
                    logo_para = doc.add_paragraph()
                    logo_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    logo_run = logo_para.add_run()
                    logo_run.add_picture(logo_path, width=Pt(60))
                except Exception as e:
                    print(f"Could not add logo: {e}")
            
            def add_center(text, bold=True, size=16, color=None):
                p = doc.add_paragraph()
                run = p.add_run(text)
                run.bold = bold
                run.font.size = Pt(size)
                if color:
                    from docx.shared import RGBColor
                    run.font.color.rgb = RGBColor(*color)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER

            # Main heading - VERY LARGE with dark blue color
            add_center("Government Polytechnic Awasari (Kh)", True, 22, (31, 71, 136))
            # Subheading - Large with medium blue color
            add_center("Departmental Library", True, 18, (46, 92, 138))
            # Sub-subheading - Medium with light blue color
            add_center("Computer Department", True, 16, (54, 95, 145))
            
            # Add a line separator
            doc.add_paragraph("_" * 60).alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            # Date and Ref aligned to the right
            meta_p = doc.add_paragraph()
            meta_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
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

            columns = ["Enrollment No", "Student Name", "Book ID", "Book Title", "Issue Date", "Due Date", "Days Overdue", "Accrued Fine"]
            table = doc.add_table(rows=1, cols=len(columns))
            table.style = 'Light Grid Accent 1'  # Professional table style with borders
            
            # Header row - bold and formatted
            hdr = table.rows[0].cells
            for i, col in enumerate(columns):
                hdr[i].text = col
                # Make header bold
                for paragraph in hdr[i].paragraphs:
                    for run in paragraph.runs:
                        run.bold = True
                        run.font.size = Pt(11)
            
            # Data rows
            for rec in overdue:
                row = table.add_row().cells
                row[0].text = str(rec['Enrollment No'])
                row[1].text = str(rec['Student Name'])
                row[2].text = str(rec['Book ID'])
                row[3].text = str(rec['Book Title'])
                row[4].text = str(rec['Issue Date'])
                row[5].text = str(rec['Due Date'])
                row[6].text = str(rec['Days Overdue'])
                row[7].text = "Rs " + str(rec['Accrued Fine'])  # Add Rs prefix for clarity

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
            doc.add_paragraph("Departmental Library")
            doc.add_paragraph("Computer Department")
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
            ("👥 Students Data", self.export_all_students_direct),
            ("📚 Books Data", self.export_books_to_excel),
            ("📋 Transaction Records", self.export_records_to_excel)
        ]
        
        def create_button_command(cmd, dialog_ref):
            """Create button command that handles dialog closing properly"""
            def button_action():
                dialog_ref.destroy()
                cmd()
            return button_action
        
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
                command=create_button_command(command, dialog),
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
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    # Write statistics
                    stats_df = pd.DataFrame(summary_data['Library Statistics'][1:], columns=summary_data['Library Statistics'][0])
                    header_end_row = 6  # Enhanced header takes 6 rows
                    stats_df.to_excel(writer, sheet_name='Statistics', index=False, startrow=header_end_row)
                    ws_stats = writer.book['Statistics']
                    self._write_excel_header_openpyxl(ws_stats, start_row=1)
                    self._auto_adjust_column_width(ws_stats)
                    
                    # Write recent activities
                    if activities:
                        activities_df = pd.DataFrame(activities, columns=[
                            'Type', 'Student', 'Book', 'Date', 'Status'
                        ])
                        activities_df.to_excel(writer, sheet_name='Recent Activities', index=False, startrow=header_end_row)
                        ws_act = writer.book['Recent Activities']
                        self._write_excel_header_openpyxl(ws_act, start_row=1)
                        self._auto_adjust_column_width(ws_act)
                
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

    # ---------------------- Excel Helpers ----------------------
    def _write_excel_header_openpyxl(self, worksheet, start_row=1):
        """Write the required header into an openpyxl worksheet with professional formatting like Word documents.
        Creates a beautifully formatted header with logo, merged cells, colors, and borders.
        Returns the next row after the header.
        """
        from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
        from openpyxl.drawing.image import Image as XLImage
        from openpyxl.utils import get_column_letter
        
        # Set generous row heights for professional appearance
        worksheet.row_dimensions[start_row].height = 45
        worksheet.row_dimensions[start_row + 1].height = 35
        worksheet.row_dimensions[start_row + 2].height = 30
        worksheet.row_dimensions[start_row + 3].height = 8  # Separator row
        worksheet.row_dimensions[start_row + 4].height = 15  # Spacing row
        
        # Add logo if available
        logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
        if os.path.exists(logo_path):
            try:
                img = XLImage(logo_path)
                # Larger logo for professional appearance
                img.width = 80
                img.height = 80
                # Position logo in column A, centered
                worksheet.add_image(img, f'A{start_row}')
            except Exception as e:
                print(f"Could not add logo: {e}")
        
        # Determine the number of columns to merge (ensure at least 8 columns for better appearance)
        max_col = max(8, worksheet.max_column if worksheet.max_column > 1 else 8)
        
        # Create border styles
        thin_border = Border(
            left=Side(style='thin', color='365F91'),
            right=Side(style='thin', color='365F91'),
            top=Side(style='thin', color='365F91'),
            bottom=Side(style='thin', color='365F91')
        )
        
        # Create background fills for gradient effect
        main_fill = PatternFill(start_color='E8F0FE', end_color='E8F0FE', fill_type='solid')  # Light blue background
        
        # Main heading - VERY LARGE, bold, centered with background
        merge_range_main = f'B{start_row}:{get_column_letter(max_col)}{start_row}'
        worksheet.merge_cells(merge_range_main)
        cell_main = worksheet[f'B{start_row}']
        cell_main.value = "Government Polytechnic Awasari(Kh)"
        cell_main.font = Font(size=22, bold=True, name='Calibri', color='1F4788')  # Dark blue
        cell_main.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell_main.fill = main_fill
        cell_main.border = thin_border
        
        # Subheading - Large, bold, centered with background
        merge_range_sub1 = f'B{start_row + 1}:{get_column_letter(max_col)}{start_row + 1}'
        worksheet.merge_cells(merge_range_sub1)
        cell_sub1 = worksheet[f'B{start_row + 1}']
        cell_sub1.value = "Departmental Library"
        cell_sub1.font = Font(size=18, bold=True, name='Calibri', color='2E5C8A')  # Medium blue
        cell_sub1.alignment = Alignment(horizontal='center', vertical='center')
        cell_sub1.fill = PatternFill(start_color='F0F6FF', end_color='F0F6FF', fill_type='solid')
        cell_sub1.border = thin_border
        
        # Sub-subheading - Medium, bold, centered with background
        merge_range_sub2 = f'B{start_row + 2}:{get_column_letter(max_col)}{start_row + 2}'
        worksheet.merge_cells(merge_range_sub2)
        cell_sub2 = worksheet[f'B{start_row + 2}']
        cell_sub2.value = "Computer Department"
        cell_sub2.font = Font(size=16, bold=True, name='Calibri', color='365F91')  # Light blue
        cell_sub2.alignment = Alignment(horizontal='center', vertical='center')
        cell_sub2.fill = PatternFill(start_color='F8FAFF', end_color='F8FAFF', fill_type='solid')
        cell_sub2.border = thin_border
        
        # Add a professional separator line across all columns
        thick_border = Border(bottom=Side(style='thick', color='1F4788'))
        for col in range(1, max_col + 1):
            cell = worksheet.cell(row=start_row + 3, column=col)
            cell.border = thick_border
            cell.fill = PatternFill(start_color='1F4788', end_color='1F4788', fill_type='solid')
        
        # Add borders to logo column for consistency
        for row in range(start_row, start_row + 3):
            logo_cell = worksheet.cell(row=row, column=1)
            logo_cell.border = thin_border
            logo_cell.fill = main_fill
        
        # Return next available row (after spacing)
        return start_row + 6

    def _xlsxwriter_write_header(self, worksheet, workbook, start_row=0):
        """Write the required header into an xlsxwriter worksheet with proper formatting and logo."""
        # Main heading - VERY LARGE, bold, centered with color
        fmt_main = workbook.add_format({
            'bold': True, 
            'font_size': 20, 
            'align': 'center',
            'valign': 'vcenter',
            'font_name': 'Arial',
            'font_color': '#1F4788'  # Dark blue
        })
        # Subheading - Large, bold, centered with color
        fmt_sub1 = workbook.add_format({
            'bold': True, 
            'font_size': 16, 
            'align': 'center',
            'valign': 'vcenter',
            'font_name': 'Arial',
            'font_color': '#2E5C8A'  # Medium blue
        })
        # Sub-subheading - Medium, bold, centered with color
        fmt_sub2 = workbook.add_format({
            'bold': True, 
            'font_size': 14, 
            'align': 'center',
            'valign': 'vcenter',
            'font_name': 'Arial',
            'font_color': '#365F91'  # Light blue
        })
        # Separator line format
        fmt_line = workbook.add_format({
            'bottom': 1,
            'bottom_color': '#000000'
        })
        
        # Set row heights for better appearance
        worksheet.set_row(start_row, 30)
        worksheet.set_row(start_row + 1, 25)
        worksheet.set_row(start_row + 2, 20)
        
        # Add logo if available
        logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
        if os.path.exists(logo_path):
            try:
                worksheet.insert_image(start_row, 0, logo_path, 
                                     {'x_scale': 0.3, 'y_scale': 0.3, 'x_offset': 5, 'y_offset': 5})
            except Exception as e:
                print(f"Could not add logo: {e}")
        
        # Merge cells for headers (assuming 7 columns minimum)
        worksheet.merge_range(start_row, 1, start_row, 6, "Government Polytechnic Awasari(Kh)", fmt_main)
        worksheet.merge_range(start_row + 1, 1, start_row + 1, 6, "Departmental Library", fmt_sub1)
        worksheet.merge_range(start_row + 2, 1, start_row + 2, 6, "Computer Department", fmt_sub2)
        
        # Add separator line
        for col in range(7):
            worksheet.write(start_row + 3, col, "", fmt_line)
        
        # Add blank row for spacing
        return start_row + 5

    def _auto_adjust_column_width(self, worksheet):
        """Auto-adjust column widths in openpyxl worksheet based on content with enhanced formatting"""
        try:
            # First, apply column formatting to data headers
            from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
            
            # Find data start row (after header)
            data_start_row = None
            for row in range(1, worksheet.max_row + 1):
                cell_value = worksheet.cell(row=row, column=1).value
                if cell_value and isinstance(cell_value, str) and any(header in cell_value.lower() for header in ['enrollment', 'book', 'student', 'name', 'id']):
                    data_start_row = row
                    break
            
            # Style data headers if found
            if data_start_row:
                header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
                header_font = Font(color='FFFFFF', bold=True, size=11, name='Calibri')
                header_alignment = Alignment(horizontal='center', vertical='center')
                header_border = Border(
                    left=Side(style='thin', color='FFFFFF'),
                    right=Side(style='thin', color='FFFFFF'),
                    top=Side(style='thin', color='FFFFFF'),
                    bottom=Side(style='thin', color='FFFFFF')
                )
                
                # Apply header styling
                for col in range(1, worksheet.max_column + 1):
                    cell = worksheet.cell(row=data_start_row, column=col)
                    if cell.value:  # Only style cells with content
                        cell.fill = header_fill
                        cell.font = header_font
                        cell.alignment = header_alignment
                        cell.border = header_border
            
            # Auto-adjust column widths based on content
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                
                for cell in column:
                    try:
                        if cell.value and not cell.coordinate.startswith('A'):  # Skip logo column
                            cell_length = len(str(cell.value))
                            if cell_length > max_length:
                                max_length = cell_length
                    except:
                        pass
                
                # Enhanced width calculation with better minimum and maximum
                if column_letter == 'A':  # Logo column
                    adjusted_width = 12
                elif max_length < 8:  # Short content
                    adjusted_width = 15
                elif max_length < 20:  # Medium content
                    adjusted_width = max_length + 6
                else:  # Long content
                    adjusted_width = min(max_length + 4, 65)
                
                worksheet.column_dimensions[column_letter].width = adjusted_width
            
            # Add alternating row colors for better readability
            if data_start_row:
                light_fill = PatternFill(start_color='F8F9FA', end_color='F8F9FA', fill_type='solid')
                data_border = Border(
                    left=Side(style='thin', color='E0E0E0'),
                    right=Side(style='thin', color='E0E0E0'),
                    top=Side(style='thin', color='E0E0E0'),
                    bottom=Side(style='thin', color='E0E0E0')
                )
                
                for row in range(data_start_row + 1, worksheet.max_row + 1):
                    if (row - data_start_row) % 2 == 0:  # Even rows
                        for col in range(1, worksheet.max_column + 1):
                            cell = worksheet.cell(row=row, column=col)
                            if not cell.coordinate.startswith('A'):  # Skip logo column
                                cell.fill = light_fill
                                cell.border = data_border
                                cell.alignment = Alignment(vertical='center')
                    else:  # Odd rows
                        for col in range(1, worksheet.max_column + 1):
                            cell = worksheet.cell(row=row, column=col)
                            if not cell.coordinate.startswith('A'):  # Skip logo column
                                cell.border = data_border
                                cell.alignment = Alignment(vertical='center')
                                
        except Exception as e:
            print(f"Could not auto-adjust columns: {e}")

    # =====================================================================
    # ANALYSIS TAB - Charts, Graphs, and Data Visualization
    # =====================================================================
    
    def create_analysis_tab(self):
        """Create comprehensive analysis tab using pie/donut charts only, with smooth scrolling"""
        analysis_frame = tk.Frame(self.notebook, bg=self.colors['primary'])
        self.notebook.add(analysis_frame, text="📊 Analysis")
        
        if not MATPLOTLIB_AVAILABLE:
            self.create_analysis_unavailable_message(analysis_frame)
            return
        
        # Main container with scrollable area (both directions)
        main_canvas = tk.Canvas(analysis_frame, bg=self.colors['primary'], highlightthickness=0)
        vscroll = ttk.Scrollbar(analysis_frame, orient="vertical", command=main_canvas.yview)
        hscroll = ttk.Scrollbar(analysis_frame, orient="horizontal", command=main_canvas.xview)
        scrollable_frame = tk.Frame(main_canvas, bg=self.colors['primary'])

        # Create a window inside the canvas and keep its ID to sync width
        window_id = main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def _on_frame_configure(event=None):
            # Update scroll region to include the whole inner frame
            main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        scrollable_frame.bind("<Configure>", _on_frame_configure)

        def _on_canvas_configure(event=None):
            # Make inner frame match canvas width for pleasant layout
            try:
                main_canvas.itemconfig(window_id, width=event.width)
            except Exception:
                pass
        main_canvas.bind("<Configure>", _on_canvas_configure)

        main_canvas.configure(yscrollcommand=vscroll.set, xscrollcommand=hscroll.set)

        # Mousewheel scrolling (Windows/Linux)
        def _wheel_units(delta):
            # Robust units across devices: at least 1 step
            if delta > 0:
                return -1
            elif delta < 0:
                return 1
            return 0
        def _on_vwheel(event):
            units = _wheel_units(event.delta)
            if units:
                main_canvas.yview_scroll(units, 'units')
            return 'break'
        def _on_hwheel(event):
            units = _wheel_units(event.delta)
            if units:
                main_canvas.xview_scroll(units, 'units')
            return 'break'
        # Bind locally to inner frame and canvas; avoid global bind/unbind to not break other tabs
        scrollable_frame.bind('<MouseWheel>', _on_vwheel)
        scrollable_frame.bind('<Shift-MouseWheel>', _on_hwheel)
        main_canvas.bind('<MouseWheel>', _on_vwheel)
        main_canvas.bind('<Shift-MouseWheel>', _on_hwheel)
        # Focus canvas when pointer enters so it receives wheel events
        main_canvas.bind('<Enter>', lambda e: main_canvas.focus_set())
        scrollable_frame.bind('<Enter>', lambda e: main_canvas.focus_set())
        # Linux fallbacks
        def _an_btn4(_e=None):
            main_canvas.yview_scroll(-1, 'units'); return 'break'
        def _an_btn5(_e=None):
            main_canvas.yview_scroll(1, 'units'); return 'break'
        main_canvas.bind('<Button-4>', _an_btn4)
        main_canvas.bind('<Button-5>', _an_btn5)
        # Additionally, pointer-scoped global binds when mouse enters/leaves this analysis tab
        def _enter_analysis(_e=None):
            try:
                analysis_frame.bind_all('<MouseWheel>', _on_vwheel, add='+')
                analysis_frame.bind_all('<Shift-MouseWheel>', _on_hwheel, add='+')
            except Exception:
                pass
        def _leave_analysis(_e=None):
            try:
                analysis_frame.unbind_all('<MouseWheel>')
                analysis_frame.unbind_all('<Shift-MouseWheel>')
            except Exception:
                pass
        analysis_frame.bind('<Enter>', _enter_analysis)
        analysis_frame.bind('<Leave>', _leave_analysis)
        # Helper so figures can hook wheel events too
        def _bind_analysis_wheel(widget):
            try:
                widget.bind('<MouseWheel>', _on_vwheel)
                widget.bind('<Shift-MouseWheel>', _on_hwheel)
            except Exception:
                pass
        self._analysis_bind_wheel = _bind_analysis_wheel

        # Pack scrollable components
        main_canvas.pack(side="top", fill="both", expand=True)
        vscroll.pack(side="right", fill="y")
        hscroll.pack(side="bottom", fill="x")
        
        # Header
        header_frame = tk.Frame(scrollable_frame, bg=self.colors['primary'])
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(
            header_frame,
            text="📊 Library Analytics Dashboard",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent']
        ).pack(side=tk.LEFT)
        
        # Time period filter
        period_frame = tk.LabelFrame(
            scrollable_frame,
            text="📅 Analysis Period",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent']
        )
        period_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        period_controls = tk.Frame(period_frame, bg=self.colors['primary'])
        period_controls.pack(padx=15, pady=15)
        
        self.analysis_period = tk.StringVar(value="7")
        
        periods = [
            ("Last 7 Days", "7"),
            ("Last 15 Days", "15"), 
            ("Last 30 Days", "30")
        ]
        
        for text, value in periods:
            rb = tk.Radiobutton(
                period_controls,
                text=text,
                variable=self.analysis_period,
                value=value,
                font=('Segoe UI', 11),
                bg=self.colors['primary'],
                fg=self.colors['accent'],
                selectcolor='white',
                command=self.refresh_analysis
            )
            rb.pack(side=tk.LEFT, padx=(0, 30))
        
        # Export controls
        export_frame = tk.Frame(period_frame, bg=self.colors['primary'])
        export_frame.pack(side=tk.RIGHT, padx=15, pady=15)
        
        export_excel_btn = tk.Button(
            export_frame,
            text="📊 Export to Excel",
            font=('Segoe UI', 10, 'bold'),
            bg='#28a745',
            fg='white',
            relief='flat',
            padx=15,
            pady=8,
            command=self.export_analysis_excel,
            cursor='hand2'
        )
        export_excel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        export_word_btn = tk.Button(
            export_frame,
            text="📄 Export to Word",
            font=('Segoe UI', 10, 'bold'),
            bg='#6f42c1',
            fg='white',
            relief='flat',
            padx=15,
            pady=8,
            command=self.export_analysis_word,
            cursor='hand2'
        )
        export_word_btn.pack(side=tk.LEFT)
        
        # Filter controls for student and book analytics
        filter_frame = tk.LabelFrame(
            scrollable_frame,
            text="🎯 Focused Analysis (Student / Book)",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent']
        )
        filter_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        self.analysis_student_var = tk.StringVar()
        self.analysis_book_var = tk.StringVar()

        ff_row = tk.Frame(filter_frame, bg=self.colors['primary'])
        ff_row.pack(fill=tk.X, padx=15, pady=12)

        tk.Label(ff_row, text="Enrollment No:", font=('Segoe UI', 10, 'bold'), bg=self.colors['primary'], fg=self.colors['accent']).pack(side=tk.LEFT)
        student_entry = tk.Entry(ff_row, textvariable=self.analysis_student_var, width=20)
        student_entry.pack(side=tk.LEFT, padx=(6, 18))

        tk.Label(ff_row, text="Book ID:", font=('Segoe UI', 10, 'bold'), bg=self.colors['primary'], fg=self.colors['accent']).pack(side=tk.LEFT)
        book_entry = tk.Entry(ff_row, textvariable=self.analysis_book_var, width=20)
        book_entry.pack(side=tk.LEFT, padx=(6, 18))

        tk.Button(
            ff_row,
            text="Apply Filter",
            font=('Segoe UI', 10, 'bold'),
            bg='#0FA958', fg='white', relief='flat', cursor='hand2',
            command=self.apply_analysis_filter
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            ff_row,
            text="Clear",
            font=('Segoe UI', 10, 'bold'),
            bg='#9e9e9e', fg='white', relief='flat', cursor='hand2',
            command=self.clear_analysis_filter
        ).pack(side=tk.LEFT)
        
        # Add Refresh Analysis button near the filters for easy access
        tk.Button(
            ff_row,
            text="🔄 Refresh Charts",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['secondary'], fg='white', relief='flat', cursor='hand2',
            command=self.refresh_analysis,
            activebackground=self.colors['accent']
        ).pack(side=tk.LEFT, padx=(20, 0))

        # Display current filter summary
        self.analysis_filter_summary = tk.Label(
            filter_frame,
            text="No focused filter applied",
            font=('Segoe UI', 10),
            bg=self.colors['primary'],
            fg='#555'
        )
        self.analysis_filter_summary.pack(anchor='w', padx=15, pady=(0, 10))

        # Focused (conditional) sections - place near the filter inputs
        self.focused_container = tk.Frame(scrollable_frame, bg=self.colors['primary'])
        self.focused_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        # Student-specific (left) and Book-specific (right)
        self.student_specific_frame = tk.LabelFrame(
            self.focused_container,
            text="👤 Student-specific Insights",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent']
        )
        self.book_specific_frame = tk.LabelFrame(
            self.focused_container,
            text="📖 Book-specific Insights",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent']
        )

    # Charts container
        charts_container = tk.Frame(scrollable_frame, bg=self.colors['primary'])
        charts_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Row 1: Pie charts
        pie_row = tk.Frame(charts_container, bg=self.colors['primary'])
        pie_row.pack(fill=tk.X, pady=(0, 20))
        
        # Borrowing Status Pie Chart
        self.borrow_status_frame = tk.LabelFrame(
            pie_row,
            text="📚 Book Status Distribution",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent']
        )
        self.borrow_status_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Student Activity Pie Chart
        self.student_activity_frame = tk.LabelFrame(
            pie_row,
            text="👥 Student Activity Distribution",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent']
        )
        self.student_activity_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Row 2: Advanced donut pie (Inventory & Overdue breakdown)
        advanced_row = tk.Frame(charts_container, bg=self.colors['primary'])
        advanced_row.pack(fill=tk.X, pady=(0, 20))

        self.inventory_overdue_frame = tk.LabelFrame(
            advanced_row,
            text="🍩 Inventory & Overdue Breakdown",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent']
        )
        self.inventory_overdue_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Row 3: Summary stats
        self.stats_summary_frame = tk.LabelFrame(
            charts_container,
            text="📋 Summary Statistics",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent']
        )
        self.stats_summary_frame.pack(fill=tk.X, pady=(0, 20))

        # Row 4: Popular & Least Popular Books
        books_popularity_row = tk.Frame(charts_container, bg=self.colors['primary'])
        books_popularity_row.pack(fill=tk.X, pady=(0, 20))
        
        self.popular_books_frame = tk.LabelFrame(
            books_popularity_row,
            text="📈 Most Popular Books (High Demand)",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent']
        )
        self.popular_books_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.least_popular_books_frame = tk.LabelFrame(
            books_popularity_row,
            text="📉 Least Popular Books (Low Demand)",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent']
        )
        self.least_popular_books_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # (Focused sections are now placed near the filter controls above)
        
    # Footer: compact mode and maintenance actions
        footer_frame = tk.Frame(scrollable_frame, bg=self.colors['primary'])
        footer_frame.pack(fill=tk.X, padx=20, pady=(10, 20))

        self.analysis_compact_mode = tk.BooleanVar(value=True)
        compact_cb = tk.Checkbutton(
            footer_frame,
            text="Compact Mode (show fewer charts)",
            variable=self.analysis_compact_mode,
            onvalue=True,
            offvalue=False,
            command=self.refresh_analysis,
            bg=self.colors['primary'],
            fg=self.colors['accent'],
            selectcolor='white'
        )
        compact_cb.pack(side=tk.LEFT)

        # Toggle to hide charts entirely (for super clean UI)
        self.analysis_show_charts = tk.BooleanVar(value=True)
        hide_cb = tk.Checkbutton(
            footer_frame,
            text="Show Charts",
            variable=self.analysis_show_charts,
            onvalue=True,
            offvalue=False,
            command=self.refresh_analysis,
            bg=self.colors['primary'],
            fg=self.colors['accent'],
            selectcolor='white'
        )
        hide_cb.pack(side=tk.LEFT, padx=(20, 0))

        # Manual refresh
        tk.Button(
            footer_frame,
            text="Refresh Analysis",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['secondary'], fg='white', relief='flat', padx=12, pady=4,
            cursor='hand2', command=self.refresh_analysis
        ).pack(side=tk.LEFT, padx=(20, 0))

        # Removed duplicate Promote Student button from footer; action available in header

        # Store chart references for click handling
        self.current_charts = {}
        # Filter state (None or string values)
        self.analysis_filter = {'enrollment_no': None, 'book_id': None}
        
        # Initial load
        self.refresh_analysis()
    
    def create_analysis_unavailable_message(self, parent):
        """Show message when matplotlib is not available"""
        container = tk.Frame(parent, bg=self.colors['primary'])
        container.pack(expand=True, fill=tk.BOTH)
        
        message_frame = tk.Frame(container, bg='white', relief='solid', bd=1)
        message_frame.place(relx=0.5, rely=0.5, anchor='center', width=600, height=400)
        
        tk.Label(
            message_frame,
            text="📊 Analysis Features Unavailable",
            font=('Segoe UI', 18, 'bold'),
            bg='white',
            fg=self.colors['accent']
        ).pack(pady=(40, 20))
        
        tk.Label(
            message_frame,
            text="The Analysis tab requires additional packages.\nPlease install the missing dependencies:",
            font=('Segoe UI', 12),
            bg='white',
            fg='#666666',
            justify='center'
        ).pack(pady=(0, 20))
        
        code_frame = tk.Frame(message_frame, bg='#f8f9fa', relief='solid', bd=1)
        code_frame.pack(padx=40, pady=20, fill=tk.X)
        
        tk.Label(
            code_frame,
            text="pip install matplotlib xlsxwriter",
            font=('Consolas', 11, 'bold'),
            bg='#f8f9fa',
            fg='#d73502'
        ).pack(pady=15)
        
        tk.Label(
            message_frame,
            text="After installation, restart the application to access charts and graphs.",
            font=('Segoe UI', 10),
            bg='white',
            fg='#666666'
        ).pack(pady=20)
    
    def refresh_analysis(self):
        """Refresh all analysis charts based on selected time period"""
        if not MATPLOTLIB_AVAILABLE:
            return
        
        # If charts are hidden, clear frames and show a small placeholder
        if hasattr(self, 'analysis_show_charts') and not self.analysis_show_charts.get():
            def _clear_and_placeholder(frame, text):
                for w in frame.winfo_children():
                    w.destroy()
                tk.Label(frame, text=text, font=('Segoe UI', 11), bg=self.colors['primary'], fg='#666').pack(expand=True, pady=20)
            _clear_and_placeholder(self.borrow_status_frame, "Charts hidden")
            _clear_and_placeholder(self.student_activity_frame, "Charts hidden")
            if hasattr(self, 'inventory_overdue_frame'):
                _clear_and_placeholder(self.inventory_overdue_frame, "Charts hidden")
            # Also clear summary
            for w in self.stats_summary_frame.winfo_children():
                w.destroy()
            tk.Label(self.stats_summary_frame, text="Charts are hidden. Enable 'Show Charts' to view.", font=('Segoe UI', 11), bg=self.colors['primary'], fg='#666').pack(pady=10)
            return

        # Clear existing widgets to avoid duplicates (charts, labels, legends)
        def _clear(frame):
            try:
                for w in frame.winfo_children():
                    w.destroy()
            except Exception:
                pass
        _clear(self.borrow_status_frame)
        _clear(self.student_activity_frame)
        if hasattr(self, 'daily_trend_frame'):
            _clear(self.daily_trend_frame)
        if hasattr(self, 'popular_books_frame'):
            _clear(self.popular_books_frame)
        if hasattr(self, 'least_popular_books_frame'):
            _clear(self.least_popular_books_frame)
        if hasattr(self, 'inventory_overdue_frame'):
            _clear(self.inventory_overdue_frame)
        _clear(self.stats_summary_frame)
        # Clear focused frames
        for w in self.student_specific_frame.winfo_children():
            if isinstance(w, FigureCanvasTkAgg):
                w.get_tk_widget().destroy()
            else:
                w.destroy()
        for w in self.book_specific_frame.winfo_children():
            if isinstance(w, FigureCanvasTkAgg):
                w.get_tk_widget().destroy()
            else:
                w.destroy()
        # Keep frames in place (they live near the filters); just clear content
        
        # Get time period
        days = int(self.analysis_period.get())
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        # Update filter summary label
        en = self.analysis_filter.get('enrollment_no')
        bk = self.analysis_filter.get('book_id')
        parts = []
        if en:
            s_name = self.get_student_name(en)
            parts.append(f"Student: {en} ({s_name or 'Unknown'})")
        if bk:
            b_title = self.get_book_title(bk)
            parts.append(f"Book: {bk} ({b_title or 'Unknown'})")
        self.analysis_filter_summary.config(text=' | '.join(parts) if parts else 'No focused filter applied')

        # Generate concise set of charts
        # Always show: Book Status (pie), Student Activity (pie), and Inventory/Overdue (donut)
        self.create_borrow_status_pie()
        self.create_student_activity_pie(days)
        self.create_inventory_overdue_donut()
        # Popular and Least Popular Books - always show for book demand analysis
        self.create_popular_books_chart(days)
        self.create_least_popular_books_chart(days)
        # Optional charts when Compact Mode is OFF
        if hasattr(self, 'analysis_compact_mode') and not self.analysis_compact_mode.get():
            self.create_daily_trend_chart(days)
        # Summary always
        self.create_summary_stats(days)

        # Focused insights
        # Pack side-by-side if any filter is present
        if en or bk:
            if en:
                if not self.student_specific_frame.winfo_manager():
                    self.student_specific_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
                self.create_student_specific_pie(days, en)
            if bk:
                if not self.book_specific_frame.winfo_manager():
                    self.book_specific_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
                self.create_book_specific_pie(days, bk)
    
    def create_borrow_status_pie(self):
        """Create pie chart showing book status distribution"""
        try:
            # Get data
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Count books by status
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN br.status = 'borrowed' THEN 'Currently Issued'
                        ELSE 'Available'
                    END as status,
                    COUNT(DISTINCT b.book_id) as count
                FROM books b
                LEFT JOIN borrow_records br ON b.book_id = br.book_id AND br.status = 'borrowed'
                GROUP BY status
            """)
            
            results = cursor.fetchall()
            conn.close()
            
            if not results:
                # Clear frame then show no-data message
                for w in self.borrow_status_frame.winfo_children():
                    w.destroy()
                tk.Label(
                    self.borrow_status_frame,
                    text="No books or borrow data to display",
                    font=('Segoe UI', 12), bg=self.colors['primary'], fg='#666'
                ).pack(expand=True, pady=20)
                return
            
            raw_labels = [row[0] for row in results]
            sizes = [row[1] for row in results]
            labels = [f"{name} ({cnt})" for name, cnt in zip(raw_labels, sizes)]
            # Colorblind-friendly palette
            colors = ['#0072B2', '#D55E00', '#F0E442', '#009E73', '#CC79A7', '#56B4E9']
            
            # Larger, modern figure with tight layout for legends
            fig = Figure(figsize=(6, 4), dpi=100)
            ax = fig.add_subplot(111)
            fig.patch.set_facecolor('white')
            fig.subplots_adjust(left=0.1, right=0.78)  # Make room for legend
            
            def on_pie_click(event):
                if event.inaxes == ax:
                    # Find which wedge was clicked
                    for i, (wedge, label, size) in enumerate(zip(ax.patches, labels, sizes)):
                        contains, info = wedge.contains(event)
                        if contains:
                            # Check the raw status name (not the formatted label with count)
                            status_name = raw_labels[i]
                            if status_name == 'Currently Issued':
                                self.show_currently_borrowed_dialog()
                            else:
                                self.show_available_books_dialog()
                            break
            
            def _autopct(pct, allvals=sizes):
                total = sum(allvals)
                val = int(round(pct*total/100.0))
                return f"{pct:.1f}%\n({val})"

            wedges, texts, autotexts = ax.pie(
                sizes, 
                labels=labels, 
                colors=colors[:len(sizes)],
                autopct=_autopct,
                startangle=90,
                wedgeprops=dict(width=0.32, edgecolor='white')  # donut style, slightly thinner
            )
            # Center label with total
            ax.text(0, 0, f"Total\n{sum(sizes)}", ha='center', va='center', fontsize=14, fontweight='bold', color='#333')
            ax.axis('equal')
            ax.set_title('Book Status Distribution', fontsize=16, fontweight='bold', color='#0072B2')
            # Add legend for clarity
            ax.legend(wedges, labels, title="Status", loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=10)
            
            # Clear any existing widgets in the frame
            for widget in self.borrow_status_frame.winfo_children():
                widget.destroy()
            
            # Add to GUI
            canvas = FigureCanvasTkAgg(fig, self.borrow_status_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            canvas.mpl_connect('button_press_event', on_pie_click)
            # Ensure wheel scrolling works when cursor is over the figure
            try:
                self._analysis_bind_wheel(canvas.get_tk_widget())
            except Exception:
                pass
            
            self.current_charts['borrow_status'] = (fig, labels, sizes)
            
        except Exception as e:
            print(f"Error creating borrow status pie chart: {e}")
    
    def create_student_activity_pie(self, days):
        """Create pie chart showing student activity levels"""
        try:
            # Get data
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            # Count students by activity level
            cursor.execute("""
                SELECT 
                    s.year,
                    COUNT(br.id) as borrow_count
                FROM students s
                LEFT JOIN borrow_records br ON s.enrollment_no = br.enrollment_no 
                    AND br.borrow_date >= ?
                GROUP BY s.year
                HAVING borrow_count > 0
                ORDER BY borrow_count DESC
            """, (start_date,))
            
            results = cursor.fetchall()
            conn.close()
            
            if not results:
                # Always render a placeholder donut so the chart area is not blank
                fig = Figure(figsize=(6, 4), dpi=100)
                ax = fig.add_subplot(111)
                fig.patch.set_facecolor('white')
                fig.subplots_adjust(left=0.1, right=0.78)

                sizes = [1]
                labels = ["No Activity"]
                colors = ['#d0d7de']  # light gray
                wedges, texts = ax.pie(
                    sizes,
                    labels=None,
                    colors=colors,
                    startangle=90,
                    wedgeprops=dict(width=0.32, edgecolor='white')
                )
                ax.text(0, 0, "No Data", ha='center', va='center', fontsize=14, fontweight='bold', color='#666')
                ax.axis('equal')
                ax.set_title(f'Student Activity (Last {days} Days)', fontsize=16, fontweight='bold', color='#D55E00')
                ax.legend(wedges, labels, title="Year", loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=10)

                for w in self.student_activity_frame.winfo_children():
                    w.destroy()
                canvas = FigureCanvasTkAgg(fig, self.student_activity_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                try:
                    self._analysis_bind_wheel(canvas.get_tk_widget())
                except Exception:
                    pass
                self.current_charts['student_activity'] = (fig, labels, sizes)
                return
            
            def _format_year_label(y):
                if y is None:
                    return "Unknown"
                s = str(y).strip()
                low = s.lower()
                # Normalize any variant that mentions pass + out to 'Pass Out'
                if ("pass" in low) and ("out" in low):
                    return "Pass Out"
                # If it already contains the word 'year', keep as-is with title casing
                if "year" in low:
                    return s.title()
                # Otherwise append 'Year' to numeric/ordinal
                return f"{s} Year"

            raw_labels = [_format_year_label(row[0]) for row in results]
            sizes = [row[1] for row in results]
            # Keep legend labels short to avoid truncation
            labels = list(raw_labels)
            # Colorblind-friendly palette
            colors = ['#0072B2', '#D55E00', '#F0E442', '#009E73', '#CC79A7', '#56B4E9']
            
            # Larger, modern figure with tight layout for legends
            fig = Figure(figsize=(6, 4), dpi=100)
            ax = fig.add_subplot(111)
            fig.patch.set_facecolor('white')
            fig.subplots_adjust(left=0.1, right=0.78)  # Make room for legend
            
            def on_activity_click(event):
                if event.inaxes == ax:
                    for i, (wedge, label, size) in enumerate(zip(ax.patches, labels, sizes)):
                        contains, info = wedge.contains(event)
                        if contains:
                            year = results[i][0]
                            self.show_students_by_year_dialog(year, days)
                            break
            
            # Explode the largest slice slightly for emphasis
            if sizes:
                max_idx = sizes.index(max(sizes))
                explode = [0.08 if i == max_idx else 0 for i in range(len(sizes))]
            else:
                explode = None

            # Build pie with labels and percentages
            def autopct_format(pct):
                return f'{pct:.1f}%' if pct > 5 else ''
            
            wedges, texts, autotexts = ax.pie(
                sizes,
                labels=labels,  # Show labels on slices
                colors=colors[:len(sizes)],
                autopct=autopct_format,
                startangle=90,
                explode=explode,
                wedgeprops=dict(width=0.32, edgecolor='white'),  # donut style, thinner
                textprops={'fontsize': 10, 'weight': 'bold'}
            )
            # Make percentage text black for better visibility
            for autotext in autotexts:
                autotext.set_color('black')
            
            ax.text(0, 0, f"Total\n{sum(sizes)}", ha='center', va='center', fontsize=14, fontweight='bold', color='#333')
            ax.axis('equal')
            ax.set_title(f'Student Activity (Last {days} Days)', fontsize=16, fontweight='bold', color='#D55E00')
            
            # Clear any existing widgets in the frame
            for widget in self.student_activity_frame.winfo_children():
                widget.destroy()
            
            # Add to GUI
            canvas = FigureCanvasTkAgg(fig, self.student_activity_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            canvas.mpl_connect('button_press_event', on_activity_click)
            try:
                self._analysis_bind_wheel(canvas.get_tk_widget())
            except Exception:
                pass
            
            self.current_charts['student_activity'] = (fig, labels, sizes)
            
        except Exception as e:
            try:
                for w in self.student_activity_frame.winfo_children():
                    w.destroy()
                tk.Label(
                    self.student_activity_frame,
                    text="Unable to render chart",
                    font=('Segoe UI', 12),
                    bg=self.colors['primary'],
                    fg='#b00020'
                ).pack(expand=True, pady=20)
            except Exception:
                pass
            print(f"Error creating student activity pie chart: {e}")

    def create_inventory_overdue_donut(self):
        """Create a nested donut pie showing Available vs Issued (outer), and inner ring splitting Issued into On-time vs Overdue."""
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            # Sum copies
            cur.execute("SELECT COALESCE(SUM(total_copies),0), COALESCE(SUM(available_copies),0) FROM books")
            total_copies, total_available = cur.fetchone()
            total_issued = max((total_copies or 0) - (total_available or 0), 0)
            # Overdue issued count (by transactions)
            today = datetime.now().strftime('%Y-%m-%d')
            cur.execute("SELECT COUNT(*) FROM borrow_records WHERE status='borrowed' AND due_date < ?", (today,))
            overdue = cur.fetchone()[0] or 0
            conn.close()

            on_time = max(total_issued - overdue, 0)

            outer_labels = ["Available", "Issued"]
            outer_sizes = [total_available, total_issued]
            inner_labels = ["Available", "On-time", "Overdue"]
            inner_sizes = [total_available, on_time, overdue]

            # Colors
            outer_colors = ['#2ed573', '#ff9f43']
            inner_colors = ['#7bed9f', '#ffa502', '#ff4757']

            # Build figure
            fig = Figure(figsize=(6, 4), dpi=100)
            ax = fig.add_subplot(111)
            fig.patch.set_facecolor('white')

            # Outer ring
            wedges1, _ = ax.pie(outer_sizes, radius=1.0, labels=outer_labels, labeldistance=1.05,
                                colors=outer_colors, startangle=90, wedgeprops=dict(width=0.3, edgecolor='white'))

            # Inner ring
            def _autopct(pct, allvals=inner_sizes):
                total = sum(allvals)
                val = int(round(pct*total/100.0))
                return f"{pct:.1f}%\n({val})"
            wedges2, _, _ = ax.pie(inner_sizes, radius=1.0-0.3, labels=None,
                                   colors=inner_colors, startangle=90,
                                   autopct=_autopct,
                                   wedgeprops=dict(width=0.3, edgecolor='white'))

            # Center text
            ax.text(0, 0, f"Total\n{int(total_copies or 0)}", ha='center', va='center', fontsize=11, fontweight='bold')
            ax.set_title('Inventory & Overdue Breakdown', fontsize=12, fontweight='bold')

            # Legend shows inner ring details
            ax.legend(wedges2, inner_labels, title="Details", loc='center left', bbox_to_anchor=(1.0, 0.5))

            canvas = FigureCanvasTkAgg(fig, self.inventory_overdue_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            try:
                self._analysis_bind_wheel(canvas.get_tk_widget())
            except Exception:
                pass

            self.current_charts['inventory_overdue_donut'] = (fig, inner_labels, inner_sizes)
        except Exception as e:
            print(f"Error creating inventory/overdue donut: {e}")
    
    def create_daily_trend_chart(self, days):
        """Create bar chart showing daily borrowing trends"""
        try:
            # Get data
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            cursor.execute("""
                SELECT 
                    borrow_date,
                    COUNT(*) as daily_count
                FROM borrow_records 
                WHERE borrow_date >= ?
                GROUP BY borrow_date
                ORDER BY borrow_date
            """, (start_date,))
            
            results = cursor.fetchall()
            conn.close()
            
            if not results:
                no_data_label = tk.Label(
                    self.daily_trend_frame,
                    text=f"No borrowing activity\nin last {days} days",
                    font=('Segoe UI', 12),
                    bg=self.colors['primary'],
                    fg='#666666'
                )
                no_data_label.pack(expand=True)
                return
            
            dates = [row[0] for row in results]
            counts = [row[1] for row in results]
            
            # Create figure
            fig = Figure(figsize=(6, 4), dpi=100)
            ax = fig.add_subplot(111)
            
            bars = ax.bar(dates, counts, color='#45b7d1', alpha=0.7)
            ax.set_title(f'Daily Borrowing Trends (Last {days} Days)', fontsize=12, fontweight='bold')
            ax.set_xlabel('Date')
            ax.set_ylabel('Books Issued')
            
            # Rotate x-axis labels for better readability
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            
            # Add click interaction
            def on_bar_click(event):
                if event.inaxes == ax:
                    for i, bar in enumerate(bars):
                        contains, info = bar.contains(event)
                        if contains:
                            self.show_borrow_details_for_date(dates[i])
                            break
            
            fig.tight_layout()
            
            # Add to GUI
            canvas = FigureCanvasTkAgg(fig, self.daily_trend_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            canvas.mpl_connect('button_press_event', on_bar_click)
            
            self.current_charts['daily_trend'] = (fig, dates, counts)
            
        except Exception as e:
            print(f"Error creating daily trend chart: {e}")
    
    def create_popular_books_chart(self, days):
        """Create bar chart showing most popular books"""
        try:
            # Get data
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            cursor.execute("""
                SELECT 
                    b.title,
                    COUNT(br.id) as borrow_count
                FROM books b
                INNER JOIN borrow_records br ON b.book_id = br.book_id
                WHERE br.borrow_date >= ?
                GROUP BY b.book_id, b.title
                ORDER BY borrow_count DESC
                LIMIT 10
            """, (start_date,))
            
            results = cursor.fetchall()
            conn.close()
            
            if not results:
                no_data_label = tk.Label(
                    self.popular_books_frame,
                    text=f"No borrowing activity\nin last {days} days",
                    font=('Segoe UI', 12),
                    bg=self.colors['primary'],
                    fg='#666666'
                )
                no_data_label.pack(expand=True)
                return
            
            titles = [row[0][:20] + ('...' if len(row[0]) > 20 else '') for row in results]
            counts = [row[1] for row in results]
            
            # Create figure
            fig = Figure(figsize=(6, 4), dpi=100)
            ax = fig.add_subplot(111)
            
            bars = ax.barh(titles, counts, color='#f9ca24', alpha=0.7)
            ax.set_title(f'Most Popular Books (Last {days} Days)', fontsize=12, fontweight='bold')
            ax.set_xlabel('Times Issued')
            
            # Add click interaction
            def on_popular_click(event):
                if event.inaxes == ax:
                    for i, bar in enumerate(bars):
                        contains, info = bar.contains(event)
                        if contains:
                            # Show all students who borrowed that book in period
                            full_title = results[i][0]
                            self.show_book_borrowers_dialog(full_title, days)
                            break
            
            fig.tight_layout()
            
            # Add to GUI
            canvas = FigureCanvasTkAgg(fig, self.popular_books_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            canvas.mpl_connect('button_press_event', on_popular_click)
            
            self.current_charts['popular_books'] = (fig, titles, counts)
            
        except Exception as e:
            print(f"Error creating popular books chart: {e}")

    def create_least_popular_books_chart(self, days):
        """Create bar chart showing least popular books (books with least borrows or zero borrows)"""
        try:
            # Get data
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            # Get books with lowest borrow count in the period (including zero borrows)
            cursor.execute("""
                SELECT 
                    b.title,
                    COALESCE(COUNT(br.id), 0) as borrow_count
                FROM books b
                LEFT JOIN borrow_records br ON b.book_id = br.book_id AND br.borrow_date >= ?
                GROUP BY b.book_id, b.title
                ORDER BY borrow_count ASC, b.title
                LIMIT 10
            """, (start_date,))
            
            results = cursor.fetchall()
            conn.close()
            
            if not results:
                no_data_label = tk.Label(
                    self.least_popular_books_frame,
                    text=f"No book data available",
                    font=('Segoe UI', 12),
                    bg=self.colors['primary'],
                    fg='#666666'
                )
                no_data_label.pack(expand=True)
                return
            
            titles = [row[0][:20] + ('...' if len(row[0]) > 20 else '') for row in results]
            counts = [row[1] for row in results]
            
            # Create figure
            fig = Figure(figsize=(6, 4), dpi=100)
            ax = fig.add_subplot(111)
            
            bars = ax.barh(titles, counts, color='#e74c3c', alpha=0.7)
            ax.set_title(f'Least Popular Books (Last {days} Days)', fontsize=12, fontweight='bold')
            ax.set_xlabel('Times Issued')
            
            # Add click interaction
            def on_least_popular_click(event):
                if event.inaxes == ax:
                    for i, bar in enumerate(bars):
                        contains, info = bar.contains(event)
                        if contains:
                            # Show all students who borrowed that book in period (if any)
                            full_title = results[i][0]
                            self.show_book_borrowers_dialog(full_title, days)
                            break
            
            fig.tight_layout()
            
            # Add to GUI
            canvas = FigureCanvasTkAgg(fig, self.least_popular_books_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            canvas.mpl_connect('button_press_event', on_least_popular_click)
            
            self.current_charts['least_popular_books'] = (fig, titles, counts)
            
        except Exception as e:
            print(f"Error creating least popular books chart: {e}")

    # ---------------------- Focused Insights ----------------------
    def create_student_specific_pie(self, days, enrollment_no):
        """Pie: student's borrow status in period (borrowed vs returned)."""
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            cur.execute("SELECT COUNT(*) FROM borrow_records WHERE enrollment_no=? AND borrow_date>=?", (enrollment_no, start_date))
            total = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM borrow_records WHERE enrollment_no=? AND borrow_date>=? AND status='borrowed'", (enrollment_no, start_date))
            active = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM borrow_records WHERE enrollment_no=? AND return_date>=? AND return_date IS NOT NULL", (enrollment_no, start_date))
            returned = cur.fetchone()[0]
            conn.close()
            sizes = [active, returned]
            labels = ["Currently Issued", "Returned"]
            if sum(sizes) == 0:
                lbl = tk.Label(self.student_specific_frame, text=f"No activity for {enrollment_no} in last {days} days", bg=self.colors['primary'], fg='#666', font=('Segoe UI', 11))
                lbl.pack(fill=tk.X, padx=10, pady=10)
            else:
                fig = Figure(figsize=(4.5, 3.5), dpi=100)
                ax = fig.add_subplot(111)
                ax.pie(sizes, labels=labels, colors=['#ff9f43', '#10ac84'], autopct='%1.1f%%', startangle=90)
                ax.set_title(f"Student {enrollment_no} - Status (Last {days}d)", fontsize=11, fontweight='bold')
                canvas = FigureCanvasTkAgg(fig, self.student_specific_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
                self.current_charts['student_specific_status'] = (fig, labels, sizes)

            # packing handled in refresh_analysis
        except Exception as e:
            print(f"Student-specific pie error: {e}")

    def create_book_specific_pie(self, days, book_id):
        """Pie: book's copies status currently (available vs borrowed)."""
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT title, total_copies, available_copies FROM books WHERE book_id=?", (book_id,))
            row = cur.fetchone()
            conn.close()
            if not row:
                lbl = tk.Label(self.book_specific_frame, text=f"Book {book_id} not found", bg=self.colors['primary'], fg='#c00', font=('Segoe UI', 11, 'bold'))
                lbl.pack(fill=tk.X, padx=10, pady=10)
            else:
                title, total, avail = row
                borrowed = max(total - (avail or 0), 0)
                sizes = [avail or 0, borrowed]
                labels = ["Available", "Borrowed"]
                fig = Figure(figsize=(4.5, 3.5), dpi=100)
                ax = fig.add_subplot(111)
                ax.pie(sizes, labels=labels, colors=['#2ed573', '#ff4757'], autopct='%1.1f%%', startangle=90)
                ax.set_title(f"Book {book_id} - Copies Status", fontsize=11, fontweight='bold')
                canvas = FigureCanvasTkAgg(fig, self.book_specific_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
                self.current_charts['book_specific_status'] = (fig, labels, sizes)

            # packing handled in refresh_analysis
        except Exception as e:
            print(f"Book-specific pie error: {e}")

    # ---------------------- Drill-down Dialogs ----------------------
    def show_currently_borrowed_dialog(self):
        """Show all currently borrowed items with student and book details, respecting filters if set."""
        en = self.analysis_filter.get('enrollment_no')
        bk = self.analysis_filter.get('book_id')
        conn = self.db.get_connection()
        cur = conn.cursor()
        base = (
            "SELECT br.enrollment_no, s.name, br.book_id, b.title, br.borrow_date, br.due_date "
            "FROM borrow_records br JOIN students s ON br.enrollment_no=s.enrollment_no "
            "JOIN books b ON br.book_id=b.book_id WHERE br.status='borrowed'"
        )
        params = []
        if en:
            base += " AND br.enrollment_no=?"
            params.append(en)
        if bk:
            base += " AND br.book_id=?"
            params.append(bk)
        base += " ORDER BY br.due_date"
        cur.execute(base, tuple(params))
        rows = cur.fetchall()
        conn.close()
        cols = ("Enrollment No", "Student Name", "Book ID", "Book Title", "Issue Date", "Due Date")
        self._show_table_dialog("Currently Issued", cols, rows, export_name="currently_issued")

    def show_available_books_dialog(self):
        """Show all books with available copies > 0 (optionally filtered by book_id)."""
        bk = self.analysis_filter.get('book_id')
        conn = self.db.get_connection()
        cur = conn.cursor()
        if bk:
            cur.execute("SELECT book_id, title, author, available_copies FROM books WHERE book_id=?", (bk,))
        else:
            cur.execute("SELECT book_id, title, author, available_copies FROM books WHERE available_copies>0 ORDER BY title")
        rows = cur.fetchall()
        conn.close()
        cols = ("Book ID", "Title", "Author", "Available Copies")
        self._show_table_dialog("Available Books", cols, rows, export_name="available_books")

    def show_students_by_year_dialog(self, year, days):
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        conn = self.db.get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT s.enrollment_no, s.name, COUNT(br.id) as borrows FROM students s "
            "LEFT JOIN borrow_records br ON s.enrollment_no=br.enrollment_no AND br.borrow_date>=? "
            "WHERE s.year=? GROUP BY s.enrollment_no, s.name HAVING borrows>0 ORDER BY borrows DESC",
            (start_date, year)
        )
        rows = cur.fetchall()
        conn.close()
        cols = ("Enrollment No", "Name", "Issue Count")
        self._show_table_dialog(f"Students in {year} Year", cols, rows, export_name=f"students_year_{year}")

    def show_borrow_details_for_date(self, date_str):
        en = self.analysis_filter.get('enrollment_no')
        bk = self.analysis_filter.get('book_id')
        conn = self.db.get_connection()
        cur = conn.cursor()
        q = (
            "SELECT br.borrow_date, br.enrollment_no, s.name, br.book_id, b.title FROM borrow_records br "
            "JOIN students s ON br.enrollment_no=s.enrollment_no JOIN books b ON br.book_id=b.book_id "
            "WHERE br.borrow_date=?"
        )
        params = [date_str]
        if en:
            q += " AND br.enrollment_no=?"; params.append(en)
        if bk:
            q += " AND br.book_id=?"; params.append(bk)
        q += " ORDER BY s.name"
        cur.execute(q, tuple(params))
        rows = cur.fetchall()
        conn.close()
        cols = ("Issue Date", "Enrollment No", "Student Name", "Book ID", "Book Title")
        self._show_table_dialog(f"Issues on {date_str}", cols, rows, export_name=f"issues_{date_str}")

    def show_book_borrowers_dialog(self, title, days):
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        conn = self.db.get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT br.enrollment_no, s.name, COUNT(br.id) as n FROM borrow_records br "
            "JOIN students s ON br.enrollment_no=s.enrollment_no JOIN books b ON br.book_id=b.book_id "
            "WHERE b.title=? AND br.borrow_date>=? GROUP BY br.enrollment_no, s.name ORDER BY n DESC",
            (title, start_date)
        )
        rows = cur.fetchall()
        conn.close()
        cols = ("Enrollment No", "Student Name", "Times Issued")
        self._show_table_dialog(f"Issuers of '{title}' (Last {days}d)", cols, rows, export_name="book_issuers")

    # Generic dialog with export
    def _show_table_dialog(self, title, columns, rows, export_name="data_export"):
        dlg = tk.Toplevel(self.root)
        dlg.title(title)
        dlg.geometry("800x500")
        frm = tk.Frame(dlg, bg=self.colors['primary'])
        frm.pack(fill=tk.BOTH, expand=True)
        tv = ttk.Treeview(frm, columns=[f"c{i}" for i in range(len(columns))], show='headings')
        for i, c in enumerate(columns):
            tv.heading(f"c{i}", text=c)
            tv.column(f"c{i}", width=max(100, int(750/len(columns))))
        vsb = ttk.Scrollbar(frm, orient='vertical', command=tv.yview)
        tv.configure(yscroll=vsb.set)
        tv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        for r in rows:
            tv.insert('', tk.END, values=r)
        btns = tk.Frame(dlg, bg=self.colors['primary'])
        btns.pack(fill=tk.X)
        def do_export():
            if not rows:
                messagebox.showinfo("Export", "No data to export.")
                return
            filename = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[["Excel", "*.xlsx"]], initialfile=f"{export_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
            if not filename:
                return
            try:
                import xlsxwriter
                wb = xlsxwriter.Workbook(filename)
                ws = wb.add_worksheet('Data')
                start = self._xlsxwriter_write_header(ws, wb, start_row=0)
                for j, c in enumerate(columns):
                    ws.write(start, j, c)
                for i, row in enumerate(rows, start=start+1):
                    for j, v in enumerate(row):
                        ws.write(i, j, v)
                wb.close()
                messagebox.showinfo("Export", f"Saved to {filename}")
                if messagebox.askyesno("Open File", "Open the exported file?"):
                    self.open_file(filename)
            except Exception as e:
                messagebox.showerror("Export", f"Failed to export: {e}")
        tk.Button(btns, text="Export to Excel", command=do_export, bg='#28a745', fg='white', relief='flat', padx=10, pady=6).pack(side=tk.RIGHT, padx=10, pady=8)

    # ---------------------- Filter handlers ----------------------
    def apply_analysis_filter(self):
        en = self.analysis_student_var.get().strip() or None
        bk = self.analysis_book_var.get().strip() or None
        # Validate existence lightly (non-blocking)
        if en and not self.get_student_name(en):
            if not messagebox.askyesno("Unknown Student", f"Enrollment {en} not found. Apply filter anyway?"):
                return
        if bk and not self.get_book_title(bk):
            if not messagebox.askyesno("Unknown Book", f"Book ID {bk} not found. Apply filter anyway?"):
                return
        self.analysis_filter = {'enrollment_no': en, 'book_id': bk}
        self.refresh_analysis()

    def clear_analysis_filter(self):
        self.analysis_student_var.set('')
        self.analysis_book_var.set('')
        self.analysis_filter = {'enrollment_no': None, 'book_id': None}
        self.refresh_analysis()

    # ---------------------- Helpers ----------------------
    def get_student_name(self, enrollment_no):
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT name FROM students WHERE enrollment_no=?", (enrollment_no,))
            row = cur.fetchone()
            conn.close()
            return row[0] if row else None
        except Exception:
            return None

    def get_book_title(self, book_id):
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT title FROM books WHERE book_id=?", (book_id,))
            row = cur.fetchone()
            conn.close()
            return row[0] if row else None
        except Exception:
            return None
    
    def create_summary_stats(self, days):
        """Create summary statistics display"""
        try:
            # Get comprehensive stats
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            # Total borrowings in period
            cursor.execute("SELECT COUNT(*) FROM borrow_records WHERE borrow_date >= ?", (start_date,))
            total_borrowings = cursor.fetchone()[0]
            
            # Total returns in period
            cursor.execute("SELECT COUNT(*) FROM borrow_records WHERE return_date >= ? AND return_date IS NOT NULL", (start_date,))
            total_returns = cursor.fetchone()[0]
            
            # Currently overdue
            today = datetime.now().strftime('%Y-%m-%d')
            cursor.execute("SELECT COUNT(*) FROM borrow_records WHERE status = 'borrowed' AND due_date < ?", (today,))
            overdue_count = cursor.fetchone()[0]
            
            # Active students (who borrowed in period)
            cursor.execute("SELECT COUNT(DISTINCT enrollment_no) FROM borrow_records WHERE borrow_date >= ?", (start_date,))
            active_students = cursor.fetchone()[0]
            
            # Total fines collected (approximation)
            cursor.execute("""
                SELECT SUM(
                    CASE 
                        WHEN return_date > due_date 
                        THEN (julianday(return_date) - julianday(due_date)) * ?
                        ELSE 0 
                    END
                ) as total_fines
                FROM borrow_records 
                WHERE return_date >= ? AND return_date IS NOT NULL
            """, (FINE_PER_DAY, start_date))
            
            total_fines = cursor.fetchone()[0] or 0
            
            conn.close()
            
            # Create stats display
            stats_container = tk.Frame(self.stats_summary_frame, bg=self.colors['primary'])
            stats_container.pack(fill=tk.X, padx=15, pady=15)
            
            stats = [
                ("📚 Total Borrowings", total_borrowings, "#4ecdc4"),
                ("📥 Total Returns", total_returns, "#45b7d1"),
                ("⚠️ Currently Overdue", overdue_count, "#ff6b6b"),
                ("👥 Active Students", active_students, "#f9ca24"),
                (f"💰 Fines Collected (₹{FINE_PER_DAY}/day)", f"₹{total_fines:.0f}", "#a55eea")
            ]
            
            for i, (label, value, color) in enumerate(stats):
                stat_frame = tk.Frame(stats_container, bg=color, relief='flat', bd=0)
                stat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
                
                tk.Label(
                    stat_frame,
                    text=str(value),
                    font=('Segoe UI', 18, 'bold'),
                    bg=color,
                    fg='white'
                ).pack(pady=(15, 5))
                
                tk.Label(
                    stat_frame,
                    text=label,
                    font=('Segoe UI', 10, 'bold'),
                    bg=color,
                    fg='white'
                ).pack(pady=(0, 15))
            
        except Exception as e:
            print(f"Error creating summary stats: {e}")
    
    def export_analysis_excel(self):
        """Export analysis charts and data to Excel with embedded charts"""
        try:
            if not XLSXWRITER_AVAILABLE:
                messagebox.showerror("Export Error", "xlsxwriter package is required for Excel export with charts.\n\nPlease install: pip install xlsxwriter")
                return
            
            days = int(self.analysis_period.get())
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            # File dialog
            filename = f"library_analysis_{days}days_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                initialfile=filename
            )
            
            if not file_path:
                return
            
            # Create workbook
            workbook = xlsxwriter.Workbook(file_path)
            
            # Add formats
            header_format = workbook.add_format({'bold': True, 'font_size': 14, 'bg_color': '#4ecdc4', 'font_color': 'white'})
            subheader_format = workbook.add_format({'bold': True, 'font_size': 12, 'bg_color': '#f0f0f0'})
            
            # Summary worksheet
            summary_ws = workbook.add_worksheet('Analysis Summary')
            # Three-line header requested by user
            row = self._xlsxwriter_write_header(summary_ws, workbook, start_row=0)
            summary_ws.write(row, 0, f'Library Analysis Report - Last {days} Days', header_format)
            summary_ws.write(row + 1, 0, f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
            row += 3
            
            # Get and write summary data
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Book status data
            summary_ws.write(row, 0, 'Book Status Distribution', subheader_format)
            row += 1
            
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN br.status = 'borrowed' THEN 'Currently Issued'
                        ELSE 'Available'
                    END as status,
                    COUNT(DISTINCT b.book_id) as count
                FROM books b
                LEFT JOIN borrow_records br ON b.book_id = br.book_id AND br.status = 'borrowed'
                GROUP BY status
            """)
            
            book_status_data = cursor.fetchall()
            for i, (status, count) in enumerate(book_status_data):
                summary_ws.write(row + i, 0, status)
                summary_ws.write(row + i, 1, count)
            
            row += len(book_status_data) + 2
            
            # Student activity data
            summary_ws.write(row, 0, f'Student Activity (Last {days} Days)', subheader_format)
            row += 1
            
            cursor.execute("""
                SELECT 
                    s.year,
                    COUNT(br.id) as borrow_count
                FROM students s
                LEFT JOIN borrow_records br ON s.enrollment_no = br.enrollment_no 
                    AND br.borrow_date >= ?
                GROUP BY s.year
                HAVING borrow_count > 0
                ORDER BY borrow_count DESC
            """, (start_date,))
            
            student_activity_data = cursor.fetchall()
            for i, (year, count) in enumerate(student_activity_data):
                summary_ws.write(row + i, 0, f"{year} Year")
                summary_ws.write(row + i, 1, count)
            
            conn.close()

            # Insert chart images for the current on-screen charts
            def fig_to_image_bytes(fig):
                bio = BytesIO()
                fig.savefig(bio, format='png', dpi=120, bbox_inches='tight')
                bio.seek(0)
                return bio

            img_row = row + len(student_activity_data) + 3
            summary_ws.write(img_row, 0, 'Charts Snapshot', subheader_format)
            img_row += 1
            col = 0
            for key in ['borrow_status', 'student_activity', 'daily_trend', 'popular_books', 'student_specific_status', 'book_specific_status']:
                if key in self.current_charts and isinstance(self.current_charts[key][0], Figure):
                    fig = self.current_charts[key][0]
                    try:
                        bio = fig_to_image_bytes(fig)
                        summary_ws.insert_image(img_row, col, f"{key}.png", {'image_data': bio, 'x_scale': 0.9, 'y_scale': 0.9})
                        col += 8  # move to the right for next image
                        if col > 8:
                            img_row += 20
                            col = 0
                    except Exception as e:
                        print(f"Failed to insert image for {key}: {e}")

            workbook.close()
            
            messagebox.showinfo("Export Successful", f"Analysis exported to:\n{file_path}")
            
            # Ask if user wants to open the file
            if messagebox.askyesno("Open File", "Do you want to open the exported file?"):
                self.open_file(file_path)
                
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export analysis: {str(e)}")
    
    def export_analysis_word(self):
        """Export analysis summary to Word document"""
        try:
            if Document is None:
                messagebox.showerror("Export Error", "python-docx package is required for Word export.\n\nPlease install: pip install python-docx")
                return
            
            days = int(self.analysis_period.get())
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            # File dialog
            filename = f"library_analysis_{days}days_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".docx",
                filetypes=[("Word documents", "*.docx")],
                initialfile=filename
            )
            
            if not file_path:
                return
            
            # Create document
            doc = Document()
            
            # Add logo at the top if available
            logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
            if os.path.exists(logo_path):
                try:
                    logo_para = doc.add_paragraph()
                    logo_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    logo_run = logo_para.add_run()
                    logo_run.add_picture(logo_path, width=Pt(60))
                except Exception as e:
                    print(f"Could not add logo: {e}")
            
            # Institutional Header with colors
            def add_colored_center(text, size, rgb):
                from docx.shared import RGBColor
                p = doc.add_paragraph()
                run = p.add_run(text)
                run.bold = True
                run.font.size = Pt(size)
                run.font.color.rgb = RGBColor(*rgb)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            add_colored_center("Government Polytechnic Awasari (Kh)", 22, (31, 71, 136))
            add_colored_center("Departmental Library", 18, (46, 92, 138))
            add_colored_center("Computer Department", 16, (54, 95, 145))
            
            # Add separator line
            doc.add_paragraph("_" * 60).alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            # Header
            header = doc.add_heading(f'Library Analysis Report', 0)
            header.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            # Metadata
            doc.add_paragraph(f'Analysis Period: Last {days} Days')
            doc.add_paragraph(f'Date Range: {start_date} to {datetime.now().strftime("%Y-%m-%d")}')
            doc.add_paragraph(f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            doc.add_paragraph('')
            
            # Get data
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Summary statistics
            doc.add_heading('Summary Statistics', level=1)
            
            cursor.execute("SELECT COUNT(*) FROM borrow_records WHERE borrow_date >= ?", (start_date,))
            total_borrowings = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM borrow_records WHERE return_date >= ? AND return_date IS NOT NULL", (start_date,))
            total_returns = cursor.fetchone()[0]
            
            today = datetime.now().strftime('%Y-%m-%d')
            cursor.execute("SELECT COUNT(*) FROM borrow_records WHERE status = 'borrowed' AND due_date < ?", (today,))
            overdue_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT enrollment_no) FROM borrow_records WHERE borrow_date >= ?", (start_date,))
            active_students = cursor.fetchone()[0]
            
            stats_table = doc.add_table(rows=5, cols=2)
            stats_table.style = 'Table Grid'
            
            stats_data = [
                ('Total Borrowings', total_borrowings),
                ('Total Returns', total_returns), 
                ('Currently Overdue', overdue_count),
                ('Active Students', active_students),
                ('Analysis Period', f'{days} days')
            ]
            
            for i, (metric, value) in enumerate(stats_data):
                stats_table.cell(i, 0).text = metric
                stats_table.cell(i, 1).text = str(value)
            
            # Student activity by year
            doc.add_heading('Student Activity by Year', level=1)
            
            cursor.execute("""
                SELECT 
                    s.year,
                    COUNT(br.id) as borrow_count
                FROM students s
                LEFT JOIN borrow_records br ON s.enrollment_no = br.enrollment_no 
                    AND br.borrow_date >= ?
                GROUP BY s.year
                HAVING borrow_count > 0
                ORDER BY borrow_count DESC
            """, (start_date,))
            
            year_activity = cursor.fetchall()
            
            if year_activity:
                year_table = doc.add_table(rows=len(year_activity) + 1, cols=2)
                year_table.style = 'Table Grid'
                year_table.cell(0, 0).text = 'Academic Year'
                year_table.cell(0, 1).text = 'Books Borrowed'
                
                for i, (year, count) in enumerate(year_activity):
                    year_table.cell(i + 1, 0).text = f"{year} Year"
                    year_table.cell(i + 1, 1).text = str(count)
            else:
                doc.add_paragraph('No student activity recorded in the selected period.')
            
            conn.close()
            
            # Save document
            doc.save(file_path)
            
            messagebox.showinfo("Export Successful", f"Analysis exported to:\n{file_path}")
            
            # Ask if user wants to open the file
            if messagebox.askyesno("Open File", "Do you want to open the exported file?"):
                self.open_file(file_path)
                
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export analysis: {str(e)}")

# Main application entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()