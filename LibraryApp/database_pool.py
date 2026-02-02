#!/usr/bin/env python3
"""
Database Connection Pool Manager
Provides efficient connection pooling for PostgreSQL/SQLite
"""

import threading
import time
import os
from queue import Queue, Empty
from datetime import datetime

class ConnectionPool:
    """Thread-safe connection pool for database operations"""
    
    def __init__(self, db_instance, min_connections=3, max_connections=10):
        self.db = db_instance
        self.min_connections = min_connections
        self.max_connections = max_connections
        self.pool = Queue(maxsize=max_connections)
        self.active_connections = 0
        self.lock = threading.Lock()
        self.last_cleanup = time.time()
        
        # Initialize minimum connections
        self._initialize_pool()
        
    def _initialize_pool(self):
        """Create initial pool of connections"""
        for _ in range(self.min_connections):
            try:
                conn = self.db.get_connection()
                if conn:
                    self.pool.put({
                        'conn': conn,
                        'created': time.time(),
                        'last_used': time.time()
                    })
                    self.active_connections += 1
            except Exception as e:
                print(f"Error initializing connection: {e}")
    
    def get_connection(self, timeout=5):
        """Get a connection from pool or create new one"""
        try:
            # Try to get from pool first
            conn_info = self.pool.get(block=True, timeout=timeout)
            
            # Check if connection is still valid
            if self._is_connection_valid(conn_info['conn']):
                conn_info['last_used'] = time.time()
                return conn_info
            else:
                # Connection is stale, create new one
                self.active_connections -= 1
                return self._create_new_connection()
                
        except Empty:
            # Pool is empty, try to create new connection
            with self.lock:
                if self.active_connections < self.max_connections:
                    return self._create_new_connection()
                else:
                    # Wait and retry
                    time.sleep(0.1)
                    return self.get_connection(timeout=timeout)
    
    def _create_new_connection(self):
        """Create a new database connection"""
        try:
            conn = self.db.get_connection()
            if conn:
                self.active_connections += 1
                return {
                    'conn': conn,
                    'created': time.time(),
                    'last_used': time.time()
                }
        except Exception as e:
            print(f"Error creating connection: {e}")
            return None
    
    def _is_connection_valid(self, conn):
        """Check if connection is still valid"""
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            return True
        except:
            return False
    
    def return_connection(self, conn_info):
        """Return connection to pool"""
        if conn_info and self.pool.qsize() < self.max_connections:
            conn_info['last_used'] = time.time()
            self.pool.put(conn_info)
        else:
            # Pool is full, close connection
            try:
                if conn_info and conn_info['conn']:
                    conn_info['conn'].close()
                    self.active_connections -= 1
            except:
                pass
    
    def cleanup_idle_connections(self, max_idle_time=300):
        """Remove idle connections older than max_idle_time seconds"""
        current_time = time.time()
        
        # Only cleanup every 60 seconds
        if current_time - self.last_cleanup < 60:
            return
        
        self.last_cleanup = current_time
        temp_connections = []
        
        # Check all connections in pool
        while not self.pool.empty():
            try:
                conn_info = self.pool.get_nowait()
                
                # Keep if recently used
                if current_time - conn_info['last_used'] < max_idle_time:
                    temp_connections.append(conn_info)
                else:
                    # Close idle connection
                    try:
                        conn_info['conn'].close()
                        self.active_connections -= 1
                    except:
                        pass
            except Empty:
                break
        
        # Return valid connections to pool
        for conn_info in temp_connections:
            self.pool.put(conn_info)
        
        # Ensure minimum connections
        while self.active_connections < self.min_connections:
            conn_info = self._create_new_connection()
            if conn_info:
                self.pool.put(conn_info)
            else:
                break
    
    def close_all(self):
        """Close all connections in pool"""
        while not self.pool.empty():
            try:
                conn_info = self.pool.get_nowait()
                conn_info['conn'].close()
                self.active_connections -= 1
            except:
                pass
    
    def get_stats(self):
        """Get pool statistics"""
        return {
            'active_connections': self.active_connections,
            'available_connections': self.pool.qsize(),
            'max_connections': self.max_connections,
            'min_connections': self.min_connections
        }


# Global pool instance
_pool_instance = None
_pool_lock = threading.Lock()

def get_pool(db_instance):
    """Get or create singleton pool instance"""
    global _pool_instance
    
    if _pool_instance is None:
        with _pool_lock:
            if _pool_instance is None:
                _pool_instance = ConnectionPool(db_instance)
    
    return _pool_instance

def close_pool():
    """Close the global pool"""
    global _pool_instance
    
    if _pool_instance:
        _pool_instance.close_all()
        _pool_instance = None
