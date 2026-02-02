from flask import Flask, session, jsonify, request, send_from_directory, send_file
import sqlite3
import os
import sys
import json
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from functools import wraps
import time
import subprocess
from collections import defaultdict
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Setup path to import database.py from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    POSTGRES_AVAILABLE = True
except ImportError:
    PostgresConnectionWrapper = None
    psycopg2 = None
    RealDictCursor = None
    POSTGRES_AVAILABLE = False


class PostgresCursorWrapper:
    """Wrapper that makes psycopg2 cursors accept SQLite-style '?' placeholders."""

    def __init__(self, cursor):
        self._cursor = cursor

    def execute(self, sql, params=None):
        try:
            sql = sql.replace('?', '%s')
        except Exception:
            pass
        return self._cursor.execute(sql, params)

    def executemany(self, sql, seq_of_params):
        try:
            sql = sql.replace('?', '%s')
        except Exception:
            pass
        return self._cursor.executemany(sql, seq_of_params)

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()

    def __iter__(self):
        return iter(self._cursor)

    def __getattr__(self, name):
        return getattr(self._cursor, name)


class PostgresConnectionWrapper:
    """Small adapter so the rest of the code can treat Postgres like sqlite3.Row."""

    def __init__(self, conn):
        self._conn = conn

    def cursor(self):
        # RealDictCursor makes rows behave like dicts (similar to sqlite3.Row -> dict(row))
        return PostgresCursorWrapper(self._conn.cursor(cursor_factory=RealDictCursor))

    def commit(self):
        return self._conn.commit()

    def rollback(self):
        return self._conn.rollback()

    def close(self):
        return self._conn.close()

    def __getattr__(self, name):
        return getattr(self._conn, name)


# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads', 'study_materials')
REGISTRATION_PHOTO_FOLDER = os.path.join(BASE_DIR, 'uploads', 'registration_photos')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx', 'txt', 'jpg', 'jpeg', 'png', 'zip', 'rar'}
ALLOWED_PHOTO_EXTENSIONS = {'jpg', 'jpeg', 'png'}
MAX_PHOTO_BYTES = 50 * 1024  # 50KB

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REGISTRATION_PHOTO_FOLDER, exist_ok=True)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def _is_postgres_connection(conn) -> bool:
    """Best-effort check to determine if this is a PostgresConnectionWrapper."""
    try:
        return PostgresConnectionWrapper is not None and isinstance(conn, PostgresConnectionWrapper)
    except Exception:
        return False


def _requests_pk_column(conn) -> str:
    """Return the primary key column for the requests table ('req_id' or legacy 'id')."""
    try:
        cursor = conn.cursor()
        if _is_postgres_connection(conn):
            cursor.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'requests'
            """)
            cols = set()
            for r in cursor.fetchall():
                try:
                    cols.add(str(r.get('column_name')))
                except Exception:
                    try:
                        cols.add(str(r[0]))
                    except Exception:
                        pass
        else:
            cursor.execute("PRAGMA table_info(requests)")
            cols = {str(r['name']) for r in cursor.fetchall()}
    except Exception:
        # Default to modern schema
        return 'req_id'

    if 'req_id' in cols:
        return 'req_id'
    if 'id' in cols:
        return 'id'
    # Last resort
    return 'req_id'


def _safe_str(v):
    return str(v).strip() if v is not None else ''


def _normalize_enrollment(enrollment: str) -> str:
    return _safe_str(enrollment).upper()


def _allowed_photo_filename(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_PHOTO_EXTENSIONS


def _read_file_size_bytes(file_storage) -> int:
    """Return size of an uploaded file without trusting Content-Length."""
    try:
        pos = file_storage.stream.tell()
        file_storage.stream.seek(0, os.SEEK_END)
        size = int(file_storage.stream.tell())
        file_storage.stream.seek(pos, os.SEEK_SET)
        return size
    except Exception:
        # Fallback: read into memory (photo is limited to 50KB anyway)
        try:
            data = file_storage.read()
            file_storage.stream.seek(0)
            return len(data)
        except Exception:
            return 0

# --- Secure Secret Key Management ---
def get_or_create_secret_key():
    """Get secret key from env variable, or generate and persist one locally"""
    # 1. Check environment variable first
    env_key = os.environ.get('FLASK_SECRET_KEY') or os.environ.get('SECRET_KEY')
    if env_key:
        return env_key
    
    # 2. Check for persisted key file
    key_file = os.path.join(BASE_DIR, '.secret_key')
    if os.path.exists(key_file):
        with open(key_file, 'r') as f:
            return f.read().strip()
    
    # 3. Generate new key and persist it
    import secrets
    new_key = secrets.token_hex(32)
    try:
        with open(key_file, 'w') as f:
            f.write(new_key)
        print(f"[Security] Generated new secret key and saved to {key_file}")
    except Exception as e:
        print(f"[Security] Warning: Could not persist secret key: {e}")
    return new_key

# Serve React Build
app = Flask(__name__, static_folder='frontend/dist')
app.secret_key = get_or_create_secret_key()


# --- Build / Version info (helps diagnose "server not updated") ---
APP_START_TIME_UTC = datetime.utcnow().isoformat(timespec='seconds') + 'Z'


def _best_effort_git_commit() -> str | None:
    """Return git commit hash if available (works locally; may be unavailable in some deployments)."""
    try:
        # Avoid hanging in some environments
        out = subprocess.check_output(
            ['git', 'rev-parse', '--short', 'HEAD'],
            cwd=BASE_DIR,
            stderr=subprocess.DEVNULL,
            timeout=2,
        )
        v = out.decode('utf-8', errors='ignore').strip()
        return v or None
    except Exception:
        return None


APP_VERSION = (
    os.environ.get('APP_VERSION')
    or os.environ.get('GIT_COMMIT')
    or _best_effort_git_commit()
    or APP_START_TIME_UTC
)


@app.after_request
def _add_version_header(resp):
    # Always present so you can quickly check in browser DevTools (Network tab)
    resp.headers['X-App-Version'] = APP_VERSION
    return resp


@app.get('/api/version')
def api_version():
    """Debug endpoint to confirm what code/static build the server is running."""
    info = {
        'status': 'success',
        'app_version': APP_VERSION,
        'app_start_time_utc': APP_START_TIME_UTC,
        'pid': os.getpid(),
    }

    try:
        index_path = os.path.join(app.static_folder, 'index.html')
        st = os.stat(index_path)
        info['static_index'] = {
            'path': 'frontend/dist/index.html',
            'size_bytes': int(st.st_size),
            'mtime_utc': datetime.utcfromtimestamp(st.st_mtime).isoformat(timespec='seconds') + 'Z',
        }
    except Exception:
        info['static_index'] = None

    return jsonify(info)


# --- Rate Limiter (Custom Implementation - No External Dependencies) ---
class RateLimiter:
    """In-memory sliding window rate limiter"""
    def __init__(self):
        self.requests = defaultdict(list)  # {key: [timestamps]}
        self.lock = threading.Lock()
        
        # Rate limit configurations: {endpoint_pattern: (max_requests, window_seconds)}
        self.limits = {
            '/api/login': (5, 60),           # 5 attempts per minute
            '/api/public/forgot-password': (3, 300),  # 3 requests per 5 minutes
            '/api/change_password': (3, 60),  # 3 attempts per minute
            'default': (60, 60)               # 60 requests per minute (default)
        }
    
    def _get_client_key(self, endpoint):
        """Generate unique key for client + endpoint"""
        # Use IP address as identifier
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr) or 'unknown'
        return f"{client_ip}:{endpoint}"
    
    def _cleanup_old_requests(self, key, window_seconds):
        """Remove requests outside the time window"""
        cutoff = time.time() - window_seconds
        self.requests[key] = [ts for ts in self.requests[key] if ts > cutoff]
    
    def is_rate_limited(self, endpoint):
        """Check if request should be rate limited"""
        # Get limit config for endpoint
        limit_config = self.limits.get(endpoint, self.limits['default'])
        max_requests, window_seconds = limit_config
        
        key = self._get_client_key(endpoint)
        current_time = time.time()
        
        with self.lock:
            self._cleanup_old_requests(key, window_seconds)
            
            if len(self.requests[key]) >= max_requests:
                return True, max_requests, window_seconds
            
            # Record this request
            self.requests[key].append(current_time)
            return False, max_requests, window_seconds
    
    def get_retry_after(self, endpoint):
        """Get seconds until rate limit resets"""
        limit_config = self.limits.get(endpoint, self.limits['default'])
        _, window_seconds = limit_config
        key = self._get_client_key(endpoint)
        
        if self.requests[key]:
            oldest = min(self.requests[key])
            return int(window_seconds - (time.time() - oldest)) + 1
        return window_seconds

# Initialize rate limiter
rate_limiter = RateLimiter()

def rate_limit(f):
    """Decorator to apply rate limiting to an endpoint"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        endpoint = request.path
        is_limited, max_req, window = rate_limiter.is_rate_limited(endpoint)
        
        if is_limited:
            retry_after = rate_limiter.get_retry_after(endpoint)
            response = jsonify({
                'status': 'error',
                'message': f'Too many requests. Please try again in {retry_after} seconds.',
                'retry_after': retry_after
            })
            response.status_code = 429
            response.headers['Retry-After'] = str(retry_after)
            return response
        
        return f(*args, **kwargs)
    return decorated_function


# --- CSRF Protection (Double-Submit Cookie Pattern) ---
def generate_csrf_token():
    """Generate a secure random CSRF token"""
    import secrets
    return secrets.token_hex(32)

# Endpoints excluded from CSRF protection (login flow needs cookie first)
CSRF_EXCLUDED_ENDPOINTS = [
    '/api/login',
    '/api/public/forgot-password',
    '/api/public/register',
    '/api/change_password',  # Part of first-time login flow
    '/api/request',  # Student requests (session-protected)
    '/api/settings',  # Settings update (session-protected)
    '/api/request-deletion',  # Deletion request (session-protected)
    '/api/admin/notices',  # Desktop app access
    '/api/admin/requests',  # Desktop app access
    '/api/admin/deletion',  # Desktop app access
]


@app.before_request
def csrf_protect():
    """Validate CSRF token for state-changing requests"""
    # Skip for safe methods (GET, HEAD, OPTIONS)
    if request.method in ['GET', 'HEAD', 'OPTIONS']:
        return
    
    # Skip for excluded endpoints
    if request.path in CSRF_EXCLUDED_ENDPOINTS:
        return
    
    # Skip for admin endpoints (desktop app access only)
    if request.path.startswith('/api/admin/'):
        return
    
    # Skip for static files
    if request.path.startswith('/static') or request.path.startswith('/assets'):
        return
    
    # Get token from header and cookie
    header_token = request.headers.get('X-CSRF-Token')
    cookie_token = request.cookies.get('csrf_token')
    
    # Validate both exist and match
    if not header_token or not cookie_token or header_token != cookie_token:
        return jsonify({
            'status': 'error', 
            'message': 'CSRF token missing or invalid. Please refresh the page.'
        }), 403

@app.after_request
def set_csrf_cookie(response):
    """Set CSRF token cookie on every response if not present"""
    if 'csrf_token' not in request.cookies:
        token = generate_csrf_token()
        # httponly=False so JavaScript can read it
        # samesite='Lax' for balance of security and usability
        response.set_cookie(
            'csrf_token', 
            token, 
            httponly=False, 
            samesite='Lax',
            max_age=86400  # 24 hours
        )
    return response


# --- Observability: Logging Middleware ---
@app.after_request
def log_request(response):
    """Log every request to the access_logs table"""
    if request.path.startswith('/static') or request.path.startswith('/assets'):
        return response
    
    try:
        # Use a separate thread to avoid slowing down the response
        def write_log(endpoint, method, status):
            try:
                conn = get_portal_db()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO access_logs (endpoint, method, status) VALUES (?, ?, ?)",
                               (endpoint, method, status))
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"Logging failed: {e}")

        threading.Thread(target=write_log, args=(request.path, request.method, response.status_code)).start()
    except Exception:
        pass
        
    return response

def cleanup_logs():
    """Delete logs older than 7 days"""
    try:
        conn = get_portal_db()
        cursor = conn.cursor()
        cutoff_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        cursor.execute("DELETE FROM access_logs WHERE timestamp < ?", (cutoff_date,))
        conn.commit()
        conn.close()
        print("System: Cleaned up old access logs.")
    except Exception as e:
        print(f"Log cleanup failed: {e}")


def _log_portal_exception(context: str, exc: Exception) -> str:
    """Log exceptions to a local file for debugging portal 500 errors.

    Returns a short error id that can be shared to find the log entry.
    """
    try:
        import traceback
        error_id = f"E{int(time.time())}"
        log_path = os.path.join(BASE_DIR, 'portal_errors.log')
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"{datetime.now().isoformat()} [{error_id}] {context}\n")
            f.write(traceback.format_exc())
            f.write("\n")
        return error_id
    except Exception:
        return "EUNKNOWN"


