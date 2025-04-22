import sqlite3

conn = sqlite3.connect("users.db")  # Connect to SQLite database (creates if not exists)
cursor = conn.cursor()
cursor.execute("SELECT sqlite_version();")
print("SQLite Version:", cursor.fetchone()[0])  # Fetch and print the SQLite version
conn.close()  # Close the connection
