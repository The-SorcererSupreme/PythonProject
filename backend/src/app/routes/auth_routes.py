# backend/src/app/routes/aut_routes.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.services.user import User  # Import the User class
from app.services.database import Database
from app.services.session import Session  # Import session management logic
from app.utils.auth import token_required  # Token required for logout

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/register", methods=["POST"])
def register():
    """Register a new user."""
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Create a User instance
    user = User(username, password)

    # Create a Database instance and connect
    db = Database()
    
    try:
        # Attempt to register the user in the database
        registration_message = user.register_user(db)
        return jsonify({"message": registration_message}), 201
    except ValueError as e:
        # Handle the case where the username already exists
        return jsonify({"error": str(e)}), 409

@auth_bp.route("/auth/login", methods=["POST"])
def login():
    """Authenticate a user."""
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Create a Database instance and connect
    db = Database()
    user = User(username, password)

    # Attempt to authenticate the user
    try:
        login_message = user.authenticate_user(db, password)
        return jsonify({"token": login_message}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

@auth_bp.route("/auth/guest", methods=["GET"])
def guest_login():
    return jsonify(User.guest_login())

@auth_bp.route("/auth/logout", methods=["POST"])
@token_required
def logout(session_id):
    """Log out the user by removing their session token."""
    print(f"Logging out of session {session_id}")
    db = Database()
    session = Session()

    # Remove the session using the session ID
    if session.remove_session(db, session_id):
        return jsonify({"message": "Logged out successfully"}), 200

    return jsonify({"error": "Failed to log out"}), 500

@auth_bp.route("/api/files", methods=["GET"])
def upload_drag_drop():
    return jsonify("Uploaded")