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
        procps \
        sysstat \
        sysvinit-utils \
        mesa-utils \
        locales \
    && rm -rf /var/lib/apt/lists/*

# Generate UTF-8 locale to silence UnixBench warnings
RUN sed -i 's/^# *\(en_US.UTF-8\)/\1/' /etc/locale.gen \
    && locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

WORKDIR /tmp

# Build UnixBench from source (Ubuntu package is outdated)
RUN wget -O unixbench.tgz https://github.com/kdlucas/byte-unixbench/archive/refs/tags/v5.1.3.tar.gz \
    && tar xvfz unixbench.tgz \
    && mv byte-unixbench-5.1.3/UnixBench /opt/UnixBench \
    && cd /opt/UnixBench && make \
    && command -v 3dinfo >/dev/null 2>&1 || (echo '#!/bin/sh' > /usr/local/bin/3dinfo && echo 'exit 0' >> /usr/local/bin/3dinfo && chmod +x /usr/local/bin/3dinfo) \
    && rm -rf /tmp/*

ENV PATH="/usr/sbin:$PATH"

# Install core Python deps used by the library
RUN pip install --no-cache-dir psutil typer rich pyyaml InquirerPy pandas numpy jc

WORKDIR /app

COPY . /app

# Install plugin without pulling linux-benchmark-lib from PyPI; host code is mounted at runtime.
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --no-deps .
