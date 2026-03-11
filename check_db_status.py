import sqlite3

conn = sqlite3.connect('LibraryApp/library.db')
cursor = conn.cursor()

cursor.execute('SELECT COUNT(*) FROM students')
students = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM books')
books = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM borrow_records')
borrows = cursor.fetchone()[0]

print(f'Database Status:')
print(f'  Students: {students}')
print(f'  Books: {books}')
print(f'  Borrow Records: {borrows}')
print()

if students > 0:
    print('Sample students:')
    cursor.execute('SELECT enrollment_no, name, email FROM students LIMIT 3')
    for r in cursor.fetchall():
        print(f'  - Enroll: {r[0]}, Name: {r[1]}, Email: {r[2]}')
    print()

if borrows > 0:
    print('Sample borrow records:')
    cursor.execute('''
        SELECT br.enrollment_no, s.name, s.email, br.book_id, br.issue_date, br.due_date 
        FROM borrow_records br 
        LEFT JOIN students s ON br.enrollment_no = s.enrollment_no 
        LIMIT 3
    ''')
    for r in cursor.fetchall():
        print(f'  - Enroll: {r[0]}, Name: {r[1]}, Email: {r[2]}, Book: {r[3]}')

conn.close()
