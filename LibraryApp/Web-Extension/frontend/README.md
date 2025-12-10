# 📱 Student Web Portal - Web Extension

> **Development Status**: 🚧 In Active Development

The Student Web Portal is a mobile-friendly web application that allows students
to access library services from their personal devices. It runs as an embedded
Flask server within the main Library Management System desktop application.

---

## 📖 Table of Contents

1. [What is the Web Extension?](#-what-is-the-web-extension)
2. [Architecture Overview](#-architecture-overview)
3. [Technology Stack](#-technology-stack)
4. [How It Works](#-how-it-works)
5. [Developer Setup Guide](#-developer-setup-guide)
6. [Database Structure](#-database-structure)
7. [API Reference](#-api-reference)
8. [Building for Production](#-building-for-production)
9. [Troubleshooting](#-troubleshooting)

---

## 🌐 What is the Web Extension?

The Web Extension is a **supplementary mobile-friendly web portal** that extends
the functionality of the desktop Library Management System. It allows:

- **Students** to check their borrowed books, request renewals, view due dates,
  and manage their library account from any device on the local network
- **Librarians** to share a QR code that students can scan to access the portal
- **Secure sandbox operations** where student requests are queued for librarian
  approval

### Key Features

| Feature           | Description                                         |
| ----------------- | --------------------------------------------------- |
| 📚 Dashboard      | View borrowed books, due dates, and account summary |
| 📖 Catalogue      | Browse available library books                      |
| 📝 Request System | Submit profile updates, book reservations, renewals |
| ⚙️ Settings       | Manage account preferences                          |
| 🔐 Secure Auth    | First-login password change enforcement             |

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    DESKTOP APPLICATION                          │
│                       (main.py)                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Tkinter GUI                           │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │   │
│  │  │Dashboard │ │Students  │ │ Books    │ │ Portal   │    │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Flask Server (student_portal.py)             │   │
│  │              Running on port 5000 (configurable)          │   │
│  │  ┌────────────────┐    ┌─────────────────────────────┐   │   │
│  │  │ REST API       │    │ Static File Server          │   │   │
│  │  │ /api/*         │    │ (React Build - /dist)       │   │   │
│  │  └────────────────┘    └─────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│              ┌───────────────┼───────────────┐                  │
│              ▼               ▼               ▼                  │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐      │
│  │  library.db    │ │   portal.db    │ │  React App     │      │
│  │  (READ-ONLY)   │ │  (READ-WRITE)  │ │  (frontend/)   │      │
│  │  Core Data     │ │  Sandbox Data  │ │                │      │
│  └────────────────┘ └────────────────┘ └────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼ (Local Network)
┌─────────────────────────────────────────────────────────────────┐
│                     STUDENT DEVICES                              │
│     📱 Phone        💻 Tablet        🖥️ Laptop                  │
│     (via QR)        (via URL)        (via URL)                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### Backend (Flask Server)

| Component | Technology     |
| --------- | -------------- |
| Server    | Flask (Python) |
| WSGI      | Waitress       |
| Database  | SQLite3        |
| Session   | Flask Session  |

### Frontend (React SPA)

| Component  | Technology                         |
| ---------- | ---------------------------------- |
| Framework  | React 18                           |
| Build Tool | Vite                               |
| Routing    | React Router DOM                   |
| Styling    | Vanilla CSS + Custom Design System |
| Icons      | Lucide React                       |

---

## ⚙️ How It Works

### 1. Server Initialization

When the desktop application starts and the user navigates to the "Portal" tab,
the Flask server is started in a background thread:

```python
# In main.py
def start_student_portal(self):
    if self.portal_thread and self.portal_thread.is_alive():
        return
    def run_server():
        serve(flask_app, host='0.0.0.0', port=self.portal_port, threads=4)
    self.portal_thread = threading.Thread(target=run_server, daemon=True)
    self.portal_thread.start()
```

### 2. Database Architecture

The system uses **two separate SQLite databases**:

| Database     | Access     | Purpose                                           |
| ------------ | ---------- | ------------------------------------------------- |
| `library.db` | READ-ONLY  | Core library data (students, books, transactions) |
| `portal.db`  | READ-WRITE | Portal-specific data (requests, auth, notes)      |

This **sandbox architecture** ensures students cannot directly modify core
library data.

### 3. Authentication Flow

```
Student Login → Check library.db for enrollment → Create session in portal.db
             → If first login → Force password change
             → Redirect to Dashboard
```

### 4. Request Flow

```
Student submits request → Saved to portal.db (status: pending)
                       → Librarian sees in Portal tab
                       → Approve/Reject → Updates portal.db
```

---

## 👨‍💻 Developer Setup Guide

### Prerequisites

- Python 3.11+ with pip
- Node.js 18+ with npm
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/YashDate31/Library-Management-System-for-Desktop.git
cd Library-Management-System-for-Desktop/LibraryApp
```

### Step 2: Install Python Dependencies

```bash
pip install flask waitress qrcode pillow
```

### Step 3: Set Up the Frontend

```bash
cd Web-Extension/frontend
npm install
```

### Step 4: Initialize Databases

The databases are automatically created when the application runs:

- `library.db` - Created by `database.py` in the LibraryApp folder
- `portal.db` - Created by `student_portal.py` on first import

> **Note**: For testing, you need sample data in `library.db`. Run the main
> desktop app first to create test students and books.

### Step 5: Development Mode (Frontend Hot Reload)

For frontend development with hot reload:

```bash
# Terminal 1: Start Flask backend
cd LibraryApp/Web-Extension
python student_portal.py

# Terminal 2: Start Vite dev server
cd LibraryApp/Web-Extension/frontend
npm run dev
```

The Vite dev server runs on `http://localhost:5173` and proxies API calls to
Flask on port 5000.

### Step 6: Production Build

```bash
cd Web-Extension/frontend
npm run build
```

This creates the `dist/` folder which Flask serves automatically.

---

## 🗄️ Database Structure

### portal.db Tables

#### `student_auth`

Stores student authentication data for the portal.

| Column         | Type      | Description                 |
| -------------- | --------- | --------------------------- |
| id             | INTEGER   | Primary key                 |
| enrollment_no  | TEXT      | Student enrollment (unique) |
| password       | TEXT      | Hashed password             |
| is_first_login | INTEGER   | 1 = must change password    |
| last_changed   | TIMESTAMP | Last password change        |

#### `requests`

Stores student requests awaiting librarian approval.

| Column        | Type      | Description                                          |
| ------------- | --------- | ---------------------------------------------------- |
| id            | INTEGER   | Primary key                                          |
| enrollment_no | TEXT      | Student enrollment                                   |
| request_type  | TEXT      | profile_update, renewal, book_reservation, extension |
| details       | TEXT      | JSON details                                         |
| status        | TEXT      | pending, approved, rejected                          |
| created_at    | TIMESTAMP | Submission time                                      |

#### `deletion_requests`

Stores account deletion requests.

| Column     | Type      | Description                 |
| ---------- | --------- | --------------------------- |
| id         | INTEGER   | Primary key                 |
| student_id | TEXT      | Enrollment number           |
| reason     | TEXT      | Deletion reason             |
| status     | TEXT      | pending, approved, rejected |
| timestamp  | TIMESTAMP | Request time                |

---

## 📡 API Reference

### Authentication

| Endpoint               | Method | Description                           |
| ---------------------- | ------ | ------------------------------------- |
| `/api/login`           | POST   | Login with enrollment_no and password |
| `/api/logout`          | POST   | End session                           |
| `/api/me`              | GET    | Get current user                      |
| `/api/change-password` | POST   | Change password                       |

### Student Data

| Endpoint          | Method | Description            |
| ----------------- | ------ | ---------------------- |
| `/api/dashboard`  | GET    | Get dashboard data     |
| `/api/books`      | GET    | Get book catalogue     |
| `/api/books/<id>` | GET    | Get book details       |
| `/api/alerts`     | GET    | Get user alerts        |
| `/api/services`   | GET    | Get available services |

### Requests

| Endpoint                | Method | Description              |
| ----------------------- | ------ | ------------------------ |
| `/api/request`          | POST   | Submit a request         |
| `/api/request-deletion` | POST   | Request account deletion |

### Admin (Librarian)

| Endpoint                                 | Method | Description              |
| ---------------------------------------- | ------ | ------------------------ |
| `/api/admin/all-requests`                | GET    | Get all pending requests |
| `/api/admin/requests/<id>/approve`       | POST   | Approve request          |
| `/api/admin/requests/<id>/reject`        | POST   | Reject request           |
| `/api/admin/deletion/<id>/approve`       | POST   | Approve deletion         |
| `/api/admin/deletion/<id>/reject`        | POST   | Reject deletion          |
| `/api/admin/password-reset/<enrollment>` | POST   | Reset password           |
| `/api/admin/stats`                       | GET    | Get portal statistics    |

---

## 🏭 Building for Production

### 1. Build the React Frontend

```bash
cd Web-Extension/frontend
npm run build
```

### 2. Verify the Build

The build output should be in `frontend/dist/`:

```
dist/
├── assets/
│   ├── index-[hash].css
│   └── index-[hash].js
├── index.html
└── vite.svg
```

### 3. Test with Flask

The Flask server automatically serves the build:

```python
app = Flask(__name__, static_folder='frontend/dist')
```

Navigate to `http://localhost:5000` to test.

---

## 🔧 Troubleshooting

### Common Issues

#### "Portal server not responding"

- Check if Flask is running on port 5000
- Verify no firewall blocking the port
- Check console for Python errors

#### "Database locked"

- Ensure only one instance of the app is running
- Close any SQLite browser tools

#### "CORS errors in development"

- Use Vite's proxy configuration in `vite.config.js`
- Or run the full production build

#### "QR code not scanning"

- Ensure both devices are on the same Wi-Fi network
- Check IP address is correct (not 127.0.0.1)

### Debug Mode

Run Flask directly for debugging:

```bash
cd Web-Extension
python student_portal.py
```

This runs with `debug=True` for hot reload and detailed error messages.

---

## 📁 Project Structure

```
Web-Extension/
├── student_portal.py      # Flask backend server
├── portal.db              # Portal sandbox database
└── frontend/
    ├── dist/              # Production build (served by Flask)
    ├── src/
    │   ├── components/    # Reusable React components
    │   ├── context/       # React context providers
    │   ├── pages/         # Page components
    │   ├── App.jsx        # Main app with routing
    │   ├── index.css      # Global styles
    │   └── main.jsx       # React entry point
    ├── package.json       # NPM dependencies
    ├── vite.config.js     # Vite build configuration
    └── README.md          # This file
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Build and test: `npm run build`
5. Commit: `git commit -m 'Add my feature'`
6. Push: `git push origin feature/my-feature`
7. Create a Pull Request

---

## 📝 License

This project is part of the GPA Library Management System.

---

_Last Updated: December 2024_
