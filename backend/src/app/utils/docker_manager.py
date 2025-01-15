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

    def stop_container(self, container_name):
        """Stops a running container by its name."""
        try:
            container = self.get_container(container_name)
            container.stop()
            return f"Container '{container_name}' stopped successfully."
        except Exception as e:
            raise RuntimeError(f"Error stopping container '{container_name}': {e}")

    def remove_container(self, container_name):
        """Removes a stopped container by its name."""
        try:
            container = self.get_container(container_name)
            container.remove()
            return f"Container '{container_name}' removed successfully."
        except Exception as e:
            raise RuntimeError(f"Error removing container '{container_name}': {e}")


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
                detach=True
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