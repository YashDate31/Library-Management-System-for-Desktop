# Setup — GPA Library Management System

## Purpose
Quick installation and first-run steps so the app works reliably on any Windows PC.

## System Requirements
- Windows 7/8/10/11 (64-bit)
- No additional software required (EXE is standalone)
- Recommended: 4 GB RAM, 1 GB free disk space

## Installation (Copy & Run)
1. Create a folder on the PC, e.g. `C:\GPA_Library\`
2. Copy `LibraryManagementSystem_v5.0_FINAL.exe` into that folder
3. Double-click the EXE to run
4. On first run the app creates these files automatically:
   - `library.db` (your database)
   - `email_settings.json` (email config)
   - `email_history.json` (sent email log)
5. Login with default credentials:
   - Username: `gpa`  Password: `gpa123`
6. Immediately change the admin password (Admin → Change Password)

## Recommended First Checks
- Verify `library.db` exists in same folder as EXE
- Configure email settings if you plan to use email features
- Make an initial backup: copy `library.db` to a USB (rename with date)

## Backup & Restore Quick Steps
- Weekly: Close the app → copy `library.db` to USB → rename `library_backup_DD_MMM_YYYY.db`
- To restore: place backup in `C:\GPA_Library\` and rename to `library.db`, then run EXE

## Run From USB
- Recommended: COPY EXE and files from USB to PC before running (do NOT run directly from USB as the app modifies files)

## Troubleshooting Quick Tips
- If EXE does nothing: run as Administrator and check antivirus
- If emails fail: ensure internet and App Password are correct
- If data seems missing: check for `library.db` in the folder and restore from backup

---
_Last updated: December 1, 2025_
