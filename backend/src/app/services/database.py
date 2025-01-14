# backend/src/app/services/database.py
import sqlite3
import os

class Database:
    def __init__(self, db_path=None):
        self.db_path = db_path or os.getenv("DB_PATH")
        self.connection = None
        # Add user when changing to Postgres/MySQL
        # self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")

    def connect(self):
        """Connect to the SQLite database."""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        return self.connection

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query, params=None):
        """Execute a query with parameters and close the cursor."""
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        connection.commit()
        cursor.close()

    def fetch_query(self, query, params=None):
        """Fetch query results and close the cursor."""
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        cursor.close()  # Close the cursor after fetching results
        return results
