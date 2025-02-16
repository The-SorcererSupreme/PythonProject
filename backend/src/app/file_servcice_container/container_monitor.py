from watchfiles import watch
import logging
import os
from flask import Flask, jsonify, request
from threading import Thread
import zipfile
import tarfile
import time
from urllib.parse import unquote
from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins="*")

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set logging level
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.StreamHandler()  # Log to stdout (Docker will capture this)
    ]
)

# Directory to monitor (this is the container's workspace)
workspace_path = "/workspace"

# === File Content Service ===
def load_file_content(decoded_path):
    """
    Load the content of a file given its decoded path.
    Args:
        decoded_path (str): The file path to read.
    Returns:
        Response: JSON response with file content or error details.
    """
    try:
        # Check if the file exists before reading
        if not os.path.isfile(decoded_path):
            print(f"File not found: {decoded_path}")  # Log when the file does not exist
            return {"success": False, "error": "File not found"}, 404

        with open(decoded_path, 'r') as file:
            content = file.read()

        return {"success": True, "content": content}, 200

    except Exception as e:
        print(f"Error reading file {decoded_path}: {str(e)}")  # Log any errors during file reading
        return {"success": False, "error": str(e)}, 400


@app.route('/api/getFile', methods=['GET'])
def get_file_content():
    """
    Endpoint to return the content of a requested file.
    Expects a 'path' parameter in the query string.
    """
    # Get the file path from the query string
    file_path = request.args.get('path')

    # Log the requested path
    print(f"Requested file path (raw): {file_path}")

    if file_path is None:
        return jsonify({"success": False, "error": "File path not provided"}), 400

    # Decode the path to handle special characters correctly
    decoded_path = unquote(file_path)

    # Log the decoded path
    print(f"Decoded file path: {decoded_path}")

    # Call the file content service
    result, status_code = load_file_content(decoded_path)
    return jsonify(result), status_code


# === Directory Structure Service ===

def get_directory_structure(directory):
    """Recursively generate a dictionary-like structure of the directory."""
    folder_structure = []

    for entry in os.scandir(directory):
        if entry.is_dir():
            # Recursively process the subdirectory
            folder_structure.append({
                "name": entry.name,
                "isFile": False,
                "path": entry.path,
                "children": get_directory_structure(entry.path)  # Recursive call
            })
        elif entry.is_file():
            folder_structure.append({
                "name": entry.name,
                "isFile": True,
                "path": entry.path
            })

    return folder_structure


@app.route('/api/file-structure', methods=['GET'])
def get_file_structure():
    """Endpoint to return the folder structure."""
    try:
        # Generate the folder structure after extraction
        folder_structure = get_directory_structure(workspace_path)
        return jsonify(folder_structure), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# === Directory Monitoring ===
def monitor_directory():
    """Monitor the directory and update structure when changes occur."""
    print(f"Monitoring {workspace_path}")
    for changes in watch(workspace_path):
        for change in changes:
            print(f"Change detected: {change}")
            # Optionally, update internal state, but for now we expose on-demand
            # Update the file structure or trigger any needed actions here.

@app.route('/api/saveFile', methods=['POST'])
def save_file():
    """
    Endpoint to save file content to a specified file path inside the container.
    Expects:
    - Query parameter `path` indicating the file path
    - JSON body with `content` field containing file content
    """
    # Extract the file path from query parameters
    file_path = request.args.get('path')

    # Ensure the file path is provided
    if not file_path:
        return jsonify({"success": False, "error": "File path not provided"}), 400

    # Decode the file path
    decoded_path = unquote(file_path)

    # Extract file content from request body
    request_data = request.get_json()
    if not request_data or 'content' not in request_data:
        return jsonify({"success": False, "error": "File content not provided"}), 400

    file_content = request_data['content']

    try:
        os.makedirs(os.path.dirname(decoded_path), exist_ok=True)

        with open(decoded_path, 'w') as file:
            file.write(file_content)

        logging.info(f"File saved successfully: {decoded_path}")

        response = jsonify({"success": True, "message": f"File saved: {decoded_path}"})
        return response  # Return only jsonify object

    except Exception as e:
        logging.error(f"Error saving file {decoded_path}: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
    
    



if __name__ == "__main__":
    # Start monitoring the directory in a separate thread
    monitor_thread = Thread(target=monitor_directory, daemon=True)
    monitor_thread.start()

    # Start Flask app
    app.run(host='0.0.0.0', port=6000)
