from watchfiles import watch
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
def extract_archive(file_path, extract_to):
    """Extracts an archive file to the specified directory."""
    try:
        if file_path.endswith(".zip"):
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                zip_ref.extractall(extract_to)
        elif file_path.endswith((".tar.gz", ".tgz", ".tar")):
            with tarfile.open(file_path, "r:*") as tar_ref:
                tar_ref.extractall(extract_to)
        else:
            raise ValueError(f"Unsupported archive format: {file_path}")
    except Exception as e:
        raise RuntimeError(f"Failed to extract archive '{file_path}': {e}")


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
        # Extract the uploaded archive (assume it's already in /workspace/archive.zip)
        archive_path = os.path.join(workspace_path, "test.zip")  # Change filename as needed
        extract_archive(archive_path, workspace_path)

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


if __name__ == "__main__":
    # Start monitoring the directory in a separate thread
    monitor_thread = Thread(target=monitor_directory, daemon=True)
    monitor_thread.start()

    # Start Flask app
    app.run(host='0.0.0.0', port=6000)
