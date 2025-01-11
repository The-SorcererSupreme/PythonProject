#!/bin/bash
sudo apt-get update -y
sudo apt-get upgrade -y
#git config --global user.name <username>
#git config --global user.email <user-mail>
cd ~
git clone https://github.com/The-SorcererSupreme/PythonProject.git
sudo apt-get install -y python3 python3-pip python3-venv
cd ~/PythonProject/backend/
python3 -m venv venv
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
source ~/.bashrc
#nvm list-remote
nvm install v22.13.0
npm install -g @angular/cli
npm install -g npm@11.0.0
cd ~/PythonProject/frontend/python-project/
npm install
source ~/PythonProject/backend/venv/bin/activate
pip install -r requirements.txt
#pip3 install flask-cors
#python3 server.py
#cd ~/PythonProject/frontend/python-project/
#ng serve


# Finished
echo "Setup completed! Now you can run the Angular frontend and Flask backend."

# Instructions for running the apps
echo "To start the Angular frontend, run:"
echo "  ng serve"

echo "To start the Flask backend, run:"
echo "  python3 server.py"