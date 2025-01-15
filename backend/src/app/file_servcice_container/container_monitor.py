from watchfiles import watch
import os
from flask import Flask, jsonify
from threading import Thread

app = Flask(__name__)

# Directory to monitor (this is the container's workspace)
workspace_path = "/workspace"

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
    """Expose the current file structure as a JSON response."""
    return jsonify(get_directory_structure(workspace_path))

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
    app.run(host='0.0.0.0', port=5000)
