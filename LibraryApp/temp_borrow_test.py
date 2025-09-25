from database import Database
from datetime import datetime, timedelta

db=Database()
students=db.get_students()
books=db.get_books()
if students and books:
    enrollment=students[0][1]
    book_id=books[0][1]
    borrow_date=datetime.now().strftime('%Y-%m-%d')
    due_date=(datetime.now()+timedelta(days=7)).strftime('%Y-%m-%d')
    ok,msg=db.borrow_book(enrollment, book_id, borrow_date, due_date)
    print('Borrow attempt:', ok, msg)
else:
    print('Missing sample data.')
