# backend/src/app/routes/aut_routes.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.services.user import User  # Import the User class
from app.services.database import Database

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
        registration_message = user.register(db)
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
        login_message = user.authenticate(db, password)
        return jsonify({"message": login_message}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401


@auth_bp.route("/auth/guest", methods=["GET"])
def guest_login():
    return jsonify(User.guest_login())

@auth_bp.route("/api/files", methods=["GET"])
def upload_drag_drop():
    return jsonify("Uploaded")