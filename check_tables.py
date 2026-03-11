import sqlite3

conn = sqlite3.connect('LibraryApp/library.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables in database:", [t[0] for t in tables])
conn.close()
