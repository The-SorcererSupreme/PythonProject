import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

# Database location - default or environment variable
DB_PATH = os.getenv("DB_PATH")

def initialize_database():
    """Initialize the database schema."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)  # Ensure directory exists

    connection = sqlite3.connect(DB_PATH)
    with connection:
        # Create users table
        connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
    print(f"Database initialized at: {DB_PATH}")
    connection.close()

if __name__ == "__main__":
    initialize_database()
