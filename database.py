import sqlite3
import os

DB_FILE = "employees.db"

def init_db():
    """Initialize database and create tables if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'employee'))
        )
    """)

    # Insert default admin if not exists
    cursor.execute("SELECT * FROM users WHERE username = ?", ("admin",))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                        ("admin", "admin123", "admin"))
        print("Default admin account created: Username: admin, Password: admin123")

    conn.commit()
    conn.close()

def validate_user(username, password):
    """Validate login credentials."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]  # returns 'admin' or 'employee'
    else:
        return None
