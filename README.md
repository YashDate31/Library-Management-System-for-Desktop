# Library Management System (Desktop)

Modern Tkinter-based library application with Word overdue notices, calendar date pickers, and Excel exports.

- Primary app: `LibraryApp/main.py`
- Packaging: PyInstaller spec(s) in `LibraryApp/`
- Executables and artifacts at project root are legacy snapshots; the source of truth is in `LibraryApp/`.

## GitHub Repository

Target repo: https://github.com/YashDate31/Library-Management-System-for-Desktop

## Quick Git Setup (PowerShell)

```powershell
# From project root
cd "c:\Users\Yash\OneDrive\Desktop\Library Management System"

git init
git branch -M main

# If you haven't configured global identity on this PC
git config user.name "Yash Date"
git config user.email "you@example.com"

# Add remote (use your repo URL)
git remote add origin https://github.com/YashDate31/Library-Management-System-for-Desktop.git

# First commit
git add .
git commit -m "Initial commit: Library Management System source and build artifacts"

# Push
git push -u origin main
```

If pushing from a new machine, ensure you’re signed in to GitHub in your browser or have a Personal Access Token (PAT) ready for HTTPS authentication.
