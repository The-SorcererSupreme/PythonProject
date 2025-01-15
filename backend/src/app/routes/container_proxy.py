import requests
from flask import Blueprint, request, jsonify
#from services.container_request_forwarder import ContainerRequestForwarder

# Configuration: Update container host and port as needed
CONTAINER_HOST = "http://172.17.0.2"  # Replace with container's hostname/IP
CONTAINER_PORT = 6000               # Port exposed by the container
CONTAINER_BASE_URL = f"{CONTAINER_HOST}:{CONTAINER_PORT}"

# Backend routes (for non-container requests like auth)
BACKEND_ROUTES = ['/auth' ]

# Define the container-specific routes
CONTAINER_ROUTES = ['/api/file-structure', '/api/getFile']

# Create a Blueprint for the proxy
container_proxy = Blueprint("container_proxy", __name__)

def forward_request_to_container(endpoint):
    """
    Forward a request to the container's API.
    Args:
        endpoint (str): The endpoint to forward the request to.
    Returns:
        Flask Response: The container's response, rewrapped in a Flask response object.
    """
    # Construct the full URL for the container API
    url = f"{CONTAINER_BASE_URL}{endpoint}"
    
    # Handle the request based on its method
    try:
        if request.method == "GET":
            # Forward GET request with query parameters
            container_response = requests.get(url, params=request.args)
        elif request.method == "POST":
            # Forward POST request with JSON data
            container_response = requests.post(url, json=request.json)
        elif request.method == "PUT":
            # Forward PUT request with JSON data
            container_response = requests.put(url, json=request.json)
        elif request.method == "DELETE":
            # Forward DELETE request
            container_response = requests.delete(url)
        else:
            # Unsupported HTTP method
            return jsonify({"error": f"Unsupported method: {request.method}"}), 405

        # Return the container's response
        return jsonify(container_response.json()), container_response.status_code

    except requests.exceptions.RequestException as e:
        # Handle errors communicating with the container
        return jsonify({"error": f"Error forwarding request to container: {str(e)}"}), 500


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
        return forward_request_to_container('/api/file-structure')
    else:
        return jsonify({"error": "Invalid request path for container"}), 400

@container_proxy.route('/api/getFile', methods=['GET'])
def proxy_get_file():
    if is_container_route(request.path):
        return forward_request_to_container('/api/getFile')
    else:
        return jsonify({"error": "Invalid request path for container"}), 400

