# Features — GPA Library Management System (Summary)

A concise reference describing what each major feature does and why it matters.

## Student Management
- Add/Edit/Search students, import/export via Excel.
- Fields: Enrollment No, Name, Class, Division, Roll No, Contact, Email, Year.

Why: Keeps all borrower details in one place and enables email notifications.

## Book Management
- Add/Edit books, manage categories, track total vs available copies.
- Bulk import from Excel and category filters.

Why: Fast cataloging and accurate availability tracking.

## Transactions (Issue/Return)
- Issue books with due date (default 7 days).
- Return books and automatic fine calculation (₹5/day).
- Prevent issuing to `Pass Out` students.

Why: Automates every-day lending operations and enforces due dates.

## Records & Overdue Letters
- Full transaction history with search and filters.
- Generate professional Word overdue letters (single or bulk).
- Option to send letters by email automatically.

Why: Simplifies follow-up and maintains records for audits.

## Email Automation & Auto-Reminders
- Send overdue letters and reminders via Gmail (App Password required).
- Auto-reminders run daily at 9:00 AM (configurable days-before).
- Email history is logged with status for each send.

Why: Reduces manual work and reduces overdue items.

## Analytics Dashboard
- Charts for issue trends, top borrowers, popular books, category distribution, and fine collection.
- Export charts and data to Excel/Word.

Why: Helps the librarian and department analyze usage and make procurement decisions.

## Academic Year Promotion
- End-of-year promotion: 1st→2nd, 2nd→3rd, 3rd→Pass Out.
- Promotion action updates academic year and maintains promotion history.
- WARNING: Promote FIRST (empties 1st year), THEN import new 1st year students (see main README).

Why: Keeps student year assignment accurate across academic cycles.

## Portability & Backup
- Single-file DB: `library.db` — backup-ready and portable.
- Recommended: weekly USB backups and optional cloud backup (Google Drive).

Why: Simple, offline-first data model for easy handover and recovery.

---
_Last updated: December 1, 2025_
