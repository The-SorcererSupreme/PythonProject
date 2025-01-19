from werkzeug.wrappers import Request, Response
import json

class RequestRoutingMiddleware:
    """
    Middleware to dynamically route requests based on their paths.
    """
    def __init__(self, app):
        self.app = app
        self.backend_routes = ["/auth", "/api/upload"]
        self.container_routes = ["/api/file-structure"]
        self.dynamic_routes = ["/api/getFile"]
        print("Request router initiated")

    def __call__(self, environ, start_response):
        request = Request(environ)
        request_path = request.path

        # Backend-specific routes
        if any(request_path.startswith(route) for route in self.backend_routes):
            # Let the backend handle the route
            print("That's for me: ", request_path)
            print('In environ: ', environ)
            return self.app(environ, start_response)

        # Container-specific routes
        if any(request_path.startswith(route) for route in self.container_routes):
            # Forwarded to container proxy (logic handled in `container_proxy.py`)
            print("Switching to container proxy with: ", request_path)
            print('In environ: ', environ)
            response = Response(
                json.dumps({"message": "Forwarded to container"}),
                content_type="application/json",
                status=200,
            )
            return response(environ, start_response)

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
