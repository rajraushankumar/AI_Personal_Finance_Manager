import sqlite3

connection = sqlite3.connect("finance.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM expense")

for row in cursor.fetchall():
    print(row)

connection.close()