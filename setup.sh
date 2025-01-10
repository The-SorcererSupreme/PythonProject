#!/bin/bash

# Update and upgrade the system
echo "Updating and upgrading system..."
sudo apt-get update -y
sudo apt-get upgrade -y
python3 -m venv venv
source venv/bin/activate
echo "Installing Node.js and npm..."

# Install Node.js and npm

echo "Node.js version:"
node -v
echo "npm version:"
npm -v
# Install Python3 and pip3
echo "Installing Python3 and pip3..."
sudo apt-get install -y python3 python3-pip python3-venv

# Verify Python and pip installation
echo "Python version:"
python3 --version
echo "pip version:"
pip3 --version

# Install Flask and other Python dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies from requirements.txt..."
    pip3 install -r requirements.txt
else
    echo "No requirements.txt found. Skipping Python dependencies installation."
fi

# Install Angular CLI globally
echo "Installing Angular CLI globally..."
sudo npm install -g @angular/cli
cd /frontend/python-project/
if [ -f "package.json" ]; then
    echo "Installing Angular project dependencies..."
    npm install
else
    echo "No package.json found. Skipping Angular dependencies installation."
fi

# Install Flask CORS for handling CORS issues
echo "Installing Flask-CORS (if needed for API)..."
pip3 install flask-cors

# Finished
echo "Setup completed! Now you can run the Angular frontend and Flask backend."

# Instructions for running the apps
echo "To start the Angular frontend, run:"
echo "  ng serve"

echo "To start the Flask backend, run:"
echo "  python3 server.py"