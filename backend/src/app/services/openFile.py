from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
from urllib.parse import unquote

app = Flask(__name__)
CORS(app, origins="*")

@app.route('/api/getFile', methods=['GET'])
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

    try:
        # Check if the file exists before reading
        if not os.path.isfile(decoded_path):
            print(f"File not found: {decoded_path}")  # Log when the file does not exist
            return jsonify({"success": False, "error": "File not found"}), 404

        with open(decoded_path, 'r') as file:
            content = file.read()

        return jsonify({"success": True, "content": content})

    except Exception as e:
        print(f"Error reading file {decoded_path}: {str(e)}")  # Log any errors during file reading
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=6000)
