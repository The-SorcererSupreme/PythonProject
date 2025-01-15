# /backend/src/app/services/docker_service.py
from app.utils.docker_manager import DockerClientManager, DockerContainerManager
import os
import requests
import time
from io import BytesIO
import tarfile

class DockerService:
    def __init__(self):
        print("Initializing Docker and Container")
        # Initialize the client manager
        self.client_manager = DockerClientManager()
        print("Initializied Docker Client")
        # Initialize the container manager
        self.container_manager = DockerContainerManager(self.client_manager)
        print("Container initialized")




    def get_file_structure_from_container(self, container_ip):
        """Fetch the file structure from the running container via its API."""
        try:
            url = f'http://{container_ip}:6000/api/file-structure'
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful
            return response.json()  # Return the directory structure as JSON
        except requests.RequestException as e:
            raise RuntimeError(f"Error fetching file structure from container: {e}")


    def upload_file_to_container(self, container_name, file_bytes, archive_name):
        """Upload the in-memory file to the container."""
        try:
            container = self.client_manager.get_container(container_name)

            # Wrap the in-memory bytes in a tarfile for upload
            tar_stream = BytesIO()
            with tarfile.open(fileobj=tar_stream, mode='w') as tar:
                info = tarfile.TarInfo(name=archive_name)
                info.size = len(file_bytes)
                tar.addfile(info, BytesIO(file_bytes))
            tar_stream.seek(0)

            # Upload to /workspace in the container
            container.put_archive(path="/workspace", data=tar_stream)
            print(f"Uploaded '{archive_name}' to container '{container_name}'")
        except Exception as e:
            raise RuntimeError(f"Error uploading file to container '{container_name}': {e}")




    def process_file_in_container(self, file_bytes, archive_name):
        """
        Create and run a Docker container to process the file.
        """
        print("Processing File to container")
        try:
            # Generate container name and set image
            container_name = f"processor_{archive_name.split('.')[0]}"
            image_name = "file-service-container"  # Update if a custom image is used

            # Create new file-service container
            container = self.container_manager.create_container(image_name, container_name, ports={'6000': '6000'}, volumes=None)
            print("Container created!")

            # Start the container
            container_ip = self.container_manager.run_container(container)
            print(f"Container '{container.name}' created successfully.")
            print(f"Container IP :'{container_ip}'")

            # Upload file structure to the container
            self.upload_file_to_container(container_name, file_bytes, archive_name)
            time.sleep(4)
            # Fetch the file structure from the container
            file_structure = self.get_file_structure_from_container(container_ip)
            print("File structure:", file_structure)

            # TODO: Return the file structure to the frontend

            return {
                'container_id': container.id,
                'status': 'Container created_and_started',
                'file_structure' : file_structure
            }
        except Exception as e:
            raise RuntimeError(f"Error processing file in container: {e}")
