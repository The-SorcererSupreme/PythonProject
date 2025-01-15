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

    # Fetch .env variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['DEBUG'] = os.getenv('DEBUG')
    app.config['DB_PATH'] = os.getenv('DB_PATH')

    # Configure app settings (e.g., app.config.from_object()) here
    #
    
    # Register blueprints
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)
    from app.routes.fileupload_routes import upload_file
    app.register_blueprint(upload_file)
    #from app.routes.loadfile_routes import load_file
    #app.register_blueprint(load_file)
    from app.routes.container_proxy import container_proxy
    app.register_blueprint(container_proxy)
    
    # Add more routes, services, etc. here
    #

    return app
