FROM ubuntu:22.04

# Moving on from Alpine and simplifying, see:
# https://pythonspeed.com/articles/alpine-docker-python/
# https://pythonspeed.com/articles/base-image-python-docker-images/

ARG build_date=unspecified
ARG terraform_version=1.3.6
ARG arch=amd64

LABEL org.opencontainers.image.title="Cisco SD-WAN" \
      org.opencontainers.image.description="Cisco SD-WAN DevOps" \
      org.opencontainers.image.vendor="Cisco Systems" \
      org.opencontainers.image.created="${build_date}" \
      org.opencontainers.image.url="https://github.com/CiscoDevNet/sdwan-devops"

ENV DEBIAN_FRONTEND noninteractive

RUN apt update && \
  apt install -y curl python-is-python3 python3-pip unzip && \
  apt clean && \
  rm -rf /var/lib/apt/lists/*

RUN curl -#O https://releases.hashicorp.com/terraform/${terraform_version}/terraform_${terraform_version}_linux_${arch}.zip
RUN unzip terraform_${terraform_version}_linux_${arch}.zip
RUN mv terraform /usr/bin
RUN rm terraform_${terraform_version}_linux_${arch}.zip

# This adds almost 1GB to the container size. Installing the .deb package has
# similar results, and it doesn't support arm64. We really need to find a way
# to avoid installing azure-cli
#RUN pip install azure-cli

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ENV ANSIBLE_HOST_KEY_CHECKING=false
ENV ANSIBLE_RETRY_FILES_ENABLED=false
ENV ANSIBLE_SSH_PIPELINING=true
ENV ANSIBLE_LOCAL_TMP=/tmp
ENV ANSIBLE_REMOTE_TMP=/tmp

WORKDIR /ansible
