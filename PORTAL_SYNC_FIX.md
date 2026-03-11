# Portal Database Sync Fix - Complete Guide

## Problem
Books added from the librarian side (main desktop app) are not showing up on the Student Portal website.

## Root Cause
The Student Portal reads from `library.db`, but due to SQLite caching and database locking, changes may not be immediately visible without:
1. Restarting the portal server
2. Refreshing the database connection
3. Using WAL mode for better concurrency

## Solution Applied

### Changes Made:

1. **Enhanced Database Connection (`get_db_connection`)**
   - Added WAL (Write-Ahead Logging) mode for better concurrency
   - Added timeout handling to avoid locks
   - Added `check_same_thread=False` for multi-threaded access
   - Fresh connections on each request

2. **Improved Books API (`/api/books`)**
   - Always creates fresh database connection
   - Disabled SQLite cache for fresh reads
   - Better error handling and logging
   - Increased limit from 50 to 500 books

3. **Added Debug Endpoints**
   - `/api/debug/database` - Shows database paths, book counts, sample books
   - `/api/refresh` - Forces database refresh

## How to Fix the Issue

### Method 1: Restart the Portal (Recommended)

1. **Stop the Student Portal** (if running)
   - In the main app, go to the "Portal" tab
   - Click "Stop Portal"

2. **Add your books** from the librarian side

3. **Restart the Student Portal**
   - Click "Start Portal" again
   - Fresh start = fresh database connection = all books visible!

### Method 2: Use the Debug API

1. **Add books** from the librarian side

2. **Check if books are in the database:**
   Open in browser: http://localhost:5000/api/debug/database
   
   This will show:
   - Database path
   - Total book count
   - Sample books
   - Last modified time

3. **Force refresh:**
   Open in browser: http://localhost:5000/api/refresh
   
   This clears caches and returns current book count

### Method 3: Use Test Script

1. **Run the test script:**
   ```
   cd LibraryApp
   python test_add_book.py
   ```

2. **Follow the on-screen instructions**

## Verification Steps

After making changes:

1. **Open Student Portal:** http://localhost:5000

2. **Navigate to Books section**

3. **You should see all books** added from the librarian side

4. **If books still don't appear:**
   - Check: http://localhost:5000/api/debug/database
   - Verify the `book_count` matches what you expect
   - Check the `sample_books` list
   - Verify the database `path` is correct

## Common Issues & Solutions

### Issue 1: Database Locked
**Symptom:** Error "database is locked"
**Solution:** 
- Close the main app
- Restart the portal
- The WAL mode should prevent this

### Issue 2: Wrong Database File
**Symptom:** Books show in app but not portal
**Solution:**
- Check `/api/debug/database` endpoint
- Verify `path` points to correct `library.db`
- Should be: `LibraryApp/library.db`

### Issue 3: Cache Not Clearing
**Symptom:** Old books visible, new ones not
**Solution:**
- Call `/api/refresh` endpoint
- Or restart the portal completely

### Issue 4: Portal Not Running Latest Code
**Symptom:** Changes don't take effect
**Solution:**
- Stop the portal completely
- Restart the main application
- Start portal again

## Technical Details

### SQLite WAL Mode
WAL (Write-Ahead Logging) allows:
- Multiple readers while writing
- Better concurrency
- Fewer locks
- Faster performance

### Database Connection Settings
```python
sqlite3.connect(
    db_path, 
    check_same_thread=False,  # Allow multi-threaded access
    timeout=10.0,              # Wait up to 10 seconds for locks
    isolation_level='DEFERRED' # Lazy transaction start
)
```

### PRAGMA Settings
```sql
PRAGMA journal_mode=WAL;      -- Enable WAL mode
PRAGMA synchronous=NORMAL;    -- Balance safety/performance
PRAGMA cache_size=0;          -- Disable cache for fresh reads
```

## Testing

To test the fix:

1. **Add a book from librarian side:**
   - Book ID: TEST001
   - Title: Test Book for Portal
   - Author: Test Author
   - Category: Testing
   - Copies: 5

2. **WITHOUT restarting portal, check:**
   http://localhost:5000/api/debug/database
   
   Should show `book_count` increased

3. **Refresh the Books page in portal**
   Should see TEST001 immediately

4. **If it works:** ✅ Fix successful!
   **If it doesn't:** Follow troubleshooting steps above

## Files Modified

1. `LibraryApp/Web-Extension/student_portal.py`
   - Enhanced `get_db_connection()` function
   - Improved `/api/books` endpoint
   - Added `/api/debug/database` endpoint
   - Added `/api/refresh` endpoint

## Rollback (if needed)

If this causes issues, you can revert by:
1. Using git: `git checkout student_portal.py`
2. Or use the old connection method:
   ```python
   conn = sqlite3.connect(db_path)
   conn.row_factory = sqlite3.Row
   ```

## Support

If issues persist:
1. Check portal logs in terminal
2. Check `portal_errors.log` file
3. Run test script: `python test_add_book.py`
4. Check database manually with SQLite viewer

---

**Fix Applied:** March 11, 2026  
**Status:** ✅ Complete - Portal should now show books immediately
