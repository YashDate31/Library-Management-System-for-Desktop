from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
import sqlite3
import os
from datetime import datetime, timedelta

# Determine the absolute path to the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the path to the React build folder (frontend/dist)
DIST_FOLDER = os.path.join(BASE_DIR, 'frontend', 'dist')

app = Flask(__name__, static_folder='frontend/dist', static_url_path='/')
app.secret_key = 'your_secret_key'

def get_db_path():
    # Database is in the parent directory of Web-Extension
    return os.path.join(os.path.dirname(BASE_DIR), 'library.db')

def get_portal_db_path():
    return os.path.join(BASE_DIR, 'portal.db')

# --- API Endpoints ---

@app.route('/api/me')
def check_session():
    if 'student_id' in session:
        try:
            conn = sqlite3.connect(get_db_path())
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE enrollment_no = ?", (session['student_id'],))
            student = cursor.fetchone()
            conn.close()
            
            if student:
                user_data = {
                    'name': student[1],
                    'enrollment_no': student[2],
                    'department': student[3],
                    'year': student[4]
                }
                return jsonify({'user': user_data})
        except:
            pass
    return jsonify({'user': None})

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    enrollment_no = data.get('enrollment_no')
    
    if not enrollment_no:
        return jsonify({'status': 'error', 'message': 'Enrollment Number required'}), 400
    
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE enrollment_no = ?", (enrollment_no,))
        student = cursor.fetchone()
        conn.close()
        
        if student:
            session['student_id'] = student[1] 
            session['student_name'] = student[2]
            
            user_data = {
                'name': student[2],
                'enrollment_no': student[1],
                'department': student[3],
                'year': student[4]
            }
            return jsonify({'status': 'success', 'user': user_data})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid Enrollment Number'}), 401
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'status': 'success'})

@app.route('/api/dashboard')
def api_dashboard():
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    enrollment_no = session['student_id']
    
    try:
        conn = sqlite3.connect(get_db_path())
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Current Borrows
        cursor.execute("""
            SELECT b.title, b.author, br.borrow_date, br.due_date, br.book_id
            FROM borrow_records br
            JOIN books b ON br.book_id = b.book_id
            WHERE br.enrollment_no = ? AND br.status = 'borrowed'
            ORDER BY br.due_date ASC
        """, (enrollment_no,))
        
        rows = cursor.fetchall()
        current_borrows = []
        today_date = datetime.now()
        
        for row in rows:
            borrow = dict(row)
            if borrow['due_date']:
                try:
                    due_dt = datetime.strptime(borrow['due_date'], '%Y-%m-%d')
                    days_left = (due_dt - today_date).days
                    if days_left < 0:
                        borrow['status'] = 'overdue'
                        borrow['days_left'] = abs(days_left)
                    elif days_left <= 2:
                        borrow['status'] = 'due_soon'
                        borrow['days_left'] = days_left
                    else:
                        borrow['status'] = 'safe'
                        borrow['days_left'] = days_left
                except:
                    borrow['status'] = 'unknown'
                    borrow['days_left'] = 0
            current_borrows.append(borrow)
        
        # History
        cursor.execute("""
            SELECT b.title, b.author, br.borrow_date, br.return_date
            FROM borrow_records br
            JOIN books b ON br.book_id = b.book_id
            WHERE br.enrollment_no = ? AND br.status = 'returned'
            ORDER BY br.return_date DESC
            LIMIT 50
        """, (enrollment_no,))
        history = [dict(row) for row in cursor.fetchall()]

        # Notices
        notices = [
            {"title": "Library Closed", "date": "2025-12-25", "msg": "Library will be closed for Christmas."},
            {"title": "New Python Books", "date": "2025-12-08", "msg": "New editions of 'Python Crash Course' arrived."}
        ]
        
        conn.close()
        
        return jsonify({
            'borrows': current_borrows,
            'history': history,
            'notices': notices
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/books')
def api_books():
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    try:
        conn = sqlite3.connect(get_db_path())
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        sql = "SELECT * FROM books WHERE 1=1"
        params = []
        
        if query:
            sql += " AND (title LIKE ? OR author LIKE ?)"
            params.extend([f'%{query}%', f'%{query}%'])
        
        if category and category != 'All':
            sql += " AND category = ?"
            params.append(category)
            
        sql += " ORDER BY title LIMIT 50"
        
        cursor.execute(sql, params)
        books_list = [dict(row) for row in cursor.fetchall()]
        
        cursor.execute("SELECT DISTINCT category FROM books WHERE category IS NOT NULL ORDER BY category")
        categories = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        
        return jsonify({'books': books_list, 'categories': categories})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- Catch-All for SPA ---
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
