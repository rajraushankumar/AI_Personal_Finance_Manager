import sqlite3

# Create database connection
connection = sqlite3.connect("finance.db")

# Create cursor
cursor = connection.cursor()

# Create Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")

# Create Income Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS income (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    amount REAL,
    source TEXT
)
""")

# Add date column to Income table
try:
    cursor.execute(
        "ALTER TABLE income ADD COLUMN date TEXT"
    )
except sqlite3.OperationalError:
    print("Income date column already exists")


# Create Expense Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS expense (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    amount REAL,
    category TEXT
)
""")

# Add date column to Expense table
try:
    cursor.execute(
        "ALTER TABLE expense ADD COLUMN date TEXT"
    )
except sqlite3.OperationalError:
    print("Expense date column already exists")




# Read Existing User
cursor.execute(
    "SELECT * FROM users WHERE email=?",
    ("rajj@gmail.com",)
)

user = cursor.fetchone()

print(user)

connection.commit()
connection.close()

print("✅ Database Ready Successfully")