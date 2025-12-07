# Detailed Implementation Report: Mobile Integration

**Date:** December 07, 2025 **System:** Library Management System (Desktop +
Mobile Extension)

---

## 1. Backend API Development

### What we done

We created a lightweight, standalone web server to act as the bridge between
mobile devices and the central library database. This allows students to query
data without needing direct access to the librarian's machine.

### How we done?

- **Technology**: Implemented using **Python Flask** for its compatibility with
  Windows 7 and minimal setup requirements.
- **File Created**: `api.py` (New component).
- **Endpoints Implemented**:
  - `/api/login`: Authenticates students against the `students` table.
  - `/api/dashboard`: Fetches borrowed books, due dates, and fines using SQL
    aggregates.
  - `/api/history`: Retrieves the complete borrowing log.
  - `/api/catalog`: Implements a search query (`LIKE %term%`) for books.
- **Networking**: Configured to run on host `0.0.0.0` to accept LAN connections.
  Enabled **CORS** (Cross-Origin Resource Sharing) to allow the frontend to
  communicate with the API.

### How can we improve it

- **Security**: Currently uses basic session handling. We could upgrade to **JWT
  (JSON Web Tokens)** for stateless, more secure authentication.
- **Validation**: Add strict schema validation (using Pydantic) for all incoming
  requests to prevent malformed data.
- **Logging**: Implement a rotating file log to track every API request for
  security auditing.

---

## 2. Mobile Frontend Interface

### What we done

We designed and built a "PhD-level" premium mobile web interface for students.
The goal was to replace a potential manual checkout process with a sleek digital
self-service portal.

### How we done?

- **Architecture**: Built as a **Single Page Application (SPA)** structure but
  using vanilla HTML/CSS/JS to avoid complex node_modules build steps on the
  legacy host machine.
- **Files Created**: `static/index.html`, `static/styles.css`, `static/app.js`.
- **Design System**:
  - **Glassmorphism**: Used semi-transparent whites
    (`rgba(255, 255, 255, 0.95)`), backdrop blurs, and subtle shadows for a
    modern feel.
  - **Responsiveness**: Used CSS Grid and Flexbox to ensure perfect rendering on
    all mobile screen sizes.
- **Logic**: `app.js` handles state management (Logged In vs Logged Out), API
  calls (`fetch`), and dynamic DOM updates (populating book lists without
  reloading the page).

### How can we improve it

- **PWA Support**: Add a `manifest.json` and Service Worker to make the website
  installable as a native-like app on phones (Offline capabilities).
- **Framework Migration**: If the features grow, migrating to **React** or
  **Vue** would allow for better component reuse, though it adds a build step.

---

## 3. Desktop Application Integration

### What we done

We modified the existing Tkinter desktop application (`main.py`) to give the
librarian full control over the new mobile system, ensuring they remain the
"Admin".

### How we done?

- **File Modified**: `main.py`.
- **Server Control**: Added a "Start/Stop Server" button to the Dashboard.
  - _Implementation_: Uses Python's `subprocess` module to launch `api.py` in
    the background. On Windows, we used the `CREATE_NO_WINDOW` flag to prevent a
    distracting console pop-up.
- **QR Code**: Integrated a "Show QR Code" feature.
  - _Implementation_: Used `socket` to auto-detect the PC's local WiFi IP (e.g.,
    `192.168.1.5`) and the `qrcode` library to generate a scannable image of
    `http://<IP>:5000`.
- **Cleanup Logic**: Added an `on_closing` handler to automatically kill the
  Flask background process when the main Desktop App is closed, preventing
  zombie processes.

### How can we improve it

- **GUI Logs**: Add a text area in the desktop app to show real-time access logs
  from the mobile server (who is logging in).
- **Configurable Port**: Allow the librarian to change the port from 5000 in
  case of conflicts.

---

## 4. Database Concurrency & Reliability

### What we done

We ensured that the database would not lock or crash when both the Librarian
(Desktop) and a Student (Mobile) tried to access it at the exact same moment.

### How we done?

- **File Modified**: `database.py` and `main.py` (Chart logic).
- **WAL Mode**: Executed `PRAGMA journal_mode=WAL;` at startup. This enables
  **Write-Ahead Logging**, allowing readers and writers to operate
  simultaneously.
- **Error Fixes**:
  - Patched a **ZeroDivisionError** in the Analysis charts (Donut chart) that
    caused crashes when the database was empty. Added safety checks
    (`if total == 0`).
  - Restored accidentally deleted initialization methods (`setup_styles`,
    `load_email_settings`) to ensure stability.

### How can we improve it

- **Database Migration**: For truly high-scale usage (hundreds of concurrent
  students), migrating from SQLite to **PostgreSQL** or **MySQL** would offer
  better performance and data integrity features.
- **Backups**: Implement an automated daily backup of `library.db` to a separate
  location.

---

## 5. Deployment & Dummy Data

### What we done

We streamlined the setup process and verified the system with realistic test
data.

### How we done?

- **Script**: Created `populate_dummy_data.py` to generate 25 students, 15
  books, and various transaction types (Active, Overdue, Returned).
- **Dependencies**: Installed `flask`, `flask-cors`, and `qrcode` using `pip`.
- **Firewall**: Identified the need for a Windows Firewall rule (Port 5000) to
  allow mobile connections.

### How can we improve it

- **Installer**: Create a single `.bat` or `.exe` installer that automatically
  installs Python, dependencies, and sets the Firewall rule, making it
  "one-click" for the user.
