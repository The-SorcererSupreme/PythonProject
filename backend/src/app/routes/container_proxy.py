import requests
from flask import Blueprint, request, jsonify, send_file
import zipfile
from urllib.parse import urlencode
from app.services.yaml_service import convert_yaml_to_json_array
from app.classes.database_actions import Database
import logging
from io import BytesIO
from pprint import pformat
import json
from urllib.request import urlopen
import docker
from app.utils.auth import token_required  # Token required to get file-strucutre


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(module)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %z'
)

ALLOWED_FILE_EXTENSIONS = ['.yml', '.yaml']
# Configuration: Update container host and port as needed
CONTAINER_HOST = "http://172.17.0.2"  # Replace with container's hostname/IP
CONTAINER_PORT = 6000               # Port exposed by the container
CONTAINER_BASE_URL = f"{CONTAINER_HOST}:{CONTAINER_PORT}"

# Backend routes (for non-container requests like auth)
BACKEND_ROUTES = ['/auth']

# Define the container-specific routes
CONTAINER_ROUTES = ['/api/file-structure', '/api/getFile', '/api/containers/export']

# Create a Blueprint for the proxy
container_proxy = Blueprint("container_proxy", __name__)

def get_container_ip(container_id):
    """
    Fetch the IP address of a running container given its containerId.
    """
    try:
        db = Database()  # Initialize the Database class
        query = """
        SELECT container_id FROM containers WHERE id = %s
        """
        result = db.fetch_query(query, (container_id,))
        print("Querying container_id")
        if result:  # If the container ID exists in the database
            container_id = result[0]['container_id']
            print(f"Fetched container ID from database: {container_id}")
            print("Found a container_id")
            client = docker.from_env()  # Connect to Docker API
            container = client.containers.get(container_id)  # Get the container by ID

            # Extract the IP address from the container's network settings
            container_ip = container.attrs['NetworkSettings']['IPAddress']
            return container_ip

    except docker.errors.NotFound:
        logging.error(f"Container with ID {container_id} not found.")
        return None
    except docker.errors.APIError as e:
        logging.error(f"Docker API error: {str(e)}")
        return None
    

