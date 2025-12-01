# Quick Reference & Suggestions — GPA Library Management System

This single-page reference is for a busy librarian or teacher who needs the essentials fast.

## Quick Start (30 seconds)
- Copy `LibraryManagementSystem_v5.0_FINAL.exe` to `C:\GPA_Library\`
- Run EXE → Login (`gpa` / `gpa123`) → Change password
- Backup `library.db` now (copy to USB)

## Most Important Rules
- **Year-end order:** Click **Promote Students** FIRST (empties 1st year) → THEN import new 1st year students.
- Always backup `library.db` before any major action (promotion, bulk import).
- **USB Pendrive:** You CAN run the EXE directly from USB - the USB becomes your backup!

## Useful Shortcuts
- Ctrl+F = Search
- Ctrl+R = Refresh
- Ctrl+E = Export
- Ctrl+P = Print (analysis)

## Emergency Recovery (fast)
1. Close app.
2. Replace `library.db` with latest backup (copy to app folder).
3. Run EXE and verify Dashboard.

## When to Contact Developer
- Data corruption or missing records after restore
- Persistent email authentication errors after resetting App Password
- Unexpected crashes or missing features

Developer contact in main README (developer phone & email).

## My Suggestion (one improvement)
- Add an import-time flag: when importing students, prompt: "Mark all imported students as 1st Year? (Yes/No)" — this prevents accidental promotions if import happens after promotion.

---
_Last updated: December 1, 2025_
