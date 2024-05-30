FROM nvcr.io/nvidia/deepstream:7.0-gc-triton-devel
SHELL ["/bin/bash", "-c"]
ARG DEBIAN_FRONTEND=noninteractive
COPY recording_setup.sh .
RUN set -eux; \
    chmod +x recording_setup.sh; \
    bash recording_setup.sh