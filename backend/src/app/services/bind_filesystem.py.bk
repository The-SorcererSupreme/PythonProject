from flask import Flask, jsonify, request
import os
from flask_cors import CORS
from urllib.parse import unquote

app = Flask(__name__)
CORS(app, origins="*")

@app.route('/api/files', methods=['GET'])
def get_directory_structure():
    """Recursively fetch directory structure starting from a given base directory."""
    cwd = os.getcwd()
    subfolder = "../../../../"
    current_dir = os.path.abspath(os.path.join(cwd, subfolder))  # Ensure absolute path

    def list_files_and_folders(path):
        """Recursively lists the files and folders in a directory."""
        result = []
        try:
            for entry in os.scandir(path):
                if entry.is_dir():
                    result.append({
                        'name': entry.name,
                        'isFile': False,
                        'path': entry.path,  # Include the full path for folders
                        'children': list_files_and_folders(entry.path)  # Recurse into subdirectories
                    })
                elif entry.is_file():
                    result.append({
                        'name': entry.name,
                        'isFile': True,
                        'path': entry.path  # Include the full path for files
                    })
        except PermissionError:
            pass
        return result

    return jsonify(list_files_and_folders(current_dir))


@app.route('/api/getFile', methods=['GET'])
def fetch_file_content():
    """Fetch the content of a file from the provided path."""
    file_path = request.args.get('path')

    # Log the raw requested path
    print(f"Requested file path (raw): {file_path}")

    # Validate file path
    if not file_path:
        return jsonify({'success': False, 'error': 'File path not provided'}), 400
    
    # Decode the path to handle special characters correctly
    decoded_path = unquote(file_path)
    
    # Log the decoded path
    app.logger.debug(f"Decoded file path: {decoded_path}")

    # Sanitize the path to avoid directory traversal and ensure file access within a safe directory
    base_dir = os.getcwd()  # You can set a specific base directory here if needed
    full_path = os.path.abspath(os.path.join(base_dir, decoded_path))

    # Ensure the path is inside the base directory
    #if not full_path.startswith(base_dir):
    #    return jsonify({'success': False, 'error': 'Invalid file path (directory traversal detected)'}), 400

    # Ensure the file exists and is a valid file
    if not os.path.isfile(full_path):
        print(f"File not found: {full_path}")
        return jsonify({'success': False, 'error': 'File not found'}), 404

    try:
        with open(full_path, 'r') as file:
            content = file.read()
        return jsonify({'success': True, 'content': content})

    except Exception as e:
        print(f"Error reading file {full_path}: {str(e)}")
        return jsonify({'success': False, 'error': 'Error reading the file'}), 500


@app.route('/api/parent', methods=['GET'])
def get_parent_directory():
    """Get the parent directory of the current directory."""
    parent_dir = os.path.dirname(os.getcwd())
    return jsonify({'parent': parent_dir})


if __name__ == '__main__':
    app.run(debug=True)
