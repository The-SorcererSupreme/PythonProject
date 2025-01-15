# /backend/src/app/services/docker_service.py
from app.utils.docker_manager import DockerClientManager, DockerContainerManager
import os
import requests

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
            url = f'http://{container_ip}:5000/api/file-structure'
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful
            return response.json()  # Return the directory structure as JSON
        except requests.RequestException as e:
            raise RuntimeError(f"Error fetching file structure from container: {e}")




    def process_file_in_container(self, file_path, archive_name):
        """
        Create and run a Docker container to process the file.
        """
        print("Processing File to container")
        try:
            # Generate container name and get image
            container_name = f"processor_{archive_name.split('.')[0]}"
            image_name = "file-service-container"  # Update if a custom image is used

            # Define host path (uploads directory) and container bind path
            host_path = os.path.abspath(file_path)
            print("Absolute path: ", host_path)
            #container_bind_path = "/workspace/uploads"

            # Create new file-service container
            self.container_manager.create_container(image_name, container_name, ports={'6000': '5000'}, volumes=None)

            # Command to extract the ZIP file inside the container's working directory
            #command = f"sh -c 'apt-get update && apt-get install -y unzip && unzip -o {container_bind_path}/{archive_name} -d /workspace && tail -f /dev/null'"

            # Start the container
            container_ip = self.container_manager.run_container(
                image_name=image_name,
                container_name=container_name,
                volumes=None,
                #command="python /workspace/container_monitor.py"
            )
            print(f"Container '{container_ip.name}' created successfully.")
            print(f"Container IP :'{container_ip}'")

            # Step 2: Start the container
            #result = self.container_manager.run_container(container)


            # Once the container is running, fetch the file structure
            file_structure = self.get_file_structure_from_container(container_ip)
            print("File structure:", file_structure)

            # Optionally: return this file structure to the frontend or update it as necessary

            return {
                'container_id': container_ip.id,
                'status': 'created_and_started',
                'file_structure' : file_structure
            }
        except Exception as e:
            raise RuntimeError(f"Error processing file in container: {e}")
