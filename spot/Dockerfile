FROM ros:melodic-ros-base-bionic

RUN DEBIAN_FRONTEND=noninteractive apt-get -yqq update && \
    apt-get install -yqq software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get -yqq update && \
    apt-get install -yqq --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        git \
        ssh \
        libssl-dev \
        pkg-config \
        python3.8-full \
        python3.8-dev \
        ffmpeg  \
        libsm6 \
        libxext6 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    python3.8 -m ensurepip --upgrade

ENV RUSTUP_HOME=/rust
ENV CARGO_HOME=/cargo
ENV PATH=/cargo/bin:/rust/bin:$PATH

RUN echo "(curl https://sh.rustup.rs -sSf | sh -s -- -y --default-toolchain nightly --no-modify-path) && rustup default nightly" > /install-rust.sh && chmod 755 /install-rust.sh
RUN /install-rust.sh

# Install NodeJS for Crust Network
RUN DEBIAN_FRONTEND=noninteractive sudo apt-get install -yqq gcc g++ make && \
    curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash - && \
    apt-get install -yqq nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/spot/spot.merklebot.com/spot

ENV PATH="/root/.cargo/bin:${PATH}"

COPY requirements.txt requirements.txt
RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install -r requirements.txt
COPY . .

# Get dependencies for Crust Network script
WORKDIR /home/spot/spot.merklebot.com/spot/utils/crust
RUN npm install

WORKDIR /home/spot/spot.merklebot.com/spot

CMD ["python3.8", "main.py"]
