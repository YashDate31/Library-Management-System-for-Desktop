import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORTAL_DB = ROOT / 'Web-Extension' / 'portal.db'
LIB_DB = ROOT / 'library.db'


def main() -> None:
    p = sqlite3.connect(str(PORTAL_DB))
    p.row_factory = sqlite3.Row
    lp = sqlite3.connect(str(LIB_DB))
    lp.row_factory = sqlite3.Row

    cp = p.cursor()
    cl = lp.cursor()

    cp.execute("SELECT id, enrollment_no, request_type, created_at FROM requests WHERE status='pending' ORDER BY created_at DESC LIMIT 50")
    rows = cp.fetchall()

    missing = []
    print('Pending requests (id, enrollment_no, request_type) -> student lookup:')
    for r in rows:
        enr = str(r['enrollment_no']).strip()
        cl.execute('SELECT name FROM students WHERE enrollment_no = ?', (enr,))
        s = cl.fetchone()
        name = s['name'] if s else None
        print(f"{r['id']:>4} {enr:<15} {r['request_type']:<25} => {name or 'MISSING'}")
        if not name:
            missing.append(enr)

    print('\nUnique missing enrollment_no:', len(set(missing)))
    if missing:
        print('Missing samples:', sorted(set(missing))[:20])


if __name__ == '__main__':
    main()
