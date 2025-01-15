# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory in the container to /workspace
WORKDIR /workspace

# Copy your project files into the container (including container_monitor.py)
# Make sure to include the file and any necessary directories for your app
COPY . /workspace/

# Install the necessary dependencies
RUN pip install --no-cache-dir watchfiles flask requests

# Expose the port that the Flask app will use
EXPOSE 5000

# Run the monitor script on container start (the Flask app will run alongside)
CMD ["python", "/workspace/container_monitor.py"]
