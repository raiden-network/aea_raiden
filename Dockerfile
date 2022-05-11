FROM python:3.8.13-slim

WORKDIR /autonomous_raiden
COPY . .
RUN mkdir -p /usr/lib/raiden/keystore

RUN pip3 install -U pip wheel setuptools
RUN apt-get update && apt-get install -y golang-go wget && pip3 install -U aea[all]

# Install GETH
RUN wget https://gethstore.blob.core.windows.net/builds/geth-linux-amd64-1.10.17-25c9b49f.tar.gz -O /tmp/geth.tar.gz && mkdir /tmp/geth && tar -xzf /tmp/geth.tar.gz -C /tmp/geth/ --strip-components=1 && mv /tmp/geth/geth /usr/bin && rm -rf /tmp/geth* && chmod +x /usr/bin/geth

# Install Raiden
RUN wget https://github.com/raiden-network/raiden/releases/download/v3.0.1/raiden-v3.0.1-linux-x86_64.tar.gz
RUN tar -xvf raiden-v3.0.1-linux-x86_64.tar.gz && mv raiden-v3.0.1-linux-x86_64 /usr/bin/raiden && chmod +x /usr/bin/raiden && rm raiden-v3.0.1-linux-x86_64.tar.gz

RUN aea fingerprint skill brainbot/channel_manager:0.1.0
RUN aea install && aea build
