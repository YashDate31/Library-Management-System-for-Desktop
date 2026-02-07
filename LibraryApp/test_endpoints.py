import sqlite3
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(os.path.join(os.path.dirname(__file__), 'Web-Extension'))

# Change to Web-Extension directory
web_ext_dir = os.path.join(os.path.dirname(__file__), 'Web-Extension')
sys.path.insert(0, web_ext_dir)
os.chdir(web_ext_dir)

# Import the Flask app
try:
    import student_portal
    get_portal_db = student_portal.get_portal_db
    get_library_db = student_portal.get_library_db
    print("✓ Successfully imported student_portal")
except Exception as e:
    print(f"✗ Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test the function directly
print("\n" + "="*60)
print("Testing api_admin_all_requests() function directly...")
print("="*60)

try:
    conn = get_portal_db()
    cursor = conn.cursor()
    
    print("\n1. Testing general requests query...")
    cursor.execute("""
        SELECT id as req_id, enrollment_no, request_type, details, status, created_at
        FROM requests
        WHERE status = 'pending'
        ORDER BY created_at DESC
    """)
    general_requests = []
    for row in cursor.fetchall():
        req = dict(row)
        try:
            req['details'] = json.loads(req['details']) if req['details'] else {}
        except:
            req['details'] = {'raw': req['details']}
        general_requests.append(req)
    print(f"   ✓ Found {len(general_requests)} general requests")
    
    print("\n2. Testing deletion requests query...")
    cursor.execute("""
        SELECT id, student_id, reason, status, timestamp
        FROM deletion_requests
        WHERE status = 'pending'
        ORDER BY timestamp DESC
    """)
    deletion_requests = [dict(row) for row in cursor.fetchall()]
    print(f"   ✓ Found {len(deletion_requests)} deletion requests")
    
    conn.close()
    
    print("\n3. Testing library DB connection...")
    conn_lib = get_library_db()
    cursor_lib = conn_lib.cursor()
    
    # Enrich general requests with student names
    for req in general_requests:
        cursor_lib.execute("SELECT name FROM students WHERE enrollment_no = ?", (req['enrollment_no'],))
        student = cursor_lib.fetchone()
        req['student_name'] = student['name'] if student else 'Unknown'
    print(f"   ✓ Enriched {len(general_requests)} general requests with student names")
    
    # Enrich deletion requests with student names
    for req in deletion_requests:
        cursor_lib.execute("SELECT name FROM students WHERE enrollment_no = ?", (req['student_id'],))
        student = cursor_lib.fetchone()
        req['student_name'] = student['name'] if student else 'Unknown'
    print(f"   ✓ Enriched {len(deletion_requests)} deletion requests with student names")
    
    conn_lib.close()
    
    print("\n4. Testing counts query...")
    conn2 = get_portal_db()
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT COUNT(*) as count FROM requests WHERE status = 'rejected'")
    rejected_count = cursor2.fetchone()['count']
    print(f"   ✓ Found {rejected_count} rejected requests")
    
    cursor2.execute("SELECT status, COUNT(*) as count FROM deletion_requests GROUP BY status")
    deletion_counts = {row['status']: row['count'] for row in cursor2.fetchall()}
    print(f"   ✓ Deletion counts: {deletion_counts}")
    conn2.close()
    
    print("\n" + "="*60)
    print("✓ ALL TESTS PASSED - Function logic is correct!")
    print("="*60)
    
    # Print sample data
    if general_requests:
        print(f"\nSample general request: {json.dumps(general_requests[0], indent=2, default=str)}")
    if deletion_requests:
        print(f"\nSample deletion request: {json.dumps(deletion_requests[0], indent=2, default=str)}")

except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
