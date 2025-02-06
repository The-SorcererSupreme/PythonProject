import datetime
import jwt
import os
from app.classes.database_actions import Database
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_JWT_KEY")

class Session:
    def __init__(self):
        self.db = Database()

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

    def create_session(self, user_id):
        """Create a new session and return a JWT token."""
        session_token = self.generate_session_token(user_id)
        expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)

        # Store the session in the database
        self.db.execute_query(
            "INSERT INTO sessions (user_id, session_token, expires_at) VALUES (%s, %s, %s);",
            (user_id, session_token, expires_at)
        )

        return self.generate_jwt(user_id, session_token, expires_at)

    def remove_session(self, session_id):
        """Remove a session by ID."""
        query = "DELETE FROM sessions WHERE id = %s RETURNING id;"
        deleted_row = self.db.delete_query(query, (session_id,))
        return bool(deleted_row)  # Returns True if a session was deleted
