"""
Test script to verify book deletion sync between desktop app and portal
"""
import sqlite3
import requests
import os
import time

def check_database_directly():
    """Check what's actually in the database file"""
    db_path = os.path.join(os.path.dirname(__file__), 'library.db')
    print(f"\n📚 Checking database file: {db_path}")
    print(f"File exists: {os.path.exists(db_path)}")
    print(f"File size: {os.path.getsize(db_path) if os.path.exists(db_path) else 0} bytes")
    print(f"Last modified: {time.ctime(os.path.getmtime(db_path)) if os.path.exists(db_path) else 'N/A'}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check WAL mode
    cursor.execute("PRAGMA journal_mode")
    journal_mode = cursor.fetchone()[0]
    print(f"\nJournal mode: {journal_mode}")
    
    # Get book count
    cursor.execute("SELECT COUNT(*) FROM books")
    count = cursor.fetchone()[0]
    print(f"\n✅ Total books in library.db: {count}")
    
    # Get last 5 books
    cursor.execute("SELECT book_id, title, author FROM books ORDER BY book_id DESC LIMIT 5")
    books = cursor.fetchall()
    print("\n📖 Last 5 books in database:")
    for book_id, title, author in books:
        print(f"   ID: {book_id} - {title} by {author}")
    
    conn.close()
    return count

def check_portal_api():
    """Check what the portal API returns"""
    print("\n🌐 Checking Portal API at http://localhost:5001/api/books")
    
    try:
        # Add cache-busting parameter
        response = requests.get(
            'http://localhost:5001/api/books',
            params={'_t': int(time.time())},  # Cache buster
            headers={'Cache-Control': 'no-cache'}
        )
        
        if response.status_code == 200:
            data = response.json()
            books = data.get('books', [])
            print(f"\n✅ Books returned by API: {len(books)}")
            
            print("\n📖 Last 5 books from API:")
            for book in books[-5:]:
                print(f"   ID: {book['book_id']} - {book['title']} by {book['author']}")
            
            return len(books)
        else:
            print(f"❌ API error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("❌ Portal is not running! Start it from the desktop app.")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def check_portal_database_config():
    """Check which database the portal is configured to use"""
    print("\n⚙️  Checking portal configuration...")
    
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            env_content = f.read()
            if 'PORTAL_FORCE_LOCAL=true' in env_content:
                print("✅ PORTAL_FORCE_LOCAL=true is set")
            else:
                print("⚠️  PORTAL_FORCE_LOCAL is NOT set to true")
            
            if 'DATABASE_URL=' in env_content:
                print("⚠️  DATABASE_URL is set (cloud database configured)")
    else:
        print("❌ .env file not found")

if __name__ == '__main__':
    print("=" * 60)
    print("BOOK DELETION SYNC TEST")
    print("=" * 60)
    
    # Check configuration
    check_portal_database_config()
    
    # Check database
    db_count = check_database_directly()
    
    # Check API
    api_count = check_portal_api()
    
    # Compare results
    print("\n" + "=" * 60)
    print("COMPARISON:")
    print("=" * 60)
    
    if api_count is not None:
        if db_count == api_count:
            print(f"✅ SYNC OK: Database ({db_count}) matches API ({api_count})")
        else:
            print(f"❌ SYNC ISSUE: Database has {db_count} books, but API returns {api_count}")
            print("\nPossible causes:")
            print("1. Browser caching - Try Ctrl+Shift+R to hard reload")
            print("2. Frontend caching - Clear browser cache")
            print("3. API caching - Already using cache-busting")
            print("4. Portal reading from different database file")
            
            print("\n🔧 RECOMMENDED FIX:")
            print("1. Close the portal")
            print("2. Restart the desktop application")
            print("3. Open portal in incognito/private window")
            print("4. Try deleting a book and refresh immediately")
    
    print("\n" + "=" * 60)
    print("\nTest complete!")
    print("=" * 60)
