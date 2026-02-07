days_int = 7

# What I'm generating
query1 = f"AND created_at >= date('now', '-{days_int} days')"
print("Generated query:")
print(query1)

# What should be generated
query2 = f"AND created_at >= date('now', '-{days_int} days')"
print("\nExpected:")
print(query2)

# Try with parameterized
import sqlite3
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Create a test table
cursor.execute("CREATE TABLE test (created_at DATETIME)")
cursor.execute("INSERT INTO test VALUES (datetime('now'))")

# Test the query
test_query = f"SELECT * FROM test WHERE created_at >= date('now', '-{days_int} days')"
print(f"\nTest query: {test_query}")

try:
    cursor.execute(test_query)
    print("Query executed successfully")
    print(f"Results: {cursor.fetchall()}")
except Exception as e:
    print(f"Error: {e}")
