from werkzeug.wrappers import Request, Response
import json
from app.routes.container_routes import container_routes

class RequestRoutingMiddleware:
    """
    Middleware to dynamically route requests based on their paths.
    """
    def __init__(self, app):
        self.app = app
        self.backend_routes = ["/auth", "/api/upload"]
        self.container_proxy = ["/api/file-structure"]
        self.dynamic_routes = ["/api/getFile"]
        self.container_routes = ["/api/containers"]  # CHANGE TO backend_routes
        print(f"------------------------------")
        print("Request router initiated")

    def __call__(self, environ, start_response):
        request = Request(environ)
        request_path = request.path
        print(f"Requested is: {request}")
        print(f"Requested path: {request_path}")
        print(f"------------------------------")

        # Backend-specific routes
        if any(request_path.startswith(route) for route in self.backend_routes):
            # Let the backend handle the route
            print("That's for me: ", request_path)
            print('In environ: ', environ)
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
            return response(environ, start_response)
        
        # Container-specific routes (like /api/containers) handled by container_routes blueprint
        if any(request_path.startswith(route) for route in self.container_routes):
            print(f"Container routes matched: {request_path}")
            print(f"Switching to container_routes")
            # Use Flask's routing to route the request to the container_routes blueprint
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
