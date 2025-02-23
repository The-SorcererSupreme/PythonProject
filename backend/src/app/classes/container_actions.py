import docker

class DockerClientManager:
    def __init__(self):
        """Initialize the Docker client."""
        try:
            self.client = docker.from_env()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Docker client: {e}")

    def get_container(self, container_name):
        """Fetch a container by its name."""
        try:
            return self.client.containers.get(container_name)
        except Exception as e:
            raise RuntimeError(f"Error retrieving container '{container_name}': {e}")

    def start_container(self, container_id):
        """Start a stopped container."""
        try:
            container = self.get_container(container_id)
            if container.status != "running":
                container.start()
                container.reload()  # Ensure the status is updated
                return container.status  # Return the new status after starting
            return container.status  # Return the current status if already running
        except Exception as e:
            raise RuntimeError(f"Error starting container '{container_id}': {e}")

    def stop_container(self, container_id):
        """Stop a running container."""
        try:
            container = self.get_container(container_id)
            print(f"container info: {container.status}")
            if container.status == "running":
                container.stop()
                container.reload()  # Ensure the status is updated
                return container.status  # Return the new status after stopping
            return container.status  # Return the current status if already stopped
        except Exception as e:
            raise RuntimeError(f"Error stopping container '{container_id}': {e}")

    def remove_container(self, container_id):
        """Remove a stopped container."""
        try:
            container = self.get_container(container_id)
            if container.status == "running":
                raise RuntimeError(f"Cannot remove running container '{container_id}'. Stop it first.")
            container.remove()
            return f"Container '{container_id}' removed successfully."
        except Exception as e:
            raise RuntimeError(f"Error removing container '{container_id}': {e}")
    
    def rename_container(self, container_id, new_name):
        """Renames an existing container."""
        try:
            container = self.get_container(container_id)
            container.rename(new_name)
            return f"Container '{container_id}' renamed to '{new_name}' successfully."
        except Exception as e:
            raise RuntimeError(f"Error renaming container '{container_id}': {e}")


class DockerContainerManager:
    def __init__(self, docker_client_manager):
        """Initialize the container manager with a Docker client."""
        self.client = docker_client_manager.client


    def create_container(self, image_name, container_name, ports, volumes=None, environment=None, command=None):
        """
        Creates a Docker container.
        - image_name: The Docker image to use.
        - container_name: The name for the container.
        - ports: Port bindings.
        - volumes: Host-container volume bindings.
        - environment: Environment variables.
        - command: Default command for the container.
        """
        try:
            container = self.client.containers.create(
                image=image_name,
                name=container_name,
                ports=ports,
                volumes=volumes,
                environment=environment,
                command=command,
                detach=True,
                network="pythonproject_app_network",
            )
            return container
        except Exception as e:
            raise RuntimeError(f"Error creating container '{container_name}': {e}")

    def run_container(self, container):
        """
        Starts an already created container.
        - container: The container instance returned by `create_container`.
        """
        try:
            container.start()
            print(f"Container '{container.name}' started successfully.")
            # Retrieve the container's IP address
            container.reload()  # Refresh container state
            network_settings = container.attrs['NetworkSettings']
            container_ip = network_settings['IPAddress']

            return container_ip  # Return the container's IP address
            
        except Exception as e:
            raise RuntimeError(f"Error starting container '{container.name}': {e}")