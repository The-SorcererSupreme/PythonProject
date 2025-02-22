from werkzeug.wrappers import Request, Response
import json
from flask import jsonify

class RequestRoutingMiddleware:
    """
    Middleware to dynamically route requests based on their paths.
    """
    def __init__(self, app):
        self.app = app
        self.backend_routes = ["/auth", "/api/upload"]
        self.container_proxy = ["/api/file-structure", "/api/containers/export"]
        self.dynamic_routes = ["/api/getFile", "/api/saveFile"]
        self.container_routes = [
            "/api/containers",
            "/api/containers/update-name",
            "/api/containers/start",
            "/api/containers/stop",
            "/api/containers/delete",
            "/api/containers/access",
            "/api/containers/share",
            "/api/containers/revoke"
            ]  # CHANGE TO backend_routes
        print(f"------------------------------")
        print("Request router initiated")

    def __call__(self, environ, start_response):
        request = Request(environ)
        request_path = request.path
        request_headers = request.headers
        request_method = request.method

        # Skip authentication check for OPTIONS pre-flight requests
        if request_method == "OPTIONS":
            return self.app(environ, start_response)
        # Check authorization for request (not authentication)
        def check_authentication(request_path):
            print(f"Request header is: {request_headers}")
            print("Check if authorization token is set if needed...")
            auth_header = request.headers.get("Authorization")
            print(f"Auth header is: {auth_header}")
            from app.services.authorization_check import AuthenticationService

            if AuthenticationService.is_protected_route(request_path):
                token = AuthenticationService.extract_token(request)
                if not token:
                    return jsonify({'message': 'Token is missing!'}), 403
                print(f"Authorization token provided: {token}")
            else:
                print("No authorization token is needed!")
        check_authentication(request_path)        
        print(f"Requested is: {request}")
        print(f"Requested path: {request_path}")
        print(f"------------------------------")

        # Backend-specific routes
        if any(request_path.startswith(route) for route in self.backend_routes):
            # Let the backend handle the route
            print("That's for me: ", request_path)
            print('In environ: ', environ)
            return self.app(environ, start_response)

        # Container-specific routes (like /api/containers) handled by container_routes blueprint
        if any(request_path.startswith(route) for route in self.container_routes):
            print(f"Container routes matched: {request_path}")
            print(f"Switching to container_routes")
            # Use Flask's routing to route the request to the container_routes blueprint
            return self.app(environ, start_response)
        
        # Container-specific routes
        if any(request_path.startswith(route) for route in self.container_proxy):
            # Forwarded to container proxy (logic handled in `container_proxy.py`)
            print("Switching to container proxy with: ", request_path)
            print('In environ: ', environ)
            response = Response(
                json.dumps({"message": "Forwarded to container"}),
                content_type="application/json",
                status=200,
            )
            return self.app(environ, start_response)

        # Dynamic routing for other sources
        if any(request_path.startswith(route) for route in self.dynamic_routes):
            # Let Flask handle the request through `dynamic_router` blueprint
            print("Switching to dynamic routing with: ", request_path)
            print('In environ: ', environ)
            return self.app(environ, start_response)

        # Fallback for unsupported routes
        response = Response(
            json.dumps({"error": "Invalid request path"}),
            content_type="application/json",
            status=404,
        )
        print('Route not provided')
        return response(environ, start_response)
