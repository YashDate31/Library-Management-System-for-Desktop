"""Full Reset Script - Clears ALL data from local SQLite + Supabase PostgreSQL"""
import os, sys, sqlite3, json
sys.path.insert(0, 'LibraryApp')

from dotenv import load_dotenv
load_dotenv('.env')

# ── LOCAL LIBRARY.DB ──────────────────────────────────────────────────────────
print("\n=== CLEARING LOCAL LIBRARY.DB ===")
lib_path = 'LibraryApp/library.db'
conn = sqlite3.connect(lib_path)
c = conn.cursor()
c.execute("PRAGMA foreign_keys = OFF")

lib_tables = [
    'admin_activity', 'promotion_history', 'borrow_records',
    'transactions', 'academic_years', 'books', 'students'
]
for t in lib_tables:
    try:
        c.execute(f"DELETE FROM {t}")
        print(f"  ✓ Cleared {t} ({conn.total_changes} rows affected)")
        conn.commit()
    except Exception as e:
        print(f"  ✗ {t}: {e}")

c.execute("PRAGMA foreign_keys = ON")
conn.commit()
conn.close()
print("Local library.db cleared.")

# ── LOCAL PORTAL.DB ───────────────────────────────────────────────────────────
print("\n=== CLEARING LOCAL PORTAL.DB ===")
portal_path = 'LibraryApp/Web-Extension/portal.db'
if os.path.exists(portal_path):
    conn2 = sqlite3.connect(portal_path)
    c2 = conn2.cursor()
    portal_tables = [
        'access_logs', 'book_ratings', 'book_waitlist', 'user_notifications',
        'user_settings', 'deletion_requests', 'notices', 'student_auth',
        'requests', 'study_materials'
    ]
    for t in portal_tables:
        try:
            c2.execute(f"DELETE FROM {t}")
            conn2.commit()
            print(f"  ✓ Cleared portal.{t}")
        except:
            pass
    conn2.close()
    print("Local portal.db cleared.")

# ── EMAIL & SYNC LOGS ─────────────────────────────────────────────────────────
print("\n=== CLEARING LOG FILES ===")
for path, default in [
    ('LibraryApp/email_history.json', '[]'),
    ('LibraryApp/sync_log.json', '{"last_sync": null, "status": "ready"}'),
]:
    try:
        with open(path, 'w') as f:
            f.write(default)
        print(f"  ✓ Reset {path}")
    except Exception as e:
        print(f"  ✗ {path}: {e}")

# ── SUPABASE PostgreSQL ───────────────────────────────────────────────────────
print("\n=== CLEARING SUPABASE (PostgreSQL) ===")
try:
    import psycopg2
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("  ✗ DATABASE_URL not found in environment. Skipping Supabase.")
    else:
        conn3 = psycopg2.connect(db_url)
        conn3.autocommit = False
        c3 = conn3.cursor()

        # Get all tables
        c3.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name")
        all_tables = [r[0] for r in c3.fetchall()]
        print(f"  Found {len(all_tables)} tables: {', '.join(all_tables)}")

        # Delete in safe order (child tables first to avoid FK violations)
        ordered = [
            'access_logs', 'book_ratings', 'book_waitlist',
            'user_notifications', 'user_settings', 'deletion_requests',
            'notices', 'student_auth', 'requests', 'study_materials',
            'borrow_records', 'transactions', 'books', 'students',
            'promotion_history', 'academic_years', 'admin_activity',
        ]
        # Add any tables not in the ordered list
        for t in all_tables:
            if t not in ordered:
                ordered.insert(0, t)

        for t in ordered:
            if t not in all_tables:
                continue
            try:
                c3.execute(f"DELETE FROM {t}")
                count = c3.rowcount
                conn3.commit()
                print(f"  ✓ Cleared supabase.{t} ({count} rows)")
            except Exception as e:
                conn3.rollback()
                # Try with TRUNCATE CASCADE as fallback
                try:
                    c3.execute(f"TRUNCATE TABLE {t} CASCADE")
                    conn3.commit()
                    print(f"  ✓ Truncated supabase.{t} (cascade)")
                except Exception as e2:
                    conn3.rollback()
                    print(f"  ✗ {t}: {e2}")

        conn3.close()
        print("Supabase cleared.")

except ImportError:
    print("  ✗ psycopg2 not installed. Skipping Supabase.")
except Exception as e:
    print(f"  ✗ Supabase error: {e}")

print("\n" + "="*60)
print("✅ FULL RESET COMPLETE - Library is brand new!")
print("="*60)
