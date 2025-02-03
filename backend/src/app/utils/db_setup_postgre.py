import os
import psycopg2
import argparse
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

# Load database connection parameters from the environment variables
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def drop_tables(cursor):
    """Drop all tables to rebuild the schema."""
    # Drop tables in reverse order to avoid foreign key constraint errors
    cursor.execute("DROP TABLE IF EXISTS shared_containers CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS containers CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS preferences CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS sessions CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS users CASCADE;")
    print("All tables dropped successfully.")

def create_tables(cursor):
    """Create the necessary tables in the database."""
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        session_token TEXT UNIQUE NOT NULL,
        expires_at TIMESTAMP NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS preferences (
        id SERIAL PRIMARY KEY,
        user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE CASCADE,
        layout_settings JSONB NOT NULL DEFAULT '{}',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Create trigger function for updating the 'updated_at' column
    cursor.execute("""
    CREATE OR REPLACE FUNCTION update_preferences_timestamp() 
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = CURRENT_TIMESTAMP;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)

    # Create the trigger for preferences table
    cursor.execute("""
    CREATE TRIGGER update_preferences_timestamp_trigger
    BEFORE UPDATE ON preferences
    FOR EACH ROW
    EXECUTE FUNCTION update_preferences_timestamp();
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS containers (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        container_id TEXT UNIQUE NOT NULL,
        status TEXT DEFAULT 'stopped',  -- Added status column for container state
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shared_containers (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        container_id TEXT NOT NULL,
        shared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (container_id) REFERENCES containers(container_id) ON DELETE CASCADE
    );
    """)

    print("Database tables created successfully.")

def initialize_database(rebuild=False):
    """Initialize the PostgreSQL database schema with an option to rebuild."""
    # Connect to the database
    connection = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cursor = connection.cursor()

    if rebuild:
        drop_tables(cursor)  # Drop all tables before creating new ones

    create_tables(cursor)  # Create the tables

    connection.commit()
    cursor.close()
    connection.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Initialize PostgreSQL database schema.")
    parser.add_argument("-rebuild", action="store_true", help="Rebuild the database (drop and recreate all tables).")
    args = parser.parse_args()

    # Initialize the database, optionally rebuilding it
    initialize_database(rebuild=args.rebuild)
