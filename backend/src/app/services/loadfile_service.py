# routes/loadfile_routes.py

from flask import Blueprint, request, jsonify
from services.yaml_service import parse_yaml

loadfile_bp = Blueprint('loadfile', __name__)

@loadfile_bp.route('/api/loadyaml', methods=['POST'])
def load_yaml():
    file_content = request.data.decode('utf-8')
    
    try:
        yaml_structure = parse_yaml(file_content)
        # Here, you could generate form inputs dynamically based on the YAML structure.
        # For simplicity, returning the parsed structure.
        return jsonify(yaml_structure)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
