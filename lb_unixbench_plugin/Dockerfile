FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

# Build dependencies for UnixBench
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libx11-dev \
        libgl1-mesa-dev \
        libxext-dev \
        wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp

# Build UnixBench from source (Ubuntu package is outdated)
RUN wget -O unixbench.tgz https://github.com/kdlucas/byte-unixbench/archive/refs/tags/v5.1.3.tar.gz \
    && tar xvfz unixbench.tgz \
    && mv byte-unixbench-5.1.3/UnixBench /opt/UnixBench \
    && cd /opt/UnixBench && make \
    && rm -rf /tmp/*

ENV PATH="/usr/sbin:$PATH"

# Install core Python deps used by the library
RUN pip install --no-cache-dir psutil typer rich pyyaml InquirerPy pandas numpy jc

WORKDIR /app

COPY . /app

# Install plugin without pulling linux-benchmark-lib from PyPI; host code is mounted at runtime.
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --no-deps .
