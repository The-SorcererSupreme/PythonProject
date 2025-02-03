# backend/src/app/services/database.py
import sqlite3
import os
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self, db_name=None, db_user=None, db_password=None, db_host=None, db_port=None):
        self.db_name = db_name or os.getenv("DB_NAME")
        self.db_user = db_user or os.getenv("DB_USER")
        self.db_password = db_password or os.getenv("DB_PASSWORD")
        self.db_host = db_host or os.getenv("DB_HOST")
        self.db_port = db_port or os.getenv("DB_PORT")
        self.connection = None

    def connect(self):
        """Connect to the PostgreSQL database."""
        if self.connection is None:
            self.connection = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port
            )
        return self.connection

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query, params=None):
        """Execute a query with parameters and commit the transaction."""
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        connection.commit()
        cursor.close()

    def fetch_query(self, query, params=None):
        """Fetch query results."""
        connection = self.connect()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)  # Use RealDictCursor
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        cursor.close()  # Close the cursor after fetching results
        return results