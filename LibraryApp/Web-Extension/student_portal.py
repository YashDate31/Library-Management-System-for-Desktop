from flask import Flask, session, jsonify, request, send_from_directory
import sqlite3
import os
import json
from datetime import datetime

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Serve React Build
# Serve React Build
app = Flask(__name__, static_folder='frontend/dist')
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
    
    # Auth Table (Shadow Auth)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_auth (
            enrollment_no TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            is_first_login INTEGER DEFAULT 1, -- 1=True, 0=False
            last_changed DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create Deletion Requests Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deletion_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            reason TEXT,
            status TEXT DEFAULT 'pending', -- pending, approved, rejected
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(student_id) REFERENCES students(enrollment_no)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize on Import
init_portal_db()

# --- Auth Endpoints ---

@app.route('/api/request-deletion', methods=['POST'])
def request_deletion():
    data = request.json
    password = data.get('password')
    reason = data.get('reason', 'User requested deletion via Student Portal')
    
    # 1. Verify Session
    if 'student_id' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
        
    student_id = session['student_id']
    
    conn = get_portal_db()
    c = conn.cursor()
    
    # 2. Verify Password (Re-authentication)
    # Check student_auth first
    c.execute("SELECT password FROM student_auth WHERE enrollment_no = ?", (student_id,))
    auth_record = c.fetchone()
    
    is_valid = False
    if auth_record:
        # Check against stored password
        if auth_record['password'] == password:
            is_valid = True
    else:
        # Fallback to legacy (enrollment_no itself) for very old accounts not yet migrated?
        # But our login flow forces migration. We'll assume if they are logged in, they might have an auth record.
        # If not, strictly check against enrollment_no if that was the "password"
        if password == student_id:
            is_valid = True
            
    if not is_valid:
        conn.close()
        return jsonify({"status": "error", "message": "Incorrect password"}), 403
        
    # 3. Check for existing pending request
    c.execute("SELECT id FROM deletion_requests WHERE student_id = ? AND status = 'pending'", (student_id,))
    existing = c.fetchone()
    if existing:
        conn.close()
        return jsonify({"status": "error", "message": "A deletion request is already pending."}), 400
        
    # 4. Create Request
    try:
        c.execute("INSERT INTO deletion_requests (student_id, reason) VALUES (?, ?)", (student_id, reason))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Deletion request submitted for librarian approval."})
    except Exception as e:
        conn.close()
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    enrollment = data.get('enrollment_no')
    password = data.get('password')
    
    if not enrollment:
        return jsonify({'status': 'error', 'message': 'Enrollment number required'}), 400
    
    # 1. Check if student exists in MAIN DB (Read-Only)
    conn_lib = get_library_db()
    cursor_lib = conn_lib.cursor()
    cursor_lib.execute("SELECT * FROM students WHERE enrollment_no = ?", (enrollment,))
    student = cursor_lib.fetchone()
    conn_lib.close()
    
    if not student:
        return jsonify({'status': 'error', 'message': 'Student not found'}), 401
    
    # 2. Check Auth Status in PORTAL DB (Shadow Auth)
    conn_portal = get_portal_db()
    cursor_p = conn_portal.cursor()
    cursor_p.execute("SELECT * FROM student_auth WHERE enrollment_no = ?", (enrollment,))
    auth_record = cursor_p.fetchone()
    
    require_change = False
    
    if not auth_record:
        # FIRST LOGIN ATTEMPT EVER for this user
        # Default behavior: Password MUST be enrollment number
        if password == enrollment:
            # Create auth record
            cursor_p.execute("INSERT INTO student_auth (enrollment_no, password, is_first_login) VALUES (?, ?, 1)", 
                             (enrollment, enrollment)) # In prod, use HASH!
            conn_portal.commit()
            require_change = True
        else:
            conn_portal.close()
            return jsonify({'status': 'error', 'message': 'Invalid credentials. For first login, use enrollment number as password.'}), 401
    else:
        # Subsequent Logins
        stored_password = auth_record['password']
        is_first = auth_record['is_first_login']
        
        if password == stored_password:
            if is_first:
                require_change = True
        else:
            conn_portal.close()
            return jsonify({'status': 'error', 'message': 'Invalid password'}), 401
            
    conn_portal.close()
    
    # Login Successful
    session['student_id'] = student['enrollment_no']
    session['name'] = student['name']
    
    return jsonify({
        'status': 'success',
        'require_change': require_change,
        'user': {
            'name': student['name'],
            'enrollment_no': student['enrollment_no'],
            'department': student['department'],
            'year': student['year'],
        }
    })

