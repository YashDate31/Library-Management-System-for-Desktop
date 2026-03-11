import sqlite3
from datetime import datetime

# Simulate what the code is doing
conn = sqlite3.connect('LibraryApp/library.db')
cursor = conn.cursor()

cursor.execute("""
    SELECT 
        br.enrollment_no,
        s.name as student_name,
        br.book_id,
        b.title as book_title,
        br.borrow_date,
        br.due_date,
        br.return_date,
        br.status,
        0 as days_overdue,
        COALESCE(br.academic_year, 'N/A') as academic_year
    FROM borrow_records br
    JOIN students s ON br.enrollment_no = s.enrollment_no
    JOIN books b ON br.book_id = b.book_id
    ORDER BY br.id DESC
""")

records = cursor.fetchall()

print(f"Found {len(records)} records")
print()

for rec in records:
    enroll, student_name, book_id, title, borrow_date, due_date, return_date_raw, status, _, academic_year = rec
    
    print(f"Enrollment: {enroll}")
    print(f"Student: {student_name}")
    print(f"Book ID: {book_id}")
    print(f"Borrow Date: {borrow_date}")
    print(f"Due Date: {due_date}")
    print(f"Status: {status}")
    print(f"Return Date Raw: {return_date_raw} (type: {type(return_date_raw)})")
    
    # Test the date parsing and comparison
    today = datetime.now().date()
    print(f"Today: {today}")
    
    try:
        due_d = datetime.strptime(str(due_date), '%Y-%m-%d').date()
        print(f"Due Date Parsed: {due_d}")
        print(f"Today > Due Date? {today > due_d}")
        
        if status == 'borrowed' and today > due_d:
            overdue_days = (today - due_d).days
            fine_per_day = 5  # Default
            fine = overdue_days * fine_per_day
            print(f"Overdue Days: {overdue_days}")
            print(f"Fine: Rs {fine}")
        else:
            print("Not overdue according to logic")
    except Exception as e:
        print(f"Error: {e}")
    
    print("-" * 60)

conn.close()
