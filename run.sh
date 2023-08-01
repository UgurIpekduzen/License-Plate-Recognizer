#!/bin/bash

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

# python3.11 -m pip install --upgrade pip && \
#                     pip install -r requirements.txt && \
#                     python3.11 mainWindow.py

python -m pip install --upgrade pip  
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python mainWindow.py