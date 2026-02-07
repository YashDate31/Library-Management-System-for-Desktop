#!/usr/bin/env python3
"""Test the portal endpoints with extensive logging"""

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
    # Monkey patch to add logging
    import student_portal
    original_request_history = student_portal.api_admin_request_history
    
    def logged_request_history():
        print(f"\n[DEBUG] api_admin_request_history called")
        from flask import request as flask_request
        print(f"[DEBUG] Query params: {dict(flask_request.args)}")
        return original_request_history()
    
    student_portal.api_admin_request_history = logged_request_history
    
    from student_portal import app
    app.run(debug=False, port=5001, threaded=True, use_reloader=False)

if __name__ == '__main__':
    # Start server
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(3)
    
    # Test with days parameter
    print("\n" + "="*80)
    print("Testing request-history with days=7")
    print("="*80)
    
    response = requests.get('http://127.0.0.1:5001/api/admin/request-history', params={'days': '7'})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json() if response.status_code == 200 else response.text[:500]}")
