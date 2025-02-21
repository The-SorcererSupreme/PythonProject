# /backend/src/app/services/docker_service.py
from app.classes.container_actions import DockerClientManager, DockerContainerManager
from app.classes.database_actions import Database  # Import your Database class
import os
import requests
import time
from io import BytesIO
import tarfile
import random
import socket

class DockerService:
    def __init__(self):
        print("Initializing Docker and Container")
        # Initialize the client manager
        self.client_manager = DockerClientManager()
        print("Initializied Docker Client")
        # Initialize the container manager
        self.container_manager = DockerContainerManager(self.client_manager)
        print("Container initialized")
        # Initialize the Database class
        self.db = Database()
        print("Database initialized")




    def get_file_structure_from_container(self, container_ip, archive_name):
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

            # Command to extract the archive inside the container
            command = f"unzip /workspace/{archive_name} -d /workspace/"
            # Execute the extraction command inside the container
            exit_code, output = container.exec_run(command)
            # If the extraction fails, the exit code will not be 0
            if exit_code != 0:
                raise RuntimeError(f"Failed to extract archive: {output.decode()}")

            print(f"Archive '{archive_name}' extracted successfully in container '{container_name}'")
            command = f"rm -f /workspace/{archive_name}"
            exit_code, output = container.exec_run(command)
            if exit_code != 0:
                raise RuntimeError(f"Failed to delete archive: {output.decode()}")
            print(f"Archive '{archive_name}' removed in '{container_name}'")
        except Exception as e:
            raise RuntimeError(f"Error uploading file to container '{container_name}': {e}")




    def process_file_in_container(self, file_bytes, archive_name, user_id):
        """
        Create and run a Docker container to process the file.
        """
        print("Processing File to container")
        try:
            # Generate container name and set image
            timestamp = int(time.time())  # Generate a timestamp
            container_name = f"processor_{user_id}_{archive_name.split('.')[0]}_{timestamp}"
            image_name = "file-service-container"  # Update if a custom image is used

            # Get an available host port
            print("Opening get_available_port function")
            host_port = self.get_available_port(5000, 65000)  
            container_port = 6000  # The internal container port remains the same

            # Create new file-service container with dynamic port mapping
            container = self.container_manager.create_container(
            image_name, 
            container_name, 
            ports={str(container_port): str(host_port)}, 
            volumes=None
            )
            print(f"Container created on port {host_port}!")

            # Start the container
            container_ip = self.container_manager.run_container(container)
            print(f"Container '{container.name}' created successfully.")
            print(f"Container IP :'{container_ip}'")

            # Upload file structure to the container
            self.upload_file_to_container(container_name, file_bytes, archive_name)
            time.sleep(4)
            # Fetch the file structure from the container
            file_structure = self.get_file_structure_from_container(container_ip, archive_name)
            print("File structure:", file_structure)

            # Save the container information to the database, linking to the user
            self.save_container_to_db(user_id, container.id, container_name, 'running', host_port)
            id_container = self.get_id_by_container_id(container.id)
            id_container = id_container[0]['id']
            print(f"Returning container ID: {id_container}")
            # TODO: Return the file structure to the frontend

            return {
                'container_id': id_container,
                'container_name' : container_name,
                'status': 'running',
                'file_structure' : file_structure
            }
        except Exception as e:
            raise RuntimeError(f"Error processing file in container: {e}")
    
    def save_container_to_db(self, user_id, container_id, container_name, status, host_port):
        """Save container information to the PostgreSQL database."""
        query = """
        INSERT INTO containers (user_id, container_id, container_name, status, host_port)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            self.db.execute_query(query, (user_id, container_id, container_name, status, host_port))
            print(f"Container {container_name} saved to database successfully.")
        except Exception as e:
            raise RuntimeError(f"Error saving container to database: {e}")
        
    def get_available_port(self, start=5000, end=65000):
        """Find an available port within the specified range."""
        print("Inside get_available_port function")
        while True:
            port = random.randint(start, end)  # Select a random port
            print(f"Checking if port {port} is unassigned...")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(('localhost', port)) != 0:  # If port is not in use
                    return port
                
    def get_id_by_container_id (self, container_id): # Limit to return id or not?
        print("Getting id for container")
        id_container = self.db.fetch_query("SELECT * FROM containers WHERE container_id = %s", (container_id,))
        print(f"ID for container {container_id}: {id_container}")
        return id_container