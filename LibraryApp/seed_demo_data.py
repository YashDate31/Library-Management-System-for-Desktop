import random
from datetime import datetime, timedelta
from database import Database

def seed():
    db = Database()
    conn = db.get_connection()
    cur = conn.cursor()

    # Basic check: if we already have some data, skip unless very sparse
    cur.execute('SELECT COUNT(*) FROM students')
    student_count = cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM books')
    book_count = cur.fetchone()[0]

    # Create diverse students if needed
    if student_count < 10:
        years = ["1st", "2nd", "3rd", "Pass Out"]
        depts = ["Computer", "IT", "Mechanical"]
        for i in range(1, 21):
            en = f"ENR{i:05d}"
            name = f"Student {i}"
            email = f"student{i}@example.com"
            phone = f"9{random.randint(100000000, 999999999)}"
            dept = random.choice(depts)
            year = random.choice(years)
            try:
                db.add_student(en, name, email, phone, dept, year)
            except Exception:
                pass

    # Create books if needed
    if book_count < 10:
        categories = ["CS", "Math", "History", "Science"]
        for i in range(1, 31):
            bid = f"B{i:04d}"
            title = f"Book Title {i}"
            author = f"Author {i}"
            isbn = f"ISBN{i:04d}"
            cat = random.choice(categories)
            copies = random.randint(1, 5)
            try:
                db.add_book(bid, title, author, isbn, cat, copies)
            except Exception:
                pass

    # Create borrow records over last 30 days with exact 7-day period
    cur.execute('SELECT enrollment_no, year FROM students')
    students = cur.fetchall()
    cur.execute('SELECT book_id FROM books')
    books = [r[0] for r in cur.fetchall()]

    # Generate 80 borrow events across different days; skip Pass Out students
    for _ in range(80):
        if not students or not books:
            break
        enr, yr = random.choice(students)
        if (yr or '').strip().lower() in ("pass out", "passout"):
            continue
        bk = random.choice(books)
        start_days_ago = random.randint(0, 29)
        borrow_date = (datetime.now() - timedelta(days=start_days_ago)).strftime('%Y-%m-%d')
        due_date = (datetime.now() - timedelta(days=start_days_ago - 7)).strftime('%Y-%m-%d')
        ok, _ = db.borrow_book(enr, bk, borrow_date, due_date)
        if ok and random.random() < 0.7:  # 70% returned
            # Return on time or a few days late
            return_shift = random.randint(0, 4)
            return_date = (datetime.strptime(due_date, '%Y-%m-%d') + timedelta(days=return_shift)).strftime('%Y-%m-%d')
            try:
                db.return_book(enr, bk, return_date)
            except Exception:
                pass

    conn.close()

if __name__ == '__main__':
    seed()
    print("Demo data seeded.")
