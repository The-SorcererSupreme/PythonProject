from flask import Flask, jsonify
import os
from flask_cors import CORS

app = Flask(__name__)

CORS(app, origins="http://localhost:4200")

@app.route('/api/files', methods=['GET'])
def get_directory_structure():
    # Fetch the current directory
    cwd = os.getcwd()
    subfolder = "src/app/"
    current_dir = os.path.join(cwd, subfolder)

    def list_files_and_folders(path):
        """Recursively lists the files and folders in a directory."""
        result = []
        try:
            for entry in os.scandir(path):
                if entry.is_dir():
                    result.append({
                        'name': entry.name,
                        'isFile': False,
                        'children': list_files_and_folders(entry.path)
                    })
                elif entry.is_file():
                    result.append({
                        'name': entry.name,
                        'isFile': True
                    })
        except PermissionError:
            pass
        return result

    # The root directory to start from can be passed, here we're starting from current_dir
    return jsonify(list_files_and_folders(current_dir))

@app.route('/api/parent', methods=['GET'])
def get_parent_directory():
    # Get the parent directory of the current directory
    parent_dir = os.path.dirname(os.getcwd())
    return jsonify({'parent': parent_dir})

if __name__ == '__main__':
    app.run(debug=True)
