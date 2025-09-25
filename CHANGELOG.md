# Changelog

All notable changes to this project will be documented here. (Manual summary – consider automating later.)

## v5.0_FINAL (Current)
- Added strict manual admin login (no pre-filled credentials)
- Due date flexibility: user can pick 1–7 days (default suggestion 7)
- Word overdue letter export retained; Excel overdue letter UI removed (feature still in code if needed)
- Improved README (system requirements, legacy build path)
- PyInstaller spec updated (correct hidden import `docx`)

## v3.4_FINAL
- Added Word (.docx) formatted overdue notice generation
- Added calendar date pickers for borrow, due, return, and record filters
- Added overdue highlighting & late fine badge
- Auto due-date logic (initially fixed to 7 days)

## Earlier Versions
- Core CRUD for students/books
- Borrow/return tracking with SQLite backend
- Initial packaging & dashboard functionality

---
Future: migrate to semantic versioning (e.g. 5.1.0) and GitHub Releases.
