#!/usr/bin/env python3
"""Quick validation test"""

import sys
import os
import time
import threading
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'LibraryApp', 'Web-Extension'))

def run_server():
    from student_portal import app
    app.run(debug=False, port=5002, threaded=True, use_reloader=False)

if __name__ == '__main__':
    print("Starting validation server on port 5002...")
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    time.sleep(3)
    
    endpoints_to_test = [
        '/api/admin/request-history',
        '/api/admin/deletion-history',
        '/api/admin/observability'
    ]
    
    print("\nTesting endpoints:")
    all_ok = True
    for endpoint in endpoints_to_test:
        try:
            response = requests.get(f'http://127.0.0.1:5002{endpoint}', timeout=5)
            status = "OK" if response.status_code == 200 else f"FAIL ({response.status_code})"
            print(f"  {endpoint}: {status}")
            if response.status_code != 200:
                all_ok = False
        except Exception as e:
            print(f"  {endpoint}: ERROR - {str(e)[:50]}")
            all_ok = False
    
    if all_ok:
        print("\nAll endpoints responding correctly! ✓")
        sys.exit(0)
    else:
        print("\nSome endpoints failed!")
        sys.exit(1)
