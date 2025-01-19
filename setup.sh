#!/bin/bash
sudo apt-get update -y
sudo apt install npm -y
sudo apt-get upgrade -y
cd ~


curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
source ~/.bashrc
#nvm list-remote
nvm install v22.13.0
npm install -g @angular/cli
npm install -g npm@11.0.0
cd ~/PythonProject/frontend/python-project/
npm install
#cd ~/PythonProject/frontend/python-project/
#ng serve

# Step 5: Set up Python environment
echo "Setting up Python environment..."
sudo apt install -y python3 python3-pip python3.12-venv
cd ~/PythonProject/backend/src/
if [ ! -d "venv" ]; then
  python3 -m venv venv || error_exit "Failed to create Python virtual environment."
#  source ../venv/bin/activate || error_exit "Failed to activate venv."
#  pip install --upgrade pip || error_exit "Failed to upgrade pip."
  pip install -r requirements.txt || error_exit "Failed to install Python dependencies."
else
  echo "Python environment already set up, skipping..."

# Step 2: Install Docker
if ! command -v docker &> /dev/null; then
  echo "Installing Docker..."
  sudo apt-get remove -y docker docker-engine docker.io containerd runc || echo "No existing Docker installation to remove."
  sudo install -m 0755 -d /etc/apt/keyrings || error_exit "Failed to create Docker keyring directory."
  sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc || error_exit "Failed to download Docker GPG key."

  # Verify Docker GPG checksum (example checksum, replace with actual)
  verify_checksum /etc/apt/keyrings/docker.asc "1500c1f56fa9e26b9b8f42452a553675796ade0807cdce11975eb98170b3a570"

  sudo chmod a+r /etc/apt/keyrings/docker.asc || error_exit "Failed to set permissions on Docker key."
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null || error_exit "Failed to configure Docker repository."
  sudo apt-get update || error_exit "Failed to update package lists for Docker."
  sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin || error_exit "Failed to install Docker."
else
  echo "Docker already installed, skipping..."
fi
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Step 6: Configure Docker
if ! groups $USER | grep -q docker; then
  echo "Configuring Docker..."
  sudo groupadd docker || echo "Docker group already exists."
  sudo usermod -aG docker $USER || error_exit "Failed to add user to Docker group."
  sudo systemctl enable docker.service || error_exit "Failed to enable Docker service."
  sudo systemctl enable containerd.service || error_exit "Failed to enable containerd service."
  exit 0
else
  echo "Docker already configured, skipping..."
fi


# Finished
echo "Setup completed! Now you can run the Angular frontend and Flask backend."

# Instructions for running the apps
echo "To start the Angular frontend, run:"
echo "  ng serve"

echo "To start the Flask backend, run:"
echo "  python3 server.py"