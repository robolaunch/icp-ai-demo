FROM ubuntu:jammy
SHELL ["/bin/bash", "-c"]
ARG DEBIAN_FRONTEND=noninteractive

RUN set -eux; \
    apt-get update; \
    apt-get install -y python3 python3-pip

RUN set -eux; \
    pip install python-snap7