@app.route('/api/change-password', methods=['POST'])
def api_change_password():
    if 'student_id' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
        
    data = request.json
    new_password = data.get('new_password')
    
    if not new_password or len(new_password) < 4:
        return jsonify({'status': 'error', 'message': 'Password too short'}), 400
        
    enrollment = session['student_id']
    
    conn = get_portal_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE student_auth 
        SET password = ?, is_first_login = 0, last_changed = CURRENT_TIMESTAMP
        WHERE enrollment_no = ?
    """, (new_password, enrollment))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'message': 'Password updated successfully'})

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
        # Get student's year properly
        student_year = student['year'] if student['year'] else '1st'
        return jsonify({'user': {
            'name': student['name'],
            'enrollment_no': student['enrollment_no'],
            'department': student['department'],
            'year': student_year,
            'email': dict(student).get('email', f"{student['name'].replace(' ', '.').lower()}@gpa.edu"),
            'phone': dict(student).get('phone', 'N/A'),
            'privileges': {
                 'max_books': 5,
                 'loan_duration': '7 Days',
                 'renewal_limit': '2 Renewals per book'
            },
            'account_info': {
                'password_last_changed': 'Recently'
            }
        }})
    return jsonify({'user': None})

@app.route('/api/user-policies')
def api_user_policies():
    """Fetch user specific policies and account info"""
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    return jsonify({
        'policies': {
            'max_books': 5,
            'loan_duration': '7 Days',
            'renewal_limit': '2 Renewals per book',
            'password_last_changed': 'Recently'
        }
    })

@app.route('/api/alerts')
def api_alerts():
    """Lightweight check for overdue items and security alerts"""
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    enrollment = session['student_id']
    
    # 1. Check Security Alert (Highest Priority)
    conn_portal = get_portal_db()
    cursor_p = conn_portal.cursor()
    cursor_p.execute("SELECT is_first_login FROM student_auth WHERE enrollment_no = ?", (enrollment,))
    auth_record = cursor_p.fetchone()
    conn_portal.close()
    
    if auth_record and auth_record['is_first_login']:
        return jsonify({
            'has_alert': True,
            'type': 'security',
            'message': 'Action Required: Change Default Password',
            'action_link': '/settings', # Or prompt modal
            'count': 1
        })
    
    # 2. Check Overdue Items
    conn = get_library_db()
    cursor = conn.cursor()
    
    # Check for active borrows only - fast query
    cursor.execute("""
        SELECT b.title, br.due_date
        FROM borrow_records br
        JOIN books b ON br.book_id = b.book_id
        WHERE br.enrollment_no = ? AND br.status = 'borrowed'
    """, (enrollment,))
    
    borrows = cursor.fetchall()
    conn.close()
    
    today = datetime.now()
    overdue_count = 0
    total_fine = 0
    overdue_titles = []
    
    for row in borrows:
        if row['due_date']:
            try:
                due_dt = datetime.strptime(row['due_date'], '%Y-%m-%d')
                delta = (due_dt - today).days
                if delta < 0:
                    overdue_count += 1
                    days_late = abs(delta)
                    total_fine += days_late * 10 # 10 INR per day
                    overdue_titles.append(row['title'])
            except:
                pass
                
    return jsonify({
        'has_alert': overdue_count > 0,
        'type': 'overdue',
        'count': overdue_count,
        'fine_estimate': total_fine,
        'items': overdue_titles
    })

@app.route('/api/services')
def api_services():
    """Fetch available digital resources and services"""
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # In a real app, these would be in a 'resources' table
    resources = [
        {
            'id': 1,
            'title': "IEEE Xplore Access",
            'type': "Research Database",
            'description': "Full access to IEEE journals, conferences, and standards.",
            'link': "#",
            'icon': "Globe"
        },
        {
            'id': 2,
            'title': "ProQuest E-Books",
            'type': "E-Book Platform",
            'description': "Access to over 150,000 academic e-books.",
            'link': "#",
            'icon': "Book"
        },
        {
            'id': 3,
            'title': "JSTOR Archive",
            'type': "Journal Archive",
            'description': "Academic journal archive for humanities and sciences.",
            'link': "#",
            'icon': "Archive"
        }
    ]
    
    return jsonify({'resources': resources})

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
    
    # High Priority Auth Alert
    conn_portal = get_portal_db()
    cursor_p = conn_portal.cursor()
    cursor_p.execute("SELECT is_first_login FROM student_auth WHERE enrollment_no = ?", (enrollment,))
    auth_record = cursor_p.fetchone()
    conn_portal.close()
    
    if auth_record and auth_record['is_first_login']:
         notifications.append({
            'type': 'danger',
            'title': 'Security Alert',
            'msg': "You are using the default password. Please change it immediately."
        })

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
        'total_books': len(raw_history) + len(borrows),
        'total_fines': sum([10 for x in borrows if x.get('status') == 'overdue']), # Estimated current fines
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

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book_details(book_id):
    """Fetch details for a specific book."""
    try:
        conn = get_library_db()
        cursor = conn.cursor()
        
        # Fetch book details
        cursor.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
        book = cursor.fetchone()
        
        if not book:
            conn.close()
            return jsonify({'error': 'Book not found'}), 404
            
        book_data = dict(book)
        
        # Calculate availability
        cursor.execute("SELECT COUNT(*) FROM borrow_records WHERE book_id = ? AND status = 'borrowed'", (book_id,))
        borrowed_count = cursor.fetchone()[0]
        book_data['available_copies'] = book_data['total_copies'] - borrowed_count
        
        conn.close()
        return jsonify(book_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

# --- Admin/Librarian API Endpoints ---

@app.route('/api/admin/all-requests')
def api_admin_all_requests():
    """Fetch all pending requests for librarian management"""
    conn = get_portal_db()
    cursor = conn.cursor()
    
    # Fetch general requests (profile_update, renewal, book_reservation, etc.)
    cursor.execute("""
        SELECT id as req_id, enrollment_no, request_type, details, status, created_at
        FROM requests
        WHERE status = 'pending'
        ORDER BY created_at DESC
    """)
    general_requests = []
    for row in cursor.fetchall():
        req = dict(row)
        # Try to parse JSON details
        try:
            req['details'] = json.loads(req['details']) if req['details'] else {}
        except:
            req['details'] = {'raw': req['details']}
        general_requests.append(req)
    
    # Fetch deletion requests
    cursor.execute("""
        SELECT id, student_id, reason, status, timestamp
        FROM deletion_requests
        WHERE status = 'pending'
        ORDER BY timestamp DESC
    """)
    deletion_requests = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    # Get student names from library DB
    conn_lib = get_library_db()
    cursor_lib = conn_lib.cursor()
    
    # Enrich general requests with student names
    for req in general_requests:
        cursor_lib.execute("SELECT name FROM students WHERE enrollment_no = ?", (req['enrollment_no'],))
        student = cursor_lib.fetchone()
        req['student_name'] = student['name'] if student else 'Unknown'
    
    # Enrich deletion requests with student names
    for req in deletion_requests:
        cursor_lib.execute("SELECT name FROM students WHERE enrollment_no = ?", (req['student_id'],))
        student = cursor_lib.fetchone()
        req['student_name'] = student['name'] if student else 'Unknown'
    
    conn_lib.close()
    
    # Get rejected count from portal DB
    conn2 = get_portal_db()
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT COUNT(*) as count FROM requests WHERE status = 'rejected'")
    rejected_count = cursor2.fetchone()['count']
    
    # Get deletion counts by status
    cursor2.execute("SELECT status, COUNT(*) as count FROM deletion_requests GROUP BY status")
    deletion_counts = {row['status']: row['count'] for row in cursor2.fetchall()}
    conn2.close()
    
    return jsonify({
        'requests': general_requests,
        'deletion_requests': deletion_requests,
        'rejected_count': rejected_count,
        'deletion_counts': deletion_counts,
        'counts': {
            'total': len(general_requests) + len(deletion_requests),
            'requests': len(general_requests),
            'deletions': len(deletion_requests)
        }
    })

@app.route('/api/admin/request-history')
def api_admin_request_history():
    """Fetch processed (approved/rejected) requests for history view"""
    conn = get_portal_db()
    cursor = conn.cursor()
    
    # Fetch approved and rejected requests
    cursor.execute("""
        SELECT id as req_id, enrollment_no, request_type, details, status, created_at
        FROM requests
        WHERE status IN ('approved', 'rejected')
        ORDER BY created_at DESC
        LIMIT 50
    """)
    processed_requests = []
    for row in cursor.fetchall():
        req = dict(row)
        try:
            req['details'] = json.loads(req['details']) if req['details'] else {}
        except:
            req['details'] = {'raw': req['details']}
        processed_requests.append(req)
    
    conn.close()
    
    # Get student names from library DB
    conn_lib = get_library_db()
    cursor_lib = conn_lib.cursor()
    
    for req in processed_requests:
        cursor_lib.execute("SELECT name FROM students WHERE enrollment_no = ?", (req['enrollment_no'],))
        student = cursor_lib.fetchone()
        req['student_name'] = student['name'] if student else 'Unknown'
    
    conn_lib.close()
    
    # Count by status
    approved_count = len([r for r in processed_requests if r['status'] == 'approved'])
    rejected_count = len([r for r in processed_requests if r['status'] == 'rejected'])
    
    return jsonify({
        'history': processed_requests,
        'counts': {
            'approved': approved_count,
            'rejected': rejected_count,
            'total': len(processed_requests)
        }
    })

@app.route('/api/admin/deletion-history')
def api_admin_deletion_history():
    """Fetch processed deletion requests for history view"""
    conn = get_portal_db()
    cursor = conn.cursor()
    
    # Fetch approved and rejected deletions
    cursor.execute("""
        SELECT id, student_id, reason, status, timestamp
        FROM deletion_requests
        WHERE status IN ('approved', 'rejected')
        ORDER BY timestamp DESC
        LIMIT 50
    """)
    processed_deletions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # Get student names from library DB
    conn_lib = get_library_db()
    cursor_lib = conn_lib.cursor()
    
    for req in processed_deletions:
        cursor_lib.execute("SELECT name FROM students WHERE enrollment_no = ?", (req['student_id'],))
        student = cursor_lib.fetchone()
        req['student_name'] = student['name'] if student else 'Deleted Account'
    
    conn_lib.close()
    
    # Count by status
    approved_count = len([r for r in processed_deletions if r['status'] == 'approved'])
    rejected_count = len([r for r in processed_deletions if r['status'] == 'rejected'])
    
    return jsonify({
        'history': processed_deletions,
        'counts': {
            'approved': approved_count,
            'rejected': rejected_count,
            'total': len(processed_deletions)
        }
    })

@app.route('/api/admin/requests/<int:req_id>/approve', methods=['POST'])
def api_admin_approve_request(req_id):
    """Approve a general request"""
    conn = get_portal_db()
    cursor = conn.cursor()
    
    # Get the request details
    cursor.execute("SELECT * FROM requests WHERE id = ?", (req_id,))
    req = cursor.fetchone()
    
    if not req:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Request not found'}), 404
    
    # Update status to approved
    cursor.execute("UPDATE requests SET status = 'approved' WHERE id = ?", (req_id,))
    conn.commit()
    conn.close()
    
    # If it's a profile update, we could apply changes to main DB here
    # For now, just mark as approved (librarian can manually update if needed)
    
    return jsonify({'status': 'success', 'message': 'Request approved'})

@app.route('/api/admin/requests/<int:req_id>/reject', methods=['POST'])
def api_admin_reject_request(req_id):
    """Reject a general request"""
    conn = get_portal_db()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE requests SET status = 'rejected' WHERE id = ?", (req_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'message': 'Request rejected'})

@app.route('/api/admin/deletion/<int:del_id>/approve', methods=['POST'])
def api_admin_approve_deletion(del_id):
    """Approve account deletion request"""
    conn = get_portal_db()
    cursor = conn.cursor()
    
    # Get deletion request
    cursor.execute("SELECT student_id FROM deletion_requests WHERE id = ?", (del_id,))
    req = cursor.fetchone()
    
    if not req:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Deletion request not found'}), 404
    
    student_id = req['student_id']
    
    # Update status
    cursor.execute("UPDATE deletion_requests SET status = 'approved' WHERE id = ?", (del_id,))
    
    # Also clean up auth record
    cursor.execute("DELETE FROM student_auth WHERE enrollment_no = ?", (student_id,))
    conn.commit()
    conn.close()
    
    # Note: Actual student deletion from main DB should be done via the main app
    # This just marks the request as approved
    
    return jsonify({
        'status': 'success', 
        'message': 'Deletion approved. Student auth removed.',
        'student_id': student_id
    })

@app.route('/api/admin/deletion/<int:del_id>/reject', methods=['POST'])
def api_admin_reject_deletion(del_id):
    """Reject account deletion request"""
    conn = get_portal_db()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE deletion_requests SET status = 'rejected' WHERE id = ?", (del_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'message': 'Deletion request rejected'})

@app.route('/api/admin/password-reset/<enrollment_no>', methods=['POST'])
def api_admin_reset_password(enrollment_no):
    """Reset student password to enrollment number"""
    conn = get_portal_db()
    cursor = conn.cursor()
    
    # Check if auth record exists
    cursor.execute("SELECT * FROM student_auth WHERE enrollment_no = ?", (enrollment_no,))
    auth = cursor.fetchone()
    
    if auth:
        # Reset to enrollment number and mark as first login
        cursor.execute("""
            UPDATE student_auth 
            SET password = ?, is_first_login = 1, last_changed = CURRENT_TIMESTAMP
            WHERE enrollment_no = ?
        """, (enrollment_no, enrollment_no))
    else:
        # Create new auth record with default password
        cursor.execute("""
            INSERT INTO student_auth (enrollment_no, password, is_first_login)
            VALUES (?, ?, 1)
        """, (enrollment_no, enrollment_no))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'status': 'success', 
        'message': f'Password reset to enrollment number. Student will be prompted to change on next login.'
    })

@app.route('/api/admin/auth-stats')
def api_admin_auth_stats():
    """Get auth statistics and recent password resets for dashboard"""
    conn = get_portal_db()
    cursor = conn.cursor()
    
    # Total registered students
    cursor.execute("SELECT COUNT(*) as count FROM student_auth")
    total_registered = cursor.fetchone()['count']
    
    # Students with changed passwords (not first login)
    cursor.execute("SELECT COUNT(*) as count FROM student_auth WHERE is_first_login = 0")
    active_users = cursor.fetchone()['count']
    
    # Students still on default password
    cursor.execute("SELECT COUNT(*) as count FROM student_auth WHERE is_first_login = 1")
    pending_change = cursor.fetchone()['count']
    
    # Recent password resets (by checking last_changed within last 7 days where is_first_login = 1)
    cursor.execute("""
        SELECT enrollment_no, last_changed 
        FROM student_auth 
        WHERE is_first_login = 1 AND last_changed IS NOT NULL
        ORDER BY last_changed DESC 
        LIMIT 10
    """)
    recent_resets = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    # Get student names
    conn_lib = get_library_db()
    cursor_lib = conn_lib.cursor()
    
    for reset in recent_resets:
        cursor_lib.execute("SELECT name FROM students WHERE enrollment_no = ?", (reset['enrollment_no'],))
        student = cursor_lib.fetchone()
        reset['student_name'] = student['name'] if student else 'Unknown'
    
    conn_lib.close()
    
    return jsonify({
        'stats': {
            'total_registered': total_registered,
            'active_users': active_users,
            'pending_change': pending_change
        },
        'recent_resets': recent_resets
    })

@app.route('/api/admin/stats')
def api_admin_stats():
    """Get portal statistics for dashboard"""
    conn = get_portal_db()
    cursor = conn.cursor()
    
    # Count requests by status
    cursor.execute("SELECT status, COUNT(*) as count FROM requests GROUP BY status")
    request_stats = {row['status']: row['count'] for row in cursor.fetchall()}
    
    # Count deletion requests by status
    cursor.execute("SELECT status, COUNT(*) as count FROM deletion_requests GROUP BY status")
    deletion_stats = {row['status']: row['count'] for row in cursor.fetchall()}
    
    # Count active auth records
    cursor.execute("SELECT COUNT(*) as count FROM student_auth")
    auth_count = cursor.fetchone()['count']
    
    # Count first-time login pending
    cursor.execute("SELECT COUNT(*) as count FROM student_auth WHERE is_first_login = 1")
    first_login_count = cursor.fetchone()['count']
    
    conn.close()
    
    return jsonify({
        'requests': request_stats,
        'deletions': deletion_stats,
        'portal_users': auth_count,
        'pending_password_change': first_login_count
    })

# --- SPA Serving ---
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    
    # If path is an API call that wasn't matched, return 404
    if path.startswith('api/'):
        return jsonify({'error': 'Not Found'}), 404
        
    # Otherwise, for SPA routing, return index.html
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)
