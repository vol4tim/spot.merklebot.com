FROM ros:melodic-ros-base-bionic

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        git \
        ssh \
        libssl-dev \
        pkg-config \
        python3-pip \
        python3-dev \
        python3-setuptools \
        ffmpeg  \
        libsm6 \
        libxext6 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV RUSTUP_HOME=/rust
ENV CARGO_HOME=/cargo
ENV PATH=/cargo/bin:/rust/bin:$PATH

RUN echo "(curl https://sh.rustup.rs -sSf | sh -s -- -y --default-toolchain nightly --no-modify-path) && rustup default nightly" > /install-rust.sh && chmod 755 /install-rust.sh
RUN /install-rust.sh

# Install NodeJS for Crust Network
RUN sudo apt-get install gcc g++ make && \
    curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash - && \
    sudo apt-get install -y nodejs

WORKDIR /home/spot/spot.merklebot.com/spot

ENV PATH="/root/.cargo/bin:${PATH}"

COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
COPY . .

# Get dependencies for Crust Network script
WORKDIR /home/spot/spot.merklebot.com/spot/utils/crust
RUN npm install

WORKDIR /home/spot/spot.merklebot.com/spot

#CMD ["python3", "--version"]
##CMD ["rostopic", "list"]

CMD ["python3", "main.py"]
