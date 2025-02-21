# /backend/src/app/routes/container_routes.py
from flask import Blueprint, request, jsonify, current_app
from app.classes.database_actions import Database
from functools import wraps
from app.classes.container_actions import DockerClientManager
from app.utils.auth import token_required  # Import the decorator


#from flask_cors import CORS
# Define the blueprint
container_routes = Blueprint('container_routes', __name__)
#CORS(container_routes)

# Route to get the containers for the logged-in user
@container_routes.route('/api/containers', methods=['GET'])
@token_required  # Apply the token_required decorator to protect the route
def get_user_containers(session_id):
    
    # Fetch containers from the database for the user
    try:
        print("Inside container_routes")
        db = Database()
        if session_id:
            query = "SELECT user_id FROM sessions WHERE id = %s"
            user_id = db.fetch_query(query, (session_id,))
            user_id = user_id[0]['user_id']
        print(f"Fetching containers from user_id: {user_id}")
        
        query = "SELECT * FROM containers WHERE user_id = %s"
        containers = db.fetch_query(query, (user_id,))

        # Initialize Docker client manager to fetch exsisting containers
        docker_manager = DockerClientManager()
        valid_containers = []

        for container in containers:
            try:
                container_id = container['container_id']
                print(f"Checking if container {container_id} exsists...")
                docker_manager.get_container(container_id)
                valid_containers.append(container)  # Keep the valid container
                print("It exsists!")
            except RuntimeError:
                # Container does not exist, delete it from the database
                print("It does not! Deleting from database...")
                query  = "DELETE FROM containers WHERE container_id = %s AND user_id = %s"
                db.execute_query(query, (container_id, user_id))
                print("Deleted container!")
        
        return jsonify({
            'message': 'Containers fetched successfully',
            'containers': containers
        }), 200
    except Exception as e:
        return jsonify({'error': f"Error fetching containers: {e}"}), 500
