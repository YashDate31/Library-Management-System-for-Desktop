#!/usr/bin/env python3
"""
Database Optimization Script
Creates indexes and optimizes database for better performance
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import Database
from datetime import datetime

def create_indexes(db):
    """Create performance indexes on frequently queried columns"""
    print("Creating database indexes for performance optimization...")
    
    indexes = [
        # Students table indexes
        ("idx_students_enrollment", "CREATE INDEX IF NOT EXISTS idx_students_enrollment ON students(enrollment_no)"),
        ("idx_students_email", "CREATE INDEX IF NOT EXISTS idx_students_email ON students(email)"),
        ("idx_students_year", "CREATE INDEX IF NOT EXISTS idx_students_year ON students(year)"),
        ("idx_students_department", "CREATE INDEX IF NOT EXISTS idx_students_department ON students(department)"),
        
        # Books table indexes
        ("idx_books_id", "CREATE INDEX IF NOT EXISTS idx_books_id ON books(book_id)"),
        ("idx_books_category", "CREATE INDEX IF NOT EXISTS idx_books_category ON books(category)"),
        ("idx_books_title", "CREATE INDEX IF NOT EXISTS idx_books_title ON books(title)"),
        ("idx_books_author", "CREATE INDEX IF NOT EXISTS idx_books_author ON books(author)"),
        
        # Borrow records indexes (most important for performance)
        ("idx_borrow_enrollment", "CREATE INDEX IF NOT EXISTS idx_borrow_enrollment ON borrow_records(enrollment_no)"),
        ("idx_borrow_book", "CREATE INDEX IF NOT EXISTS idx_borrow_book ON borrow_records(book_id)"),
        ("idx_borrow_date", "CREATE INDEX IF NOT EXISTS idx_borrow_date ON borrow_records(borrow_date)"),
        ("idx_borrow_due", "CREATE INDEX IF NOT EXISTS idx_borrow_due ON borrow_records(due_date)"),
        ("idx_borrow_return", "CREATE INDEX IF NOT EXISTS idx_borrow_return ON borrow_records(return_date)"),
        ("idx_borrow_status", "CREATE INDEX IF NOT EXISTS idx_borrow_status ON borrow_records(status)"),
        
        # Composite indexes for common queries
        ("idx_borrow_composite", "CREATE INDEX IF NOT EXISTS idx_borrow_composite ON borrow_records(enrollment_no, book_id, return_date)"),
        ("idx_overdue_composite", "CREATE INDEX IF NOT EXISTS idx_overdue_composite ON borrow_records(return_date, due_date) WHERE return_date IS NULL"),
    ]
    
    conn = db.get_connection()
    cursor = conn.cursor()
    
    created_count = 0
    for index_name, index_sql in indexes:
        try:
            cursor.execute(index_sql)
            conn.commit()
            print(f"  ✓ Created index: {index_name}")
            created_count += 1
        except Exception as e:
            print(f"  ⚠ Index {index_name} already exists or error: {e}")
    
    conn.close()
    print(f"\n✓ Successfully created/verified {created_count} indexes")


def analyze_tables(db):
    """Run ANALYZE on all tables to update statistics"""
    print("\nAnalyzing tables for query optimization...")
    
    tables = ['students', 'books', 'borrow_records', 'admin_activity', 'promotion_history']
    
    conn = db.get_connection()
    cursor = conn.cursor()
    
    for table in tables:
        try:
            cursor.execute(f"ANALYZE {table}")
            conn.commit()
            print(f"  ✓ Analyzed table: {table}")
        except Exception as e:
            print(f"  ⚠ Error analyzing {table}: {e}")
    
    conn.close()
    print("✓ Table analysis completed")


def vacuum_database(db):
    """Vacuum database to reclaim space and optimize"""
    print("\nOptimizing database storage...")
    
    try:
        conn = db.get_connection()
        
        # PostgreSQL uses VACUUM, SQLite uses VACUUM
        try:
            # Try PostgreSQL VACUUM
            conn.set_isolation_level(0)  # AUTOCOMMIT mode for VACUUM
            cursor = conn.cursor()
            cursor.execute("VACUUM ANALYZE")
            print("  ✓ PostgreSQL VACUUM completed")
        except:
            # Try SQLite VACUUM
            cursor = conn.cursor()
            cursor.execute("VACUUM")
            conn.commit()
            print("  ✓ SQLite VACUUM completed")
        
        conn.close()
        
    except Exception as e:
        print(f"  ⚠ Vacuum operation not supported or error: {e}")


def get_database_stats(db):
    """Get and display database statistics"""
    print("\n" + "="*60)
    print("DATABASE STATISTICS")
    print("="*60)
    
    conn = db.get_connection()
    cursor = conn.cursor()
    
    try:
        # Count records in each table
        tables = {
            'Students': 'students',
            'Books': 'books',
            'Borrow Records': 'borrow_records',
            'Admin Activity': 'admin_activity'
        }
        
        for display_name, table_name in tables.items():
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"{display_name:20} : {count:,} records")
            except:
                print(f"{display_name:20} : N/A")
        
        # Get overdue books count
        try:
            cursor.execute("""
                SELECT COUNT(*) FROM borrow_records 
                WHERE return_date IS NULL AND due_date < CURRENT_DATE
            """)
            overdue = cursor.fetchone()[0]
            print(f"{'Overdue Books':20} : {overdue:,} records")
        except:
            pass
        
        # Get active loans
        try:
            cursor.execute("""
                SELECT COUNT(*) FROM borrow_records 
                WHERE return_date IS NULL
            """)
            active = cursor.fetchone()[0]
            print(f"{'Active Loans':20} : {active:,} records")
        except:
            pass
        
    except Exception as e:
        print(f"Error getting stats: {e}")
    
    conn.close()
    print("="*60)


def main():
    """Main optimization function"""
    print("\n" + "="*60)
    print("IARE LIBRARY MANAGEMENT SYSTEM - DATABASE OPTIMIZER")
    print("="*60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Initialize database
    db = Database()
    
    # Show current stats
    get_database_stats(db)
    
    # Run optimizations
    print("\nStarting optimization process...\n")
    
    create_indexes(db)
    analyze_tables(db)
    vacuum_database(db)
    
    # Show final stats
    get_database_stats(db)
    
    print("\n" + "="*60)
    print("✓ OPTIMIZATION COMPLETED SUCCESSFULLY")
    print("="*60)
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nYour database is now optimized for better performance!")
    print("Restart your application to see improvements.\n")


if __name__ == "__main__":
    main()