def forward_request_to_container(endpoint, path, container_id, content=None):
    print(f"forward_request_to_container triggered with: {endpoint}, {path}")
    """
    Forward a request to the container's API, appending the file path in the query string.
    Args:
        endpoint (str): The endpoint to forward the request to.
        path (str): The file path to be passed as a query parameter.
    Returns:
        Flask Response: The container's response, rewrapped in a Flask response object.
    """
    # print(f"--------------CONTENT IS: {content}")
    if not container_id:
        return jsonify({"error": "Container ID is required"}), 400
    # Fetch the correct container's IP dynamically
    print(f"Calling IP for container ID: {container_id}")
    container_ip = get_container_ip(container_id)
    print(f"Container IP: {container_ip}")
    if not container_ip:
        return jsonify({"error": f"Could not determine IP for container {container_id}"}), 500
    

    # Construct the correct container URL
    container_url = f"http://{container_ip}:{CONTAINER_PORT}{endpoint}"
    query_string = urlencode({'path': path, 'containerId': container_id})
    url = f"{container_url}?{query_string}"  # Append query params
    print(f"Forwarding request to container URL: {url}")

    # Handle the request based on its method
    try:
        if request.method == "GET":
            method = "GET"
            # Forward GET request with query parameters
            container_response = urlopen(url)
            container_status = container_response.getcode()
            logging.info(f"{method} - Container status code: {container_status}")
            json_content = container_response.read()
            content_data = json.loads(json_content)
            logging.info(f"{method} - Container responded with: {content_data}")
        
            if is_allowed_file_extension(path):
                # Attempt to convert YAML to JSON
                generated_json = convert_yaml_to_json_array(content_data, path)
                logging.info(f"{method} - Generated json: {generated_json}")
        
                # Check if the response indicates success or failure
                if generated_json.get('success') is False:
                    # If conversion fails, return the original content_data
                    logging.error(f"YAML to JSON conversion failed: {generated_json.get('content')}")
                    return content_data  # Return the original content data in case of failure
                else:
                    # If conversion is successful, return the generated JSON
                    return generated_json
            else:
                # If file extension is not allowed, return the content data
                return content_data, {'success': True}
        elif request.method == "POST":
            method = "POST"
            print(f"Received {method} request with body: {request.json}")
            # **Ensure content is correctly extracted**
            if content:
                print(f"Content passed explicitly: {content}")
                # **Wrap the content in a proper JSON structure**
                payload = {"content": content}
            elif "content" in request.json:
                print(f"Content from request: {json.dumps(request.json['content'], indent=2)}")
            else:
                if "containerId" in request.json:
                    print("Set payload to 'export'")
                    payload = "export"
                else:
                    print("No content found in request.")


            # Forward POST request with updated JSON data
            container_response = requests.post(url, json=payload)
            # container_response = requests.post(url, json=request.json)
            # If it's an export, handle the response differently
            if payload == "export":
                # If the container responds with a file (ZIP), handle it appropriately
                if container_response.status_code == 200:
                    # Assume the response contains the zip file
                    return send_file(
                        BytesIO(container_response.content), 
                        as_attachment=True, 
                        mimetype='application/zip', 
                        download_name='workspace_export.zip'
                    )
                else:
                    # If export fails, return an error message
                    return jsonify({"error": "Failed to export the container's workspace."}), 500


            json_content = container_response.text
            #logging.info(f"{method} - Raw container response: {json_content}")  
            content_data = json.loads(json_content)
            #logging.info(f"{method} - Container response: {content_data}")
            return container_response.json(), container_response.status_code
        elif request.method == "PUT":
            method = "PUT"
            # Forward PUT request with JSON data
            container_response = requests.put(url, json=request.json)
        elif request.method == "DELETE":
            method = "DELETE"
            # Forward DELETE request
            container_response = requests.delete(url)
        else:
            # Unsupported HTTP method
            return jsonify({"error": f"Unsupported method: {request.method}"}), 405

        # Return the container's response
        logging.info(f"Form generator provided: {container_response}")
        return jsonify(container_response.json()), container_response.status_code

    except requests.exceptions.RequestException as e:
        # Handle errors communicating with the container
        return jsonify({"error": f"Error forwarding request to container: {str(e)}"}), 500

# Check if the request is meant for a container route.
def is_container_route(route):
    """
    Check if the request is meant for a container route.
    Args:
        route (str): The route or endpoint of the request.
    Returns:
        bool: True if the request is for a container route, False otherwise.
    """
    return any(route.startswith(container_route) for container_route in CONTAINER_ROUTES)


def is_allowed_file_extension(file_path):
    """
    Checks if the file path has an allowed extension.
    """
    return any(file_path.endswith(ext) for ext in ALLOWED_FILE_EXTENSIONS)

# Handle GET requests to /api/file-structure and /api/getFile, which should be forwarded to the container
@container_proxy.route('/api/file-structure', methods=['GET'])
@token_required
def proxy_file_structure(user_session):
    print(f"Calling container file structure for user session: {user_session}")
    print(f"request args: {request.args}")
    if is_container_route(request.path):
        # Get the file path from the request and forward it to the container
        file_path = "/workspace/"  # Workspace path of container
        container_id = request.args.get("containerId")  # Extract containerId
        print(f"File path: {file_path}")
        print(f"containerID: {container_id}")

        if file_path and container_id:
            # Forward the file path correctly with the query string
            return forward_request_to_container('/api/file-structure', file_path, container_id)
        else:
            return jsonify({"error": "File path is required"}), 400
    else:
        return jsonify({"error": "Invalid request path for container"}), 400
    

@container_proxy.route('/api/containers/export', methods=['POST'])
@token_required
def export_container(user_session):
        data = request.get_json()
        print(f"Exporting container file structure for user session: {user_session}")
        if is_container_route(request.path):
            # Get the file path from the request and forward it to the container
            file_path = "/workspace/"  # Workspace path of container
            container_id = data.get('containerId')  # Extract containerId
            print(f"containerID: {container_id}")
            # Verify that the user is the owner of the container (security)
            if container_id:
                # Forward the file path correctly with the query string
                return forward_request_to_container('/api/containers/export', file_path, container_id)
            else:
                return jsonify({"error": "File path is required"}), 400
        else:
            return jsonify({"error": "Invalid request path for container"}), 400