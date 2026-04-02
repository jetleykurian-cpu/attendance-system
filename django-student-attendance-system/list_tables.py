import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Get CREATE TABLE statement
cursor.execute("SELECT sql FROM sqlite_master WHERE name='student_management_app_parent';")
create_stmt = cursor.fetchone()
print("CREATE TABLE statement:")
print(create_stmt[0])

conn.close()