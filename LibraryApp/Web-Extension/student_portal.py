from flask import Flask, session, jsonify, request, send_from_directory
import sqlite3
import os
import json
from datetime import datetime

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Serve React Build
app = Flask(__name__, static_folder='frontend/dist', static_url_path='/')
app.secret_key = 'LIBRARY_PORTAL_SECRET_KEY_YASH_MVP'

def get_library_db():
    """Read-Only Connection to Core Data"""
    db_path = os.path.join(os.path.dirname(BASE_DIR), 'library.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def get_portal_db():
    """Read-Write Connection to Sandbox Data"""
    db_path = os.path.join(BASE_DIR, 'portal.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_portal_db():
    """Initialize the Sandbox DB for Requests and Notes"""
    conn = get_portal_db()
    cursor = conn.cursor()
    
    # Requests Table (Profile Updates, Book Renewals, etc.)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            req_id INTEGER PRIMARY KEY AUTOINCREMENT,
            enrollment_no TEXT,
            request_type TEXT,      -- 'profile_update', 'renewal', 'extension', 'notification'
            details TEXT,           -- JSON payload or text description
            status TEXT DEFAULT 'pending', -- 'pending', 'approved', 'rejected'
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Notes Table (Personal Reading Log)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS personal_notes (
            note_id INTEGER PRIMARY KEY AUTOINCREMENT,
            enrollment_no TEXT,
            book_title TEXT,
            note_content TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

# Initialize on Import
init_portal_db()

# --- Auth Endpoints ---

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    enrollment = data.get('enrollment_no')
    
    conn = get_library_db() # READ ONLY
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE enrollment_no = ?", (enrollment,))
    student = cursor.fetchone()
    conn.close()
    
    if student:
        session['student_id'] = student['enrollment_no']
        session['name'] = student['name']
        
        return jsonify({
            'status': 'success',
            'user': {
                'name': student['name'],
                'enrollment_no': student['enrollment_no'],
                'department': student['department'],
                'year': student['year'],
                # Only showing read-only fields
            }
        })
    return jsonify({'status': 'error', 'message': 'Invalid Enrollment Number'}), 401

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'status': 'success'})

@app.route('/api/me')
def api_me():
    if 'student_id' not in session:
        return jsonify({'user': None})
    
    conn = get_library_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE enrollment_no = ?", (session['student_id'],))
    student = cursor.fetchone()
    conn.close()
    
    if student:
        return jsonify({'user': {
            'name': student['name'],
            'enrollment_no': student['enrollment_no'],
            'department': student['department'],
            'year': student['year']
        }})
    return jsonify({'user': None})

# --- Dashboard Data Aggregation ---

@app.route('/api/dashboard')
def api_dashboard():
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    enrollment = session['student_id']
    
    # 1. Fetch Core Data (Read-Only)
    conn = get_library_db()
    cursor = conn.cursor()
    
    # Active Loans
    cursor.execute("""
        SELECT b.title, b.author, br.borrow_date, br.due_date, br.book_id
        FROM borrow_records br
        JOIN books b ON br.book_id = b.book_id
        WHERE br.enrollment_no = ? AND br.status = 'borrowed'
        ORDER BY br.due_date ASC
    """, (enrollment,))
    raw_borrows = cursor.fetchall()
    
    # History
    cursor.execute("""
        SELECT b.title, b.author, b.category, br.borrow_date, br.return_date, br.status
        FROM borrow_records br
        JOIN books b ON br.book_id = b.book_id
        WHERE br.enrollment_no = ? AND br.status = 'returned'
        ORDER BY br.return_date DESC
        LIMIT 50
    """, (enrollment,))
    raw_history = cursor.fetchall()
    
    conn.close()
    
    # 2. Process Business Logic (Fines/Alerts)
    borrows = []
    notifications = []
    today = datetime.now()
    
    for row in raw_borrows:
        item = dict(row)
        if item['due_date']:
            try:
                due_dt = datetime.strptime(item['due_date'], '%Y-%m-%d')
                delta = (due_dt - today).days
                
                # Logic: Green (3+), Yellow (1-2), Red (<0)
                if delta < 0:
                    item['status'] = 'overdue'
                    overdue_days = abs(delta)
                    item['days_msg'] = f"Overdue by {overdue_days} days"
                    item['fine_est'] = overdue_days * 10 # Example fine calculation
                    notifications.append({
                        'type': 'danger',
                        'msg': f"'{item['title']}' is OVERDUE! Please return immediately."
                    })
                elif delta <= 2:
                    item['status'] = 'warning'
                    item['days_msg'] = f"Due in {delta} days"
                    notifications.append({
                        'type': 'warning',
                        'msg': f"'{item['title']}' is due soon ({delta} days)."
                    })
                else:
                    item['status'] = 'safe'
                    item['days_msg'] = f"{delta} days left"
            except:
                item['status'] = 'unknown'
                item['days_msg'] = '-'
        borrows.append(item)

    # 3. Fetch Sandbox Data (Requests Status)
    conn_portal = get_portal_db()
    cursor_p = conn_portal.cursor()
    cursor_p.execute("SELECT * FROM requests WHERE enrollment_no = ? ORDER BY created_at DESC LIMIT 5", (enrollment,))
    requests = [dict(row) for row in cursor_p.fetchall()]
    conn_portal.close()

    # 4. Analytics & Gamification (Computed on Read-Only Data)
    stats = {
        'total_books': len(raw_history) + len(raw_borrows),
        'total_fines': sum([10 for x in raw_borrows if x.get('status') == 'overdue']), # Mock calculation
        'fav_category': 'General',
        'categories': {}
    }
    
    # Category Dist
    cat_count = {}
    for book in raw_history:
        cat = book['category'] or 'Uncategorized'
        cat_count[cat] = cat_count.get(cat, 0) + 1
    
    stats['categories'] = cat_count
    if cat_count:
        stats['fav_category'] = max(cat_count, key=cat_count.get)
        
    # Badges Logic
    badges = []
    if stats['total_books'] >= 5:
        badges.append({'id': 'bookworm', 'label': 'Bookworm', 'icon': '🐛', 'color': 'bg-emerald-100 text-emerald-700'})
    if stats['total_books'] >= 10:
        badges.append({'id': 'scholar', 'label': 'Scholar', 'icon': '🎓', 'color': 'bg-indigo-100 text-indigo-700'})
    
    # Check for overdue history
    has_overdues = any(x['status'] == 'overdue' for x in raw_history) # raw_history needs status mapping
    if not has_overdues and stats['total_books'] > 2:
        badges.append({'id': 'clean_sheet', 'label': 'Clean Sheet', 'icon': '🛡️', 'color': 'bg-blue-100 text-blue-700'})

    # 4. Library Notices (Mock/Static for now)
    notices = [
        {"id": 1, "title": "Repo Update", "date": "2025-12-09", "content": "System maintenance scheduled for Sunday."},
        {"id": 2, "title": "New Arrivals", "date": "2025-12-08", "content": "Check out the new AI section in Isle 4."}
    ]

    return jsonify({
        'borrows': borrows,
        'history': [dict(row) for row in raw_history],
        'notices': notices,
        'notifications': notifications,
        'recent_requests': requests,
        'analytics': {
            'stats': stats,
            'badges': badges
        }
    })

# --- Write Endpoints (Sandbox Only) ---

@app.route('/api/request', methods=['POST'])
def api_submit_request():
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    req_type = data.get('type') # 'profile_update', 'renewal'
    details = data.get('details') # e.g., "Change email to x@y.com"
    
    if not req_type or not details:
        return jsonify({'error': 'Missing data'}), 400
    
    try:
        conn = get_portal_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO requests (enrollment_no, request_type, details) VALUES (?, ?, ?)",
                       (session['student_id'], req_type, json.dumps(details)))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Request submitted to librarian'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/books')
def api_books():
    # Read-Only Catalogue
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    conn = get_library_db()
    cursor = conn.cursor()
    
    sql = "SELECT book_id, title, author, category, total_copies, available_copies FROM books WHERE 1=1"
    params = []
    
    if query:
        sql += " AND (title LIKE ? OR author LIKE ?)"
        params.extend([f'%{query}%', f'%{query}%'])
    if category and category != 'All':
        sql += " AND category = ?"
        params.append(category)
        
    sql += " ORDER BY title LIMIT 50"
    
    cursor.execute(sql, params)
    books = [dict(row) for row in cursor.fetchall()]
    
    # Get distinct categories for filter
    cursor.execute("SELECT DISTINCT category FROM books WHERE category IS NOT NULL ORDER BY category")
    categories = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return jsonify({'books': books, 'categories': categories})

# --- SPA Serving ---
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)
