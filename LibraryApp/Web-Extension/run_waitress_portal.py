"""Run the Student Portal Flask app under Waitress.

This is a small helper for local debugging without the Flask auto-reloader.
"""

import os

# Ensure we run relative to this folder so portal.db resolves correctly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# Desktop/local default: do NOT use cloud DATABASE_URL unless explicitly enabled.
os.environ.setdefault('PORTAL_FORCE_LOCAL', '1')

from waitress import serve  # type: ignore
from student_portal import app

if __name__ == '__main__':
    print('Waitress starting Student Portal on http://127.0.0.1:5000')
    serve(app, host='127.0.0.1', port=5000, threads=25)
