
import requests
import json

BASE_URL = "http://localhost:5000"
SESSION = requests.Session()

def login():
    print("1. Testing Login & Profile Year...")
    # Demo student
    resp = SESSION.post(f"{BASE_URL}/api/login", json={
        "enrollment_no": "2023CS002", # Saanvi Verma (2nd Year)
        "password": "password"
    })
    if resp.status_code == 200:
        data = resp.json()
        print(f"   ✓ Login Successful: {data.get('name')}")
        if data.get('year') == '2nd Year':
            print("   ✓ Profile Year Fix Verified: '2nd Year' returned in login response")
        else:
            print(f"   ❌ Profile Year Fix Failed: Got {data.get('year')}")
    else:
        print(f"   ❌ Login Failed: {resp.text}")

def check_book_details():
    print("\n2. Testing Book Details (Alphanumeric ID)...")
    book_id = "PY001" # String ID
    resp = SESSION.get(f"{BASE_URL}/api/books/{book_id}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"   ✓ Book Details Loaded: {data.get('title')}")
        if data.get('available_copies') is not None:
             print("   ✓ Availability Data Present")
    else:
        print(f"   ❌ Failed to load book {book_id}: {resp.status_code}")

def test_ratings():
    print("\n3. Testing Star Ratings...")
    book_id = "PY001"
    rating = 5
    resp = SESSION.post(f"{BASE_URL}/api/books/{book_id}/rate", json={'rating': rating})
    if resp.status_code == 200:
        data = resp.json()
        print(f"   ✓ Rating Submitted. New Average: {data.get('new_avg')} ({data.get('new_count')} reviews)")
    else:
        print(f"   ❌ Rating Failed: {resp.text}")

def check_dashboard_overdue():
    print("\n4. Testing Overdue Alerts & Fines...")
    # 2023CS002 has an overdue transaction in demo data for book JAVA001
    resp = SESSION.get(f"{BASE_URL}/api/dashboard")
    if resp.status_code == 200:
        data = resp.json()
        overdue = [b for b in data.get('borrows', []) if b.get('status') == 'overdue']
        if overdue:
            print(f"   ✓ Overdue Items Found: {len(overdue)}")
            print(f"   ✓ First Overdue Item Fine: ₹{overdue[0].get('fine', 'N/A')}")
        else:
            print("   ⚠ No overdue items found (Check demo data)")
        
        # Check alerts/notifications
        alerts = [n for n in data.get('notifications', []) if 'OVERDUE' in n.get('msg', '')]
        if alerts:
            print(f"   ✓ Overdue Notification Present: {alerts[0].get('msg')}")
        else:
            print("   ⚠ No overdue notifications found")

if __name__ == "__main__":
    try:
        login()
        check_book_details()
        test_ratings()
        check_dashboard_overdue()
    except Exception as e:
        print(f"Verification Failed: {e}")
        print("Ensure the server is running on localhost:5000")
