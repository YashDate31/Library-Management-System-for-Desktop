# Rules for Librarian — GPA Library Management System

This short guide lists daily/weekly/monthly rules and important policies for librarians using the system.

## Daily Tasks
- Open the app and check the Dashboard for new alerts (overdue, low-stock books).
- Issue and return books using correct Enrollment No and Book ID.
- Verify student identity before issuing (match name + enrollment).
- Note any damaged books and update book record.
- **Before sending any email notice:** Verify the student's email address is correct and valid (not blank, no typos).

## Weekly Tasks
- Backup `library.db` to USB (rename with date). Keep one copy off-site.
- Check Records for unreturned books and contact students.
- Send bulk overdue letters if necessary.
- Verify email automation is working by using "Send Reminders Now (Test)" occasionally.

## Monthly Tasks
- Generate monthly reports from Analysis tab and save copies.
- Reconcile fine collection records with cash register (if applicable).
- Archive old reports to a separate folder or USB.

## Promotion / Student Import Best Practices

⚠️ **CRITICAL:** Follow this EXACT order at year-end:

**✅ CORRECT ORDER:**
1. **FIRST:** Click "Promote Students" button
   - 3rd year → Pass Out
   - 2nd year → 3rd year  
   - 1st year → 2nd year
   - Result: No students in 1st year (empty)
2. **THEN:** Import new 1st year students Excel file
   - New students fill the empty 1st year
   - Result: Everyone in correct year ✅

**❌ WRONG ORDER:**
1. ~~Import new students first~~
2. ~~Then promote~~
3. ❌ **Result:** New students get promoted from 1st → 2nd year (WRONG!)

**Why this order works:**
- Promotion empties 1st year by moving everyone up
- Import fills the empty 1st year with new students
- New students never get promoted because they arrive AFTER promotion

**If you did it wrong:**
- New students will be in 2nd year (incorrect)
- Manually edit each student: Change `Class` field to `1st Year`

## Backup & Safety
- Keep at least 3 backups (weekly) and one emergency copy at a different location.
- Never delete `library.db` from the app folder.
- Do not share admin credentials; keep them secure.

## Security & Conduct
- Lock the PC when leaving the desk.
- Use the dedicated Gmail account for library emails (use App Password).
- Do not use personal email for library operations.

## Handling Errors & Escalation
- If data is lost or corrupted, stop using the app and restore latest backup.
- Contact the developer (details in main README) with clear description and a copy of error message.

## Quick Emergency Checklist
1. Close the app.
2. Locate latest USB backup.
3. Replace `library.db` in app folder.
4. Run EXE and verify data.

---
_Last updated: December 1, 2025_
