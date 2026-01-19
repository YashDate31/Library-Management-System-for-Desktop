import sys
import os

# Add the Web-Extension directory to the python path so we can import student_portal
sys.path.append(os.path.join(os.path.dirname(__file__), 'LibraryApp', 'Web-Extension'))

from student_portal import app

if __name__ == "__main__":
    app.run()
