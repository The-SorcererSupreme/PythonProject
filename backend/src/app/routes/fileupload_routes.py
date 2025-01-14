# /app/routes/file-upload.route.py

from flask import Blueprint, request, jsonify
from app.services.fileupload_service import FileUploadService

file_upload_blueprint = Blueprint('file_upload', __name__)

@file_upload_blueprint.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Process the file using the service
    file_upload_service = FileUploadService()
    filepath = file_upload_service.save_uploaded_file(file)

    # Here you can add any Docker logic or further processing
    # For example, calling the Docker container service to process the file

    return jsonify({'message': 'File uploaded successfully', 'path': filepath}), 200
