FROM ubuntu:22.04

# Moving on from Alpine and simplifying, see:
# https://pythonspeed.com/articles/alpine-docker-python/
# https://pythonspeed.com/articles/base-image-python-docker-images/

ARG build_date=unspecified
ARG terraform_version=1.4.6
ARG arch=amd64

LABEL org.opencontainers.image.title="Cisco SD-WAN" \
      org.opencontainers.image.description="Cisco SD-WAN DevOps" \
      org.opencontainers.image.vendor="Cisco Systems" \
      org.opencontainers.image.created="${build_date}" \
      org.opencontainers.image.url="https://github.com/CiscoDevNet/sdwan-devops"

ENV DEBIAN_FRONTEND noninteractive

RUN apt update && \
    apt install -y curl genisoimage git python-is-python3 python3-pip unzip && \
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

RUN git clone https://github.com/reismarcelo/sastre-ansible.git /tmp/sastre-ansible && \
    ansible-galaxy collection build /tmp/sastre-ansible/cisco/sastre --output-path /tmp/sastre-ansible && \
    ansible-galaxy collection install -f /tmp/sastre-ansible/cisco-sastre-1.0.16.tar.gz && \
    rm -fr /tmp/sastre-ansible

COPY sdwan_config_builder/ /tmp/sdwan_config_builder/
RUN pip install /tmp/sdwan_config_builder && \
    rm -fr /tmp/sdwan_config_builder

WORKDIR /ansible
