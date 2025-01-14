# backend/src/app/__init__.py
from flask_cors import CORS
from dotenv import load_dotenv
from flask import Flask
import os

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app, origins="*")

    # You can now access environment variables like this:
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['DEBUG'] = os.getenv('DEBUG')
    app.config['DB_PATH'] = os.getenv('DB_PATH')
    # Configure app settings (e.g., app.config.from_object())
    
    # Register blueprints
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)
    from app.routes.fileupload_routes import upload_file
    app.register_blueprint(upload_file)
    # Add other routes, services, etc.

    return app
