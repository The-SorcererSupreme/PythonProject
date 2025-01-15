import os
from flask import jsonify


def loadfile_service(decoded_path):
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
            return jsonify({"success": False, "error": "File not found"}), 404

        with open(decoded_path, 'r') as file:
            content = file.read()

        return jsonify({"success": True, "content": content})

    except Exception as e:
        print(f"Error reading file {decoded_path}: {str(e)}")  # Log any errors during file reading
        return jsonify({"success": False, "error": str(e)}), 400
