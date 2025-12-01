FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /tmp

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libx11-dev \
        libgl1-mesa-dev \
        libxext-dev \
        wget \
    && rm -rf /var/lib/apt/lists/*

# Build UnixBench from source
RUN wget http://byte-unixbench.googlecode.com/files/UnixBench5.1.3.tgz \
    && tar xvfz UnixBench5.1.3.tgz \
    && mv UnixBench /opt/UnixBench \
    && cd /opt/UnixBench && make \
    && rm -rf /tmp/*

WORKDIR /opt/UnixBench

# Default command: show help
CMD ["./Run", "--help"]
