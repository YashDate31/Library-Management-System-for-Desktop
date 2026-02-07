#!/usr/bin/env python3
"""Debug the query generation"""

import sys
import os

# Add Web-Extension to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'LibraryApp', 'Web-Extension'))

from student_portal import get_portal_db
import json

# Test the endpoint code directly
def test_request_history_query():
    """Simulate the endpoint query logic"""
    
    is_postgres = False  # Using SQLite
    days = '7'
    
    # Base query
    query = """
        SELECT id as req_id, enrollment_no, request_type, details, status, created_at
        FROM requests
        WHERE status IN ('approved', 'rejected')
    """
    params = []
    
    # Date filter (compatible with both PostgreSQL and SQLite)
    if days and days.isdigit():
        days_int = int(days)
        if is_postgres:
            query += f" AND created_at >= CURRENT_TIMESTAMP - INTERVAL '{days_int} days'"
        else:
            query += f" AND created_at >= date('now', '-{days_int} days')"
    
    query += " ORDER BY created_at DESC LIMIT 100"
    
    print("Generated query:")
    print(repr(query))
    print("\nFormatted query:")
    print(query)
    
    # Try to execute
    conn = get_portal_db()
    cursor = conn.cursor()
    cursor.row_factory = lambda x: dict(zip([col[0] for col in cursor.description], x))
    
    try:
        cursor.execute(query, params)
        results = cursor.fetchall()
        print(f"\nQuery executed successfully!")
        print(f"Rows returned: {len(results)}")
        if results:
            print(f"First row: {results[0]}")
    except Exception as e:
        print(f"\nQuery failed with error:")
        print(f"  {e}")
        print(f"  Type: {type(e).__name__}")
    finally:
        conn.close()

if __name__ == '__main__':
    test_request_history_query()
