# backend/src/app/__init__.py
from flask_cors import CORS
from dotenv import load_dotenv
from flask import Flask, request, jsonify, url_for
import os

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:4200"], supports_credentials=True, 
         allow_headers=["Authorization", "Content-Type", "Access-Control-Allow-Origin"])

    # Fetch .env variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['DEBUG'] = os.getenv('DEBUG')
    app.config['DB_PATH'] = os.getenv('DB_PATH')
    app.config['SECRET_JWT_KEY'] = os.getenv('SECRET_JWT_KEY')

    # Add middleware to handle dynamic routing
    from app.utils.request_router import RequestRoutingMiddleware
    app.wsgi_app = RequestRoutingMiddleware(app.wsgi_app)
    
    # Register blueprints
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.fileupload_routes import upload_file
    app.register_blueprint(upload_file)

    from app.routes.dynamic_router import dynamic_router
    app.register_blueprint(dynamic_router)

    from app.routes.container_proxy import container_proxy
    app.register_blueprint(container_proxy)

    from app.routes.container_routes import container_routes
    app.register_blueprint(container_routes)
    return app

