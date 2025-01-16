import requests
from flask import Blueprint, request, jsonify
from urllib.parse import urlencode
from app.services.yaml_service import convert_yaml_to_json_array
import logging
from pprint import pformat
import json
from urllib.request import urlopen

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(module)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %z'
)

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

def forward_request_to_container(endpoint, path):
    print(f"forward_request_to_container triggered with: {endpoint}, {path}")
    """
    Forward a request to the container's API, appending the file path in the query string.
    Args:
        endpoint (str): The endpoint to forward the request to.
        path (str): The file path to be passed as a query parameter.
    Returns:
        Flask Response: The container's response, rewrapped in a Flask response object.
    """
    # Use urlencode to safely encode the path for the query string
    query_string = urlencode({'path': path})
    url = f"{CONTAINER_BASE_URL}{endpoint}?{query_string}"  # Pass the path in the query string
    print(f"Forwarding request from container_proxy with path: ", url)
    
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
            container_response = convert_yaml_to_json_array(content_data, path)
            logging.info(f"{method} - Generated json: {container_response}")
            return jsonify({"content": container_response}, container_status)
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



# Handle GET requests to /api/file-structure and /api/getFile, which should be forwarded to the container
@container_proxy.route('/api/file-structure', methods=['GET'])
def proxy_file_structure():
    if is_container_route(request.path):
        # Get the file path from the request and forward it to the container
        file_path = request.args.get("path")  # Extract the path from the query parameters
        if file_path:
            # Forward the file path correctly with the query string
            return forward_request_to_container('/api/file-structure', file_path)
        else:
            return jsonify({"error": "File path is required"}), 400
    else:
        return jsonify({"error": "Invalid request path for container"}), 400