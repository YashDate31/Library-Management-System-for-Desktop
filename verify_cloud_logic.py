import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Ensure we can import from LibraryApp
sys.path.append(os.path.join(os.path.dirname(__file__), 'LibraryApp'))

class TestCloudMigration(unittest.TestCase):
    def setUp(self):
        # Clear env var before each test
        if 'DATABASE_URL' in os.environ:
            del os.environ['DATABASE_URL']
            
    def test_local_fallback(self):
        """Test that Database uses SQLite when DATABASE_URL is missing"""
        from database import Database
        
        # Reload module to reset global state (load_dotenv might have run)
        # But Database class checks env in __init__, so just instantiating is enough if we patch os.getenv?
        # Database uses os.getenv('DATABASE_URL') in __init__
        
        db = Database()
        print(f"\n[Fallback Test] Use Cloud: {db.use_cloud}")
        self.assertFalse(db.use_cloud)
        self.assertTrue(db.db_path.endswith('library.db'))
        
        # Check connection type (should be sqlite3.Connection)
        conn = db.get_connection()
        print(f"[Fallback Test] Connection Type: {type(conn).__name__}")
        self.assertIn('Connection', type(conn).__name__) # sqlite3.Connection
        conn.close()

    @patch('database.psycopg2')
    def test_cloud_connection_logic(self, mock_psycopg2):
        """Test that Database attempts Postgres connection when DATABASE_URL is set"""
        os.environ['DATABASE_URL'] = "postgres://user:pass@localhost:5432/testdb"
        from database import Database, PostgresConnectionWrapper
        
        # Force POSTGRES_AVAILABLE to True for this test context?
        # It's a global in database.py.
        import database
        database.POSTGRES_AVAILABLE = True
        
        db = Database()
        print(f"\n[Cloud Test] Use Cloud: {db.use_cloud}")
        self.assertTrue(db.use_cloud, "Should use cloud when DATABASE_URL is set")
        
        # Mock connect
        mock_conn = MagicMock()
        mock_psycopg2.connect.return_value = mock_conn
        
        conn = db.get_connection()
        self.assertIsInstance(conn, PostgresConnectionWrapper)
        print(f"[Cloud Test] Connection Wrapper Created Successfully")
        
        # Verify psycopg2.connect was called with correct URL
        mock_psycopg2.connect.assert_called_with("postgres://user:pass@localhost:5432/testdb")

if __name__ == '__main__':
    unittest.main()
