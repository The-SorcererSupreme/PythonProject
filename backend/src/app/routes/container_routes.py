# /backend/src/app/routes/container_routes.py
from flask import Blueprint, request, jsonify, current_app
from app.services.database import Database
#from app.services.docker_service import DockerService
from functools import wraps
from app.utils.auth import token_required  # Import the decorator


# Define the blueprint
container_routes = Blueprint('container_routes', __name__)

# Route to get the containers for the logged-in user
@container_routes.route('/api/containers', methods=['GET'])
@token_required  # Apply the token_required decorator to protect the route
def get_user_containers(session_id):
    
    # Fetch containers from the database for the user
    try:
        db = Database()
        if session_id:
            query = "SELECT user_id FROM sessions WHERE id = %s"
            user_id = db.fetch_query(query, (session_id,))
        print(f"Fetching containers from user_id: {user_id[0]['user_id']}")
        #user_id = request.user.get('user_id')  # Get the user ID from the token
        query = "SELECT * FROM containers WHERE user_id = %s"
        containers = db.fetch_query(query, (user_id[0]['user_id'],))
        return jsonify({
            'message': 'Containers fetched successfully',
            'containers': containers
        }), 200
    except Exception as e:
        return jsonify({'error': f"Error fetching containers: {e}"}), 500
