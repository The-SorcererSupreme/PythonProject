from flask import Blueprint, request, jsonify
from app.classes.user_actions import User
from app.classes.session_actions import Session
from app.utils.auth import token_required

auth_bp = Blueprint("auth", __name__)

def get_request_data():
    """Extract and validate username and password from request."""
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return None, None, jsonify({"error": "Username and password are required"}), 400

    return username, password, None, None

@auth_bp.route("/auth/register", methods=["POST"])
def register():
    """Register a new user."""
    username, password, error_response, status_code = get_request_data()
    if error_response:
        return error_response, status_code

    user = User(username, password)

    try:
        return jsonify({"message": user.register_user()}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

@auth_bp.route("/auth/login", methods=["POST"])
def login():
    """Authenticate a user and return JWT."""
    username, password, error_response, status_code = get_request_data()
    if error_response:
        return error_response, status_code

    user = User(username)

    try:
        return jsonify({"token": user.authenticate_user(password)}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

@auth_bp.route("/auth/guest", methods=["GET"])
def guest_login():
    """Guest login (currently not implemented)."""
    return jsonify({"message": User("guest").guest_login()})

@auth_bp.route("/auth/logout", methods=["POST"])
@token_required
def logout(session_id):
    """Log out the user by removing their session."""
    if Session().remove_session(session_id):
        return jsonify({"message": "Logged out successfully"}), 200
    return jsonify({"error": "Failed to log out"}), 500

@auth_bp.route("/api/files", methods=["GET"])
def upload_drag_drop():
    return jsonify("Uploaded")
