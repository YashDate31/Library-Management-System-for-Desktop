#!/usr/bin/env python3
"""
Database Synchronization Manager
Syncs data between local SQLite and remote PostgreSQL databases
"""

import os
import json
import sqlite3

# Load .env if available (for DATABASE_URL)
try:
    from dotenv import load_dotenv
    _env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(_env_path):
        load_dotenv(_env_path)
    else:
        load_dotenv()
except ImportError:
    pass

try:
    import psycopg2  # type: ignore
except Exception:  # pragma: no cover
    psycopg2 = None
from datetime import datetime
import threading
import time

class SyncManager:
    """Manages bidirectional sync between local and remote databases"""
    
    def __init__(self, local_db_path, remote_config):
        self.local_db_path = local_db_path
        self.remote_config = remote_config
        self.sync_log_path = os.path.join(os.path.dirname(local_db_path), 'sync_log.json')
        self.is_syncing = False
        self.last_sync_time = self._load_last_sync_time()
        
    def _load_last_sync_time(self):
        """Load last sync timestamp from log"""
        if os.path.exists(self.sync_log_path):
            try:
                with open(self.sync_log_path, 'r') as f:
                    data = json.load(f)
                    return data.get('last_sync', '2000-01-01 00:00:00')
            except:
                pass
        return '2000-01-01 00:00:00'
    
    def _save_sync_time(self, status='completed'):
        """Save current sync timestamp"""
        try:
            with open(self.sync_log_path, 'w') as f:
                json.dump({
                    'last_sync': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'status': status
                }, f, indent=4)
        except Exception as e:
            print(f"Error saving sync time: {e}")
    
    def _mark_sync_in_progress(self):
        """Mark sync as in progress"""
        try:
            with open(self.sync_log_path, 'w') as f:
                json.dump({
                    'last_sync': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'status': 'in_progress'
                }, f, indent=4)
        except Exception as e:
            print(f"Error marking sync in progress: {e}")
    
    def sync_now(self, direction='both', progress_callback=None):
        """
        Perform synchronization with graceful interruption handling
        
        Args:
            direction: 'local_to_remote', 'remote_to_local', or 'both'
            progress_callback: Function to call with progress updates
        
        Returns:
            Dictionary with sync statistics
        """
        if self.is_syncing:
            return {'error': 'Sync already in progress'}
        
        self.is_syncing = True
        self._mark_sync_in_progress()  # Mark as in progress
        results = {
            'success': False,
            'direction': direction,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'tables_synced': [],
            'records_synced': 0,
            'errors': []
        }
        
        try:
            if psycopg2 is None:
                results['errors'].append(
                    "Remote sync requires 'psycopg2'. Install it (e.g., psycopg2-binary) and restart the app."
                )
                self._save_sync_time(status='failed')
                return results

            local_conn = sqlite3.connect(self.local_db_path)
            remote_conn = psycopg2.connect(**self.remote_config)
            
            # Library tables (bidirectional sync)
            tables_to_sync = ['students', 'books', 'borrow_records', 'admin_activity']
            
            for idx, table in enumerate(tables_to_sync):
                if progress_callback:
                    progress = ((idx + 1) / len(tables_to_sync)) * 50  # First half for library
                    progress_callback(table, progress)
                
                try:
                    if direction in ['local_to_remote', 'both']:
                        records = self._sync_table_local_to_remote(
                            local_conn, remote_conn, table
                        )
                        results['records_synced'] += records
                    
                    if direction in ['remote_to_local', 'both']:
                        records = self._sync_table_remote_to_local(
                            local_conn, remote_conn, table
                        )
                        results['records_synced'] += records
                    
                    results['tables_synced'].append(table)
                    
                except Exception as e:
                    results['errors'].append(f"{table}: {str(e)}")
            
            # Portal tables (requests) - sync from remote to local so desktop sees web requests
            try:
                portal_db_path = os.path.join(os.path.dirname(self.local_db_path), 'Web-Extension', 'portal.db')
                if os.path.exists(os.path.dirname(portal_db_path)):
                    portal_conn = sqlite3.connect(portal_db_path)
                    portal_conn.row_factory = sqlite3.Row
                    
                    portal_tables = ['requests', 'notices']
                    for idx, table in enumerate(portal_tables):
                        if progress_callback:
                            progress = 50 + ((idx + 1) / len(portal_tables)) * 50
                            progress_callback(f"portal.{table}", progress)
                        
                        try:
                            # Only sync from remote to local for portal data
                            # (students submit on web → desktop admin sees them)
                            records = self._sync_portal_table_remote_to_local(
                                portal_conn, remote_conn, table
                            )
                            results['records_synced'] += records
                            results['tables_synced'].append(f'portal.{table}')
                        except Exception as e:
                            # Don't fail entire sync if portal tables have issues
                            results['errors'].append(f"portal.{table}: {str(e)}")
                    
                    portal_conn.commit()
                    portal_conn.close()
            except Exception as e:
                results['errors'].append(f"Portal sync: {str(e)}")
            
            local_conn.close()
            remote_conn.close()
            
            results['success'] = len(results['errors']) == 0
            # Save sync time with status
            if results['success']:
                self._save_sync_time(status='completed')
            else:
                self._save_sync_time(status='completed_with_errors')
            
        except Exception as e:
            results['errors'].append(f"Connection error: {str(e)}")
            self._save_sync_time(status='failed')
        
        finally:
            self.is_syncing = False
        
        return results
    
    def _sync_table_local_to_remote(self, local_conn, remote_conn, table_name):
        """Sync a table from local to remote"""
        try:
            local_cursor = local_conn.cursor()
            remote_cursor = remote_conn.cursor()
            
            # Get records modified since last sync
            local_cursor.execute(f"SELECT * FROM {table_name}")
            rows = local_cursor.fetchall()
            
            if not rows:
                return 0
            
            # Get column names
            columns = [desc[0] for desc in local_cursor.description]
            
            synced_count = 0
            for row in rows:
                try:
                    # Try to insert or update
                    placeholders = ', '.join(['%s'] * len(row))
                    cols = ', '.join(columns)
                    
                    # Use UPSERT (INSERT ... ON CONFLICT)
                    primary_key = self._get_primary_key(table_name)
                    update_cols = ', '.join([f"{col} = EXCLUDED.{col}" for col in columns if col != primary_key])
                    
                    query = f"""
                        INSERT INTO {table_name} ({cols})
                        VALUES ({placeholders})
                        ON CONFLICT ({primary_key}) 
                        DO UPDATE SET {update_cols}
                    """
                    
                    remote_cursor.execute(query, row)
                    synced_count += 1
                    
                except Exception as e:
                    print(f"Error syncing row in {table_name}: {e}")
            
            remote_conn.commit()
            return synced_count
            
        except Exception as e:
            print(f"Error syncing table {table_name} local to remote: {e}")
            return 0
    
    def _sync_table_remote_to_local(self, local_conn, remote_conn, table_name):
        """Sync a table from remote to local"""
        try:
            local_cursor = local_conn.cursor()
            remote_cursor = remote_conn.cursor()
            
            # Get records from remote
            remote_cursor.execute(f"SELECT * FROM {table_name}")
            rows = remote_cursor.fetchall()
            
            if not rows:
                return 0
            
            # Get column names
            columns = [desc[0] for desc in remote_cursor.description]
            
            synced_count = 0
            for row in rows:
                try:
                    # Try to insert or replace
                    placeholders = ', '.join(['?'] * len(row))
                    cols = ', '.join(columns)
                    
                    query = f"INSERT OR REPLACE INTO {table_name} ({cols}) VALUES ({placeholders})"
                    local_cursor.execute(query, row)
                    synced_count += 1
                    
                except Exception as e:
                    print(f"Error syncing row in {table_name}: {e}")
            
            local_conn.commit()
            return synced_count
            
        except Exception as e:
            print(f"Error syncing table {table_name} remote to local: {e}")
            return 0
    
    def _get_primary_key(self, table_name):
        """Get primary key column name for table"""
        pk_map = {
            'students': 'enrollment_no',
            'books': 'book_id',
            'borrow_records': 'id',
            'admin_activity': 'id',
            'requests': 'req_id',
            'notices': 'id'
        }
        return pk_map.get(table_name, 'id')
    
    def _sync_portal_table_remote_to_local(self, local_conn, remote_conn, table_name):
        """Sync portal tables (requests, notices) from remote Postgres to local SQLite"""
        try:
            local_cursor = local_conn.cursor()
            remote_cursor = remote_conn.cursor()
            
            # Check if table exists remotely
            remote_cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = %s
                )
            """, (table_name,))
            if not remote_cursor.fetchone()[0]:
                return 0
            
            # Get records from remote
            remote_cursor.execute(f"SELECT * FROM {table_name}")
            rows = remote_cursor.fetchall()
            
            if not rows:
                return 0
            
            # Get column names
            columns = [desc[0] for desc in remote_cursor.description]
            
            synced_count = 0
            pk = self._get_primary_key(table_name)
            
            for row in rows:
                try:
                    # Create dict for easier access
                    row_dict = dict(zip(columns, row))
                    pk_value = row_dict.get(pk)
                    
                    if pk_value is None:
                        continue
                    
                    # Check if exists locally
                    local_cursor.execute(f"SELECT {pk} FROM {table_name} WHERE {pk} = ?", (pk_value,))
                    exists = local_cursor.fetchone()
                    
                    if exists:
                        # Update existing record
                        update_cols = [f"{col} = ?" for col in columns if col != pk]
                        update_vals = [row_dict[col] for col in columns if col != pk]
                        update_vals.append(pk_value)
                        
                        query = f"UPDATE {table_name} SET {', '.join(update_cols)} WHERE {pk} = ?"
                        local_cursor.execute(query, update_vals)
                    else:
                        # Insert new record
                        placeholders = ', '.join(['?'] * len(columns))
                        cols = ', '.join(columns)
                        values = [row_dict[col] for col in columns]
                        
                        query = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
                        local_cursor.execute(query, values)
                    
                    synced_count += 1
                    
                except Exception as e:
                    print(f"Error syncing portal row in {table_name}: {e}")
            
            return synced_count
            
        except Exception as e:
            print(f"Error syncing portal table {table_name} remote to local: {e}")
            return 0
    
    def auto_sync_daemon(self, interval_minutes=30):
        """Run automatic sync in background thread"""
        def sync_loop():
            while True:
                time.sleep(interval_minutes * 60)
                print(f"[Auto-Sync] Starting sync at {datetime.now()}")
                result = self.sync_now(direction='both')
                if result['success']:
                    print(f"[Auto-Sync] Completed: {result['records_synced']} records")
                else:
                    print(f"[Auto-Sync] Failed: {result['errors']}")
        
        thread = threading.Thread(target=sync_loop, daemon=True)
        thread.start()
        print(f"[Auto-Sync] Daemon started (every {interval_minutes} minutes)")


def create_sync_manager(db):
    """
    Create a sync manager instance for the given database
    
    Args:
        db: Database instance (should be using local SQLite)
    
    Returns:
        SyncManager instance or None if remote config not available
    """
    try:
        # Get local database path from the Database instance
        local_db_path = db.db_path
        
        if not local_db_path:
            print("[WARNING] Sync Manager: No local database path available")
            return None
        
        # Get remote database config from environment
        database_url = os.getenv('DATABASE_URL')
        
        if not database_url:
            print("[WARNING] Sync Manager: No remote database URL configured (DATABASE_URL not set)")
            print("   Sync disabled - desktop will work offline only")
            return None

        if psycopg2 is None:
            print("[WARNING] Sync Manager: psycopg2 not installed - remote sync disabled")
            return None
        
        # Parse PostgreSQL connection string
        # Format: postgresql://user:password@host:port/database
        try:
            import re
            match = re.match(r'postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)', database_url)
            if not match:
                print("[WARNING] Sync Manager: Invalid DATABASE_URL format")
                return None
            
            user, password, host, port, dbname = match.groups()
            
            remote_config = {
                'host': host,
                'port': int(port),
                'database': dbname,
                'user': user,
                'password': password
            }
            
            print(f"[OK] Sync Manager: Configured for remote sync to {host}/{dbname}")
            print(f"   Local: {local_db_path}")
            return SyncManager(local_db_path, remote_config)
            
        except Exception as e:
            print(f"[WARNING] Sync Manager: Failed to parse DATABASE_URL: {e}")
            return None
            
    except Exception as e:
        print(f"[WARNING] Sync Manager: Failed to initialize: {e}")
        return None
