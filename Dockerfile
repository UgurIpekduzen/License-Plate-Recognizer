# FROM ubuntu:22.04

# # EXPOSE 8080/tcp 

# ARG DEBIAN_FRONTEND=noninteractive

# RUN apt-get update 
# RUN apt-get dist-upgrade -y
# RUN apt-get install software-properties-common -y 
# RUN add-apt-repository ppa:deadsnakes/ppa
# RUN apt-get install net-tools \
#                     python3.11 \
#                     python3-pip \
#                     python3-venv \
#                     libgl1-mesa-glx \ 
#                     '^libxcb.*-dev' \
#                     libx11-xcb-dev \ 
#                     libglu1-mesa-dev \
#                     libxrender-dev \
#                     libxi-dev \
#                     net-tools \
#                     libxkbcommon-dev \
#                     libxkbcommon-x11-dev -y
                   
# WORKDIR /app
# COPY . ./

# RUN python3.11 -m pip install --upgrade pip && \
#                     # python3.11 -m venv venv && \
#                     # source venv/bin/activate && \
#                     pip install -r requirements.txt && \
#                     python3.11 mainWindow.py


# FROM python:3.11

# WORKDIR /app
# COPY . /app
# RUN python3 -m venv /app/venv
# RUN apt-get install python3.11 \
#                     python3-pip \
#                     python3-venv \
#                     libgl1-mesa-glx \ 
#                     '^libxcb.*-dev' \
#                     libx11-xcb-dev \ 
#                     libglu1-mesa-dev \
#                     libxrender-dev \
#                     libxi-dev \
#                     libxkbcommon-dev \
#                     libxkbcommon-x11-dev -y
# RUN /app/venv/bin/pip install -r requirements.txt
# CMD ["/app/venv/bin/python", "mainWindow.py"]

# FROM python:3.11

# WORKDIR /usr/app/src

# COPY . ./
# # COPY requirements.txt ./
# # COPY mainWindow.py ./

# RUN pip install -r requirements.txt
# CMD ["python", "mainWindow.py"]

# FROM python:3.11

# WORKDIR /usr/src/app

# COPY . .

# RUN pip install --no-cache-dir -r requirements.txt


# CMD ["python","./mainWindow.py"]

FROM ubuntu:22.04

ENV PORT 8080
EXPOSE 8080

ARG DEBIAN_FRONTEND=noninteractive

ENV DATABASE_USERNAME=root
ENV DATABASE_PASSWORD=mypassword
ENV DATABASE=lpr
ENV DATABASE_HOST=0.0.0.0
ENV DATABASE_SOCKET=3306

RUN apt-get update 
RUN apt-get dist-upgrade -y
RUN apt-get install software-properties-common -y 
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install net-tools \
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
                   
WORKDIR /usr/src/app
COPY . .

RUN python3.11 -m pip install --upgrade pip && \
                    pip install -r requirements.txt
                    # pip install -r requirements.txt && \
                    # python3.11 mainWindow.py

# CMD ["python3.11","mainWindow.py"]
