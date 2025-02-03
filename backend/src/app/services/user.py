# backend/src/app/services/user.py
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import os
import jwt
from dotenv import load_dotenv

load_dotenv()
# Secret key for JWT encoding/decoding (should be stored securely)
SECRET_KEY = os.getenv("SECRET_JWT_KEY")

class User:
    def __init__(self, username, password=None):
        self.username = username
        self.password = password

    def register_user(self, db):
        """Register a new user."""
        # First, check if the username already exists in the database
        existing_user = db.fetch_query("SELECT * FROM users WHERE username = %s", (self.username,))
        
        if existing_user:
            # If a user with the same username exists, raise an error
            raise ValueError("Username already exists")

        # Proceed with registering the user if the username is unique
        hashed_password = generate_password_hash(self.password)
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        db.execute_query(query, (self.username, hashed_password))
        return f"User {self.username} registered successfully"

    def authenticate_user(self, db, password):
        """Authenticate a user and create a session with a JWT token."""
        # Check if the user exists in the database
        user_data = db.fetch_query("SELECT * FROM users WHERE username = %s", (self.username,))
        if not user_data:
            raise ValueError("Invalid username or password")

        user = user_data[0]
        
        # Check if the password is correct
        if not check_password_hash(user["password"], password):
            raise ValueError("Invalid password")

        # Generate a session token
        session_token = self.generate_session_token(user["id"])

        # Store the session in the database
        expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        db.execute_query("""
        INSERT INTO sessions (user_id, session_token, expires_at)
        VALUES (%s, %s, %s);
        """, (user["id"], session_token, expires_at))

        # Generate JWT token for the user
        jwt_token = self.generate_jwt(user["id"], session_token, expires_at)

        return jwt_token
        
    def guest_login(self):
        """Generate a temporary session for guest users."""
        return "Not implemented yet."
    

    def generate_session_token(self, user_id):
        """Generate a unique session token."""
        return str(user_id) + str(datetime.datetime.utcnow().timestamp())

    def generate_jwt(self, user_id, session_token, expires_at):
        """Generate JWT token for the authenticated user."""
        payload = {
            'user_id': user_id,
            'session_token': session_token,
            'exp': expires_at
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')