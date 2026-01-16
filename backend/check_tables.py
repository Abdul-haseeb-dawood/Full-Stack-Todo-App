import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('todo_app.db')
cursor = conn.cursor()

# Query to list all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in the database:")
for table in tables:
    print(table[0])

# Close the connection
conn.close()