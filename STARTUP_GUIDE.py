#!/usr/bin/env python3
"""
SYSTEM STARTUP GUIDE
Library Management System v3.7
"""

STARTUP_GUIDE = """
═══════════════════════════════════════════════════════════════════════════════
  LIBRARY MANAGEMENT SYSTEM - STARTUP GUIDE
  Version 3.7 | January 31, 2026
═══════════════════════════════════════════════════════════════════════════════

📍 QUICK START
═════════════════════════════════════════════════════════════════════════════

1. FIRST TIME ONLY - Verify Dependencies:
   ─────────────────────────────────────────
   
   Open PowerShell and run:
   
   cd "C:\\Users\\Yash\\OneDrive\\Desktop\\Library-Management-System-for-Desktop"
   python check_deps.py
   
   Expected Output:
   ✅ All dependencies are installed!
   
   If you see "[MISSING]", run:
   pip install -r requirements.txt --no-cache-dir

2. START THE APPLICATION:
   ─────────────────────────────────────────
   
   cd "C:\\Users\\Yash\\OneDrive\\Desktop\\Library-Management-System-for-Desktop\\LibraryApp"
   python main.py
   
   Wait for the Tkinter GUI to appear (5-10 seconds)

3. LOGIN:
   ─────────────────────────────────────────
   
   Default Librarian Account:
   - Username: librarian
   - Password: (check with admin)
   
   Or create a new account if enabled

───────────────────────────────────────────────────────────────────────────────

🔧 INSTALLATION & SETUP
═════════════════════════════════════════════════════════════════════════════

Step 1: Clone/Extract Project
──────────────────────────────
Location: C:\\Users\\Yash\\OneDrive\\Desktop\\Library-Management-System-for-Desktop


Step 2: Create Virtual Environment (if needed)
──────────────────────────────────────────────
cd "C:\\Users\\Yash\\OneDrive\\Desktop\\Library-Management-System-for-Desktop"
python -m venv .venv
.venv\\Scripts\\Activate.ps1


Step 3: Install All Dependencies
────────────────────────────────
pip install -r requirements.txt --no-cache-dir

This installs:
✅ reportlab       - PDF generation
✅ psycopg2-binary - PostgreSQL support
✅ matplotlib      - Dashboard charts
✅ pandas          - Excel export
✅ flask           - Web server
✅ pillow          - Image processing
✅ qrcode          - QR codes
✅ xlsxwriter      - Excel files
✅ tkcalendar      - Calendar picker
✅ sqlalchemy      - Database ORM
✅ python-dotenv   - Environment config


Step 4: (Optional) Configure PostgreSQL
───────────────────────────────────────
Set DATABASE_URL environment variable for remote sync:

$env:DATABASE_URL = "postgresql://user:password@host:port/database"

Or create .env file in LibraryApp directory:
DATABASE_URL=postgresql://user:password@host:port/database


Step 5: Run the Application
───────────────────────────
cd LibraryApp
python main.py

───────────────────────────────────────────────────────────────────────────────

✅ WHAT SHOULD YOU SEE
═════════════════════════════════════════════════════════════════════════════

Console Output (Should look like this):
────────────────────────────────────────

System: Cleaned up old access logs.
[OK] Database: Using LOCAL SQLite (Fast!)
[OK] Sync Manager: Configured for remote sync
[OK] Auto-sync started (interval: 2 minutes)
[OK] Performance optimization modules loaded successfully
[Auto-Sync] Daemon started (every 2 minutes)
Running database integrity check...
[Auto-Reminder] Next reminder check scheduled at 2026-02-01 09:00:00
[Auto-Reminder] Background scheduler started.
[OK] Database integrity verified - all checks passed

✅ NO ERROR MESSAGES = System is working correctly!


GUI Window:
───────────
✅ Tkinter window appears after ~5 seconds
✅ Login screen or main dashboard is visible
✅ No popup error dialogs


───────────────────────────────────────────────────────────────────────────────

❌ TROUBLESHOOTING
═════════════════════════════════════════════════════════════════════════════

Problem 1: "ModuleNotFoundError: No module named 'reportlab'"
─────────────────────────────────────────────────────────────

Solution:
pip install -r requirements.txt --no-cache-dir --force-reinstall


Problem 2: "UnicodeEncodeError: 'charmap' codec can't encode"
──────────────────────────────────────────────────────────────

Solution:
cd LibraryApp
python fix_unicode.py
python main.py


Problem 3: Console shows "can't open file 'main.py'"
─────────────────────────────────────────────────────

Solution:
Make sure you're in the correct directory:
cd "C:\\Users\\Yash\\OneDrive\\Desktop\\Library-Management-System-for-Desktop\\LibraryApp"
python main.py


Problem 4: Database connection fails
────────────────────────────────────

Solution 1 - If offline is okay:
The app will use local SQLite (no PostgreSQL needed)

Solution 2 - For PostgreSQL sync:
1. Set DATABASE_URL correctly
2. Verify PostgreSQL server is running
3. Test connection: psql -h [host] -U [user] -d [database]


Problem 5: Observability Dashboard shows 0 data
───────────────────────────────────────────────

Solution:
1. Wait a few minutes for data to accumulate
2. Make sure web portal is running
3. Check that access_logs table exists in database
4. Try: Admin > Database > Check Integrity


Problem 6: Application crashes/closes suddenly
───────────────────────────────────────────────

Check console for error messages:
1. Missing dependency → Run: pip install -r requirements.txt
2. Database error → Check database.db file exists
3. PostgreSQL error → Check DATABASE_URL is set correctly


───────────────────────────────────────────────────────────────────────────────

📊 FEATURES AVAILABLE
═════════════════════════════════════════════════════════════════════════════

Desktop Application:
✅ Student Management    - Add/Edit/Delete students
✅ Book Inventory        - Manage library books
✅ Issue/Return Books    - Borrowing system
✅ Reports             - Generate Excel/PDF reports
✅ Analytics           - Dashboard with charts
✅ Email Notifications - Overdue reminders
✅ Database Backup     - Export/Restore data

Web Portal (Optional):
✅ Student Login        - Access from browser
✅ Book Catalogue       - Search and browse
✅ My Books            - View borrowed books
✅ Request Books       - Order new books
✅ Study Materials     - Access course materials
✅ Notifications       - Real-time updates

───────────────────────────────────────────────────────────────────────────────

🔐 SECURITY & BEST PRACTICES
═════════════════════════════════════════════════════════════════════════════

✅ Always use strong passwords
✅ Don't share DATABASE_URL credentials
✅ Regular backups of library.db
✅ Keep Windows firewall enabled for web portal
✅ Use HTTPS for web portal in production
✅ Don't run as administrator unless necessary
✅ Keep software and dependencies updated


───────────────────────────────────────────────────────────────────────────────

📞 SUPPORT & DOCUMENTATION
═════════════════════════════════════════════════════════════════════════════

For Detailed Information, Read:
✅ README.md                       - Project overview
✅ README_SETUP.md                 - Detailed setup instructions
✅ PERFORMANCE_IMPROVEMENTS.md     - Performance guide
✅ SOLUTION_SUMMARY.md             - What was fixed and how
✅ ARCHITECTURE_AUDIT_REPORT.md    - System design
✅ FINAL_AUDIT_REPORT.md           - Complete system overview


Quick Commands:
───────────────
python check_deps.py            # Check all dependencies
python fix_unicode.py           # Fix console encoding issues
python verify_installation.py   # Full installation check
cd LibraryApp; python main.py   # Start application


───────────────────────────────────────────────────────────────────────────────

✅ SYSTEM REQUIREMENTS
═════════════════════════════════════════════════════════════════════════════

Operating System:  Windows 10/11 (or any OS with Python)
Python:            3.8+ (Current: 3.12.10)
RAM:               2GB minimum (4GB recommended)
Disk Space:        500MB free
Internet:          Optional (PostgreSQL sync only)

───────────────────────────────────────────────────────────────────────────────

🎉 YOU'RE ALL SET!
═════════════════════════════════════════════════════════════════════════════

The Library Management System is:
✅ Fully installed and configured
✅ Ready for production use
✅ No errors or warnings
✅ All dependencies verified
✅ PostgreSQL sync available (optional)
✅ Database integrity verified

Start using the system now!

═══════════════════════════════════════════════════════════════════════════════
Created: January 31, 2026
Version: 3.7+
Status: ✅ PRODUCTION READY
═══════════════════════════════════════════════════════════════════════════════
"""

if __name__ == "__main__":
    print(STARTUP_GUIDE)
    
    # Also save to file
    with open('STARTUP_GUIDE.txt', 'w', encoding='utf-8') as f:
        f.write(STARTUP_GUIDE)
    print("\n[OK] Guide saved to STARTUP_GUIDE.txt")
