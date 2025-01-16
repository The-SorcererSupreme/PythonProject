from flask import Blueprint, request, jsonify, redirect, url_for
from app.utils.request_router import RequestRoutingMiddleware
from app.services.yaml_service import parse_yaml, analyze_yaml
import requests
from app.routes.container_proxy import forward_request_to_container  # Import the forward_request_to_container function

dynamic_router = Blueprint("dynamic_router", __name__)

print('inside dynamic router')
@dynamic_router.route('/api/getFile', methods=['GET'])
def handle_get_file():
    print('inside dynamic router')
    """
    Handles requests to fetch a file dynamically from any source.
    """
    file_path = request.args.get("path")  # File path as a query parameter
    print(f"File path received: {file_path}")
    
    # Check for the source, defaulting to 'container'
    source_type = request.args.get("source", "container")  # Dynamically set the source
    
    if not file_path:
        # If no file path is provided, return error
        return jsonify({"error": "File path is required"}), 400

    try:
        # Route the request based on the source type
        if source_type == "container":
            # Forward the request to the container_proxy if source is 'container'
            print("Routing to container")
            return forward_request_to_container(file_path)  # Call the function to forward to container
        
        elif source_type == "git":
            # Dummy logic for git source
            print("Routing to git source (dummy)")
            return jsonify({"message": "Git source dummy response"}), 200
        
        elif source_type == "agent":
            # Dummy logic for agent source
            print("Routing to agent source (dummy)")
            return jsonify({"message": "Agent source dummy response"}), 200
        
        elif source_type == "remote":
            # Dummy logic for remote source
            print("Routing to remote source (dummy)")
            return jsonify({"message": "Remote source dummy response"}), 200
        
        else:
            return jsonify({"error": f"Unknown source type: {source_type}"}), 400
        
        # Process the file based on its extension
        response_data = process_file(file_path, source_type)
        return jsonify(response_data["data"]), response_data["status"]

    except ValueError as e:
        # Handle known errors, e.g., if source type is invalid
        return jsonify({"error": str(e)}), 400
    except FileNotFoundError as e:
        # Handle cases where the file is not found
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        # Catch any other errors
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


def process_file(file_path, source_type):
    """
    Processes the file based on its extension and manipulates the response based on the source type.
    """
    # Check if file is YAML
    if file_path.endswith(('.yaml', '.yml')):
        print("It is YAML data")
        # Parse the YAML file content
        yaml_data = parse_yaml(file_path)

        if "error" in yaml_data:
            # Return error if YAML parsing fails
            return {"data": yaml_data, "status": 400}  # Error during YAML parsing

        # Analyze YAML and generate the form structure
        form_structure = analyze_yaml(yaml_data)
        
        # Modify form structure based on source type
        form_structure = modify_form_structure_for_source(form_structure, source_type)
        
        return {"data": {"form_structure": form_structure}, "status": 200}

    # Add logic here for other file types (JSON, XML, etc.) if needed
    # Example:
    # elif file_path.endswith('.json'):
    #     return process_json_file(file_path)

    # If the file is not YAML or other supported types, return error
    return {"data": {"error": "Unsupported file format. Only YAML files are allowed."}, "status": 400}


def modify_form_structure_for_source(form_structure, source_type):
    """
    Modifies the form structure based on the source type.
    """
    if source_type == "git":
        print("Modifying form structure for Git source")
        form_structure["source"] = "Git source"
        form_structure["message"] = "Form structure for Git source"
    
    elif source_type == "agent":
        print("Modifying form structure for Agent source")
        form_structure["source"] = "Agent source"
        form_structure["message"] = "Form structure for Agent source"
    
    elif source_type == "remote":
        print("Modifying form structure for Remote source")
        form_structure["source"] = "Remote source"
        form_structure["message"] = "Form structure for Remote source"
    
    return form_structure
