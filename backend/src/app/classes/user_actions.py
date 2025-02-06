from werkzeug.security import generate_password_hash, check_password_hash
from app.classes.database_actions import Database
from app.classes.session_actions import Session

class User:
    def __init__(self, username, password=None):
        self.username = username
        self.password = password
        self.db = Database()

    def register_user(self):
        """Register a new user."""
        existing_user = self.db.fetch_query("SELECT * FROM users WHERE username = %s", (self.username,))
        
        if existing_user:
            raise ValueError("Username already exists")

        hashed_password = generate_password_hash(self.password)
        self.db.execute_query("INSERT INTO users (username, password) VALUES (%s, %s)", (self.username, hashed_password))
        return f"User {self.username} registered successfully"

    def authenticate_user(self, password):
        """Authenticate a user and create a session."""
        user_data = self.db.fetch_query("SELECT * FROM users WHERE username = %s", (self.username,))
        if not user_data:
            raise ValueError("Invalid username or password")

        user = user_data[0]
        if not check_password_hash(user["password"], password):
            raise ValueError("Invalid username or password")

        # Create session using Session class
        session_service = Session()
        jwt_token = session_service.create_session(user["id"])

        return jwt_token

    def guest_login(self):
        """Generate a temporary session for guest users."""
        return "Not implemented yet."
