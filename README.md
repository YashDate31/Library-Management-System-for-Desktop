# 📚 Library Management System for Computer Department

**Version:** 5.0 FINAL  
**Developer:** Yash Vijay Date  
**Enrollment:** 24210270230  
**Branch:** Computer Engineering, 2nd Year  
**Institution:** Government Polytechnic Awasari (Kh)
**Contact Number** 9527266485
**Email** yashdate36@gmail.com

---

## 🎯 Overview

A comprehensive desktop application designed specifically for managing the Computer Department library at Government Polytechnic Awasari. This system provides complete book tracking, student management, automated email notifications, and detailed analytics.

### ✨ Key Features

- **Student Management** - Add, edit, search, import/export students
- **Book Management** - Track books, categories, availability, and copies
- **Transaction System** - Issue and return books with automatic fine calculation
- **Email Automation** - Send overdue letters and reminder emails automatically
- **Auto-Reminders** - Proactive reminders 2 days before books are due
- **Analytics Dashboard** - Visual charts showing library statistics and trends
- **Academic Year Management** - Automatic student promotion system
- **Record Keeping** - Complete history of all transactions
- **Excel/Word Export** - Generate professional reports
- **Fine Management** - Automatic calculation at ₹5 per day

---

## 🚀 Quick Start

### System Requirements

- **Operating System:** Windows 7/8/10/11 (64-bit)
- **No additional software needed** - Standalone EXE file

### Installation

