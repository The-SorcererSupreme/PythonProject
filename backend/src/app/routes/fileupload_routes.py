# /PythonProject/backend/src/app/routes/fileupload_routes.py

from flask import Blueprint, request, jsonify, current_app
#from app.services.fileupload_service import FileUploadService
from app.services.docker_service import DockerService
from app.utils.auth import token_required  # Import the decorator
import jwt
from functools import wraps

# Define the blueprint
upload_file = Blueprint('upload_file', __name__)

# Define the route for file upload
@upload_file.route('/api/upload', methods=['POST'])
@token_required  # Apply the token_required decorator to protect the route
def upload_file_route(user_session):
    user_id = request.user.get('user_id') # Get the user ID from the token
    # Handle the file upload logic here
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    upload_type = 'drag_and_drop'  # !!! NEEDS TO BE FETCHED FROM THE REQUEST (you can fetch it from the form data or request body)
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Handle upload type
    if upload_type == 'drag_and_drop':
        print("Checking upload type")
        try:
            print("Launching Docker Service")
            archive_name = file.filename
            file_bytes = file.read()  # Read file into memory
            docker_service = DockerService()
            container_response = docker_service.process_file_in_container(file_bytes, archive_name, user_id)
            return jsonify({
                'message': 'File uploaded and processed successfully',
                'container_id': container_response['container_id'],
                'container_status': container_response['status'],
                'file_structure': container_response['file_structure']
            }), 200
        except Exception as e:
            return jsonify({'error': f'Failed to process file in Docker container: {e}'}), 500
    else:
        return jsonify({'error': f'Unknown upload type: {upload_type}'}), 400