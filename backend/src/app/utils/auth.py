# /backend/src/app/utils/auth.py
from functools import wraps
from flask import request, jsonify, current_app
import jwt
from app.classes.database_actions import Database

def token_required(f):
    """Decorator to check if the user is authenticated and has a valid session."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        # Extract token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            print(f"Authorization is set with: {auth_header}")
            if auth_header.startswith("Bearer "):
                token = auth_header.split("Bearer ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            secret_jwt_key = current_app.config['SECRET_JWT_KEY']
            decoded = jwt.decode(token, secret_jwt_key, algorithms=["HS256"])
            request.user = decoded  # Attach user info to request
            print(f"Decoded token: {decoded}")
            # Extract session_token and user_id from decoded token
            session_token = decoded.get("session_token")
            session_token = str(session_token)
            user_id = decoded.get("user_id")
            print(f"UserID={user_id} and Session_token={session_token}")

            #if not session_token or not user_id:
            #    return jsonify({'message': 'Invalid token payload!'}), 401
            # Verify session exists and matches the user
            user_session = get_user_session(session_token, user_id)
            if not user_session:
                return jsonify({'message': 'Session is invalid or expired!'}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(str(user_session), *args, **kwargs)

    return decorated_function


def get_user_session(session_token: str, user_id: int):
    """Retrieve the session linked to the token."""
    db = Database()
    print(f"SELECT id FROM sessions WHERE session_token = '{session_token}' AND user_id = {user_id};")
    result = db.fetch_query("SELECT id FROM sessions WHERE session_token = %s AND user_id = %s", (session_token, user_id))
    print(f"Result: {result[0]['id']}")
    return result[0]['id'] if result else None  # Return the user_id if session exists to use it in other modules