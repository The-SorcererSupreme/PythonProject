'''
from flask import Blueprint, jsonify, request
from app.services.fileupload_service import FileUploadDockerService

docker_bp = Blueprint("docker", __name__)
file_service = FileUploadDockerService()

@docker_bp.route("/api/docker/process-file", methods=["POST"])
def process_file():
    """Creates a container to process an uploaded file."""
    data = request.json
    file_path = data.get("file_path")

    if not file_path:
        return jsonify({"error": "File path is required"}), 400

    try:
        result = file_service.process_file(file_path)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
'''