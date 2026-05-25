FROM ubuntu:22.04

RUN apt-get update \
  && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    gcc \
    gdb \
    make \
    coreutils \
    tar \
    curl \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

RUN useradd -m sandbox && mkdir -p /sandbox /code && chown sandbox:sandbox /sandbox /code
WORKDIR /sandbox
USER sandbox

CMD ["tail", "-f", "/dev/null"]
