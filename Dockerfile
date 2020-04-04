ARG UBUNTU=rolling
FROM ubuntu:$UBUNTU as basestage

RUN apt-get update && apt-get install --no-install-recommends -y -q \
    python3 \
    python3-coverage \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY LICENSE coverage-service.py ./
MAINTAINER Sebastian Braun <sebastian.braun@fh-aachen.de>
ENTRYPOINT ["python3", "coverage-service.py"]
