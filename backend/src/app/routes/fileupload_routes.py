# /app/routes/file_upload.routes.py

from flask import Blueprint, request, jsonify
from app.services.fileupload_service import FileUploadService
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
    #upload_type = request.form.get('upload_type', 'drag_and_drop')  # Default to drag-and-drop upload
    upload_type = 'drag_and_drop'
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Process the file (e.g., save it, validate it, etc.)
    file_upload_service = FileUploadService()
    file_path = file_upload_service.save_uploaded_file(file)
    archive_name = file.filename
    print("Path: ", file_path, "File: ", archive_name)

    # Here you can add any Docker logic or further processing
    # For example, calling the Docker container service to process the file
    if upload_type == 'drag_and_drop':
        print("Checking upload type")
        try:
            print("Launching Docker Service")
            docker_service = DockerService()
            container_response = docker_service.process_file_in_container(file_path, archive_name)
            return jsonify({
                'message': 'File uploaded and processed successfully',
                'container_id': container_response['container_id']
            }), 200
        except Exception as e:
            return jsonify({'error': f'Failed to process file in Docker container: {e}'}), 500
    else:
        return jsonify({'error': f'Unknown upload type: {upload_type}'}), 400
