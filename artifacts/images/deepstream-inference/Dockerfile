FROM nvcr.io/nvidia/deepstream:7.0-gc-triton-devel
SHELL ["/bin/bash", "-c"]
ARG DEBIAN_FRONTEND=noninteractive
COPY deepstream_setup.sh .
RUN set -eux; \
    chmod +x deepstream_setup.sh; \
    bash deepstream_setup.sh