1. Copy `LibraryManagementSystem_v5.0_FINAL.exe` to desired location (e.g., `C:\GPA_Library\`)
2. Double-click the EXE file to run
3. Login with default credentials:
   - **Username:** gpa
   - **Password:** gpa123

**Important:** Change the password after first login!

---

## 📖 User Guide

### 1. Dashboard

The dashboard provides an at-a-glance view of:
- Total students, books, and available books
- Currently issued books count
- Total fines collected
- Recent transactions
- Overdue alerts

### 2. Students Tab

**Add Student:**
- Click "➕ Add Student"
- Fill in: Enrollment No, Name, Email, Phone, Department, Year
- Click "Save"

**Edit Student:**
- Double-click any student in the list
- Edit: Name, Email, Phone, Year (Enrollment No cannot be changed)
- Click "💾 Save Changes" or "🗑️ Delete" to remove

**Import Students from Excel:**
- Prepare Excel file with columns: `Enrollment No | Name | Email | Phone | Department | Year`
- Click "Import from Excel"
- Select your Excel file
- Students will be added in bulk

**📊 Excel Column Names for Import:**

The app accepts **flexible column names** - both formats work:

**Students Import - Use either format:**
```
Option 1 (Human-readable):  Enrollment No | Name | Email | Phone | Department | Year
Option 2 (Technical style):  enrollment_no | name | email | phone | department | year
```

**Field Details:**
- **Enrollment No** - Required, unique student ID
- **Name** - Required, student full name
- **Email** - Optional (needed for email notifications)
- **Phone** - Optional, contact number
- **Department** - Optional, defaults to "Computer"
- **Year** - Optional, use: "1st Year", "2nd Year", "3rd Year", or "Pass Out"

**Key Points:**
- ✅ Both formats work (app auto-converts)
- ✅ Spaces or underscores - both accepted
- ✅ Case insensitive (ENROLLMENT NO, enrollment no, Enrollment No all work)
- ✅ Column order doesn't matter

**Search & Filter:**
- Use search box to find students by name or enrollment
- Filter by year (1st/2nd/3rd/Pass Out)
- Export to Excel anytime

### 3. Books Tab

**Add Book:**
- Click "➕ Add Book"
- Fill in: Book ID, Title, Author, ISBN, Category, Total Copies
- Click "Save"

**Edit Book:**
- Double-click any book in the list
- Edit: Title, Author, ISBN, Category, Total Copies (Book ID cannot be changed)
- Available copies are calculated automatically (Total - Borrowed)
- Click "💾 Save Changes" or "🗑️ Delete" to remove

**Categories Available:**
- Core CS, Web Development, Programming, Database, AI/ML, Networking, Operating Systems, Algorithms, Software Engineering, Mobile Development, Cloud Computing, Cybersecurity, IoT, Competitive Programming, Project Guides, Others

**Import Books from Excel:**
- Prepare Excel with columns: `Book ID | Title | Author | ISBN | Category | Total Copies`
- Click "Import from Excel"
- Bulk add books instantly

**📊 Excel Column Names for Import:**

The app accepts **flexible column names** - both formats work:

**Books Import - Use either format:**
```
Option 1 (Human-readable):  Book ID | Title | Author | ISBN | Category | Total Copies
Option 2 (Technical style):  book_id | title | author | isbn | category | total_copies
```

**Field Details:**
- **Book ID** - Required, unique identifier for the book
- **Title** - Required, book title
- **Author** - Required, book author name
- **ISBN** - Optional, International Standard Book Number
- **Category** - Optional (defaults to "Others")
- **Total Copies** - Optional, defaults to 1

**Key Points:**
- ✅ Both formats work (app auto-converts)
- ✅ Spaces or underscores - both accepted  
- ✅ Case insensitive (all variations work)
- ✅ Column order doesn't matter

**Available Categories:**
- Core CS, Web Development, Programming, Database, AI/ML, Networking, Operating Systems, 
  Algorithms, Software Engineering, Mobile Development, Cloud Computing, 
  Cybersecurity, IoT, Competitive Programming, Project Guides, Others

### 4. Transactions Tab

**Issue a Book:**
1. Click "📤 Issue Book"
2. Enter Student Enrollment Number
3. Enter Book ID
4. Select Due Date (default: 7 days from today)
5. Click "Issue Book"
6. System validates student status and book availability

**Return a Book:**
1. Click "📥 Return Book"
2. Enter Student Enrollment Number
3. Enter Book ID
4. Click "Return Book"
5. Fine automatically calculated if overdue (₹5/day)
6. Book becomes available again

### 5. Records Tab

View complete history of all transactions:
- **Filter by Status:** All / Borrowed / Returned / Overdue
- **Search:** By student name, enrollment, or book title
- **Export Records:** Generate Excel reports
- **Overdue Letters:** Generate professional Word documents

**Double-click any overdue record** to:
- Generate overdue letter (Word document)
- Automatically email to student (if email configured)
- Save document locally

**Bulk Overdue Letters:**
- Click "📄 Overdue Letter (Word)" button
- Generates master document with all overdue students
- Option to send emails to ALL overdue students at once
- Progress tracking and summary report

### 6. Analysis Tab

Visual analytics with interactive charts:
- **Issue Trends** - Track borrowing patterns over time
- **Top Borrowers** - Most active students
- **Popular Books** - Most borrowed books
- **Category Distribution** - Which subjects are popular
- **Fine Collection** - Total fines over time period

**Export Options:**
- Export to Excel (data + charts)
- Export to Word (professional report)

**Filters:**
- Time period: 7 days, 15 days, 30 days
- Specific student analysis
- Specific book analysis

### 7. Admin Functions Tab

**Promote Students (End of Academic Year):**

⚠️ **IMPORTANT:** Click promote FIRST to empty 1st year, THEN import new students! (See Year-End Process section below)

1. Click "⬆️ Promote Student Years"
2. System will:
   - Move 3rd year → Pass Out
   - Move 2nd year → 3rd year
   - Move 1st year → 2nd year
   - Update academic year (e.g., 25-26 → 26-27)
3. **⚠️ Make database backup before promotion!**

**View Promotion History:**
- Track all past promotions
- See which students were promoted when
- Audit trail maintained

**Change Password:**
- Update admin password for security
- Never share credentials with students

---

## 📧 Email Setup Guide

### Why Use Email Automation?

- **Save Time:** Automatically notify students about overdue books
- **Prevent Overdue:** Send reminders BEFORE books become late
- **Professional:** Generate and send official overdue letters
- **Track History:** See all emails sent with timestamps

### Step 1: Configure Gmail App Password

1. **Enable 2-Step Verification:**
   - Go to: https://myaccount.google.com/security
   - Enable "2-Step Verification"

2. **Generate App Password:**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Click "Generate"
   - Copy the 16-character password (format: `xxxx xxxx xxxx xxxx`)

### Step 2: Configure in App

1. Click **"📧 Email"** button in top-right header
2. Go to **Configuration** tab
3. Check **"✓ Enable automatic email sending"**
4. Fill in:
   - **SMTP Server:** `smtp.gmail.com` (default)
   - **SMTP Port:** `587` (default)
   - **Gmail Address:** `your.library@gmail.com`
   - **Gmail App Password:** Paste 16-character password
5. Click **"💾 Save Settings"**

### Step 3: Enable Auto-Reminders (Optional)

In the same Configuration tab, scroll down to **"📅 Automatic Reminders"**:

1. Check **"✉️ Send automatic reminder emails before due date"**
2. Set days before: **2** (recommended)
3. Click **"💾 Save Settings"**

**How Auto-Reminders Work:**
- System checks daily at 9:00 AM
- Finds books due in 2 days
- Sends friendly reminder emails automatically
- Prevents books from becoming overdue
- All logged in Email History

**Test Immediately:**
- Click **"🔔 Send Reminders Now (Test)"** button
- Verifies email setup works
- Shows how many reminders will be sent

### Email Features

**Individual Overdue Letters:**
- Double-click overdue student in Records tab
- Generates Word document + sends email automatically
- Professional template with student and book details

**Bulk Overdue Letters:**
- Click "Overdue Letter (Word)" button
- Option to email ALL overdue students at once
- Progress window shows sending status
- Summary report with success/failure counts

**Email History Tab:**
- View all sent emails with timestamps
- See student name, email, book title, and status (✅ success / ❌ failed)
- Refresh to see latest emails
- Clear history option

### Troubleshooting Email

**"Authentication failed" Error:**
- Verify you're using App Password, NOT regular password
- Check 2-Step Verification is enabled on Google account
- Regenerate App Password if needed

**"Student email not available":**
- Add email address in Students tab
- Edit student record and fill Email field

**Email not sending:**
- Check internet connection
- Verify "Enable automatic email sending" is checked
- Confirm settings are saved correctly

---

## 💾 Data Backup & Recovery

### Why Backup?

Your **entire library data** is stored in ONE file: `library.db`

This file contains:
- All students
- All books
- All transactions
- All records
- All history
- Everything!

**If this file is lost, ALL DATA IS LOST!** 

### Weekly Backup Routine

**Every Friday (or weekly):**

1. **Close the Library app**
2. Go to folder where app is installed (e.g., `C:\GPA_Library\`)
3. Find file: `library.db`
4. Copy it to USB drive
5. Rename on USB: `library_backup_01_Dec_2025.db` (include date)
6. Store USB in safe location

**⏰ Set a calendar reminder!**

### Recovery Process

**If computer crashes or data is lost:**

1. **On new/repaired computer:**
   - Copy `LibraryManagementSystem_v5.0_FINAL.exe` to `C:\GPA_Library\`
   - Run it once (creates empty database)
   - Close the app

2. **Restore your data:**
   - Get USB with backups
   - Find latest backup: `library_backup_XX_XXX_2025.db`
   - Copy it to `C:\GPA_Library\`
   - Rename to: `library.db`
   - Replace the empty database

3. **Run app - All data restored!** ✅

### Backup Best Practices

- ✅ **Backup weekly** (minimum)
- ✅ **Keep 3-4 recent backups** (in case one is corrupted)
- ✅ **Use 2 USB drives** (Primary + Emergency)
- ✅ **Store in different locations** (office + principal's room)
- ✅ **Test restore once** (verify backup works on test PC)
- ❌ **Never delete old backup** until new one is confirmed working

### Cloud Backup (Optional)

For automatic cloud backup:

1. Install Google Drive Desktop on library PC
2. Move entire `C:\GPA_Library\` folder to:
   - `C:\Users\[Username]\Google Drive\GPA_Library\`
3. Run app from there
4. Every change backed up to cloud automatically
5. Access from any PC with Google account

---

## 🔧 Technical Information

### File Structure

```
C:\GPA_Library\
├── LibraryManagementSystem_v5.0_FINAL.exe  (Application)
├── library.db  (Database - ALL DATA)
├── logo.png  (College logo - auto-created)
├── email_settings.json  (Email config - auto-created)
└── email_history.json  (Email log - auto-created)
```

### Database Schema

**Students Table:**
- Enrollment No (Primary Key)
- Name, Class, Division, Roll No
- Contact, Email
- Year (1st/2nd/3rd/Pass Out)
- Academic Year

**Books Table:**
- Book ID (Primary Key)
- Title, Author, Publisher
- Category
- Total Copies, Available Copies

**Borrow Records Table:**
- Record ID (Auto-increment)
- Enrollment No, Book ID
- Issue Date, Due Date, Return Date
- Fine Amount
- Academic Year

### Technologies Used

- **Python 3.11** - Core programming language
- **Tkinter** - GUI framework
- **SQLite3** - Database management
- **Pandas** - Data processing and Excel export
- **python-docx** - Word document generation
- **Matplotlib** - Charts and analytics
- **smtplib** - Email automation
- **PyInstaller** - EXE packaging

---

## 📋 Tips for Smooth Operation

### Do's ✅

- Add student email addresses - enables email automation
- Backup database every Friday (set reminder!)
- Check overdue books weekly in Records tab
- Send overdue letters monthly
- Review analytics to understand borrowing patterns
- Test email functionality after initial setup
- Keep only ONE person using app at a time
- Store backups in multiple locations

### Don'ts ❌

- Don't delete `library.db` file - it's ALL your data!
- Don't rename `library.db` on computer (only on backups)
- Don't run app from USB drive (copy to computer first)
- Don't share admin password with students
- Don't skip weekly backups!
- **⚠️ Don't promote students BEFORE importing new 1st year batch!** (Critical!)
- Don't use personal email for library (use dedicated Gmail)

### Keyboard Shortcuts

- **Ctrl+F** - Search in current tab
- **Ctrl+R** - Refresh data
- **Ctrl+E** - Export data
- **Ctrl+P** - Print (in analysis)

---

## 🔒 Security Notes

### Password Security

- **Default credentials:** `gpa / gpa123`
- **Change immediately** after installation
- Use strong password (8+ characters, mix of letters/numbers)
- Never share with students or unauthorized staff

### Email Security

- Use **dedicated Gmail account** for library (not personal)
- Use **App Password** (more secure than regular password)
- Gmail credentials stored locally in `email_settings.json`
- Keep computer physically secure (lock when leaving desk)

### Data Privacy

- Student email addresses used only for library notifications
- No data shared with third parties
- All data stored locally (not in cloud unless you choose)
- GDPR compliant (students can request data deletion)

---

## 🆘 Troubleshooting

### App Won't Start

**Problem:** Double-clicking EXE does nothing  
**Solution:** 
- Check if `library.db` is in same folder as EXE
- Try running as Administrator
- Check Windows antivirus hasn't blocked it

### "Student Already Exists" Error

**Problem:** Can't add student  
**Solution:**
- Check if enrollment number is unique
- Search for student first - may already exist
- Check for typos in enrollment number

### "Book Not Available"

**Problem:** Can't issue book  
**Solution:**
- Check if all copies are already issued
- Go to Books tab - verify Available Copies > 0
- Return some copies if all are issued

### Can't Issue to Student

**Problem:** Error when trying to issue  
**Solution:**
- Check if student status is "Pass Out" (can't issue to graduates)
- Verify student hasn't been deleted
- Check if student has overdue books (some libraries restrict)

### Email Not Sending

**Problem:** Email fails to send  
**Solution:**
- Check internet connection
- Verify email settings are correct
- Regenerate Gmail App Password
- Check student has valid email address
- Test with "Send Reminders Now" button

### Data Disappeared

**Problem:** Students/books missing  
**Solution:**
- Check if `library.db` file exists in app folder
- If file exists but data missing, restore from USB backup
- Check if accidentally filtered view (reset filters)

---

## 🎓 Year-End Process

### Academic Year Promotion

**When:** End of academic year (after results declared)

---

### ⚠️ CRITICAL WARNING - READ CAREFULLY!

**⚠️ DO NOT IMPORT NEW STUDENTS AFTER PROMOTION!**

If you make this mistake, new 1st year students will be incorrectly promoted to 2nd year!

**❌ WRONG ORDER (Will cause problems):**
1. ~~Click "Promote Students"~~ ⬅️ DON'T DO THIS FIRST!
2. ~~Import new 1st year Excel file~~
3. ❌ **Result:** New students go to 2nd year (WRONG!)

**✅ CORRECT ORDER (Follow this exactly):**
1. ✅ **FIRST:** Import new 1st year students Excel file
2. ✅ **THEN:** Click "Promote Students" button
3. ✅ **Result:** Old students promoted correctly, new students stay in 1st year (CORRECT!)

**Why this order matters:**
- "Promote Students" moves ALL students up one year
- If you import AFTER promotion, those new students will also be promoted
- This means new 1st year students become 2nd year students (WRONG!)

---

**Before Promotion:**
1. ✅ **BACKUP DATABASE!** (Most important!)
2. ✅ **Import new 1st year students from Excel** (if available)
3. ✅ Clear all overdue books or document them
4. ✅ Collect all pending fines
5. ✅ Generate year-end reports for records

**Promotion Process:**
1. Go to **Admin Functions** tab
2. Click **"⬆️ Promote Student Years"**
3. Read the confirmation warning carefully
4. Confirm the action
5. System automatically:
   - Moves 3rd year → Pass Out
   - Moves 2nd year → 3rd year
   - Moves 1st year → 2nd year
   - **New imported students remain in 1st year** (correct!)
   - Updates academic year everywhere

**After Promotion:**
1. ✅ Verify promotion in Promotion History
2. ✅ Check student counts in Dashboard
   - 1st year count should show new students only
   - 2nd year count should show old 1st year students
   - 3rd year count should show old 2nd year students
   - Pass Out count should include old 3rd year students
3. ✅ Create backup with promotion done
4. ✅ Start new academic year fresh

### Adding New 1st Year Students

**Best Practice: Add BEFORE promotion**

If new student list arrives late (after promotion already done):
1. ⚠️ **Don't panic** - You can still add them
2. Import new students from Excel
3. ⚠️ **Problem:** They will be marked as 2nd year (wrong!)
4. **Solution:** Manually edit each student's class to "1st Year"
   - Go to Students tab
   - Search for new students
   - Click Edit → Change Class to "1st Year" → Save

**To avoid manual work:**
- Always try to get new 1st year list BEFORE doing promotion
- Coordinate with admissions office for timing

---

## 📞 Support & Contact

### For Technical Issues

**Developer:** Yash Vijay Date  
**Enrollment:** 24210270230  
**Branch:** Computer Engineering, 2nd Year  
**Institution:** Government Polytechnic Awasari (Kh)

### Common Issues & Quick Fixes

Most issues can be resolved by:
1. Restarting the application
2. Checking if `library.db` exists
3. Restoring from backup if needed
4. Verifying internet connection (for email)

---

## 📄 Version History

### Version 5.0 FINAL (Current)
- ✅ Complete student and book management
- ✅ Transaction system with fine calculation
- ✅ Email automation (overdue + reminders)
- ✅ Auto-reminder emails (daily at 9 AM)
- ✅ Analytics dashboard with charts
- ✅ Academic year promotion system
- ✅ Excel/Word export functionality
- ✅ Professional UI with college branding
- ✅ Comprehensive record keeping

---

## 📜 License & Usage

This software is developed specifically for **Government Polytechnic Awasari (Kh), Computer Department**.

**Usage Rights:**
- Free to use within the institution
- No commercial redistribution
- Source code not provided with EXE distribution
- All rights reserved by developer

**Attribution:**
When using this software, please credit:  
*"Developed by Yash Vijay Date, 2nd Year Computer Engineering Student"*

---

## 🎯 Final Notes

### For Librarians

This system is designed to be **simple and intuitive**. No technical knowledge required!

**Daily routine:**
- Issue/return books as students come
- Check dashboard for quick overview

**Weekly routine:**
- Backup `library.db` to USB (Friday)
- Check overdue students
- Send reminders if needed

**Monthly routine:**
- Generate reports from Analysis tab
- Send overdue letters
- Review statistics

### For IT Administrators

**Installation:** Copy EXE to computer  
**Backup:** Copy `library.db` weekly  
**Recovery:** Replace `library.db` from backup  
**Migration:** Copy entire folder to new PC  

**That's it!** No complex setup, no server configuration, no database administration needed.

---

## 🌟 Thank You!

Thank you for using the GPA Library Management System. This project represents hundreds of hours of development to make library operations smoother and more efficient.

If this system helps your library, please consider:
- Providing a project completion certificate
- Writing a recommendation letter
- Acknowledging the work in placement season

**Happy Library Management!** 📚✨

---

*Last Updated: December 1, 2025*  
*Version: 5.0 FINAL*  
*For: Government Polytechnic Awasari (Kh) - Computer Department*
