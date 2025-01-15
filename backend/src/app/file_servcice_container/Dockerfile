# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory for user-uploaded files
WORKDIR /workspace

# Copy the monitoring script to a separate directory
COPY container_monitor.py /app/

# Install dependencies
RUN pip install --no-cache-dir watchfiles flask requests

# Run the monitor script on container start
CMD ["python", "/app/container_monitor.py"]
