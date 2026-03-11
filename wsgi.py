import sys
import os

# Add both LibraryApp and Web-Extension directories to sys.path
# LibraryApp is needed for database.py (PostgresConnectionWrapper)
# Web-Extension is needed for student_portal.py
_base = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_base, 'LibraryApp'))
sys.path.insert(0, os.path.join(_base, 'LibraryApp', 'Web-Extension'))

from student_portal import app

if __name__ == "__main__":
    app.run()
