import requests
from flask import Blueprint, request, jsonify
from urllib.parse import urlencode
from app.services.yaml_service import convert_yaml_to_json_array
import logging
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
CONTAINER_ROUTES = ['/api/file-structure', '/api/getFile']

# Create a Blueprint for the proxy
container_proxy = Blueprint("container_proxy", __name__)

def get_container_ip(container_id):
    """
    Fetch the IP address of a running container given its containerId.
    """
    try:
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
    

def forward_request_to_container(endpoint, path, container_id):
    print(f"forward_request_to_container triggered with: {endpoint}, {path}")
    """
    Forward a request to the container's API, appending the file path in the query string.
    Args:
        endpoint (str): The endpoint to forward the request to.
        path (str): The file path to be passed as a query parameter.
    Returns:
        Flask Response: The container's response, rewrapped in a Flask response object.
    """
    if not container_id:
        return jsonify({"error": "Container ID is required"}), 400
    # Fetch the correct container's IP dynamically
    container_ip = get_container_ip(container_id)
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
                container_response = convert_yaml_to_json_array(content_data, path)
                logging.info(f"{method} - Generated json: {container_response}")
                return container_response
            else:
                return content_data, {'success' : True}
        elif request.method == "POST":
            method = "POST"
            # Forward POST request with JSON data
            container_response = requests.post(url, json=request.json)
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
def proxy_file_structure(container_id):
    print(f"Calling container file structure for: {container_id}")
    if is_container_route(request.path):
        # Get the file path from the request and forward it to the container
        file_path = request.args.get("path")  # Extract the path from the query parameters
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