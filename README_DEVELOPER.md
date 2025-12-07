# Developer Documentation — Library Management System

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Architecture & Design Patterns](#architecture--design-patterns)
4. [Database Schema](#database-schema)
5. [Core Components](#core-components)
6. [Key Features Implementation](#key-features-implementation)
7. [File Structure](#file-structure)
8. [Build & Deployment](#build--deployment)

---

## 🎯 Project Overview

**Project Name:** Library Management System for Computer Department  
**Type:** Desktop Application (Windows)  
**Language:** Python 3.11  
**Architecture:** MVC-inspired (Model-View-Controller)  
**Database:** SQLite3 (embedded)  
**GUI Framework:** Tkinter + ttk (themed widgets)

**Purpose:**  
A complete library management solution for educational institutions to track students, books, transactions, fines, and generate automated email notifications.

---

## 🛠️ Technology Stack

### Core Technologies

#### 1. **Python 3.11**
- Main programming language
- Chosen for: Cross-platform compatibility, rich library ecosystem, ease of deployment

#### 2. **Tkinter (GUI Framework)**
```python
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
```
- **Why:** Built-in with Python, no external dependencies, native look
- **Usage:** 
  - `tk` - Base widgets (Button, Label, Entry, Frame)
  - `ttk` - Themed widgets (Combobox, Treeview, Notebook for tabs)
  - `messagebox` - Dialog boxes (showinfo, showerror, askyesno)
  - `filedialog` - File selection dialogs (askopenfilename)

#### 3. **SQLite3 (Database)**
```python
import sqlite3
```
- **Why:** Serverless, zero-configuration, single-file database
- **Usage:** CRUD operations, foreign keys, transactions
- **Benefits:** 
  - No separate database server needed
  - Perfect for desktop applications
  - ACID compliant (Atomicity, Consistency, Isolation, Durability)

### Data Processing Libraries

#### 4. **Pandas (Excel & Data Manipulation)**
```python
import pandas as pd
```
- **Why:** Industry-standard for data analysis
- **Usage:**
  - Read Excel files: `pd.read_excel()`
  - Data normalization: `df.columns.str.lower().str.replace(' ', '_')`
  - Export to Excel: `df.to_excel()`
- **Features Used:**
  - Column renaming and mapping
  - Iterating rows with `.iterrows()`
  - Handling missing data (NaN values)

#### 5. **python-docx (Word Document Generation)**
```python
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
```
- **Why:** Create professional overdue letters
- **Usage:**
  - Create documents: `Document()`
  - Add paragraphs with formatting
  - Set font sizes, alignment, bold text
  - Save as `.docx` files

#### 6. **Matplotlib (Charts & Analytics)**
```python
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
```
- **Why:** Powerful plotting library
- **Usage:**
  - Bar charts (top borrowers, popular books)
  - Line charts (issue trends over time)
  - Pie charts (category distribution)
  - Embedded in Tkinter with `FigureCanvasTkAgg`
- **Features:**
  - Professional styling
  - Interactive legends
  - Color customization

### Email & Background Processing

#### 7. **smtplib (Email Automation)**
```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
```
- **Why:** Built-in Python library for sending emails
- **Usage:**
  - SMTP connection to Gmail (smtp.gmail.com:587)
  - TLS encryption
  - Attach Word documents
  - Send HTML/plain text emails
- **Security:** Uses Gmail App Passwords (not regular passwords)

#### 8. **threading (Background Scheduler)**
```python
import threading
import time
```
- **Why:** Non-blocking background tasks
- **Usage:**
  - Daily reminder scheduler (runs at 9 AM)
  - Daemon threads (auto-terminate when app closes)
  - Prevents UI freezing during email sending

### Utility Libraries

#### 9. **datetime (Date Calculations)**
```python
from datetime import datetime, timedelta
```
- **Usage:**
  - Fine calculation: `(return_date - due_date).days * FINE_PER_DAY`
  - Due date calculation: `datetime.now() + timedelta(days=7)`
  - Date formatting: `strftime('%Y-%m-%d')`
  - Overdue detection

#### 10. **json (Configuration Storage)**
```python
import json
```
- **Usage:**
  - Store email settings: `email_settings.json`
  - Store email history: `email_history.json`
  - Read/write configuration: `json.load()`, `json.dump()`

#### 11. **os & sys (File System & Paths)**
```python
import os
import sys
```
- **Usage:**
  - Get executable directory: `os.path.dirname(sys.executable)`
  - Check if running as PyInstaller executable: `hasattr(sys, '_MEIPASS')`
  - File path operations: `os.path.join()`

### Optional Libraries

#### 12. **tkcalendar (Date Picker Widget)**
```python
from tkcalendar import DateEntry
```
- **Why:** User-friendly date selection
- **Usage:** Calendar popup for selecting dates
- **Fallback:** Manual entry if not installed

#### 13. **xlsxwriter (Advanced Excel Export)**
```python
import xlsxwriter
```
- **Why:** Create formatted Excel files with charts
- **Usage:** Export analytics data with embedded charts
- **Fallback:** Basic pandas export if not available

---

## 🏗️ Architecture & Design Patterns

### 1. **MVC-Inspired Architecture**

```
┌─────────────────────────────────────────────┐
│              View (UI Layer)                │
│  - Tkinter widgets                          │
│  - User interactions                        │
│  - Display logic                            │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│          Controller (Logic Layer)           │
│  - LibraryApp class (main.py)              │
│  - Event handlers                           │
│  - Business logic                           │
│  - Validation                               │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│           Model (Data Layer)                │
│  - Database class (database.py)             │
│  - CRUD operations                          │
│  - SQL queries                              │
│  - Data persistence                         │
└─────────────────────────────────────────────┘
```

**Separation of Concerns:**
- `main.py` → UI + Business Logic (7,698 lines)
- `database.py` → Data Access Layer (593 lines)
- No mixing of SQL queries in UI code

### 2. **Object-Oriented Programming**

**Main Classes:**

```python
class Database:
    def __init__(self):
        self.db_path = "library.db"
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def add_student(self, ...): pass
    def update_student(self, ...): pass
    def delete_student(self, ...): pass
    # ... more CRUD methods
```

```python
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.db = Database()  # Composition
        self.create_ui()
    
    def create_ui(self): pass
    def refresh_dashboard(self): pass
    # ... UI methods
```

**Design Pattern Used:**
- **Composition:** `LibraryApp` contains `Database` instance
- **Single Responsibility:** Each method does one thing
- **Encapsulation:** Private helper methods (prefixed with `_`)

### 3. **Event-Driven Programming**

```python
# Button clicks
save_btn.config(command=self.save_student)

# Double-click events
self.students_tree.bind('<Double-1>', self.on_student_double_click)

# Combobox selection
combo.bind('<<ComboboxSelected>>', lambda e: self.filter_data())

# Entry field changes (real-time search)
search_var.trace('w', lambda *args: self.search_records())
```

---

## 🗄️ Database Schema

### Tables & Relationships

```sql
┌─────────────────────────────────────────────┐
│              students                        │
├─────────────────────────────────────────────┤
│ id (PK, AUTO)                               │
│ enrollment_no (UNIQUE, NOT NULL)            │
│ name (NOT NULL)                             │
│ email                                        │
│ phone                                        │
│ department                                   │
│ year                                         │
│ date_registered (DEFAULT CURRENT_DATE)      │
└─────────────────┬───────────────────────────┘
                  │
                  │ 1:N
                  │
┌─────────────────▼───────────────────────────┐
│           borrow_records                     │
├─────────────────────────────────────────────┤
│ id (PK, AUTO)                               │
│ enrollment_no (FK → students)               │
│ book_id (FK → books)                        │
│ borrow_date (NOT NULL)                      │
│ due_date (NOT NULL)                         │
│ return_date                                  │
│ status (DEFAULT 'borrowed')                 │
│ academic_year                                │
└─────────────────┬───────────────────────────┘
                  │
                  │ N:1
                  │
┌─────────────────▼───────────────────────────┐
│                books                         │
├─────────────────────────────────────────────┤
│ id (PK, AUTO)                               │
│ book_id (UNIQUE, NOT NULL)                  │
│ title (NOT NULL)                            │
│ author (NOT NULL)                           │
│ isbn                                         │
│ category                                     │
│ total_copies (DEFAULT 1)                    │
│ available_copies (DEFAULT 1)                │
│ date_added (DEFAULT CURRENT_DATE)           │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│          promotion_history                   │
├─────────────────────────────────────────────┤
│ id (PK, AUTO)                               │
│ enrollment_no (FK → students)               │
│ student_name                                 │
│ old_year                                     │
│ new_year                                     │
│ letter_number                                │
│ academic_year                                │
│ promotion_date (DEFAULT CURRENT_TIMESTAMP)  │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│           academic_years                     │
├─────────────────────────────────────────────┤
│ id (PK, AUTO)                               │
│ year_name (UNIQUE, NOT NULL)                │
│ start_date                                   │
│ end_date                                     │
│ is_active (DEFAULT 0)                       │
│ created_date (DEFAULT CURRENT_TIMESTAMP)    │
└─────────────────────────────────────────────┘
```

**Key Design Decisions:**
1. **Foreign Keys:** Maintain referential integrity
2. **Soft Deletes:** Students with borrowed books cannot be deleted
3. **Timestamps:** Track when records were created
4. **Status Field:** 'borrowed' or 'returned' for transactions
5. **Normalization:** 3NF (Third Normal Form) - no redundant data

---

## 🔧 Core Components

### 1. **Database Layer (database.py)**

**Methods by Category:**

**Students:**
```python
def add_student(enrollment_no, name, email, phone, department, year)
def update_student(enrollment_no, name, email, phone, department, year)
def delete_student(enrollment_no)
def get_students(search_term='')
```

**Books:**
```python
def add_book(book_id, title, author, isbn, category, total_copies)
def update_book(book_id, title, author, isbn, category, total_copies)
def delete_book(book_id)
def get_books(search_term='')
def get_next_book_id()  # Auto-increment logic
```

**Transactions:**
```python
def borrow_book(enrollment_no, book_id, borrow_date, due_date)
def return_book(enrollment_no, book_id, return_date=None)
def get_borrowed_books()
```

**Promotions:**
```python
def add_promotion_history(enrollment_no, student_name, old_year, new_year, letter_number, academic_year)
def get_promotion_history()
def undo_last_promotion()
```

**Academic Years:**
```python
def create_academic_year(year_name)
def get_active_academic_year()
def get_all_academic_years()
```

**Pattern Used:** Each method returns `(success: bool, message: str)` tuple

### 2. **UI Layer (main.py)**

**Tab Structure:**
```python
self.notebook = ttk.Notebook(self.root)

# 7 main tabs
tabs = [
    ("Dashboard", self.create_dashboard_tab),
    ("Students", self.create_students_tab),
    ("Books", self.create_books_tab),
    ("Transactions", self.create_transactions_tab),
    ("Records", self.create_records_tab),
    ("Analysis", self.create_analysis_tab),
    ("Admin", self.create_admin_tab)
]
```

**Widget Hierarchy:**
```
Window (root)
└── Header Frame
    └── Title + Logo + Email Button
└── Notebook (Tabs)
    └── Tab Frame
        └── Top Controls (Search, Filters, Buttons)
        └── Treeview (Data Table)
        └── Bottom Actions
```

**Color Scheme:**
```python
self.colors = {
    'primary': '#ffffff',      # Pure white backgrounds
    'secondary': '#2E86AB',    # Professional blue (buttons)
    'accent': '#0F3460',       # Dark blue (headers)
    'text': '#333333'          # Dark gray text
}
```

### 3. **Treeview Pattern (Data Tables)**

**Standard Implementation:**
```python
# Create scrollable treeview
tree_frame = tk.Frame(parent)
scrollbar = ttk.Scrollbar(tree_frame)
tree = ttk.Treeview(
    tree_frame,
    columns=('col1', 'col2', 'col3'),
    show='headings',
    yscrollcommand=scrollbar.set
)
scrollbar.config(command=tree.yview)

# Configure columns
tree.heading('col1', text='Header 1')
tree.column('col1', width=150, anchor='center')

# Bind events
tree.bind('<Double-1>', self.on_double_click)

# Populate data
for row in data:
    tree.insert('', 'end', values=row)
```

**Features:**
- Sortable columns (click header)
- Double-click to edit
- Right-click context menus (future enhancement)
- Striped row colors for readability

---

## 🎯 Key Features Implementation

### 1. **Fine Calculation**

**Logic:**
```python
FINE_PER_DAY = 5  # ₹5 per day

# Calculate overdue days
due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
return_date = datetime.strptime(return_date_str, '%Y-%m-%d')
overdue_days = (return_date - due_date).days

# Apply fine only if overdue
if overdue_days > 0:
    fine_amount = overdue_days * FINE_PER_DAY
    messagebox.showwarning("Late Return", f"Fine: Rs {fine_amount}")
```

**Edge Cases Handled:**
- Early returns (no fine)
- Same-day returns (no fine)
- Negative days (validation error)

### 2. **Auto-Reminder Email System**

**Architecture:**
```python
def schedule_reminder_emails(self):
    def run_scheduler():
        while True:
            # Calculate seconds until 9 AM
            now = datetime.now()
            target = now.replace(hour=9, minute=0, second=0)
            if now >= target:
                target += timedelta(days=1)
            
            wait_seconds = (target - now).total_seconds()
            time.sleep(wait_seconds)
            
            # Send reminders
            if self.email_settings.get('reminder_enabled'):
                self.check_and_send_reminders()
    
    # Daemon thread (auto-stops with app)
    thread = threading.Thread(target=run_scheduler, daemon=True)
    thread.start()
```

**Query for Due Books:**
```sql
SELECT b.enrollment_no, s.name, s.email, bk.title, b.due_date
FROM borrow_records b
JOIN students s ON b.enrollment_no = s.enrollment_no
JOIN books bk ON b.book_id = bk.book_id
WHERE b.due_date = ? 
  AND b.return_date IS NULL 
  AND s.email IS NOT NULL 
  AND s.email != ''
```

**Why Daemon Thread?**
- Runs in background
- Doesn't block UI
- Auto-terminates when app closes
- No manual cleanup needed

### 3. **Student Year Promotion**

**Algorithm:**
```python
def promote_student_years(self):
    # Normalization function
    def _norm(label):
        s = str(label).strip().lower()
        if s in ('1st', 'first', 'first year', '1', 'fy'):
            return '1st'
        if s in ('2nd', 'second', 'second year', '2', 'sy'):
            return '2nd'
        if s in ('3rd', 'third', 'third year', '3', 'ty'):
            return '3rd'
        if 'pass' in s:
            return 'Pass Out'
        return label
    
    # Promotion mapping
    def _promote_once(label):
        l = _norm(label)
        return {
            '1st': '2nd',
            '2nd': '3rd',
            '3rd': 'Pass Out'
        }.get(l, l)
    
    # Batch update all students
    for enrollment, name, year in students:
        new_year = _promote_once(year)
        if new_year != year:
            update_student_year(enrollment, new_year)
            log_promotion_history(enrollment, name, year, new_year)
```

**Why Normalization?**
- Handles typos: "First year", "FIRST", "1st Year" → all become "1st"
- Case-insensitive
- User-friendly

### 4. **Excel Import with Column Mapping**

**Smart Column Detection:**
```python
# Read Excel
df = pd.read_excel(file_path)

# Normalize column names
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Map synonyms
column_map = {
    'enrollment': 'enrollment_no',
    'enrollmentno': 'enrollment_no',
    'enrollment_number': 'enrollment_no'
}
df.rename(columns=column_map, inplace=True)

# Validate required columns
required = ['enrollment_no', 'name']
if not all(col in df.columns for col in required):
    raise ValueError("Missing required columns")
```

**Why This Approach?**
- Flexible: Accepts "Enrollment No" or "enrollment_no"
- Forgiving: Handles spaces, underscores, case
- Clear errors: Shows which columns are missing

### 5. **Email with Attachment**

**MIME Multipart:**
```python
def send_email_with_attachment(to_email, subject, body, attachment_path):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Add body
    msg.attach(MIMEText(body, 'plain'))
    
    # Add attachment if provided
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
            msg.attach(part)
    
    # Send via SMTP
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # TLS encryption
    server.login(sender_email, app_password)
    server.send_message(msg)
    server.quit()
```

**Security:**
- Uses App Password (not regular Gmail password)
- TLS encryption
- Never logs passwords

### 6. **Analytics Charts**

**Matplotlib Integration:**
```python
# Create figure
fig = Figure(figsize=(10, 6), dpi=100)
ax = fig.add_subplot(111)

# Plot data
ax.bar(categories, values, color='#2E86AB')
ax.set_xlabel('Category')
ax.set_ylabel('Count')
ax.set_title('Popular Books')

# Embed in Tkinter
canvas = FigureCanvasTkAgg(fig, parent=frame)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
```

**Chart Types:**
- Bar charts: Top borrowers, popular books
- Line charts: Issue trends over time
- Pie charts: Category distribution

---

## 📁 File Structure

```
Library Management System/
├── LibraryApp/
│   ├── main.py                    # Main application (7,698 lines)
│   ├── database.py                # Database layer (593 lines)
│   ├── logo.png                   # College logo
│   ├── requirements.txt           # Python dependencies
│   ├── build_app.spec             # PyInstaller build config
│   └── dist/
│       └── LibraryManagementSystem_v5.0_FINAL.exe
├── README.md                      # User documentation
├── README_SETUP.md                # Installation guide
├── README_LIBRARIAN.md            # Librarian rules
├── README_FEATURES.md             # Feature summary
├── README_QUICK.md                # Quick reference
├── README_DEVELOPER.md            # This file
├── PROJECT_STRUCTURE.md           # Project overview
└── .venv/                         # Python virtual environment (dev only)
```

---

## 🔨 Build & Deployment

### Development Setup

**1. Create Virtual Environment:**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**2. Install Dependencies:**
```powershell
pip install -r requirements.txt
```

**requirements.txt:**
```
pandas==2.0.3
python-docx==0.8.11
matplotlib==3.7.2
tkcalendar==1.6.1
xlsxwriter==3.1.2
pyinstaller==5.13.0
```

**3. Run Application:**
```powershell
python LibraryApp/main.py
```

### Building Executable

**PyInstaller Configuration (build_app.spec):**
```python
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('logo.png', '.')],  # Include logo
    hiddenimports=[
        'pandas',
        'matplotlib',
        'docx',
        'tkcalendar'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='LibraryManagementSystem_v5.0_FINAL',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='logo.png'  # App icon
)
```

**Build Command:**
```powershell
cd LibraryApp
pyinstaller build_app.spec
```

**Output:** `dist/LibraryManagementSystem_v5.0_FINAL.exe`

**Single File Benefits:**
- No installation needed
- All dependencies bundled
- Creates `library.db` on first run
- Portable (copy to USB and run)

---

## 🎓 Key Programming Concepts Used

### 1. **Object-Oriented Programming (OOP)**
- Classes: `LibraryApp`, `Database`
- Encapsulation: Private methods, public interfaces
- Composition: LibraryApp contains Database

### 2. **Event-Driven Programming**
- Button callbacks
- Keyboard events
- Mouse events (double-click)
- Timer events (scheduler)

### 3. **Multi-threading**
- Daemon threads for background tasks
- Non-blocking UI
- Thread safety considerations

### 4. **Database Design**
- Normalization (3NF)
- Foreign keys and constraints
- ACID transactions
- Prepared statements (SQL injection prevention)

### 5. **Error Handling**
```python
try:
    # Risky operation
    result = db.add_student(...)
except sqlite3.IntegrityError:
    messagebox.showerror("Error", "Duplicate enrollment number")
except Exception as e:
    messagebox.showerror("Error", f"Unexpected error: {e}")
finally:
    conn.close()
```

### 6. **Design Patterns**
- **MVC:** Separation of UI, logic, and data
- **Singleton-like:** Single Database instance
- **Observer Pattern:** Tkinter event binding
- **Template Method:** Consistent dialog creation

### 7. **Data Validation**
```python
# Required field check
if not enrollment_no.strip():
    return False, "Enrollment number required"

# Format validation
datetime.strptime(date_str, '%Y-%m-%d')

# Business logic validation
if student_year == "Pass Out":
    return False, "Pass Out students cannot borrow books"
```

---

## 🚀 Performance Optimizations

1. **Database Indexing:** Enrollment No and Book ID are indexed (UNIQUE constraint)
2. **Lazy Loading:** Charts generated only when Analytics tab opened
3. **Efficient Queries:** JOINs instead of multiple queries
4. **Connection Pooling:** Single connection per operation (closed immediately)
5. **UI Rendering:** Virtual scrolling in Treeviews (only visible rows rendered)

---

## 🔐 Security Considerations

**Implemented:**
- ✅ Prepared statements (SQL injection prevention)
- ✅ App Password for Gmail (not storing regular password)
- ✅ TLS encryption for emails
- ✅ Input validation
- ✅ Foreign key constraints

**Future Enhancements:**
- 🔒 Encrypt `email_settings.json` (currently plain text)
- 🔒 Hash admin credentials (currently hardcoded)
- 🔒 Role-based access control
- 🔒 Audit logging

---

## 📚 Learning Resources

If you want to understand this project better:

**Python Basics:**
- [Python Official Docs](https://docs.python.org/3/)
- [Real Python Tutorials](https://realpython.com/)

**Tkinter GUI:**
- [TkDocs Tutorial](https://tkdocs.com/tutorial/)
- [Tkinter by Example](https://likegeeks.com/python-gui-examples-tkinter-tutorial/)

**SQLite:**
- [SQLite Tutorial](https://www.sqlitetutorial.net/)
- [Python SQLite3 Docs](https://docs.python.org/3/library/sqlite3.html)

**Libraries:**
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Guide](https://matplotlib.org/stable/tutorials/index.html)
- [Python-docx](https://python-docx.readthedocs.io/)

---

## 🎯 Interview Talking Points

When explaining this project:

**1. Architecture Decision:**
"I used MVC-inspired architecture to separate concerns - UI logic in main.py, data access in database.py. This makes the code maintainable and testable."

**2. Technology Choice:**
"I chose Tkinter because it's built into Python, ensuring the app works without internet. SQLite provides zero-configuration database with full ACID compliance."

**3. Complex Feature:**
"The auto-reminder system uses daemon threads to check daily at 9 AM without blocking the UI. I calculate which books are due in N days using SQL JOINs and send batch emails with SMTP."

**4. Problem Solving:**
"For the Excel import, I implemented smart column normalization to handle variations like 'Enrollment No' vs 'enrollment_no', making it user-friendly for teachers."

**5. Scale & Performance:**
"The app handles 10,000+ students efficiently using indexed queries and lazy-loading charts. Database is single-file for easy backup."

---

**Version:** 5.0 FINAL  
**Last Updated:** December 1, 2025  
**Developer:** Yash Vijay Date  
**Institution:** Government Polytechnic Awasari (Kh)
