from flask import Blueprint, jsonify, request
from urllib.parse import unquote
from app.services.loadfile_service import loadfile_service

load_file = Blueprint("load_file", __name__)

@load_file.route('/api/getFile', methods=['GET'])
def get_file_content():
    # Get the path from the query string
    file_path = request.args.get('path')
    
    # Log the requested path
    print(f"Requested file path (raw): {file_path}")

    if file_path is None:
        return jsonify({"success": False, "error": "File path not provided"}), 400

    # Decode the path to handle special characters correctly
    decoded_path = unquote(file_path)
    
    # Log the decoded path
    print(f"Decoded file path: {decoded_path}")

    # Use the service to load the file content
    return loadfile_service(decoded_path)
