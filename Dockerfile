# vim:set ft=dockerfile:
ARG UBUNTU=rolling
FROM ubuntu:$UBUNTU
MAINTAINER Sebastian Braun <sebastian.braun@fh-aachen.de>

ENV DEBIAN_FRONTEND noninteractive
ENV LANG en_US.UTF-8

RUN apt-get update && apt-get install --no-install-recommends -y -q \
    build-essential \
    python3 \
    python3-dev \
    python3-pip \
&& pip3 install --no-cache-dir coverage \
&& apt-get remove --purge --autoremove -y -q \
    build-essential \
    python3-dev \
    python3-pip \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY LICENSE coverage-service.py ./

ENTRYPOINT ["python3", "coverage-service.py"]