def _parse_date_any(value):
    """Parse a value into a `date`.

    Supports SQLite text dates and Postgres date/datetime objects.
    Returns `datetime.date` or None.
    """
    if value is None:
        return None

    # psycopg2 may return date/datetime objects
    try:
        from datetime import date as _date
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, _date):
            return value
    except Exception:
        pass

    s = str(value).strip()
    if not s:
        return None

    # Common formats we have seen across environments
    fmts = (
        '%Y-%m-%d',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M:%S.%f',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%S.%f',
        '%Y-%m-%dT%H:%M:%S%z',
        '%Y-%m-%dT%H:%M:%S.%f%z',
    )

    # Try fast ISO parsing first
    try:
        # Handles YYYY-MM-DD and many ISO datetime strings
        dt = datetime.fromisoformat(s.replace('Z', '+00:00'))
        return dt.date()
    except Exception:
        pass

    for fmt in fmts:
        try:
            return datetime.strptime(s, fmt).date()
        except Exception:
            continue

    return None


def _to_iso_date(value):
    d = _parse_date_any(value)
    return d.isoformat() if d else (str(value) if value is not None else None)


@app.route('/api/admin/observability', methods=['GET'])
def api_admin_observability():
    """Observability stats used by the Desktop Admin -> Observability tab.

    The desktop UI expects specific keys (total_24h, hourly_data, endpoint_data, etc.).
    """
    try:
        def _parse_ts(value):
            if value is None:
                return None
            if isinstance(value, datetime):
                return value
            s = str(value)
            try:
                return datetime.fromisoformat(s)
            except Exception:
                pass
            for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f'):
                try:
                    return datetime.strptime(s, fmt)
                except Exception:
                    continue
            return None

        now = datetime.now()
        cutoff_24h = now - timedelta(hours=24)
        cutoff_7d = now - timedelta(days=7)

        conn = get_portal_db()
        cursor = conn.cursor()

        # Pull last 7 days and compute everything in Python to keep it backend-agnostic (SQLite/Postgres).
        cursor.execute(
            "SELECT endpoint, status, timestamp FROM access_logs WHERE timestamp >= ?",
            (cutoff_7d.strftime('%Y-%m-%d %H:%M:%S'),)
        )
        rows_7d = [dict(r) for r in cursor.fetchall()]
        conn.close()

        # Normalize
        normalized = []
        for r in rows_7d:
            ts = _parse_ts(r.get('timestamp'))
            try:
                status = int(r.get('status') or 0)
            except Exception:
                status = 0
            normalized.append({
                'endpoint': r.get('endpoint') or '',
                'status': status,
                'ts': ts,
            })

        rows_24h = [r for r in normalized if r['ts'] and r['ts'] >= cutoff_24h]

        total_24h = len(rows_24h)
        total_7d = len([r for r in normalized if r['ts']])

        success_24h = sum(1 for r in rows_24h if 200 <= r['status'] < 300)
        errors_24h = sum(1 for r in rows_24h if r['status'] >= 400)
        success_rate = (success_24h / total_24h * 100.0) if total_24h else 0.0

        # Hourly breakdown (00-23)
        hourly_data = {f"{h:02d}": 0 for h in range(24)}
        for r in rows_24h:
            h = r['ts'].hour
            hourly_data[f"{h:02d}"] = hourly_data.get(f"{h:02d}", 0) + 1

        peak_count = max(hourly_data.values()) if hourly_data else 0
        peak_hour_key = None
        if peak_count > 0:
            # choose earliest peak hour for stability
            for h in sorted(hourly_data.keys()):
                if hourly_data[h] == peak_count:
                    peak_hour_key = h
                    break
        peak_hour = f"{peak_hour_key}:00" if peak_hour_key is not None else 'N/A'

        # Endpoint counts (last 24h)
        ep_counts = {}
        for r in rows_24h:
            ep = r['endpoint']
            ep_counts[ep] = ep_counts.get(ep, 0) + 1
        endpoint_data = sorted(ep_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        # Status buckets (last 24h)
        status_data = {
            '2xx Success': 0,
            '3xx Redirect': 0,
            '4xx Client Error': 0,
            '5xx Server Error': 0,
        }
        for r in rows_24h:
            s = r['status']
            if 200 <= s < 300:
                status_data['2xx Success'] += 1
            elif 300 <= s < 400:
                status_data['3xx Redirect'] += 1
            elif 400 <= s < 500:
                status_data['4xx Client Error'] += 1
            elif s >= 500:
                status_data['5xx Server Error'] += 1

        # 7-day trend: YYYY-MM-DD -> count
        trend_counts = {}
        for r in normalized:
            if not r['ts']:
                continue
            day = r['ts'].strftime('%Y-%m-%d')
            trend_counts[day] = trend_counts.get(day, 0) + 1
        trend_data = sorted(trend_counts.items(), key=lambda x: x[0])

        return jsonify({
            'status': 'ok',
            'total_24h': total_24h,
            'total_7d': total_7d,
            'success_24h': success_24h,
            'success_rate': success_rate,
            'errors_24h': errors_24h,
            'peak_hour': peak_hour,
            'peak_count': peak_count,
            'hourly_data': hourly_data,
            'endpoint_data': endpoint_data,
            'status_data': status_data,
            'trend_data': trend_data,
        })
    except Exception as e:
        error_id = _log_portal_exception('api_admin_observability', e)
        return jsonify({'status': 'error', 'message': 'Observability failed', 'error_id': error_id}), 500

def get_db_connection(local_db_name):
    """Generic connection factory: Postgres (if env) or Local SQLite"""
    def _should_use_cloud_db() -> bool:
        # Desktop app should default to LOCAL DB even if a cloud DATABASE_URL exists in .env.
        # Enable cloud explicitly when deploying the portal.
        force_local = os.getenv('PORTAL_FORCE_LOCAL', '').strip().lower() in ('1', 'true', 'yes')
        if force_local:
            return False

        use_cloud = os.getenv('PORTAL_USE_CLOUD', '').strip().lower() in ('1', 'true', 'yes')
        if use_cloud:
            return True

        # Auto-detect common cloud runtimes
        if os.getenv('DYNO') or os.getenv('RENDER') or os.getenv('FLY_APP_NAME') or os.getenv('WEBSITE_INSTANCE_ID'):
            return True

        return False

    database_url = os.getenv('DATABASE_URL')
    if database_url and POSTGRES_AVAILABLE and _should_use_cloud_db():
        try:
            conn = psycopg2.connect(database_url)
            return PostgresConnectionWrapper(conn)
        except Exception as e:
            print(f"Cloud DB Connection Error: {e}")
            # Fallback to local if connection fails
            pass
            
    # Local SQLite fallback
    if local_db_name == 'library.db':
        db_path = os.path.join(os.path.dirname(BASE_DIR), 'library.db')
    else:
        db_path = os.path.join(BASE_DIR, 'portal.db')
        
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def get_library_db():
    """Read-Only Connection to Core Data"""
    # If generic DB is used, both library and portal data are in the same Postgres DB
    return get_db_connection('library.db')

def get_portal_db():
    """Read-Write Connection to Sandbox Data"""
    # If generic DB is used, both library and portal data are in the same Postgres DB
    return get_db_connection('portal.db')

def create_table_safe(cursor, table_name, pg_sql, sqlite_sql):
    """Helper to create tables with backend-specific syntax"""
    # Use backend detection rather than only checking DATABASE_URL, because
    # desktop/local runs may have DATABASE_URL present but still be using SQLite.
    try:
        use_pg = False
        try:
            # If the cursor is from our postgres wrapper, it will have a _cursor attr.
            # The connection wrapper check is more reliable when available.
            use_pg = isinstance(getattr(cursor, 'connection', None), PostgresConnectionWrapper)  # type: ignore
        except Exception:
            pass

        if not use_pg:
            # Fallback: if we can import psycopg2 and the environment indicates cloud runtime
            database_url = os.getenv('DATABASE_URL')
            force_local = os.getenv('PORTAL_FORCE_LOCAL', '').strip().lower() in ('1', 'true', 'yes')
            use_cloud = os.getenv('PORTAL_USE_CLOUD', '').strip().lower() in ('1', 'true', 'yes')
            auto_cloud = bool(os.getenv('DYNO') or os.getenv('RENDER') or os.getenv('FLY_APP_NAME') or os.getenv('WEBSITE_INSTANCE_ID'))
            use_pg = bool(database_url and POSTGRES_AVAILABLE and (use_cloud or auto_cloud) and not force_local)

        if use_pg:
            try:
                cursor.execute(pg_sql)
            except Exception as e:
                print(f"Table creation warning ({table_name}): {e}")
        else:
            cursor.execute(sqlite_sql)
    except Exception as e:
        # Last resort: attempt SQLite statement
        try:
            cursor.execute(sqlite_sql)
        except Exception:
            print(f"Table creation failed ({table_name}): {e}")

def init_portal_db():
    """Initialize the Sandbox DB for Requests and Notes"""
    conn = get_portal_db()
    cursor = conn.cursor()
    
    # Requests Table
    create_table_safe(cursor, 'requests', '''
        CREATE TABLE IF NOT EXISTS requests (
            req_id SERIAL PRIMARY KEY,
            enrollment_no TEXT,
            request_type TEXT,
            details TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''', '''
        CREATE TABLE IF NOT EXISTS requests (
            req_id INTEGER PRIMARY KEY AUTOINCREMENT,
            enrollment_no TEXT,
            request_type TEXT,      -- 'profile_update', 'renewal', 'extension', 'notification'
            details TEXT,           -- JSON payload or text description
            status TEXT DEFAULT 'pending', -- 'pending', 'approved', 'rejected'
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Auth Table
    create_table_safe(cursor, 'student_auth', '''
        CREATE TABLE IF NOT EXISTS student_auth (
            enrollment_no TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            is_first_login INTEGER DEFAULT 1,
            last_changed TIMESTAMP
        )
    ''', '''
        CREATE TABLE IF NOT EXISTS student_auth (
            enrollment_no TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            is_first_login INTEGER DEFAULT 1, -- 1=True, 0=False
            last_changed DATETIME
        )
    ''')

    # Notices Table
    create_table_safe(cursor, 'notices', '''
        CREATE TABLE IF NOT EXISTS notices (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''', '''
        CREATE TABLE IF NOT EXISTS notices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            active INTEGER DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Deletion Requests
    create_table_safe(cursor, 'deletion_requests', '''
        CREATE TABLE IF NOT EXISTS deletion_requests (
            id SERIAL PRIMARY KEY,
            student_id TEXT NOT NULL,
            reason TEXT,
            status TEXT DEFAULT 'pending',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(student_id) REFERENCES students(enrollment_no)
        )
    ''', '''
        CREATE TABLE IF NOT EXISTS deletion_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            reason TEXT,
            status TEXT DEFAULT 'pending', -- pending, approved, rejected
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(student_id) REFERENCES students(enrollment_no)
        )
    ''')

    # User Settings
    create_table_safe(cursor, 'user_settings', '''
        CREATE TABLE IF NOT EXISTS user_settings (
            enrollment_no TEXT PRIMARY KEY,
            email TEXT,
            library_alerts INTEGER DEFAULT 0,
            loan_reminders INTEGER DEFAULT 1,
            theme TEXT DEFAULT 'light',
            language TEXT DEFAULT 'English',
            data_consent INTEGER DEFAULT 1
        )
    ''', '''
        CREATE TABLE IF NOT EXISTS user_settings (
            enrollment_no TEXT PRIMARY KEY,
            email TEXT,
            library_alerts INTEGER DEFAULT 0,
            loan_reminders INTEGER DEFAULT 1,
            theme TEXT DEFAULT 'light',
            language TEXT DEFAULT 'English',
            data_consent INTEGER DEFAULT 1
        )
    ''')

    # Notifications
    create_table_safe(cursor, 'user_notifications', '''
        CREATE TABLE IF NOT EXISTS user_notifications (
            id SERIAL PRIMARY KEY,
            enrollment_no TEXT,
            type TEXT,
            title TEXT,
            message TEXT,
            link TEXT,
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''', '''
        CREATE TABLE IF NOT EXISTS user_notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            enrollment_no TEXT,
            type TEXT,              -- 'request_update', 'security', 'system', 'overdue'
            title TEXT,
            message TEXT,
            link TEXT,              -- Optional action link
            is_read INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Book Waitlist
    create_table_safe(cursor, 'book_waitlist', '''
        CREATE TABLE IF NOT EXISTS book_waitlist (
            id SERIAL PRIMARY KEY,
            enrollment_no TEXT NOT NULL,
            book_id TEXT NOT NULL,
            book_title TEXT,
            notified INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(enrollment_no, book_id)
        )
    ''', '''
        CREATE TABLE IF NOT EXISTS book_waitlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            enrollment_no TEXT NOT NULL,
            book_id INTEGER NOT NULL,
            book_title TEXT,
            notified INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(enrollment_no, book_id)
        )
    ''')

    # Access Logs
    create_table_safe(cursor, 'access_logs', '''
        CREATE TABLE IF NOT EXISTS access_logs (
            id SERIAL PRIMARY KEY,
            endpoint TEXT,
            method TEXT,
            status INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''', '''
        CREATE TABLE IF NOT EXISTS access_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            endpoint TEXT,
            method TEXT,
            status INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Study Materials
    create_table_safe(cursor, 'study_materials', '''
        CREATE TABLE IF NOT EXISTS study_materials (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            filename TEXT NOT NULL,
            original_filename TEXT,
            file_size INTEGER,
            branch TEXT DEFAULT 'Computer',
            year TEXT NOT NULL,
            category TEXT,
            uploaded_by TEXT DEFAULT 'Library Admin',
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            active INTEGER DEFAULT 1
        )
    ''', '''
        CREATE TABLE IF NOT EXISTS study_materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            filename TEXT NOT NULL,
            original_filename TEXT,
            file_size INTEGER,
            branch TEXT DEFAULT 'Computer',
            year TEXT NOT NULL,  -- '1st', '2nd', '3rd', '4th', '5th', '6th' (Semester)
            category TEXT,  -- 'Notes', 'PYQ', 'Study Material', 'Other'
            uploaded_by TEXT DEFAULT 'Library Admin',
            upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            active INTEGER DEFAULT 1
        )
    ''')

    # Ratings
    create_table_safe(cursor, 'book_ratings', '''
        CREATE TABLE IF NOT EXISTS book_ratings (
            id SERIAL PRIMARY KEY,
            book_id TEXT NOT NULL,
            enrollment_no TEXT NOT NULL,
            rating INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(book_id, enrollment_no)
        )
    ''', '''
        CREATE TABLE IF NOT EXISTS book_ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id TEXT NOT NULL,
            enrollment_no TEXT NOT NULL,
            rating INTEGER NOT NULL, -- 1-5
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(book_id, enrollment_no)
        )
    ''')

    
    conn.commit()
    conn.close()

# Initialize on Import
init_portal_db()

# Run cleanup on startup (after all functions are defined)
threading.Thread(target=cleanup_logs, daemon=True).start()

# --- Helper Functions for Email ---

def send_email_bg(recipient, subject, body):
    """Background task to send email using shared settings"""
    if not recipient:
        return
        
    try:
        # Path to email_settings.json (One level up from Web-Extension)
        # student_portal.py is in LibraryApp/Web-Extension
        # email_settings.json is in LibraryApp/
        settings_path = os.path.join(os.path.dirname(BASE_DIR), 'email_settings.json')
        
        if not os.path.exists(settings_path):
            print(f"Email settings not found at {settings_path}")
            return

        with open(settings_path, 'r') as f:
            settings = json.load(f)

        if not settings.get('enabled'):
            return

        msg = MIMEMultipart('alternative')
        msg['From'] = settings['sender_email']
        msg['To'] = recipient
        msg['Subject'] = subject
        
        # Attach plain text version (fallback)
        msg.attach(MIMEText("Please enable HTML to view this email.", 'plain'))
        
        # Attach HTML version if body looks like HTML, otherwise plain
        if body.strip().startswith('<html') or body.strip().startswith('<!DOCTYPE html'):
             msg.attach(MIMEText(body, 'html'))
        else:
             msg.attach(MIMEText(body, 'plain'))

        # Standard SMTP (Gmail/Outlook)
        server = smtplib.SMTP(settings['smtp_server'], settings['smtp_port'])
        server.starttls()
        server.login(settings['sender_email'], settings['sender_password'])
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {recipient}")
        
    except Exception as e:
        print(f"Failed to send email: {e}")

def trigger_notification_email(enrollment_no, subject, body):
    """Fetches user email and triggers background send"""
    try:
        # 1. Check User Settings (Portal DB)
        conn_portal = get_portal_db()
        cursor_portal = conn_portal.cursor()
        cursor_portal.execute("SELECT email FROM user_settings WHERE enrollment_no = ?", (enrollment_no,))
        setting = cursor_portal.fetchone()
        conn_portal.close()
        
        email = setting['email'] if setting and setting['email'] else None
        
        # 2. If no custom email, check College Records (Library DB)
        if not email:
            conn_lib = get_library_db()
            cursor_lib = conn_lib.cursor()
            cursor_lib.execute("SELECT email FROM students WHERE enrollment_no = ?", (enrollment_no,))
            student = cursor_lib.fetchone()
            conn_lib.close()
            email = student['email'] if student else None
            
        if email:
            threading.Thread(target=send_email_bg, args=(email, subject, body)).start()
            
    except Exception as e:
        print(f"Error triggering email: {e}")

# --- Auth Endpoints ---

@app.route('/api/request-deletion', methods=['POST'])
def request_deletion():
    data = request.json
    password = data.get('password', '').strip()
    reason = data.get('reason', 'User requested deletion via Student Portal')
    
    # 1. Verify Session
    if 'student_id' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
        
    student_id = session['student_id']
    
    conn = get_portal_db()
    c = conn.cursor()
    
    # 2. Verify Password (Re-authentication)
    # Check student_auth first
    c.execute("SELECT password FROM student_auth WHERE enrollment_no = ?", (student_id,))
    auth_record = c.fetchone()
    
    is_valid = False
    if auth_record:
        stored_pw = auth_record['password']
        # Try hash verification first
        try:
            if check_password_hash(stored_pw, password):
                is_valid = True
        except:
            # Fallback to plain text comparison
            if stored_pw == password:
                is_valid = True
    else:
        # No auth record - check against enrollment_no as default password
        if password == student_id:
            is_valid = True
            
    if not is_valid:
        conn.close()
        return jsonify({"status": "error", "message": "Incorrect password"}), 403
        
    # 3. Check for existing pending request
    c.execute("SELECT id FROM deletion_requests WHERE student_id = ? AND status = 'pending'", (student_id,))
    existing = c.fetchone()
    if existing:
        conn.close()
        return jsonify({"status": "error", "message": "A deletion request is already pending."}), 400
        
    # 4. Create Request
    try:
        c.execute("INSERT INTO deletion_requests (student_id, reason) VALUES (?, ?)", (student_id, reason))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Deletion request submitted for librarian approval."})
    except Exception as e:
        conn.close()
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/login', methods=['POST'])
@rate_limit
def api_login():
    data = request.json
    enrollment = data.get('enrollment_no', '').strip()
    password = data.get('password', '').strip()
    
    if not enrollment:
        return jsonify({'status': 'error', 'message': 'Enrollment number required'}), 400
    
    # 1. Check if student exists in MAIN DB (Read-Only)
    conn_lib = get_library_db()
    cursor_lib = conn_lib.cursor()
    cursor_lib.execute("SELECT * FROM students WHERE enrollment_no = ?", (enrollment,))
    student = cursor_lib.fetchone()
    conn_lib.close()
    
    if not student:
        return jsonify({'status': 'error', 'message': 'Student not found'}), 401
    
    # 2. Check Auth Status in PORTAL DB (Shadow Auth)
    conn_portal = get_portal_db()
    cursor_p = conn_portal.cursor()
    cursor_p.execute("SELECT * FROM student_auth WHERE enrollment_no = ?", (enrollment,))
    auth_record = cursor_p.fetchone()
    
    require_change = False
    
    if not auth_record:
        # FIRST LOGIN ATTEMPT EVER for this user
        # Default behavior: Password MUST be enrollment number
        if password == enrollment:
            # Create auth record with HASHED password
            hashed_pw = generate_password_hash(enrollment)
            cursor_p.execute("INSERT INTO student_auth (enrollment_no, password, is_first_login) VALUES (?, ?, 1)", 
                             (enrollment, hashed_pw))
            conn_portal.commit()
            require_change = True
        else:
            conn_portal.close()
            return jsonify({'status': 'error', 'message': 'Invalid password (First login? Use Enrollment No.)'}), 401
    else:
        # Existing auth record
        stored_pw = auth_record['password']
        
        # 1. Try verifying hash
        is_valid = False
        try:
            if check_password_hash(stored_pw, password):
                is_valid = True
        except:
            # Not a hash (legacy plain text)
            if stored_pw == password:
                is_valid = True
                # MIGRATION: Upgrade to hash immediatey
                new_hash = generate_password_hash(password)
                cursor_p.execute("UPDATE student_auth SET password = ? WHERE enrollment_no = ?", (new_hash, enrollment))
                conn_portal.commit()
        
        if not is_valid:
            conn_portal.close()
            return jsonify({'status': 'error', 'message': 'Invalid password'}), 401
            
        if auth_record['is_first_login']:
            require_change = True

    # Login Success - Create Session
    session['student_id'] = enrollment
    session['logged_in'] = True
    
    conn_portal.close()
    
    # Return full user details (similar to /api/me) for Profile page consistency
    student_year = student['year'] if student['year'] else '1st'
    
    return jsonify({
        'status': 'success', 
        'enrollment_no': enrollment,
        'name': student['name'],
        'department': student['department'] if student['department'] else 'General',
        'year': student_year,
        'email': student['email'],
        'require_change': require_change
    })

@app.route('/api/public/forgot-password', methods=['POST'])
@rate_limit
def api_forgot_password():
    data = request.json
    enrollment = data.get('enrollment_no')
    
    if not enrollment:
        return jsonify({'status': 'error', 'message': 'Enrollment number required'}), 400
        
    try:
        # Verify Student Exists in Library DB
        conn_lib = get_library_db()
        cursor_lib = conn_lib.cursor()
        cursor_lib.execute("SELECT name, email FROM students WHERE enrollment_no = ?", (enrollment,))
        student = cursor_lib.fetchone()
        conn_lib.close()
        
        if not student:
            return jsonify({'status': 'error', 'message': 'Student not found'}), 404
            
        student_name = student['name'].split()[0] if student and student['name'] else "Student"
        
        # Create Request in Portal DB
        conn_portal = get_portal_db()
        cursor_portal = conn_portal.cursor()
        
        # Check for existing pending request to avoid spam
        cursor_portal.execute("SELECT id FROM requests WHERE enrollment_no = ? AND request_type = 'password_reset' AND status = 'pending'", (enrollment,))
        existing = cursor_portal.fetchone()
        if existing:
             conn_portal.close()
             return jsonify({'status': 'error', 'message': 'A reset request is already pending.'}), 400
             
        cursor_portal.execute("INSERT INTO requests (enrollment_no, request_type, details) VALUES (?, ?, ?)",
                       (enrollment, 'password_reset', 'Request to reset password to default.'))
        conn_portal.commit()
        conn_portal.close()
        
        # Send Receipt Email
        email_body = generate_email_template(
            header_title="Password Reset Requested",
            user_name=student_name,
            main_text="We have received your request to reset your password.",
            details_dict={'Action': 'Account Password Reset', 'Status': 'Pending Librarian Approval'},
            theme='blue',
            footer_note="If you did not request this, please contact the library immediately."
        )
        trigger_notification_email(enrollment, "Password Reset Request", email_body)
        
        return jsonify({'status': 'success', 'message': 'Request sent to librarian'})
        
    except Exception as e:
        print(f"Forgot password error: {e}")
        return jsonify({'status': 'error', 'message': 'Internal Server Error'}), 500

@app.route('/api/change_password', methods=['POST'])
@rate_limit
def api_change_password():
    if not session.get('logged_in'):
        return jsonify({'status': 'error', 'message': 'Not logged in'}), 401
        
    data = request.json
    new_password = data.get('new_password', '').strip()
    enrollment = session.get('student_id')
    
    if not new_password or len(new_password) < 6:
        return jsonify({'status': 'error', 'message': 'Password must be at least 6 characters'}), 400
    
    # Get student name from library.db
    conn_lib = get_library_db()
    cursor_lib = conn_lib.cursor()
    cursor_lib.execute("SELECT name FROM students WHERE enrollment_no = ?", (enrollment,))
    student = cursor_lib.fetchone()
    conn_lib.close()
    student_name = student['name'] if student else enrollment
    
    # Update password in portal.db
    conn = get_portal_db()
    cursor = conn.cursor()
    
    # Hash the new password
    hashed_pw = generate_password_hash(new_password)
    
    cursor.execute("""
        UPDATE student_auth 
        SET password = ?, is_first_login = 0, last_changed = CURRENT_TIMESTAMP
        WHERE enrollment_no = ?
    """, (hashed_pw, enrollment))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'status': 'success', 
        'message': 'Password updated successfully',
        'name': student_name,
        'enrollment_no': enrollment
    })


# =====================================================================
# PUBLIC STUDENT REGISTRATION (REQUEST FLOW)
# =====================================================================


@app.route('/api/public/register', methods=['POST'])
@rate_limit
def api_public_register_student():
    """Students can submit a registration request (pending librarian approval)."""
    try:
        # Expect multipart/form-data
        enrollment_no = _normalize_enrollment(request.form.get('enrollment_no', ''))
        name = _safe_str(request.form.get('name', ''))
        year = _safe_str(request.form.get('year', ''))
        department = _safe_str(request.form.get('department', ''))
        phone = _safe_str(request.form.get('phone', ''))
        email = _safe_str(request.form.get('email', ''))

        if not enrollment_no or not name or not year or not department or not phone or not email:
            return jsonify({'status': 'error', 'message': 'All fields are required (except photo).'}), 400

        if len(phone) < 8:
            return jsonify({'status': 'error', 'message': 'Invalid mobile number.'}), 400

        if '@' not in email or '.' not in email:
            return jsonify({'status': 'error', 'message': 'Invalid email address.'}), 400

        # 1) Ensure student does NOT already exist in library DB
        conn_lib = get_library_db()
        cursor_lib = conn_lib.cursor()
        cursor_lib.execute("SELECT enrollment_no FROM students WHERE enrollment_no = ?", (enrollment_no,))
        existing = cursor_lib.fetchone()
        conn_lib.close()
        if existing:
            return jsonify({'status': 'error', 'message': 'You are already registered in the library.'}), 409

        # 2) Prevent duplicate pending registration requests
        conn_portal = get_portal_db()
        cursor_p = conn_portal.cursor()
        cursor_p.execute(
            """
            SELECT 1 FROM requests
            WHERE enrollment_no = ? AND request_type = 'student_registration' AND status = 'pending'
            LIMIT 1
            """,
            (enrollment_no,)
        )
        pending = cursor_p.fetchone()
        if pending:
            conn_portal.close()
            return jsonify({'status': 'error', 'message': 'A registration request is already pending. Please wait for librarian approval.'}), 400

        # 3) Optional photo upload (<=50KB)
        photo_path = None
        if 'photo' in request.files and request.files['photo'] and request.files['photo'].filename:
            photo = request.files['photo']
            if not _allowed_photo_filename(photo.filename):
                conn_portal.close()
                return jsonify({'status': 'error', 'message': 'Photo must be JPG or PNG.'}), 400

            size = _read_file_size_bytes(photo)
            if size > MAX_PHOTO_BYTES:
                conn_portal.close()
                return jsonify({'status': 'error', 'message': 'Photo too large. Max size is 50KB.'}), 400

            original_filename = secure_filename(photo.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_filename = f"{timestamp}_{enrollment_no}_{original_filename}"
            photo_path = os.path.join(REGISTRATION_PHOTO_FOLDER, unique_filename)
            photo.save(photo_path)

        details = {
            'name': name,
            'year': year,
            'department': department,
            'phone': phone,
            'email': email,
            'photo_filename': os.path.basename(photo_path) if photo_path else None
        }

        cursor_p.execute(
            "INSERT INTO requests (enrollment_no, request_type, details) VALUES (?, 'student_registration', ?)",
            (enrollment_no, json.dumps(details))
        )
        conn_portal.commit()
        conn_portal.close()

        return jsonify({
            'status': 'success',
            'message': 'Registration request submitted. Please wait for librarian approval.'
        })
    except Exception as e:
        error_id = _log_portal_exception('api_public_register_student', e)
        return jsonify({'status': 'error', 'message': 'Registration failed', 'error_id': error_id}), 500


@app.route('/api/settings', methods=['POST'])
def api_update_settings():
    if 'student_id' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
        
    data = request.json
    enrollment = session['student_id']
    email = data.get('email')
    library_alerts = 1 if data.get('libraryAlerts') else 0
    loan_reminders = 1 if data.get('loanReminders') else 0
    theme = data.get('theme', 'light') # 'light' or 'dark'
    language = data.get('language', 'English')
    data_consent = 1 if data.get('dataConsent') else 0
    
    conn = get_portal_db()
    cursor = conn.cursor()
    
    # Upsert Settings
    cursor.execute("""
        INSERT INTO user_settings (enrollment_no, email, library_alerts, loan_reminders, theme, language, data_consent)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(enrollment_no) DO UPDATE SET
            email=excluded.email,
            library_alerts=excluded.library_alerts,
            loan_reminders=excluded.loan_reminders,
            theme=excluded.theme,
            language=excluded.language,
            data_consent=excluded.data_consent
    """, (enrollment, email, library_alerts, loan_reminders, theme, language, data_consent))
    
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'message': 'Settings updated successfully'})

# --- Broadcast APIs ---

@app.route('/api/notices', methods=['GET'])
def api_public_notices():
    """Get active notices for students"""
    conn = get_portal_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, message, created_at FROM notices WHERE active = 1 ORDER BY created_at DESC")
    notices = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({'notices': notices})

@app.route('/api/loan-history')
def api_loan_history():
    """Get comprehensive loan history with all statuses"""
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    enrollment = session['student_id']
    conn = get_library_db()
    cursor = conn.cursor()
    
    # Get ALL borrow records (borrowed, returned, overdue)
    cursor.execute("""
        SELECT b.title, b.author, b.category, br.borrow_date, br.due_date, br.return_date, br.status, br.fine
        FROM borrow_records br
        JOIN books b ON br.book_id = b.book_id
        WHERE br.enrollment_no = ?
        ORDER BY br.borrow_date DESC
    """, (enrollment,))
    
    all_records = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # Categorize records
    currently_borrowed = []
    returned_on_time = []
    returned_late = []
    currently_overdue = []
    
    today = datetime.now()
    
    for record in all_records:
        # Determine actual status
        if record['status'] == 'borrowed':
            if record['due_date']:
                try:
                    due_dt = datetime.strptime(record['due_date'], '%Y-%m-%d')
                    if due_dt < today:
                        record['actual_status'] = 'Currently Overdue'
                        record['overdue_days'] = (today - due_dt).days
                        currently_overdue.append(record)
                    else:
                        record['actual_status'] = 'Currently Borrowed'
                        record['days_left'] = (due_dt - today).days
                        currently_borrowed.append(record)
                except:
                    record['actual_status'] = 'Currently Borrowed'
                    currently_borrowed.append(record)
        elif record['status'] == 'returned':
            if record['due_date'] and record['return_date']:
                try:
                    due_dt = datetime.strptime(record['due_date'], '%Y-%m-%d')
                    return_dt = datetime.strptime(record['return_date'], '%Y-%m-%d')
                    if return_dt > due_dt:
                        record['actual_status'] = 'Returned Late'
                        record['fine_paid'] = record.get('fine', 0) > 0
                        returned_late.append(record)
                    else:
                        record['actual_status'] = 'Returned On Time'
                        returned_on_time.append(record)
                except:
                    record['actual_status'] = 'Returned'
                    returned_on_time.append(record)
    
    return jsonify({
        'currently_borrowed': currently_borrowed,
        'currently_overdue': currently_overdue,
        'returned_on_time': returned_on_time,
        'returned_late': returned_late,
        'total_borrowed': len(all_records),
        'total_fines_paid': sum([r.get('fine', 0) for r in returned_late])
    })

# --- Notification System API ---

@app.route('/api/notifications', methods=['GET'])
def api_get_notifications():
    """Unified Notification Stream"""
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    enrollment = session['student_id']
    notifications = []
    
    # 1. Fetch Persistent Notifications (History)
    conn = get_portal_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM user_notifications 
        WHERE enrollment_no = ? 
        ORDER BY created_at DESC 
        LIMIT 50
    """, (enrollment,))
    history_items = [dict(row) for row in cursor.fetchall()]
    
    # 2. Real-time Overdue Alerts (High Priority)
    conn_lib = get_library_db()
    cursor_lib = conn_lib.cursor()
    cursor_lib.execute("""
        SELECT b.title, br.due_date, br.book_id
        FROM borrow_records br
        JOIN books b ON br.book_id = b.book_id
        WHERE br.enrollment_no = ? AND br.status = 'borrowed'
    """, (enrollment,))
    borrows = cursor_lib.fetchall()
    conn_lib.close()
    
    today = datetime.now()
    active_alerts = []
    
    for row in borrows:
        if row['due_date']:
            try:
                due_dt = datetime.strptime(row['due_date'], '%Y-%m-%d')
                delta = (due_dt - today).days
                
                if delta < 0:
                    active_alerts.append({
                        'id': f"overdue_{row['book_id']}", # Virtual ID
                        'type': 'danger',
                        'title': 'Overdue Book',
                        'message': f"'{row['title']}' is overdue by {abs(delta)} days. Please return immediately.",
                        'is_read': 0, # Always unread/active until resolved
                        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'link': f"/books/{row['book_id']}"
                    })
                elif delta <= 2:
                    active_alerts.append({
                        'id': f"warning_{row['book_id']}",
                        'type': 'warning',
                        'title': 'Due Soon',
                        'message': f"'{row['title']}' is due in {delta} days.",
                        'is_read': 0,
                        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'link': f"/books/{row['book_id']}"
                    })
            except:
                pass

    # 3. Security Alert
    cursor.execute("SELECT is_first_login FROM student_auth WHERE enrollment_no = ?", (enrollment,))
    auth = cursor.fetchone()
    if auth and auth['is_first_login']:
        active_alerts.insert(0, {
            'id': 'security_alert',
            'type': 'danger',
            'title': 'Security Alert',
            'message': 'You are using a default password. Change it now to secure your account.',
            'is_read': 0,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'link': '/settings'
        })

    # 4. Broadcast Notices (System)
    cursor.execute("SELECT * FROM notices WHERE active = 1 ORDER BY created_at DESC LIMIT 10")
    notices = [dict(row) for row in cursor.fetchall()]
    broadcasts = []
    
    for note in notices:
        broadcasts.append({
            'id': f"notice_{note['id']}",
            'type': 'system',
            'title': note['title'],
            'message': note['message'],
            'is_read': 0, # Notices are technically always "unread" unless tracked separately, but for now we show them.
            'created_at': note['created_at'],
            'link': None
        })

    conn.close()
    
    # Combine: Security > Overdue > History > Broadcasts
    # Note: History includes past request updates. Broadcasts are general.
    # We'll merge them all and sort by date for the "All" tab.
    
    combined = active_alerts + history_items + broadcasts
    
    # Sort by created_at desc
    def get_date(item):
        try:
            return datetime.strptime(item['created_at'], '%Y-%m-%d %H:%M:%S')
        except:
             try:
                 # Backup format if milliseconds exist
                 return datetime.strptime(item['created_at'].split('.')[0], '%Y-%m-%d %H:%M:%S')
             except:
                 return datetime.min

    combined.sort(key=get_date, reverse=True)
    
    # Count Unread
    # For generated items (alerts/broadcasts), they count as unread if they aren't explicitly suppressed.
    # Logic: Database items have 'is_read'. Virtual items (Overdue/Security) depend on existence.
    # Broadcasts: We don't have per-user read state yet. We'll mark them as read for badge count to avoid permanent red dot,
    # OR we just count DB items + Active Alerts.
    
    unread_db = len([n for n in history_items if not n['is_read']])
    unread_alerts = len(active_alerts) # Alerts are always actionable/unread
    # We won't count Broadcasts in the badge to avoid annoyance, they appear in the list silently (or maybe separate logic later)
    
    return jsonify({
        'notifications': combined,
        'unread_count': unread_db + unread_alerts
    })

@app.route('/api/notifications/mark-read', methods=['POST'])
def api_mark_read():
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    notif_id = data.get('id')
    enrollment = session['student_id']
    
    conn = get_portal_db()
    cursor = conn.cursor()
    
    if notif_id == 'all':
        cursor.execute("UPDATE user_notifications SET is_read = 1 WHERE enrollment_no = ?", (enrollment,))
    elif str(notif_id).isdigit():
        # Only mark DB items (virtual alerts can't be marked read via API, they persist until resolved)
        cursor.execute("UPDATE user_notifications SET is_read = 1 WHERE id = ? AND enrollment_no = ?", (notif_id, enrollment))
        
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/api/notifications/<int:notif_id>', methods=['DELETE'])
def api_delete_notification(notif_id):
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    enrollment = session['student_id']
    conn = get_portal_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_notifications WHERE id = ? AND enrollment_no = ?", (notif_id, enrollment))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/api/admin/notices', methods=['GET', 'POST', 'DELETE'])
def api_admin_notices():
    """Admin management for notices"""
    conn = get_portal_db()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        # List all notices (active and inactive)
        cursor.execute("SELECT * FROM notices ORDER BY created_at DESC")
        notices = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify({'notices': notices})
        
    elif request.method == 'POST':
        # Create new notice
        data = request.json
        title = data.get('title')
        message = data.get('message')
        
        if not title or not message:
            conn.close()
            return jsonify({'status': 'error', 'message': 'Title and message required'}), 400
            
        cursor.execute("INSERT INTO notices (title, message) VALUES (?, ?)", (title, message))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Notice posted'})

@app.route('/api/admin/notices/<int:notice_id>', methods=['DELETE'])
def api_delete_notice(notice_id):
    """Deactivate a notice"""
    conn = get_portal_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE notices SET active = 0 WHERE id = ?", (notice_id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'message': 'Notice deleted'})


@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'status': 'success'})

@app.route('/api/me')
def api_me():
    if 'student_id' not in session:
        return jsonify({'user': None})
    
    conn = get_library_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE enrollment_no = ?", (session['student_id'],))
    student = cursor.fetchone()
    conn.close()
    
    if student:
        # Determine if Pass Out
        student_year = student['year'] if student['year'] else '1st'
        is_pass_out = False
        # Normalize year string for pass out detection
        if student_year.strip().lower() in ['pass out', 'passout', 'passed out', 'alumni', 'graduate']:
            student_year = 'Pass Out'
            is_pass_out = True
        
        # Fetch User Settings Override
        conn_portal = get_portal_db()
        cursor_p = conn_portal.cursor()
        cursor_p.execute("SELECT * FROM user_settings WHERE enrollment_no = ?", (session['student_id'],))
        settings = cursor_p.fetchone()
        conn_portal.close()
        
        # Default Email logic
        default_email = f"{student['name'].replace(' ', '.').lower()}@gpa.edu"
        user_email = settings['email'] if settings and settings['email'] else dict(student).get('email', default_email)
        
        return jsonify({'user': {
            'name': student['name'],
            'enrollment_no': student['enrollment_no'],
            'department': student['department'],
            'year': student_year,
            'email': user_email,
            'phone': dict(student).get('phone', 'N/A'),
            'settings': {
                'libraryAlerts': bool(settings['library_alerts']) if settings else False,
                'loanReminders': bool(settings['loan_reminders']) if settings else True,
                'theme': settings['theme'] if settings else 'light',
                'language': settings['language'] if settings else 'English',
                'dataConsent': bool(settings['data_consent']) if settings else True
            },
            'privileges': {
                 'max_books': 5,
                 'loan_duration': '7 Days',
                 'renewal_limit': '2 Renewals per book'
            },
            'account_info': {
                'password_last_changed': 'Recently'
            },
            'can_request': not is_pass_out
        }})
    return jsonify({'user': None})

@app.route('/api/user-policies')
def api_user_policies():
    """Fetch user specific policies and account info"""
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    return jsonify({
        'policies': {
            'max_books': 5,
            'loan_duration': '7 Days',
            'renewal_limit': '2 Renewals per book',
            'password_last_changed': 'Recently'
        }
    })

@app.route('/api/alerts')
def api_alerts():
    """Lightweight check for overdue items and security alerts"""
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    enrollment = session['student_id']
    
    # 1. Check Security Alert (Highest Priority)
    conn_portal = get_portal_db()
    cursor_p = conn_portal.cursor()
    cursor_p.execute("SELECT is_first_login FROM student_auth WHERE enrollment_no = ?", (enrollment,))
    auth_record = cursor_p.fetchone()
    conn_portal.close()
    
    if auth_record and auth_record['is_first_login']:
        return jsonify({
            'has_alert': True,
            'type': 'security',
            'message': 'Action Required: Change Default Password',
            'action_link': '/settings', # Or prompt modal
            'count': 1
        })
    
    # 2. Check Overdue Items
    conn = get_library_db()
    cursor = conn.cursor()
    
    # Check for active borrows only - fast query
    cursor.execute("""
        SELECT b.title, br.due_date
        FROM borrow_records br
        JOIN books b ON br.book_id = b.book_id
        WHERE br.enrollment_no = ? AND br.status = 'borrowed'
    """, (enrollment,))
    
    borrows = cursor.fetchall()
    conn.close()
    
    today = datetime.now()
    overdue_count = 0
    total_fine = 0
    overdue_titles = []
    
    for row in borrows:
        if row['due_date']:
            try:
                due_dt = datetime.strptime(row['due_date'], '%Y-%m-%d')
                delta = (due_dt - today).days
                if delta < 0:
                    overdue_count += 1
                    days_late = abs(delta)
                    total_fine += days_late * 10 # 10 INR per day
                    overdue_titles.append(row['title'])
            except:
                pass
                
    return jsonify({
        'has_alert': overdue_count > 0,
        'type': 'overdue',
        'count': overdue_count,
        'fine_estimate': total_fine,
        'items': overdue_titles
    })

@app.route('/api/services')
def api_services():
    """Fetch available digital resources and services"""
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # In a real app, these would be in a 'resources' table
    resources = [
        {
            'id': 1,
            'title': "IEEE Xplore Access",
            'type': "Research Database",
            'description': "Full access to IEEE journals, conferences, and standards.",
            'link': "#",
            'icon': "Globe"
        },
        {
            'id': 2,
            'title': "ProQuest E-Books",
            'type': "E-Book Platform",
            'description': "Access to over 150,000 academic e-books.",
            'link': "#",
            'icon': "Book"
        },
        {
            'id': 3,
            'title': "JSTOR Archive",
            'type': "Journal Archive",
            'description': "Academic journal archive for humanities and sciences.",
            'link': "#",
            'icon': "Archive"
        }
    ]
    
    return jsonify({'resources': resources})

# --- Dashboard Data Aggregation ---

@app.route('/api/dashboard')
def api_dashboard():
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    enrollment = session['student_id']
    
    # 1. Fetch Core Data (Read-Only)
    conn = get_library_db()
    cursor = conn.cursor()
    
    # Active Loans
    cursor.execute("""
        SELECT b.title, b.author, br.borrow_date, br.due_date, br.book_id
        FROM borrow_records br
        JOIN books b ON br.book_id = b.book_id
        WHERE br.enrollment_no = ? AND br.status = 'borrowed'
        ORDER BY br.due_date ASC
    """, (enrollment,))
    raw_borrows = cursor.fetchall()
    
    # History
    cursor.execute("""
        SELECT b.title, b.author, b.category, br.borrow_date, br.return_date, br.status
        FROM borrow_records br
        JOIN books b ON br.book_id = b.book_id
        WHERE br.enrollment_no = ? AND br.status = 'returned'
        ORDER BY br.return_date DESC
        LIMIT 50
    """, (enrollment,))
    raw_history = cursor.fetchall()
    
    conn.close()
    
    # 2. Process Business Logic (Fines/Alerts)
    borrows = []
    notifications = []
    
    # High Priority Auth Alert
    conn_portal = get_portal_db()
    cursor_p = conn_portal.cursor()
    cursor_p.execute("SELECT is_first_login FROM student_auth WHERE enrollment_no = ?", (enrollment,))
    auth_record = cursor_p.fetchone()
    conn_portal.close()
    
    if auth_record and auth_record['is_first_login']:
         notifications.append({
            'type': 'danger',
            'title': 'Security Alert',
            'msg': "You are using the default password. Please change it immediately."
        })

    today = datetime.now().date()
    
    for row in raw_borrows:
        item = dict(row)
        if item['due_date']:
            try:
                due_d = _parse_date_any(item['due_date'])
                if not due_d:
                    raise ValueError('Unparseable due_date')

                # Normalize outgoing date format for frontend
                item['due_date'] = due_d.isoformat()
                item['borrow_date'] = _to_iso_date(item.get('borrow_date'))

                delta = (due_d - today).days
                
                # Logic: Green (3+), Yellow (1-2), Red (<0)
                if delta < 0:
                    item['status'] = 'overdue'
                    overdue_days = abs(delta)
                    item['days_msg'] = f"Overdue by {overdue_days} days"
                    item['fine'] = overdue_days * 5 # ₹5 per day per logic in create_demo_data
                    notifications.append({
                        'type': 'danger',
                        'msg': f"'{item['title']}' is OVERDUE! Fine: ₹{item['fine']}"
                    })
                elif delta <= 2:
                    item['status'] = 'warning'
                    item['days_msg'] = f"Due in {delta} days"
                    notifications.append({
                        'type': 'warning',
                        'msg': f"'{item['title']}' is due soon ({delta} days)."
                    })
                else:
                    item['status'] = 'safe'
                    item['days_msg'] = f"{delta} days left"
            except:
                item['status'] = 'unknown'
                item['days_msg'] = '-'
        borrows.append(item)

    # 3. Fetch Sandbox Data (Requests Status)
    conn_portal = get_portal_db()
    cursor_p = conn_portal.cursor()
    cursor_p.execute("SELECT * FROM requests WHERE enrollment_no = ? ORDER BY created_at DESC LIMIT 5", (enrollment,))
    requests = [dict(row) for row in cursor_p.fetchall()]
    conn_portal.close()

    # 4. Analytics & Gamification (Computed on Read-Only Data)
    stats = {
        'total_books': len(raw_history) + len(borrows),
        'total_fines': sum([10 for x in borrows if x.get('status') == 'overdue']), # Estimated current fines
        'fav_category': 'General',
        'categories': {}
    }
    
    # Category Dist
    cat_count = {}
    for book in raw_history:
        cat = book['category'] or 'Uncategorized'
        cat_count[cat] = cat_count.get(cat, 0) + 1
    
    stats['categories'] = cat_count
    if cat_count:
        stats['fav_category'] = max(cat_count, key=cat_count.get)
        
    # Badges Logic
    badges = []
    if stats['total_books'] >= 5:
        badges.append({'id': 'bookworm', 'label': 'Bookworm', 'icon': '🐛', 'color': 'bg-emerald-100 text-emerald-700'})
    if stats['total_books'] >= 10:
        badges.append({'id': 'scholar', 'label': 'Scholar', 'icon': '🎓', 'color': 'bg-indigo-100 text-indigo-700'})
    
    # Check for overdue history
    has_overdues = any(x['status'] == 'overdue' for x in raw_history) # raw_history needs status mapping
    if not has_overdues and stats['total_books'] > 2:
        badges.append({'id': 'clean_sheet', 'label': 'Clean Sheet', 'icon': '🛡️', 'color': 'bg-blue-100 text-blue-700'})

    # 4. Library Notices (Active Broadcasts)
    conn_portal = get_portal_db()
    cursor_p = conn_portal.cursor()
    cursor_p.execute("SELECT id, title, message as content, created_at as date FROM notices WHERE active = 1 ORDER BY created_at DESC")
    notices = [dict(row) for row in cursor_p.fetchall()]
    conn_portal.close()

    # Normalize dates for frontend JS Date parsing
    for n in notices:
        n['date'] = _to_iso_date(n.get('date'))

    history = [dict(row) for row in raw_history]
    for h in history:
        h['borrow_date'] = _to_iso_date(h.get('borrow_date'))
        h['return_date'] = _to_iso_date(h.get('return_date'))

    return jsonify({
        'borrows': borrows,
        'history': history,
        'notices': notices,
        'notifications': notifications,
        'recent_requests': requests,
        'analytics': {
            'stats': stats,
            'badges': badges
        }
    })

# --- Write Endpoints (Sandbox Only) ---

@app.route('/api/books/<book_id>', methods=['GET'])
def get_book_details(book_id):
    """Fetch details for a specific book."""
    try:
        conn = get_library_db()
        cursor = conn.cursor()
        
        # Fetch book details
        cursor.execute("SELECT * FROM books WHERE book_id = ?", (str(book_id),))
        book = cursor.fetchone()
        
        if not book:
            conn.close()
            return jsonify({'error': 'Book not found'}), 404
            
        book_data = dict(book)
        
        # Calculate availability
        cursor.execute("SELECT COUNT(*) FROM borrow_records WHERE book_id = ? AND status = 'borrowed'", (str(book_id),))
        borrowed_count = cursor.fetchone()[0]
        book_data['available_copies'] = book_data['total_copies'] - borrowed_count
        
        # Fetch Ratings
        portal_conn = get_portal_db()
        portal_cursor = portal_conn.cursor()
        
        # Check if current user is on waitlist & Get their rating
        user_rating = 0
        
        if 'student_id' in session:
            portal_cursor.execute(
                "SELECT id FROM book_waitlist WHERE enrollment_no = ? AND book_id = ? AND notified = 0",
                (session['student_id'], str(book_id))
            )
            waitlist_entry = portal_cursor.fetchone()
            book_data['on_waitlist'] = waitlist_entry is not None
            
            portal_cursor.execute(
                "SELECT rating FROM book_ratings WHERE enrollment_no = ? AND book_id = ?",
                (session['student_id'], str(book_id))
            )
            rating_entry = portal_cursor.fetchone()
            if rating_entry:
                user_rating = rating_entry['rating']
        else:
            book_data['on_waitlist'] = False
            
        # Get Average Rating
        portal_cursor.execute("SELECT AVG(rating), COUNT(rating) FROM book_ratings WHERE book_id = ?", (str(book_id),))
        rating_stats = portal_cursor.fetchone()
        
        book_data['rating_avg'] = round(rating_stats[0], 1) if rating_stats[0] else None
        book_data['rating_count'] = rating_stats[1] if rating_stats[1] else 0
        book_data['user_rating'] = user_rating
        
        portal_conn.close()
        conn.close()
        return jsonify(book_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/books/<book_id>/notify', methods=['POST'])
def add_to_waitlist(book_id):
    """Add student to waitlist for out-of-stock book."""
    if 'student_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        enrollment_no = session['student_id']
        
        # Get book details
        library_conn = get_library_db()
        library_cursor = library_conn.cursor()
        library_cursor.execute("SELECT title, total_copies FROM books WHERE book_id = ?", (book_id,))
        book = library_cursor.fetchone()
        
        if not book:
            library_conn.close()
            return jsonify({'error': 'Book not found'}), 404
        
        book_title = book['title']
        
        # Check availability
        library_cursor.execute("SELECT COUNT(*) FROM borrow_records WHERE book_id = ? AND status = 'borrowed'", (book_id,))
        borrowed_count = library_cursor.fetchone()[0]
        available = book['total_copies'] - borrowed_count
        library_conn.close()
        
        if available > 0:
            return jsonify({'error': 'Book is currently available'}), 400
        
        # Add to waitlist
        portal_conn = get_portal_db()
        portal_cursor = portal_conn.cursor()
        
        try:
            portal_cursor.execute(
                "INSERT INTO book_waitlist (enrollment_no, book_id, book_title) VALUES (?, ?, ?)",
                (enrollment_no, book_id, book_title)
            )
            portal_conn.commit()
            portal_conn.close()
            
            return jsonify({
                'success': True,
                'message': 'You will be notified when this book becomes available'
            })
        except sqlite3.IntegrityError:
            portal_conn.close()
            return jsonify({'error': 'You are already on the waitlist for this book'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/books/<book_id>/notify', methods=['DELETE'])
def remove_from_waitlist(book_id):
    """Remove student from waitlist."""
    if 'student_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        enrollment_no = session['student_id']
        
        portal_conn = get_portal_db()
        portal_cursor = portal_conn.cursor()
        
        portal_cursor.execute(
            "DELETE FROM book_waitlist WHERE enrollment_no = ? AND book_id = ? AND notified = 0",
            (enrollment_no, book_id)
        )
        portal_conn.commit()
        
        if portal_cursor.rowcount == 0:
            portal_conn.close()
            return jsonify({'error': 'Not on waitlist for this book'}), 404
        
        portal_conn.close()
        return jsonify({
            'success': True,
            'message': 'Removed from waitlist'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_email_template(header_title, user_name, main_text, details_dict=None, theme='blue', footer_note=None):
    """
    Generates a unified responsive HTML email.
    theme: 'blue' (Info/Receipt), 'green' (Success/Approved), 'orange' (Warning/Rejected)
    """
    colors = {
        'blue': {'bg': '#0F3460', 'box_bg': '#f0f4f8', 'box_border': '#d9e2ec', 'accent': '#0F3460'},
        'green': {'bg': '#28a745', 'box_bg': '#f0fdf4', 'box_border': '#bbf7d0', 'accent': '#15803d'},
        'orange': {'bg': '#dc3545', 'box_bg': '#fff5f5', 'box_border': '#feb2b2', 'accent': '#c53030'}
    }
    c = colors.get(theme, colors['blue'])
    
    # Build Details Table
    details_html = ""
    if details_dict:
        rows = ""
        for label, value in details_dict.items():
            rows += f"""
            <tr>
                <td style="padding: 8px 0; vertical-align: top; width: 35%; color: #666; font-weight: bold;">{label}:</td>
                <td style="padding: 8px 0; vertical-align: top; color: #333; font-weight: 500;">{value}</td>
            </tr>"""
        details_html = f"""
        <div style="background-color: {c['box_bg']}; border: 1px solid {c['box_border']}; border-radius: 8px; padding: 20px; margin: 25px 0;">
            <table style="width: 100%; border-collapse: collapse;">
                {rows}
            </table>
            {f'<p style="font-size: 13px; color: #666; font-style: italic; margin-top: 15px; border-top: 1px solid {c["box_border"]}; padding-top: 10px;">{footer_note}</p>' if footer_note else ''}
        </div>"""

    return f"""<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: 'Helvetica', 'Arial', sans-serif; margin: 0; padding: 0; background-color: #f4f4f4; }}
        .container {{ max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
        .header {{ background-color: {c['bg']}; color: #ffffff; padding: 30px 20px; text-align: center; }}
        .content {{ padding: 40px 30px; color: #333333; line-height: 1.6; }}
        .footer {{ text-align: center; font-size: 12px; color: #888888; padding: 20px; background-color: #f8f9fa; border-top: 1px solid #e1e1e1; }}
    </style>
</head>
<body>
    <div style="padding: 20px 0;">
        <div class="container">
            <div class="header">
                <h2 style="margin:0; font-size: 24px;">{header_title}</h2>
            </div>
            <div class="content">
                <p style="font-size: 16px;">Dear <strong>{user_name}</strong>,</p>
                <p style="font-size: 16px;">{main_text}</p>
                
                {details_html}
                
                <p style="margin-top: 30px;">Best regards,<br><strong>GPA Library Team</strong></p>
            </div>
            <div class="footer">
                &copy; {datetime.now().year} Government Polytechnic Awasari (Kh).<br>
                Automated System Message.
            </div>
        </div>
    </div>
</body>
</html>"""

@app.route('/api/request', methods=['POST'])
def api_submit_request():
    if 'student_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    # Restrict Pass Out students from submitting requests
    conn_lib = get_library_db()
    cursor_lib = conn_lib.cursor()
    cursor_lib.execute("SELECT year FROM students WHERE enrollment_no = ?", (session['student_id'],))
    student = cursor_lib.fetchone()
    conn_lib.close()
    student_year = student['year'] if student and student['year'] else ''
    if student_year.strip().lower() in ['pass out', 'passout', 'passed out', 'alumni', 'graduate']:
        return jsonify({'error': 'Requests are not allowed for Pass Out students.'}), 403

    data = request.json
    req_type = data.get('type') # 'profile_update', 'renewal'
    details = data.get('details') # e.g., "Change email to x@y.com"

    if not req_type or not details:
        return jsonify({'error': 'Missing data'}), 400

    try:
        conn = get_portal_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO requests (enrollment_no, request_type, details) VALUES (?, ?, ?)",
                       (session['student_id'], req_type, json.dumps(details)))
        conn.commit()
        conn.close()
        
        # Send Email Notification
        # Send Email Notification
        conn_lib = get_library_db()
        cursor_lib = conn_lib.cursor()
        
        # Fetch Name
        cursor_lib.execute("SELECT name FROM students WHERE enrollment_no = ?", (session['student_id'],))
        student = cursor_lib.fetchone()
        student_name = student['name'].split()[0] if student and student['name'] else "Student"
        
        # Helper to parse book title from string details
        def get_title_from_details(details_obj):
            t = req_type
            if isinstance(details_obj, dict):
                 if 'title' in details_obj: return details_obj['title']
                 if 'book_id' in details_obj:
                     try:
                        cursor_lib.execute("SELECT title FROM books WHERE book_id = ?", (details_obj['book_id'],))
                        bd = cursor_lib.fetchone()
                        if bd: return bd['title']
                     except: pass
            elif isinstance(details_obj, str):
                if "Request for book: " in details_obj:
                    import re
                    match = re.search(r"Request for book: (.*?) \(ID:", details_obj)
                    if match: return match.group(1)
                    return details_obj.replace("Request for book: ", "")
            return t

        # Prepare Email Content based on Type
        email_subject = ""
        header_title = "Request Received"
        main_text = ""
        details_dict = {}
        theme = 'blue'
        
        current_date_str = datetime.now().strftime('%d %b %Y, %I:%M %p')

        if req_type == 'book_request':
            b_title = get_title_from_details(details)
            email_subject = f"Request Received: {b_title}"
            header_title = "Reservation Received"
            main_text = f"We have received your request to reserve <strong>{b_title}</strong>."
            details_dict = {
                'Book Title': b_title,
                'Request Date': current_date_str,
                'Status': 'Pending Approval'
            }
            
        elif req_type == 'renewal':
            b_title = get_title_from_details(details)
            email_subject = f"Renewal Request: {b_title}"
            header_title = "Renewal Request"
            main_text = f"We have received your request to renew <strong>{b_title}</strong>."
            details_dict = {
                'Book Title': b_title,
                'Request Date': current_date_str,
                'Status': 'Pending Approval'
            }
            
        elif req_type == 'profile_update':
            email_subject = "Profile Update Request"
            header_title = "Profile Update"
            main_text = "We have received your request to update your library profile."
            details_summary = json.dumps(details) if isinstance(details, dict) else str(details)
            details_dict = {
                'Requested Changes': details_summary,
                'Request Date': current_date_str
            }
            
        else:
            # Generic fallback
            email_subject = f"Request Received: {req_type}"
            main_text = f"We have received your {req_type} request."
            details_dict = {'Details': str(details)}

        conn_lib.close()

        email_body = generate_email_template(
            header_title=header_title,
            user_name=student_name,
            main_text=main_text,
            details_dict=details_dict,
            theme='blue',
            footer_note="You will be notified once the librarian reviews your request."
        )
        
        trigger_notification_email(session['student_id'], email_subject, email_body)
        
        return jsonify({'status': 'success', 'message': 'Request submitted to librarian'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/books')
def api_books():
    # Read-Only Catalogue
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    conn = get_library_db()
    cursor = conn.cursor()
    
    sql = "SELECT book_id, title, author, category, total_copies, available_copies FROM books WHERE 1=1"
    params = []
    
    if query:
        sql += " AND (title LIKE ? OR author LIKE ?)"
        params.extend([f'%{query}%', f'%{query}%'])
    if category and category != 'All':
        sql += " AND category = ?"
        params.append(category)
        
    sql += " ORDER BY title LIMIT 50"
    
    cursor.execute(sql, params)
    books = [dict(row) for row in cursor.fetchall()]
    
    # Recalculate available_copies in real-time for data consistency
    for book in books:
        cursor.execute("SELECT COUNT(*) FROM borrow_records WHERE book_id = ? AND status = 'borrowed'", (book['book_id'],))
        borrowed_count = cursor.fetchone()[0]
        book['available_copies'] = book['total_copies'] - borrowed_count
    
    # Get distinct categories for filter
    cursor.execute("SELECT DISTINCT category FROM books WHERE category IS NOT NULL ORDER BY category")
    categories = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return jsonify({'books': books, 'categories': categories})

# --- Admin/Librarian API Endpoints ---

@app.route('/api/admin/all-requests')
def api_admin_all_requests():
    """Fetch all pending requests for librarian management"""
    try:
        conn = get_portal_db()
        cursor = conn.cursor()

        # Fetch general requests (profile_update, renewal, book_reservation, student_registration, etc.)
        pk = _requests_pk_column(conn)
        cursor.execute(f"""
            SELECT {pk} as req_id, enrollment_no, request_type, details, status, created_at
            FROM requests
            WHERE status = 'pending'
            ORDER BY created_at DESC
        """)
        general_requests = []
        for row in cursor.fetchall():
            req = dict(row)
            # Try to parse JSON details
            try:
                req['details'] = json.loads(req['details']) if req['details'] else {}
            except Exception:
                req['details'] = {'raw': req.get('details')}
            general_requests.append(req)

        # Fetch deletion requests
        cursor.execute("""
            SELECT id, student_id, reason, status, timestamp
            FROM deletion_requests
            WHERE status = 'pending'
            ORDER BY timestamp DESC
        """)
        deletion_requests = [dict(row) for row in cursor.fetchall()]

        conn.close()

        # Enrich with student names from library DB.
        # IMPORTANT: In deployed environments, the portal DB may exist even when the library DB
        # (or students table) is missing/unmigrated. Don't fail the whole endpoint in that case.
        try:
            conn_lib = get_library_db()
            cursor_lib = conn_lib.cursor()

            # Enrich general requests with student names
            for req in general_requests:
                enrollment_no = str(req.get('enrollment_no', '')).strip()
                cursor_lib.execute("SELECT name FROM students WHERE enrollment_no = ?", (enrollment_no,))
                student = cursor_lib.fetchone()
                if not student:
                    # If this is a registration request, use the submitted name
                    if req.get('request_type') == 'student_registration':
                        try:
                            d = req.get('details') or {}
                            req['student_name'] = d.get('name') or 'New Student'
                        except Exception:
                            req['student_name'] = 'New Student'
                    else:
                        req['student_name'] = 'Unknown'
                else:
                    try:
                        req['student_name'] = student['name']
                    except Exception:
                        # Last-resort fallback
                        req['student_name'] = dict(student).get('name', 'Unknown')

            # Enrich deletion requests with student names
            for req in deletion_requests:
                enrollment_no = str(req.get('student_id', '')).strip()
                cursor_lib.execute("SELECT name FROM students WHERE enrollment_no = ?", (enrollment_no,))
                student = cursor_lib.fetchone()
                if not student:
                    req['student_name'] = 'Unknown'
                else:
                    try:
                        req['student_name'] = student['name']
                    except Exception:
                        req['student_name'] = dict(student).get('name', 'Unknown')

            conn_lib.close()
        except Exception:
            # Fallback: ensure required fields exist
            for req in general_requests:
                if req.get('request_type') == 'student_registration':
                    try:
                        d = req.get('details') or {}
                        req['student_name'] = d.get('name') or 'New Student'
                    except Exception:
                        req['student_name'] = 'New Student'
                else:
                    req['student_name'] = req.get('student_name') or 'Unknown'

            for req in deletion_requests:
                req['student_name'] = req.get('student_name') or 'Unknown'

        # Get rejected count from portal DB
        conn2 = get_portal_db()
        cursor2 = conn2.cursor()
        cursor2.execute("SELECT COUNT(*) as count FROM requests WHERE status = 'rejected'")
        rejected_count = cursor2.fetchone()['count']

        # Get deletion counts by status
        cursor2.execute("SELECT status, COUNT(*) as count FROM deletion_requests GROUP BY status")
        deletion_counts = {row['status']: row['count'] for row in cursor2.fetchall()}
        conn2.close()

        return jsonify({
            'requests': general_requests,
            'deletion_requests': deletion_requests,
            'rejected_count': rejected_count,
            'deletion_counts': deletion_counts,
            'counts': {
                'total': len(general_requests) + len(deletion_requests),
                'requests': len(general_requests),
                'deletions': len(deletion_requests)
            }
        })
    except Exception as e:
        error_id = _log_portal_exception('api_admin_all_requests', e)
        return jsonify({'status': 'error', 'message': 'Failed to load requests', 'error_id': error_id}), 500

@app.route('/api/admin/request-history')
def api_admin_request_history():
    """Fetch processed (approved/rejected) requests with search and filter"""
    conn = get_portal_db()
    cursor = conn.cursor()
    
    # Get filter params
    q = request.args.get('q', '').strip()
    days = request.args.get('days')
    
    pk = _requests_pk_column(conn)
    # Base query
    query = f"""
        SELECT {pk} as req_id, enrollment_no, request_type, details, status, created_at
        FROM requests
        WHERE status IN ('approved', 'rejected')
    """
    params = []
    
    # Date filter (backend-agnostic)
    if days and days.isdigit():
        cutoff = datetime.now() - timedelta(days=int(days))
        query += " AND created_at >= ?"
        params.append(cutoff.strftime('%Y-%m-%d %H:%M:%S'))
    
    query += " ORDER BY created_at DESC LIMIT 100"
    
    cursor.execute(query, params)
    processed_requests = []
    for row in cursor.fetchall():
        req = dict(row)
        try:
            req['details'] = json.loads(req['details']) if req['details'] else {}
        except:
            req['details'] = {'raw': req['details']}
        processed_requests.append(req)
    
    conn.close()
    
    # Get student names and filter by search query.
    # If the library DB isn't available in deployed mode, do not fail the endpoint.
    filtered_requests = []

    cursor_lib = None
    conn_lib = None
    try:
        conn_lib = get_library_db()
        cursor_lib = conn_lib.cursor()
    except Exception:
        cursor_lib = None

    for req in processed_requests:
        student_name = None
        if cursor_lib is not None:
            try:
                cursor_lib.execute("SELECT name FROM students WHERE enrollment_no = ?", (req['enrollment_no'],))
                student = cursor_lib.fetchone()
                if student:
                    try:
                        student_name = student['name']
                    except Exception:
                        student_name = dict(student).get('name')
            except Exception:
                student_name = None

        if not student_name:
            # For registration requests, show the submitted name
            if req.get('request_type') == 'student_registration':
                try:
                    d = req.get('details') or {}
                    student_name = d.get('name') or 'New Student'
                except Exception:
                    student_name = 'New Student'
            else:
                student_name = 'Unknown'

        req['student_name'] = student_name

        # Apply search filter (if search query exists)
        if q:
            search_str = q.lower()
            if (search_str in str(req.get('enrollment_no', '')).lower() or
                search_str in str(student_name).lower() or
                search_str in str(req.get('request_type', '')).lower()):
                filtered_requests.append(req)
        else:
            filtered_requests.append(req)

    try:
        if conn_lib is not None:
            conn_lib.close()
    except Exception:
        pass
    
    conn_lib.close()
    
    # Count by status (of filtered results)
    approved_count = len([r for r in filtered_requests if r['status'] == 'approved'])
    rejected_count = len([r for r in filtered_requests if r['status'] == 'rejected'])
    
    return jsonify({
        'history': filtered_requests,
        'counts': {
            'approved': approved_count,
            'rejected': rejected_count,
            'total': len(filtered_requests)
        }
    })

@app.route('/api/admin/deletion-history')
def api_admin_deletion_history():
    """Fetch processed deletion requests with search and filter"""
    conn = get_portal_db()
    cursor = conn.cursor()
    
    # Get filter params
    q = request.args.get('q', '').strip()
    days = request.args.get('days')
    
    # Base query
    query = """
        SELECT id, student_id, reason, status, timestamp
        FROM deletion_requests
        WHERE status IN ('approved', 'rejected')
    """
    params = []
    
    # Date filter (backend-agnostic)
    if days and days.isdigit():
        cutoff = datetime.now() - timedelta(days=int(days))
        query += " AND timestamp >= ?"
        params.append(cutoff.strftime('%Y-%m-%d %H:%M:%S'))
    
    query += " ORDER BY timestamp DESC LIMIT 100"
    
    cursor.execute(query, params)
    processed_deletions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # Get student names and filter
    conn_lib = get_library_db()
    cursor_lib = conn_lib.cursor()
    
    filtered_deletions = []
    
    for req in processed_deletions:
        cursor_lib.execute("SELECT name FROM students WHERE enrollment_no = ?", (req['student_id'],))
        student = cursor_lib.fetchone()
        student_name = student['name'] if student else 'Deleted Account'
        req['student_name'] = student_name
        
        # Apply search filter
        if q:
            search_str = q.lower()
            if (search_str in req['student_id'].lower() or 
                search_str in student_name.lower()):
                filtered_deletions.append(req)
        else:
            filtered_deletions.append(req)
    
    conn_lib.close()
    
    # Count by status (of filtered results)
    approved_count = len([r for r in filtered_deletions if r['status'] == 'approved'])
    rejected_count = len([r for r in filtered_deletions if r['status'] == 'rejected'])
    
    return jsonify({
        'history': filtered_deletions,
        'counts': {
            'approved': approved_count,
            'rejected': rejected_count,
            'total': len(filtered_deletions)
        }
    })

@app.route('/api/admin/requests/<int:req_id>/approve', methods=['POST'])
def api_admin_approve_request(req_id):
    """Approve a general request"""
    conn = get_portal_db()
    cursor = conn.cursor()
    
    pk = _requests_pk_column(conn)
    # Get the request details
    cursor.execute(f"SELECT * FROM requests WHERE {pk} = ?", (req_id,))
    req = cursor.fetchone()
    
    if not req:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Request not found'}), 404
    
    # Handle special request types
    if req['request_type'] == 'student_registration':
        # Approving a registration inserts into the library DB
        try:
            details = json.loads(req['details']) if req['details'] else {}
        except Exception:
            details = {}

        enrollment_no = _normalize_enrollment(req['enrollment_no'])
        name = _safe_str(details.get('name'))
        year = _safe_str(details.get('year'))
        department = _safe_str(details.get('department'))
        phone = _safe_str(details.get('phone'))
        email = _safe_str(details.get('email'))

        if not enrollment_no or not name:
            conn.close()
            return jsonify({'status': 'error', 'message': 'Invalid registration details.'}), 400

        conn_lib = get_library_db()
        cursor_lib = conn_lib.cursor()
        cursor_lib.execute("SELECT enrollment_no FROM students WHERE enrollment_no = ?", (enrollment_no,))
        exists = cursor_lib.fetchone()
        if exists:
            conn_lib.close()
            conn.close()
            return jsonify({'status': 'error', 'message': 'Student already exists in library.'}), 409

        # Insert into students
        cursor_lib.execute(
            """
            INSERT INTO students (enrollment_no, name, email, phone, department, year)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (enrollment_no, name, email, phone, department, year)
        )
        conn_lib.commit()
        conn_lib.close()

        # Ensure portal user settings has email so notifications can be delivered
        try:
            cursor.execute(
                """
                INSERT INTO user_settings (enrollment_no, email)
                VALUES (?, ?)
                ON CONFLICT(enrollment_no) DO UPDATE SET email=excluded.email
                """,
                (enrollment_no, email)
            )
        except Exception:
            pass

        # Update status to approved
        cursor.execute(f"UPDATE requests SET status = 'approved' WHERE {pk} = ?", (req_id,))

        # Notify student (stored notification for when they login)
        cursor.execute(
            """
            INSERT INTO user_notifications (enrollment_no, type, title, message, link, created_at)
            VALUES (?, 'request_update', 'Registration Approved', ?, '/login', ?)
            """,
            (enrollment_no, "Your library registration has been approved. You can now login.", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        )

        # Email (best-effort)
        try:
            email_body = generate_email_template(
                header_title="Registration Approved",
                user_name=name.split()[0] if name else "Student",
                main_text="Your library registration request has been approved. You can now login to the portal.",
                details_dict={
                    'Enrollment No': enrollment_no,
                    'Status': 'Approved',
                    'Date': datetime.now().strftime('%d %b %Y')
                },
                theme='green',
                footer_note="Welcome to the library portal."
            )
            trigger_notification_email(enrollment_no, "✅ Registration Approved", email_body)
        except Exception:
            pass

        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Registration approved and student added to library.'})

    # Update status to approved
    cursor.execute(f"UPDATE requests SET status = 'approved' WHERE {pk} = ?", (req_id,))
    
    # NOTIFICATION TRIGGER: Notify student
    # Parse details to get book name
    message = f"Your {req['request_type']} request has been approved."
    book_title = req['request_type']
    
    try:
        details = json.loads(req['details']) if req['details'] else {}
        
        # Try to find title in details first
        if 'title' in details:
            book_title = details['title']
            message = f"Your request for '{book_title}' has been approved."
        
        # If not, look update from library DB using book_id
        elif 'book_id' in details:
            try:
                conn_lib = get_library_db()
                cursor_lib = conn_lib.cursor()
                cursor_lib.execute("SELECT title FROM books WHERE book_id = ?", (details['book_id'],))
                book_data = cursor_lib.fetchone()
                conn_lib.close()
                
                if book_data:
                    book_title = book_data['title']
                    message = f"Your request for '{book_title}' has been approved."
            except:
                pass
        
        # Handle string details (e.g. "Request for book: Title (ID: X)")
        if isinstance(details, str):
            try:
                if "Request for book: " in details:
                    import re
                    match = re.search(r"Request for book: (.*?) \(ID:", details)
                    if match:
                        book_title = match.group(1)
                    else:
                        book_title = details.replace("Request for book: ", "")
                    message = f"Your request for '{book_title}' has been approved."
            except:
                pass
    except:
        pass

    cursor.execute("""
        INSERT INTO user_notifications (enrollment_no, type, title, message, link, created_at)
        VALUES (?, 'request_update', 'Request Approved', ?, '/requests', ?)
    """, (req['enrollment_no'], message, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    
    # Email Trigger
    conn_lib = get_library_db()
    cursor_lib = conn_lib.cursor()
    cursor_lib.execute("SELECT name FROM students WHERE enrollment_no = ?", (req['enrollment_no'],))
    student_record = cursor_lib.fetchone()
    conn_lib.close()
    
    student_name = student_record['name'].split()[0] if student_record and student_record['name'] else "Student"
    
    # Email Construction
    email_subject = "Request Approved"
    header_title = "Request Approved"
    main_text = f"Your request has been approved."
    details_dict = {}
    footer_note = "Thank you for using the GPA Library System."

    if req['request_type'] == 'book_request':
        email_subject = f"✅ Ready for Pickup: {book_title}"
        header_title = "Request Approved"
        main_text = f"Great news! Your request to reserve <strong>{book_title}</strong> has been approved. It is ready for collection."
        deadline = (datetime.now() + timedelta(days=2)).strftime('%d %b %Y')
        details_dict = {
            'Location': 'Main Library Desk',
            'Bring': 'Student ID Card',
            'Deadline': deadline
        }
        footer_note = "If not collected by the deadline, the reservation will be cancelled."

    elif req['request_type'] == 'renewal':
        email_subject = f"✅ Renewal Approved: {book_title}"
        header_title = "Renewal Approved"
        main_text = f"Your request to renew <strong>{book_title}</strong> was successful."
        new_due = (datetime.now() + timedelta(days=15)).strftime('%d %b %Y')
        details_dict = {
            'Item': book_title,
            'New Due Date': new_due
        }
        footer_note = "Please return the book by the new date to avoid fines."

    elif req['request_type'] == 'profile_update':
        email_subject = "✅ Profile Updated"
        header_title = "Update Successful"
        main_text = "Your profile update request has been processed and applied to your account."
        details_dict = {
            'Status': 'Changes Applied',
            'Date': datetime.now().strftime('%d %b %Y')
        }

    elif req['request_type'] == 'password_reset':
        # Execute Reset Logic
        try:
             # Reset to Enrollment Number using EXISTING cursor (Fixes Timeout)
             default_hash = generate_password_hash(req['enrollment_no'])
             cursor.execute("UPDATE student_auth SET password = ?, is_first_login = 1 WHERE enrollment_no = ?", (default_hash, req['enrollment_no']))
        except Exception as e:
             return jsonify({'error': f"Failed to reset password: {str(e)}"}), 500

        email_subject = "✅ Password Reset Successful"
        header_title = "Password Reset"
        main_text = "Your password has been successfully reset by the librarian."
        details_dict = {
            'New Password': 'Your Enrollment Number',
            'Action Required': 'Login & Set New Password'
        }
        footer_note = "Please change your password immediately after logging in."

    email_body = generate_email_template(
        header_title=header_title,
        user_name=student_name,
        main_text=main_text,
        details_dict=details_dict,
        theme='green',
        footer_note=footer_note
    )

    trigger_notification_email(req['enrollment_no'], email_subject, email_body)
    
    conn.commit()
    conn.close()
    
    # If it's a profile update, we could apply changes to main DB here
    # For now, just mark as approved (librarian can manually update if needed)
    
    return jsonify({'status': 'success', 'message': 'Request approved'})

@app.route('/api/admin/requests/<int:req_id>/reject', methods=['POST'])
def api_admin_reject_request(req_id):
    """Reject a general request"""
    conn = get_portal_db()
    cursor = conn.cursor()
    
    pk = _requests_pk_column(conn)
    cursor.execute(f"UPDATE requests SET status = 'rejected' WHERE {pk} = ?", (req_id,))
    
    # Get enrollment to notify
    cursor.execute(f"SELECT enrollment_no, request_type, details FROM requests WHERE {pk} = ?", (req_id,))
    req = cursor.fetchone()
    
    if req:
         # Parse details to get book name
         message = f"Your {req['request_type']} request was rejected."
         book_title = req['request_type']
         
         try:
            details = json.loads(req['details']) if req['details'] else {}
            
            if 'title' in details:
                book_title = details['title']
                message = f"Your request for '{book_title}' was rejected."
            elif 'book_id' in details:
                try:
                    conn_lib = get_library_db()
                    cursor_lib = conn_lib.cursor()
                    cursor_lib.execute("SELECT title FROM books WHERE book_id = ?", (details['book_id'],))
                    book_data = cursor_lib.fetchone()
                    conn_lib.close()
                    
                    if book_data:
                        book_title = book_data['title']
                        message = f"Your request for '{book_title}' was rejected."
                except:
                    pass
            
            # Handle string details
            if isinstance(details, str):
                try:
                    if "Request for book: " in details:
                        import re
                        match = re.search(r"Request for book: (.*?) \(ID:", details)
                        if match:
                            book_title = match.group(1)
                        else:
                            book_title = details.replace("Request for book: ", "")
                        message = f"Your request for '{book_title}' was rejected."
                except:
                    pass
         except:
             pass

         reject_link = '/requests'
         reject_title = 'Request Rejected'
         if req['request_type'] == 'student_registration':
             reject_link = '/login'
             reject_title = 'Registration Rejected'
             message = "Your library registration request was rejected. Please contact the librarian."

         cursor.execute("""
            INSERT INTO user_notifications (enrollment_no, type, title, message, link, created_at)
            VALUES (?, 'request_update', ?, ?, ?, ?)
        """, (req['enrollment_no'], reject_title, message, reject_link, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

         # Email Trigger
         conn_lib = get_library_db()
         cursor_lib = conn_lib.cursor()
         cursor_lib.execute("SELECT name FROM students WHERE enrollment_no = ?", (req['enrollment_no'],))
         student_record = cursor_lib.fetchone()
         conn_lib.close()
         student_name = student_record['name'].split()[0] if student_record and student_record['name'] else "Student"

         email_subject = f"Request Declined: {book_title}"
         main_text = f"We regret to inform you that your request regarding <strong>{book_title}</strong> could not be fulfilled at this time."
         
         if req['request_type'] == 'profile_update':
             email_subject = "Profile Update Declined"
             main_text = "Your request to update profile details was not approved."
             
         email_body = generate_email_template(
            header_title="Request Declined",
            user_name=student_name,
            main_text=main_text,
            details_dict=None,
            theme='orange',
            footer_note="For more information, please visit the library desk."
         )
         
         trigger_notification_email(req['enrollment_no'], email_subject, email_body)

    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'message': 'Request rejected'})

@app.route('/api/admin/deletion/<int:del_id>/approve', methods=['POST'])
def api_admin_approve_deletion(del_id):
    """Approve account deletion request"""
    conn = get_portal_db()
    cursor = conn.cursor()
    
    # Get deletion request
    cursor.execute("SELECT student_id FROM deletion_requests WHERE id = ?", (del_id,))
    req = cursor.fetchone()
    
    if not req:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Deletion request not found'}), 404
    
    student_id = req['student_id']
    
    # Update status
    cursor.execute("UPDATE deletion_requests SET status = 'approved' WHERE id = ?", (del_id,))
    
    # Also clean up auth record
    cursor.execute("DELETE FROM student_auth WHERE enrollment_no = ?", (student_id,))
    conn.commit()
    conn.close()
    
    # Note: Actual student deletion from main DB should be done via the main app
    # This just marks the request as approved
    
    return jsonify({
        'status': 'success', 
        'message': 'Deletion approved. Student auth removed.',
        'student_id': student_id
    })

@app.route('/api/admin/deletion/<int:del_id>/reject', methods=['POST'])
def api_admin_reject_deletion(del_id):
    """Reject account deletion request"""
    conn = get_portal_db()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE deletion_requests SET status = 'rejected' WHERE id = ?", (del_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'message': 'Deletion request rejected'})

@app.route('/api/admin/password-reset/<enrollment_no>', methods=['POST'])
def api_admin_reset_password(enrollment_no):
    """Reset student password to enrollment number"""
    conn = get_portal_db()
    cursor = conn.cursor()
    
    # Check if auth record exists
    cursor.execute("SELECT * FROM student_auth WHERE enrollment_no = ?", (enrollment_no,))
    auth = cursor.fetchone()
    
    # Hash the enrollment number for reset
    hashed_pw = generate_password_hash(enrollment_no)
    
    if auth:
        # Reset to enrollment number and mark as first login
        cursor.execute("""
            UPDATE student_auth 
            SET password = ?, is_first_login = 1, last_changed = CURRENT_TIMESTAMP
            WHERE enrollment_no = ?
        """, (hashed_pw, enrollment_no))
    else:
        # Create new auth record with default password
        cursor.execute("""
            INSERT INTO student_auth (enrollment_no, password, is_first_login)
            VALUES (?, ?, 1)
        """, (enrollment_no, hashed_pw))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'status': 'success', 
        'message': f'Password reset to enrollment number. Student will be prompted to change on next login.'
    })

@app.route('/api/admin/bulk-password-reset', methods=['POST'])
def api_admin_bulk_password_reset():
    """Reset passwords for all students in a year group or all students"""
    data = request.json
    year = data.get('year')  # '1st', '2nd', '3rd', or None for all
    
    try:
        # Get students from library.db
        conn_lib = get_library_db()
        cursor_lib = conn_lib.cursor()
        
        if year:
            cursor_lib.execute("SELECT enrollment_no FROM students WHERE year = ?", (year,))
        else:
            cursor_lib.execute("SELECT enrollment_no FROM students")
        
        students = cursor_lib.fetchall()
        conn_lib.close()
        
        if not students:
            return jsonify({'status': 'error', 'message': 'No students found'}), 404
        
        # Reset each student's password in portal.db
        conn_portal = get_portal_db()
        cursor_portal = conn_portal.cursor()
        
        reset_count = 0
        for student in students:
            enrollment_no = student['enrollment_no']
            hashed_pw = generate_password_hash(enrollment_no)
            
            # Check if auth record exists
            cursor_portal.execute("SELECT * FROM student_auth WHERE enrollment_no = ?", (enrollment_no,))
            auth = cursor_portal.fetchone()
            
            if auth:
                cursor_portal.execute("""
                    UPDATE student_auth 
                    SET password = ?, is_first_login = 1, last_changed = CURRENT_TIMESTAMP
                    WHERE enrollment_no = ?
                """, (hashed_pw, enrollment_no))
            else:
                cursor_portal.execute("""
                    INSERT INTO student_auth (enrollment_no, password, is_first_login)
                    VALUES (?, ?, 1)
                """, (enrollment_no, hashed_pw))
            
            reset_count += 1
        
        conn_portal.commit()
        conn_portal.close()
        
        year_label = f"{year} Year" if year else "All Years"
        return jsonify({
            'status': 'success',
            'message': f'Password reset for {reset_count} students in {year_label}',
            'count': reset_count
        })
        
    except Exception as e:
        print(f"Bulk reset error: {e}")
        return jsonify({'status': 'error', 'message': 'Bulk reset failed'}), 500

@app.route('/api/admin/auth-stats')

def api_admin_auth_stats():
    """Get auth statistics and recent password resets for dashboard"""
    conn = get_portal_db()
    cursor = conn.cursor()
    
    # Total registered students
    cursor.execute("SELECT COUNT(*) as count FROM student_auth")
    total_registered = cursor.fetchone()['count']
    
    # Students with changed passwords (not first login)
    cursor.execute("SELECT COUNT(*) as count FROM student_auth WHERE is_first_login = 0")
    active_users = cursor.fetchone()['count']
    
    # Students still on default password
    cursor.execute("SELECT COUNT(*) as count FROM student_auth WHERE is_first_login = 1")
    pending_change = cursor.fetchone()['count']
    
    # Recent password resets (by checking last_changed within last 7 days where is_first_login = 1)
    cursor.execute("""
        SELECT enrollment_no, last_changed 
        FROM student_auth 
        WHERE is_first_login = 1 AND last_changed IS NOT NULL
        ORDER BY last_changed DESC 
        LIMIT 10
    """)
    recent_resets = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    # Get student names
    conn_lib = get_library_db()
    cursor_lib = conn_lib.cursor()
    
    for reset in recent_resets:
        cursor_lib.execute("SELECT name FROM students WHERE enrollment_no = ?", (reset['enrollment_no'],))
        student = cursor_lib.fetchone()
        reset['student_name'] = student['name'] if student else 'Unknown'
    
    conn_lib.close()
    
    return jsonify({
        'stats': {
            'total_registered': total_registered,
            'active_users': active_users,
            'pending_change': pending_change
        },
        'recent_resets': recent_resets
    })

@app.route('/api/admin/stats')
def api_admin_stats():
    """Get portal statistics for dashboard"""
    conn = get_portal_db()
    cursor = conn.cursor()
    
    # Count requests by status
    cursor.execute("SELECT status, COUNT(*) as count FROM requests GROUP BY status")
    request_stats = {row['status']: row['count'] for row in cursor.fetchall()}
    
    # Count deletion requests by status
    cursor.execute("SELECT status, COUNT(*) as count FROM deletion_requests GROUP BY status")
    deletion_stats = {row['status']: row['count'] for row in cursor.fetchall()}
    
    # Count active auth records
    cursor.execute("SELECT COUNT(*) as count FROM student_auth")
    auth_count = cursor.fetchone()['count']
    
    # Count first-time login pending
    cursor.execute("SELECT COUNT(*) as count FROM student_auth WHERE is_first_login = 1")
    first_login_count = cursor.fetchone()['count']
    
    conn.close()
    
    return jsonify({
        'requests': request_stats,
        'deletions': deletion_stats,
        'portal_users': auth_count,
        'pending_password_change': first_login_count
    })

# =====================================================================
# STUDY MATERIALS API ENDPOINTS
# =====================================================================

@app.route('/api/study-materials', methods=['GET'])
def api_get_study_materials():
    """Get study materials (optionally filtered by year)"""
    year_filter = request.args.get('year', None)
    
    conn = get_portal_db()
    cursor = conn.cursor()
    
    if year_filter and year_filter != 'All':
        cursor.execute("""
            SELECT * FROM study_materials 
            WHERE active = 1 AND year = ?
            ORDER BY upload_date DESC
        """, (year_filter,))
    else:
        cursor.execute("""
            SELECT * FROM study_materials 
            WHERE active = 1
            ORDER BY upload_date DESC
        """)
    
    materials = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({'materials': materials})

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/admin/study-materials', methods=['GET', 'POST'])
def api_admin_study_materials():
    """Admin: Manage study materials"""
    conn = get_portal_db()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        # Get all materials (including inactive)
        cursor.execute("SELECT * FROM study_materials ORDER BY upload_date DESC")
        materials = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify({'materials': materials})
    
    elif request.method == 'POST':
        # Handle file upload
        if 'file' not in request.files:
            conn.close()
            return jsonify({'status': 'error', 'message': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            conn.close()
            return jsonify({'status': 'error', 'message': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            conn.close()
            return jsonify({'status': 'error', 'message': 'File type not allowed'}), 400
        
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description', '')
        year = request.form.get('year')
        category = request.form.get('category', 'Notes')
        branch = request.form.get('branch', 'Computer')
        
        if not title or not year:
            conn.close()
            return jsonify({'status': 'error', 'message': 'Title and year required'}), 400
        
        # Save file with unique name
        original_filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{original_filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        try:
            file.save(file_path)
            file_size = os.path.getsize(file_path)
            
            cursor.execute("""
                INSERT INTO study_materials (title, description, filename, original_filename, file_size, branch, year, category)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (title, description, unique_filename, original_filename, file_size, branch, year, category))
            
            conn.commit()
            conn.close()
            return jsonify({'status': 'success', 'message': 'File uploaded successfully'})
        except Exception as e:
            conn.close()
            if os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({'status': 'error', 'message': f'Upload failed: {str(e)}'}), 500

@app.route('/api/study-materials/<int:material_id>/download')
def download_study_material(material_id):
    """Download a study material file"""
    conn = get_portal_db()
    cursor = conn.cursor()
    cursor.execute("SELECT filename, original_filename FROM study_materials WHERE id = ? AND active = 1", (material_id,))
    material = cursor.fetchone()
    conn.close()
    
    if not material:
        return jsonify({'error': 'File not found'}), 404
    
    file_path = os.path.join(UPLOAD_FOLDER, material['filename'])
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found on server'}), 404
    
    return send_file(file_path, as_attachment=True, download_name=material['original_filename'])

@app.route('/api/admin/study-materials/<int:material_id>', methods=['DELETE', 'PUT'])
def api_admin_manage_material(material_id):
    """Admin: Delete or update study material"""
    conn = get_portal_db()
    cursor = conn.cursor()
    
    if request.method == 'DELETE':
        # Get filename before deletion
        cursor.execute("SELECT filename FROM study_materials WHERE id = ?", (material_id,))
        material = cursor.fetchone()
        
        # Soft delete (set active = 0)
        cursor.execute("UPDATE study_materials SET active = 0 WHERE id = ?", (material_id,))
        conn.commit()
        
        # Optionally delete physical file (commented out to keep files)
        # if material:
        #     file_path = os.path.join(UPLOAD_FOLDER, material['filename'])
        #     if os.path.exists(file_path):
        #         os.remove(file_path)
        
        conn.close()
        return jsonify({'status': 'success', 'message': 'Material deleted'})
    
    elif request.method == 'PUT':
        # Update material
        data = request.json
        cursor.execute("""
            UPDATE study_materials 
            SET title = ?, description = ?, drive_link = ?, year = ?, category = ?
            WHERE id = ?
        """, (data['title'], data.get('description', ''), data['drive_link'], 
              data['year'], data.get('category', 'Notes'), material_id))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Material updated'})

# --- SPA Serving ---
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        resp = send_from_directory(app.static_folder, path)
        # Prevent stale UI when using PWA/service worker.
        # Hashed assets can be cached, but entrypoints should always revalidate.
        if path in ('index.html', 'sw.js', 'manifest.webmanifest') or path.endswith('registerSW.js') or path.startswith('workbox-'):
            resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            resp.headers['Pragma'] = 'no-cache'
        return resp
    
    # If path is an API call that wasn't matched, return 404
    if path.startswith('api/'):
        return jsonify({'error': 'Not Found'}), 404
        
    # Otherwise, for SPA routing, return index.html
    resp = send_from_directory(app.static_folder, 'index.html')
    resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    resp.headers['Pragma'] = 'no-cache'
    return resp

if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)

#