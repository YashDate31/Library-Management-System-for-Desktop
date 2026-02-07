#!/usr/bin/env python3
"""Comprehensive test of the HTTP 500 fixes"""

import sys
import os
import time
import threading
import requests
import json

# Add Web-Extension to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'LibraryApp', 'Web-Extension'))

def run_server():
    """Run the Flask server in a thread"""
    from student_portal import app
    app.run(debug=False, port=5001, threaded=True, use_reloader=False)

def test_endpoints_comprehensive():
    """Test the endpoints with various scenarios"""
    time.sleep(2)  # Give server time to start
    
    test_cases = [
        {
            'name': 'Deletion History - No filters',
            'method': 'GET',
            'endpoint': '/api/admin/deletion-history',
            'params': {},
        },
        {
            'name': 'Deletion History - 7 days filter',
            'method': 'GET',
            'endpoint': '/api/admin/deletion-history',
            'params': {'days': '7'},
        },
        {
            'name': 'Deletion History - Search filter',
            'method': 'GET',
            'endpoint': '/api/admin/deletion-history',
            'params': {'q': 'test'},
        },
        {
            'name': 'Request History - No filters',
            'method': 'GET',
            'endpoint': '/api/admin/request-history',
            'params': {},
        },
        {
            'name': 'Request History - 7 days filter',
            'method': 'GET',
            'endpoint': '/api/admin/request-history',
            'params': {'days': '7'},
        },
        {
            'name': 'Request History - Search filter',
            'method': 'GET',
            'endpoint': '/api/admin/request-history',
            'params': {'q': 'profile'},
        },
    ]
    
    base_url = 'http://127.0.0.1:5001'
    passed = 0
    failed = 0
    
    print("\n" + "="*80)
    print("COMPREHENSIVE API TEST REPORT")
    print("="*80)
    
    for test in test_cases:
        try:
            url = base_url + test['endpoint']
            
            if test['method'] == 'GET':
                response = requests.get(url, params=test['params'], timeout=5)
            else:
                response = requests.post(url, json=test['params'], timeout=5)
            
            # Check response
            status_ok = response.status_code == 200
            json_ok = False
            
            try:
                data = response.json()
                json_ok = isinstance(data, dict) and 'counts' in data and 'history' in data
            except:
                pass
            
            if status_ok and json_ok:
                passed += 1
                result = "[PASS]"
            else:
                failed += 1
                result = "[FAIL]"
            
            print(f"\n{result} {test['name']}")
            print(f"  Endpoint: {test['method']} {test['endpoint']}")
            if test['params']:
                print(f"  Params: {test['params']}")
            print(f"  Status: {response.status_code}")
            
            if not (status_ok and json_ok):
                print(f"  Response: {response.text[:200]}...")
            else:
                # Show data counts
                try:
                    data = response.json()
                    print(f"  Data: {json.dumps(data['counts'], indent=2)}")
                except:
                    pass
                
        except Exception as e:
            failed += 1
            print(f"\n[ERROR] {test['name']}")
            print(f"  Exception: {str(e)[:200]}")
    
    print("\n" + "="*80)
    print(f"SUMMARY: {passed} passed, {failed} failed")
    print("="*80)
    
    return failed == 0

if __name__ == '__main__':
    # Start server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Test endpoints
    success = test_endpoints_comprehensive()
    
    sys.exit(0 if success else 1)
