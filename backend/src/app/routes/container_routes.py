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
        print(f"Available containers for user with id {user_id}:\n{containers}")
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


@container_routes.route('/api/containers/update-name', methods=['PUT'])
@token_required  # Ensure user authentication
def update_container_name(session_id):
    try:
        data = request.get_json()
        container_id = data.get('id')
        new_name = data.get('name')

        if not container_id or not new_name:
            return jsonify({'error': 'Missing container ID or name'}), 400

        # Fetch the user ID based on session_id
        db = Database()
        query = "SELECT user_id FROM sessions WHERE id = %s"
        user_id_result = db.fetch_query(query, (session_id,))

        if not user_id_result:
            return jsonify({'error': 'Invalid session'}), 403

        user_id = user_id_result[0]['user_id']

        # Check if the container belongs to the user
        query = "SELECT * FROM containers WHERE id = %s AND user_id = %s"
        container = db.fetch_query(query, (container_id, user_id))

        if not container:
            return jsonify({'error': 'Container not found or unauthorized'}), 404

        # Rename the container in Docker
        docker_manager = DockerClientManager()
        rename_result = docker_manager.rename_container(container[0]['container_id'], new_name)
        print(rename_result)

        # Update the container name in the database
        update_query = "UPDATE containers SET container_name = %s WHERE id = %s AND user_id = %s"
        db.execute_query(update_query, (new_name, container_id, user_id))

        return jsonify({'message': 'Container name updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': f"Error updating container name: {e}"}), 500
    



@container_routes.route('/api/containers/start', methods=['POST'])
@token_required
def start_container(session_id):
    try:
        # Retrieve the containerId sent from the frontend
        data = request.get_json()
        container_id_from_db = data.get('containerId')

        # Initialize the database and Docker manager
        db = Database()
        
        # Fetch the real Docker container ID from the database
        query = "SELECT container_id FROM containers WHERE id = %s"
        result = db.fetch_query(query, (container_id_from_db,))
        
        if not result:
            return jsonify({'error': 'Container not found in the database'}), 404
        
        real_container_id = result[0]['container_id']
        
        # Now use the real Docker container ID to start the container
        docker_manager = DockerClientManager()
        status = docker_manager.start_container(real_container_id)

        # Update the status in the database
        update_query = "UPDATE containers SET status = %s WHERE id = %s"
        db.execute_query(update_query, (status, container_id_from_db))

        return jsonify({'message': f"Container started. Current status: {status}"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@container_routes.route('/api/containers/stop', methods=['POST'])
@token_required
def stop_container(session_id):
    try:
        # Retrieve the containerId sent from the frontend
        data = request.get_json()
        container_id_from_db = data.get('containerId')

        # Initialize the database and Docker manager
        db = Database()
        
        # Fetch the real Docker container ID from the database
        query = "SELECT container_id FROM containers WHERE id = %s"
        result = db.fetch_query(query, (container_id_from_db,))
        
        if not result:
            return jsonify({'error': 'Container not found in the database'}), 404
        
        real_container_id = result[0]['container_id']
        
        # Now use the real Docker container ID to stop the container
        docker_manager = DockerClientManager()
        status = docker_manager.stop_container(real_container_id)

        # Update the status in the database
        update_query = "UPDATE containers SET status = %s WHERE id = %s"
        db.execute_query(update_query, (status, container_id_from_db))

        return jsonify({'message': f"Container stopped. Current status: {status}"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@container_routes.route('/api/containers/delete', methods=['POST'])
@token_required
def delete_container(session_id):
    try:
        # Retrieve the containerId sent from the frontend
        data = request.get_json()
        container_id_from_db = data.get('containerId')

        # Initialize the database and Docker manager
        db = Database()

        # Fetch the real Docker container ID and the name from the database
        query = "SELECT container_id, container_name FROM containers WHERE id = %s"
        result = db.fetch_query(query, (container_id_from_db,))

        if not result:
            return jsonify({'error': 'Container not found in the database'}), 404
        
        real_container_id = result[0]['container_id']
        container_name = result[0]['container_name']

        # Initialize Docker manager and attempt to remove the container
        docker_manager = DockerClientManager()
        message = docker_manager.remove_container(real_container_id)

        # If the container was successfully removed, remove it from the database as well
        delete_query = "DELETE FROM containers WHERE id = %s"
        db.execute_query(delete_query, (container_id_from_db,))

        return jsonify({'message': f"Container '{container_name}' deleted successfully. {message}"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


@container_routes.route('/api/containers/share', methods=['POST'])
@token_required
def share_container(session_id):
    try:
        data = request.get_json()
        container_id_from_db = data.get('containerId')
        target_user_id = data.get('userId')

        # Fetch the container's owner from the database
        db = Database()
        query = "SELECT user_id, container_name FROM containers WHERE container_id = %s"
        result = db.fetch_query(query, (container_id_from_db,))

        if not result:
            return jsonify({'error': 'Container not found in the database'}), 404

        container_owner_id = result[0]['user_id']
        container_name = result[0]['container_name']

        # Only the owner can share the container
        if container_owner_id != session_id:
            return jsonify({'error': 'You are not the owner of this container.'}), 403

        # Share the container with the target user
        insert_query = """
        INSERT INTO shared_containers (user_id, container_id)
        VALUES (%s, %s) ON CONFLICT (user_id, container_id) DO NOTHING;
        """
        db.execute_query(insert_query, (target_user_id, container_id_from_db))

        return jsonify({'message': f"Container '{container_name}' shared successfully with user {target_user_id}."}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@container_routes.route('/api/containers/revoke', methods=['POST'])
@token_required
def revoke_access(session_id):
    try:
        data = request.get_json()
        container_id_from_db = data.get('containerId')
        target_user_id = data.get('userId')

        # Fetch the container's owner from the database
        db = Database()
        query = "SELECT user_id, container_name FROM containers WHERE container_id = %s"
        result = db.fetch_query(query, (container_id_from_db,))

        if not result:
            return jsonify({'error': 'Container not found in the database'}), 404

        container_owner_id = result[0]['user_id']
        container_name = result[0]['container_name']

        # Only the owner can revoke access
        if container_owner_id != session_id:
            return jsonify({'error': 'You are not the owner of this container.'}), 403

        # Revoke access for the target user
        delete_query = "DELETE FROM shared_containers WHERE container_id = %s AND user_id = %s"
        db.execute_query(delete_query, (container_id_from_db, target_user_id))

        return jsonify({'message': f"Access to container '{container_name}' revoked for user {target_user_id}."}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@container_routes.route('/api/containers/access', methods=['GET'])
@token_required
def get_container_access(session_id):
    try:
        container_id_from_db = request.args.get('containerId')

        # Fetch users who have access to the container
        db = Database()
        query = """
        SELECT u.username, u.id
        FROM users u
        JOIN shared_containers sc ON u.id = sc.user_id
        WHERE sc.container_id = %s;
        """
        result = db.fetch_query(query, (container_id_from_db,))

        if not result:
            return jsonify({'message': 'No users have access to this container.'}), 404

        return jsonify({'users_with_access': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500