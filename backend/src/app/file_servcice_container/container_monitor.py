from watchfiles import watch
import os
from flask import Flask, jsonify
from threading import Thread
import zipfile
import tarfile

app = Flask(__name__)

# Directory to monitor (this is the container's workspace)
workspace_path = "/workspace"

# Extracts the acrhive
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

# This function will return the directory structure as a dictionary
def get_directory_structure(root_dir):
    dir_structure = {}
    for root, dirs, files in os.walk(root_dir):
        root_dir_name = os.path.relpath(root, workspace_path)
        dir_structure[root_dir_name] = {
            "files": files,
            "subdirs": {d: [] for d in dirs}
        }
    return dir_structure

@app.route('/api/file-structure', methods=['GET'])
def get_file_structure():
    """Endpoint to return the folder structure."""
    try:
        # Extract the uploaded archive (assume it's already in /workspace/archive.zip)
        archive_path = os.path.join(workspace_path, "archive.zip")  # Change filename as needed
        extract_archive(archive_path, workspace_path)

        # Generate the folder structure after extraction
        folder_structure = get_directory_structure(workspace_path)
        return jsonify(folder_structure), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
