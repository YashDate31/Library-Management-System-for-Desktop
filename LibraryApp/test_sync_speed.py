#!/usr/bin/env python3
"""
Test script to measure sync speed
"""
import time
from database import Database
from sync_manager import create_sync_manager

print("=" * 60)
print("📊 SYNC SPEED TEST")
print("=" * 60)

# Initialize database
db = Database()
print(f"\n✅ Local database: {db.db_path}")

# Create sync manager
sync_mgr = create_sync_manager(db)

if not sync_mgr:
    print("\n❌ Sync manager not available (DATABASE_URL not set)")
    print("   This is normal if you're testing offline")
    exit(0)

print("✅ Sync manager initialized")

# Count local records
conn = db.get_connection()
cursor = conn.cursor()

print("\n📦 Local Database Records:")
cursor.execute("SELECT COUNT(*) FROM students")
students_count = cursor.fetchone()[0]
print(f"   Students: {students_count}")


cursor.execute("SELECT COUNT(*) FROM books")
books_count = cursor.fetchone()[0]
print(f"   Books: {books_count}")

cursor.execute("SELECT COUNT(*) FROM borrow_records")
borrow_count = cursor.fetchone()[0]
print(f"   Borrow Records: {borrow_count}")

cursor.execute("SELECT COUNT(*) FROM admin_activity")
activity_count = cursor.fetchone()[0]
print(f"   Admin Activities: {activity_count}")

total_records = students_count + books_count + borrow_count + activity_count
print(f"\n   📊 Total Records: {total_records}")

conn.close()

# Test sync speed
print("\n" + "=" * 60)
print("🔄 Starting Sync Test (Local → Remote)...")
print("=" * 60)

start_time = time.time()

try:
    result = sync_mgr.sync_now(direction='local_to_remote')
    
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n✅ SYNC COMPLETED!")
    print(f"\n⏱️  Time taken: {duration:.2f} seconds")
    print(f"📤 Records synced: {result.get('records_synced', 0)}")
    print(f"📋 Tables synced: {', '.join(result.get('tables_synced', []))}")
    
    if result.get('errors'):
        print(f"\n⚠️  Errors encountered:")
        for error in result['errors']:
            print(f"   - {error}")
    
    # Calculate speed
    if duration > 0 and total_records > 0:
        records_per_sec = total_records / duration
        print(f"\n🚀 Sync Speed: {records_per_sec:.1f} records/second")
    
    # Estimate for different data sizes
    print("\n" + "=" * 60)
    print("📈 SYNC TIME ESTIMATES:")
    print("=" * 60)
    
    if duration > 0:
        # Estimate for different record counts
        estimates = [100, 500, 1000, 5000, 10000]
        for estimate in estimates:
            estimated_time = (estimate / total_records) * duration if total_records > 0 else duration
            print(f"   {estimate:>6} records: ~{estimated_time:.1f} seconds ({estimated_time/60:.1f} minutes)")
    
    print("\n💡 TIP: Sync happens automatically every 30 minutes in background")
    print("   You can also trigger manual sync from Admin tab → 'Sync Now' button")
    
except Exception as e:
    print(f"\n❌ Sync failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
