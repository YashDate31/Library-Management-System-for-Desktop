#!/usr/bin/env python3
"""Direct test of the endpoint logic with print statements"""

import sys
import os

# Add Web-Extension to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'LibraryApp', 'Web-Extension'))

from student_portal import get_portal_db, get_library_db
import json

def test_deletion_history():
    """Test deletion history query"""
    
    print("\n" + "="*80)
    print("Testing deletion_history query with days=7")
    print("="*80)
    
    try:
        conn = get_portal_db()
        cursor = conn.cursor()
        cursor.row_factory = lambda x: dict(zip([col[0] for col in cursor.description], x))
        
        # Check if using PostgreSQL
        is_postgres = bool(os.getenv('DATABASE_URL'))
        print(f"is_postgres: {is_postgres}")
        
        # Get filter params
        q = ''
        days = '7'
        
        # Base query
        query = """
            SELECT id, student_id, reason, status, timestamp
            FROM deletion_requests
            WHERE status IN ('approved', 'rejected')
        """
        params = []
        
        print(f"\nBase query: {query}")
        
        # Date filter (compatible with both PostgreSQL and SQLite)
        if days and days.isdigit():
            days_int = int(days)
            print(f"days_int = {days_int}")
            if is_postgres:
                date_clause = f" AND timestamp >= CURRENT_TIMESTAMP - INTERVAL '{days_int} days'"
            else:
                date_clause = f" AND timestamp >= date('now', '-{days_int} days')"
            
            print(f"date_clause: {date_clause}")
            query += date_clause
        
        query += " ORDER BY timestamp DESC LIMIT 100"
        
        print(f"\nFinal query:\n{query}")
        print(f"\nParams: {params}")
        
        # Execute
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        print(f"\nQuery executed successfully!")
        print(f"Rows returned: {len(results)}")
        
        conn.close()
        
    except Exception as e:
        import traceback
        print(f"\nError: {e}")
        traceback.print_exc()

if __name__ == '__main__':
    test_deletion_history()
