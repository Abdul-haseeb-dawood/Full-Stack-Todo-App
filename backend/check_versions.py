import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('todo_app.db')
cursor = conn.cursor()

# Query to see alembic versions
cursor.execute("SELECT * FROM alembic_version;")
versions = cursor.fetchall()
print("Applied alembic versions:")
for version in versions:
    print(version[0])

# Close the connection
conn.close()