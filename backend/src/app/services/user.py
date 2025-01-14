# backend/src/app/services/user.py
from werkzeug.security import generate_password_hash, check_password_hash
#import jwt
#from datetime import datetime, timedelta

class User:
    def __init__(self, username, password=None):
        self.username = username
        self.password = password

    def register(self, db):
        """Register a new user."""
        # First, check if the username already exists in the database
        existing_user = db.fetch_query("SELECT * FROM users WHERE username = ?", (self.username,))
        
        if existing_user:
            # If a user with the same username exists, raise an error
            raise ValueError("Username already exists")

        # Proceed with registering the user if the username is unique
        hashed_password = generate_password_hash(self.password)
        query = "INSERT INTO users (username, password) VALUES (?, ?)"
        db.execute_query(query, (self.username, hashed_password))
        return f"User {self.username} registered successfully"

    def authenticate(self, db, password):
        """Authenticate a user."""
        user_data = db.fetch_query("SELECT * FROM users WHERE username = ?", (self.username,))
        if not user_data:
            raise ValueError("Invalid username or password")

        user = user_data[0]
        if check_password_hash(user["password"], password):
            return f"User {self.username} authenticated successfully"
        else:
            raise ValueError("Invalid password")
        
    def guest_login():
        # Generate a temporary token for guest users
        #token = jwt.encode(
        #    {"guest": True, "exp": datetime.utcnow() + timedelta(hours=1)},
        #    current_app.config["SECRET_KEY"],
        #    algorithm="HS256"
        #)
        return {"token": "token_123", "message": "Guest login successful"}, 200