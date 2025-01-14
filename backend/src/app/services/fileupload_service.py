# /app/services/file-upload.service.py

import os
import zipfile
from flask import current_app
from werkzeug.utils import secure_filename

class FileUploadService:
    # Here you can add any Docker logic or further processing
    # For example, calling the Docker container service to process the file
    # or in fileupload_routes.py
    @staticmethod
    def save_uploaded_file(file, upload_folder='uploads'):
        """Save the uploaded zip file to the server."""
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        # Optionally, handle zip file extraction here
        if filename.endswith('.zip'):
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(os.path.join(upload_folder, filename[:-4]))
        
        return filepath
