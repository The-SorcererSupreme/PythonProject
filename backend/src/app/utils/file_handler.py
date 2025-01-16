# utils/file_handler.py

import os
import mimetypes
from io import BytesIO
import requests

class FileHandler:
    """
    Handles loading files from different sources (local, container, git, etc.)
    and checking file types based on extensions.
    """
    def __init__(self, file_path, source_type="local"):
        self.file_path = file_path
        self.source_type = source_type

    def get_file_content(self):
        """
        Fetches the file content from the source (local, container, git, etc.)
        Returns the file content as bytes.
        """
        if self.source_type == "local":
            return self._get_local_file_content()
        elif self.source_type == "container":
            return self._get_container_file_content()
        # Add more source types as needed (git, remote, etc.)
        else:
            raise ValueError(f"Unsupported source type: {self.source_type}")

    def _get_local_file_content(self):
        """Read file content from the local file system."""
        try:
            with open(self.file_path, 'rb') as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Local file '{self.file_path}' not found.")

    def _get_container_file_content(self):
        """Fetch file content from a container."""
        # For simplicity, assuming we already have a URL to get the file from the container
        response = requests.get(f"http://172.17.0.2/api/getFile?file={self.file_path}")
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Failed to fetch file from container. Status code: {response.status_code}")

    @staticmethod
    def is_yaml_file(file_content):
        """
        Checks if the file content is YAML by checking its extension or content.
        """
        # Check based on file extension
        mime_type, _ = mimetypes.guess_type(file_content)
        return mime_type == "application/x-yaml" or file_content.endswith((".yaml", ".yml"))

    @staticmethod
    def is_json_file(file_content):
        """Checks if the file content is JSON based on extension."""
        mime_type, _ = mimetypes.guess_type(file_content)
        return mime_type == "application/json" or file_content.endswith(".json")
