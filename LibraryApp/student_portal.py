from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
import sys
from datetime import datetime

# Helper to locate database in both dev and PyInstaller modes
def get_db_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(os.path.dirname(sys.executable), 'library.db')
    return os.path.join(os.path.dirname(__file__), 'library.db')

app = Flask(__name__)
app.secret_key = 'super_secret_key_change_this_for_prod'  # Simple key for local session

@app.route('/')
def index():
    if 'student_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    enrollment_no = request.form.get('enrollment_no')
    
    if not enrollment_no:
        flash('Please enter Enrollment Number', 'error')
        return redirect(url_for('index'))
    
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE enrollment_no = ?", (enrollment_no,))
        student = cursor.fetchone()
        conn.close()
        
        if student:
            # Map student tuple to dictionary for session
            # student structure: id, enrollment_no, name, email, phone, department, year, date_registered
            session['student_id'] = student[1]  # enrollment_no
            session['student_name'] = student[2]
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Enrollment Number', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        flash(f'System Error: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'student_id' not in session:
        return redirect(url_for('index'))
    
    enrollment_no = session['student_id']
    
    try:
        conn = sqlite3.connect(get_db_path())
        conn.row_factory = sqlite3.Row  # Access columns by name
        cursor = conn.cursor()
        
        # Get Student Details
        cursor.execute("SELECT * FROM students WHERE enrollment_no = ?", (enrollment_no,))
        student = cursor.fetchone()
        
        # Get Current Borrows
        cursor.execute("""
            SELECT b.title, b.author, br.borrow_date, br.due_date, br.book_id
            FROM borrow_records br
            JOIN books b ON br.book_id = b.book_id
            WHERE br.enrollment_no = ? AND br.status = 'borrowed'
            ORDER BY br.due_date ASC
        """, (enrollment_no,))
        current_borrows = cursor.fetchall()
        
        # Get History (Returned Books)
        cursor.execute("""
            SELECT b.title, b.author, br.borrow_date, br.return_date
            FROM borrow_records br
            JOIN books b ON br.book_id = b.book_id
            WHERE br.enrollment_no = ? AND br.status = 'returned'
            ORDER BY br.return_date DESC
            LIMIT 50
        """, (enrollment_no,))
        history = cursor.fetchall()
        
        conn.close()
        
        return render_template('dashboard.html', student=student, current_borrows=current_borrows, history=history)
        
    except Exception as e:
        return f"Database Error: {e}"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # This block is for independent testing of the portal
    app.run(host='0.0.0.0', port=5000, debug=True)
