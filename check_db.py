import sqlite3

# Connect to the database
conn = sqlite3.connect('data.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Example: Select all rows from a table
cursor.execute('SELECT * FROM employees')
rows = cursor.fetchall()

count=0
for row in rows:
    count+=1
    print(count)
# Close the cursor and connection
cursor.close()
conn.close()