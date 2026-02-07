# HTTP 500 Errors - Fix Summary

## Issues Fixed

### 1. Account Deletion Requests Page - HTTP 500 Error
**Error Message:** "Could not load requests"

### 2. Student Portal Requests Page - HTTP 500 Error  
**Error Message:** "Could not load requests"

---

## Root Causes Identified and Fixed

### Issue 1: Incorrect Column Name Mapping
**Location:** [LibraryApp/Web-Extension/student_portal.py](LibraryApp/Web-Extension/student_portal.py#L2033)  
**Problem:** The SQL query was trying to select a column named `req_id`, but the actual column in the `requests` table is named `id`.

**Fix Applied:**
```python
# BEFORE
SELECT req_id, enrollment_no, request_type, details, status, created_at
FROM requests

# AFTER
SELECT id as req_id, enrollment_no, request_type, details, status, created_at
FROM requests
```

### Issue 2: Incorrect PostgreSQL Detection Logic
**Location:** [LibraryApp/Web-Extension/student_portal.py](LibraryApp/Web-Extension/student_portal.py#L2029), [L2114](LibraryApp/Web-Extension/student_portal.py#L2114), [L2619](LibraryApp/Web-Extension/student_portal.py#L2619)

**Problem:** The code was checking only if `DATABASE_URL` environment variable was set to determine whether to use PostgreSQL or SQLite:
```python
is_postgres = bool(os.getenv('DATABASE_URL'))
```

However, even if `DATABASE_URL` is set, the application might not have PostgreSQL libraries installed (`psycopg2`). In such cases, the code would fall back to SQLite, but the SQL syntax generation would still use PostgreSQL's INTERVAL syntax, causing syntax errors.

**Error Example:**
```
sqlite3.OperationalError: near "'7 days'": syntax error
# When trying to execute:
# AND timestamp >= CURRENT_TIMESTAMP - INTERVAL '7 days'
# (PostgreSQL syntax on SQLite)
```

**Fix Applied:**
```python
# BEFORE (all 3 locations)
is_postgres = bool(os.getenv('DATABASE_URL'))

# AFTER (all 3 locations)
is_postgres = bool(os.getenv('DATABASE_URL') and POSTGRES_AVAILABLE)
```

---

## Endpoints Fixed

### 1. GET `/api/admin/request-history`
- **Purpose:** Fetch approved/rejected student requests with search and date filtering
- **Fixed Issues:**
  - Column name `req_id` → `id as req_id` (line 2033)
  - Database detection logic (line 2029)

### 2. GET `/api/admin/deletion-history`
- **Purpose:** Fetch approved/rejected student deletion requests with search and date filtering
- **Fixed Issues:**
  - Database detection logic (line 2114)

### 3. GET `/api/admin/observability` (Bonus)
- **Purpose:** Get observability/analytics data for desktop dashboard
- **Fixed Issues:**
  - Database detection logic (line 2619)

---

## Testing Results

All 6 test cases now pass with 200 status codes:

- ✓ Deletion History - No filters
- ✓ Deletion History - 7 days filter
- ✓ Deletion History - Search filter
- ✓ Request History - No filters
- ✓ Request History - 7 days filter
- ✓ Request History - Search filter

---

## Files Modified

- [LibraryApp/Web-Extension/student_portal.py](LibraryApp/Web-Extension/student_portal.py)
  - Line 2029: Fixed `is_postgres` check in `/api/admin/request-history`
  - Line 2033: Fixed column name `id as req_id` in SELECT statement
  - Line 2114: Fixed `is_postgres` check in `/api/admin/deletion-history`
  - Line 2619: Fixed `is_postgres` check in `/api/admin/observability`

---

## How to Verify

1. Start the application
2. Click "Start the portal server to view analytics" in the Admin > Portal > Analytics tab
3. Navigate to Admin > Portal > Deletions - should load without HTTP 500 error
4. Navigate to Admin > Portal > Requests - should load without HTTP 500 error
5. Try filtering by date (7 days) and searching for specific records

Both pages should now display properly with data counts and request history.

---

## Technical Details

### Database Detection Logic
The corrected logic now properly checks:
```python
is_postgres = bool(os.getenv('DATABASE_URL') and POSTGRES_AVAILABLE)
```

Where:
- `os.getenv('DATABASE_URL')` - checks if the environment variable is set
- `POSTGRES_AVAILABLE` - checks if psycopg2 library is installed and importable

This ensures that:
1. If `DATABASE_URL` is not set → uses SQLite
2. If `DATABASE_URL` is set but `psycopg2` is not installed → falls back to SQLite
3. If both are available → uses PostgreSQL

### Date Filtering
The correct SQL syntax is now generated:
- **For SQLite:** `date('now', '-7 days')`
- **For PostgreSQL:** `CURRENT_TIMESTAMP - INTERVAL '7 days'`

This ensures compatibility with both local SQLite development and cloud PostgreSQL production.
