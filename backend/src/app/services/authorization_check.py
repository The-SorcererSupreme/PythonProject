from flask import request, jsonify

class AuthenticationService:
    """Handles authentication logic for the application."""

    @staticmethod
    def extract_token(request):
        """Extracts the Bearer token from the Authorization header."""
        auth_header = request.headers.get("Authorization", "")
        print(f"Checking bearer in: {request.headers}")
        if auth_header.startswith("Bearer "):
            return auth_header.split("Bearer ")[1]
        return None

    @staticmethod
    def is_protected_route(request_path):
        """
        Checks if the request is for a protected route.
        Excludes authentication-related routes like login and register.
        """
        public_routes = ["/auth/login", "/auth/register"]
        return request_path not in public_routes
