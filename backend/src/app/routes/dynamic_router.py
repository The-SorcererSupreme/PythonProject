from flask import Blueprint, request, jsonify, redirect, url_for
from app.routes.container_proxy import forward_request_to_container  # Import the forward_request_to_container function
from app.services.yaml_service import convert_json_array_to_yaml

dynamic_router = Blueprint("dynamic_router", __name__)

#print('inside dynamic router')
@dynamic_router.route('/api/getFile', methods=['GET'])
def handle_get_file():
    print('inside dynamic router')
    """
    Handles requests to fetch a file dynamically from any source.
    """
    endpoint = request.path
    file_path = request.args.get("path")  # File path as a query parameter
    container_id = request.args.get("containerID")

    print(f"File path received: {file_path}")
    
    # Check for the source, defaulting to 'container'
    source_type = "container"  # Dynamically set the source
    
    if not file_path:
        # If no file path is provided, return error
        return jsonify({"error": "File path is required"}), 400

    try:
        # Route the request based on the source type
        if source_type == "container":
            # Forward the request to the container_proxy if source is 'container'
            print("Routing to container with: ", file_path)
            return forward_request_to_container(endpoint, file_path, container_id)  # Call the function to forward to container
        
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

    except ValueError as e:
        # Handle known errors, e.g., if source type is invalid
        return jsonify({"error": str(e)}), 400
    except FileNotFoundError as e:
        # Handle cases where the file is not found
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        # Catch any other errors
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500



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








@dynamic_router.route('/api/saveFile', methods=['POST'])
def handle_save_file():
    """
    Handles saving a file content dynamically to the specified container.
    """
    endpoint = request.path
    file_path = request.args.get("path")  # File path as a query parameter
    container_id = request.args.get("containerID")  # Container ID as a query parameter
    format_type = request.json.get("format") # Get the format of the file/request
    content = request.json.get("content")  # File content from the request body

    if not file_path:
        return jsonify({"error": "File path is required"}), 400
    if not container_id:
        return jsonify({"error": "Container ID is required"}), 400
    if not content:
        return jsonify({"error": "File content is required"}), 400

    # Handle the logic to save the file content.
    try:
        print(f"Format type: {format_type}")
        # Convert JSON to YAML if format is YAML
        if format_type == "yaml":
            print("Converting JSON to YAML...")
            content = convert_json_array_to_yaml(content)  # Convert JSON to YAML string
            print(f"Converted json array to file: {content}")
        # Call the function that saves the file
        save_response = forward_request_to_container(endpoint, file_path, container_id, content)
        print(f"Save response: {save_response}")
        
        # Now create the response using the returned data
        return jsonify(save_response), 200

    except Exception as e:
        print(f"Error while saving file: {e}")
        return jsonify({"error": f"An error occurred while saving the file: {str(e)}"}), 500


def save_file_to_container(container_id, file_path, content):
    file_name = file_path  # Extract the file name from the full path
    print(f"Saving file {file_name} to container {container_id}")
    print(f"With content: {content}")

    return {"message": "File saved successfully", "saved_file" : file_name}