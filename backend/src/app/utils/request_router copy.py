# utils/request_router.py

from app.utils.file_handler import FileHandler
from app.services.docker_service import DockerService

class RequestRouter:
    """
    Routes file requests dynamically to the appropriate source.
    """
    def __init__(self, source_type, file_path):
        self.source_type = source_type
        self.file_path = file_path

    def route_request(self):
        """
        Route the request based on the source type.
        Returns:
            dict: Parsed or processed file data.
        """
        if self.source_type == "container":
            return self._handle_container_request()
        elif self.source_type == "local":
            return self._handle_local_request()
        elif self.source_type == "git":
            return self._handle_git_request()
        else:
            raise ValueError(f"Unsupported source type: {self.source_type}")

    def _handle_container_request(self):
        """
        Fetch and process a file from a container.
        """
        docker_service = DockerService()
        file_content = docker_service.get_file(self.file_path)
        return FileHandler.parse_file(file_content, file_extension=".yaml")

    def _handle_local_request(self):
        """
        Fetch and process a file from the local filesystem.
        """
        with open(self.file_path, 'r') as file:
            file_content = file.read()
        return FileHandler.parse_file(file_content, file_extension=".yaml")

    def _handle_git_request(self):
        """
        Fetch and process a file from a Git repository.
        """
        # Add Git logic here
        raise NotImplementedError("Git integration is not yet implemented.")
