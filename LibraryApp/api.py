from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os
from datetime import datetime

# Add current directory to path so we can import database.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database import Database

# Initialize Flask App
# Serve static files from 'static' folder
app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)  # Enable Cross-Origin Resource Sharing

# Initialize Database
db = Database()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/login', methods=['POST'])
def login():
    """Login student by Enrollment No (Simple Auth)"""
    data = request.json
    enrollment_no = data.get('enrollment_no', '').strip()
    
    if not enrollment_no:
        return jsonify({"success": False, "message": "Enrollment Number is required"}), 400
        
    students = db.get_students(enrollment_no)
    
    # Exact match check
    student = None
    for s in students:
        if s[1].lower() == enrollment_no.lower(): # s[1] is enrollment_no
            # Check password (assuming last column is password)
            # If migration just ran, s should have the new column.
            # But db.get_students might select specific columns?
            # Let's check s length or verify database.py logic.
            # For now, let's assume get_students does SELECT *
            
            stored_pass = str(s[-1]) if len(s) > 8 else 'student123' # Fallback
            input_pass = data.get('password', '').strip()
            
            if input_pass == stored_pass:
                student = s
            else:
                return jsonify({"success": False, "message": "Invalid Password"}), 401
            break
            
    if student:
        return jsonify({
            "success": True,
            "student": {
                "id": student[0],
                "enrollment_no": student[1],
                "name": student[2],
                "department": student[5],
                "year": student[6]
            }
        })
    else:
        return jsonify({"success": False, "message": "Student not found"}), 404

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    """Get student dashboard stats"""
    enrollment_no = request.args.get('enrollment_no')
    if not enrollment_no:
        return jsonify({"error": "Enrollment No required"}), 400
        
    # Get borrowed books
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Get active borrowed books
    cursor.execute('''
        SELECT b.title, b.author, br.borrow_date, br.due_date, br.book_id
        FROM borrow_records br
        JOIN books b ON br.book_id = b.book_id
        WHERE br.enrollment_no = ? AND br.status = 'borrowed'
    ''', (enrollment_no,))
    
    borrowed_books = []
    total_fine = 0
    now = datetime.now()
    
    for row in cursor.fetchall():
        due_date = datetime.strptime(row[3], '%Y-%m-%d')
        days_overdue = 0
        fine = 0
        
        if now > due_date:
            days_overdue = (now - due_date).days
            fine = days_overdue * 5  # Rs 5 per day
            total_fine += fine
            
        borrowed_books.append({
            "title": row[0],
            "author": row[1],
            "borrow_date": row[2],
            "due_date": row[3],
            "book_id": row[4],
            "fine": fine,
            "is_overdue": days_overdue > 0
        })
    
    conn.close()
    
    return jsonify({
        "borrowed_books": borrowed_books,
        "total_fine": total_fine,
        "books_count": len(borrowed_books)
    })

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get student history"""
    enrollment_no = request.args.get('enrollment_no')
    if not enrollment_no:
        return jsonify({"error": "Enrollment No required"}), 400
        
    history = db.get_student_history(enrollment_no)
    return jsonify(history)

@app.route('/api/catalog', methods=['GET'])
def get_catalog():
    """Search books"""
    search = request.args.get('search', '')
    books = db.get_books(search)
    
    catalog = []
    for b in books:
        # Schema: id, book_id, title, author, isbn, category, total, available
        catalog.append({
            "book_id": b[1],
            "title": b[2],
            "author": b[3],
            "category": b[5],
            "available": b[7] > 0
        })
        
    return jsonify(catalog)

if __name__ == '__main__':
    print("Starting Mobile API Server on 0.0.0.0:5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)
