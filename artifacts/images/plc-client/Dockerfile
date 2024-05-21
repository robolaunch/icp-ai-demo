FROM ubuntu:jammy
SHELL ["/bin/bash", "-c"]
ARG DEBIAN_FRONTEND=noninteractive

ARG APPLICATION_PATH=/opt/plc
RUN mkdir -p ${APPLICATION_PATH}
COPY . ${APPLICATION_PATH}

WORKDIR ${APPLICATION_PATH}

RUN set -eux; \
    apt-get update; \
    apt-get install -y python3 python3-pip

RUN set -eux; \
    pip install -r requirements.txt

CMD ["/bin/bash", "-c", "python3 connect_to_plc.py sample.yaml"]