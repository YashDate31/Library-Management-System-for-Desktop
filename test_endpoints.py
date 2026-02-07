#!/usr/bin/env python3
"""Test script to verify the API endpoints are working"""

import sys
import os
import time
import threading
import requests

# Add Web-Extension to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'LibraryApp', 'Web-Extension'))

def run_server():
    """Run the Flask server in a thread"""
    from student_portal import app
    app.run(debug=False, port=5001, threaded=True, use_reloader=False)

def test_endpoints():
    """Test the endpoints"""
    time.sleep(2)  # Give server time to start
    
    endpoints = [
        ('GET', '/api/admin/deletion-history', None),
        ('GET', '/api/admin/request-history', None),
    ]
    
    base_url = 'http://127.0.0.1:5001'
    
    for method, endpoint, data in endpoints:
        try:
            url = base_url + endpoint
            print(f"\n{'='*60}")
            print(f"Testing: {method} {endpoint}")
            print('='*60)
            
            if method == 'GET':
                response = requests.get(url, timeout=5)
            else:
                response = requests.post(url, json=data, timeout=5)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Length: {len(response.text)} bytes")
            
            if response.status_code == 200:
                print("[SUCCESS]")
                try:
                    data = response.json()
                    print(f"Response keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")
                except:
                    print(f"Response (first 200 chars): {response.text[:200]}")
            else:
                print("[FAILED]")
                print(f"Response: {response.text[:500]}")
                
        except Exception as e:
            print(f"[ERROR]: {e}")

if __name__ == '__main__':
    # Start server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Test endpoints
    test_endpoints()
