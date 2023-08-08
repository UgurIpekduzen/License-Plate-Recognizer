#!/bin/bash

# Python installation
sudo apt-get update 
sudo apt-get dist-upgrade -y
sudo apt-get install software-properties-common -y 
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get install net-tools \
                    python3.11 \
                    python3-pip \
                    python3-venv \
                    libgl1-mesa-glx \ 
                    '^libxcb.*-dev' \
                    libx11-xcb-dev \ 
                    libglu1-mesa-dev \
                    libxrender-dev \
                    libxi-dev \
                    net-tools \
                    libxkbcommon-dev \
                    libxkbcommon-x11-dev -y

sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.11 4

# Docker installation
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg -y
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker

# Build the server
docker compose up --force-recreate --build -d

# Installing the libraries and run the application
python -m pip install --upgrade pip  
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python mainWindow.py