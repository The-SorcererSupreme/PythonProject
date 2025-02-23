-- Drop tables in reverse order to avoid foreign key constraint errors
DROP TABLE IF EXISTS shared_containers CASCADE;
DROP TABLE IF EXISTS containers CASCADE;
DROP TABLE IF EXISTS preferences CASCADE;
DROP TABLE IF EXISTS sessions CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create sessions table
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    session_token TEXT UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create preferences table
CREATE TABLE preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    layout_settings JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create trigger function for updating the 'updated_at' column
CREATE OR REPLACE FUNCTION update_preferences_timestamp() 
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger for preferences table
CREATE TRIGGER update_preferences_timestamp_trigger
BEFORE UPDATE ON preferences
FOR EACH ROW
EXECUTE FUNCTION update_preferences_timestamp();

-- Create containers table
CREATE TABLE containers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    container_id TEXT UNIQUE NOT NULL,
    container_name TEXT UNIQUE NOT NULL,
    status TEXT DEFAULT 'stopped',  -- Status column for container state
    host_port INTEGER UNIQUE NOT NULL,  -- Stores assigned host port
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create shared_containers table
CREATE TABLE shared_containers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    container_id INTEGER NOT NULL,
    shared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, container_id),
    FOREIGN KEY (container_id) REFERENCES containers(id) ON DELETE CASCADE
);

-- Print a message after successful initialization
DO $$ 
BEGIN 
    RAISE NOTICE 'Database tables created successfully.';
END $$;
