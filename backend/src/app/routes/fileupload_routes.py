# /PythonProject/backend/src/app/routes/fileupload_routes.py

from flask import Blueprint, request, jsonify
#from app.services.fileupload_service import FileUploadService
from app.services.docker_service import DockerService
# Define the blueprint
upload_file = Blueprint('upload_file', __name__)

# Define the route for file upload
@upload_file.route('/api/upload', methods=['POST'])
def upload_file_route():
    # Handle the file upload logic here
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    upload_type = 'drag_and_drop' # !!! NEEDS TO BE FETCHED FROM THE REQUEST
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Handle upload type
    if upload_type == 'drag_and_drop':
        print("Checking upload type")
        try:
            print("Launching Docker Service")
            archive_name = file.filename
            file_bytes = file.read() # Read file into memory 
            docker_service = DockerService()
            container_response = docker_service.process_file_in_container(file_bytes, archive_name)
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
