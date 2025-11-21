FROM ubuntu:noble

WORKDIR /home/main

#TODO: Change user to run in Open-Shift. Docker-compose volume model_cache will also need to change.
USER root

# Update and install required packages.
RUN apt update -y && \
    apt install -y --no-install-recommends \
    python3-full \
    python3-dev \
    python3-pip \
    ffmpeg
    #wget 

# # Set Up Cuda Repos
# RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-ubuntu2404.pin
# RUN mv cuda-ubuntu2404.pin /etc/apt/preferences.d/cuda-repository-pin-600
# RUN wget https://developer.download.nvidia.com/compute/cuda/13.0.0/local_installers/cuda-repo-ubuntu2404-13-0-local_13.0.0-580.65.06-1_amd64.deb
# RUN dpkg -i cuda-repo-ubuntu2404-13-0-local_13.0.0-580.65.06-1_amd64.deb
# RUN cp /var/cuda-repo-ubuntu2404-13-0-local/cuda-*-keyring.gpg /usr/share/keyrings/

# # Install Cuda Repos
# RUN apt update -y && \
#     apt install -y --no-install-recommends \
#     cuda-toolkit-13-0 \
#     nvidia-cuda-toolkit

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Allow PIP to install packages outside Python ENV
RUN python3 -m pip config set global.break-system-packages true

# Install python CUDA API
RUN pip install cuda-python

#* Installing the version of torch we want first to override the openai-whisper dependency version.
#* Avoids clean-up and keeps the container smaller.
# Install torch version for CUDA 12.1
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install Whisper and Rust tools.
RUN pip install -U openai-whisper
RUN pip install setuptools-rust

# Clean Up caches
RUN pip cache purge
RUN apt clean && rm -rf /var/lib/apt/lists/*

# Copy main folder into container.
COPY ./main .
