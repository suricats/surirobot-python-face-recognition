FROM python:3.6-slim
LABEL maintainer="Thomas BERDY <tberdy@hotmail.fr>"

RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    libopenblas-dev \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS

RUN cd ~ && \
    mkdir -p facerecognition && \
    git clone https://github.com/suricats/surirobot-python-face-recognition.git facerecognition/ && \
    cd  facerecognition/ && \
    pip3 install -r requirements.txt

CMD cd /root/facerecognition && \
    python3 start.py
