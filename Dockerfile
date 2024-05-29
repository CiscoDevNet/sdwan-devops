FROM ubuntu:22.04

# Moving on from Alpine and simplifying, see:
# https://pythonspeed.com/articles/alpine-docker-python/
# https://pythonspeed.com/articles/base-image-python-docker-images/

ARG build_date=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
# After releasing 1.5.5, Hashicorp changed the license from MPL to BSL.
# Unless OSPO/Cisco Legal confirms that we can keep using Terraform under the
# new license, we shouldn't update this version.
ARG terraform_version=1.5.5
ARG TARGETARCH

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

RUN curl -#O https://releases.hashicorp.com/terraform/${terraform_version}/terraform_${terraform_version}_linux_${TARGETARCH}.zip
RUN unzip terraform_${terraform_version}_linux_${TARGETARCH}.zip
RUN mv terraform /usr/bin
RUN rm terraform_${terraform_version}_linux_${TARGETARCH}.zip

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

RUN git clone https://github.com/CiscoDevNet/sastre-ansible /tmp/sastre-ansible && \
    ansible-galaxy collection build /tmp/sastre-ansible/cisco/sastre --output-path /tmp/sastre-ansible && \
    ansible-galaxy collection install -f /tmp/sastre-ansible/cisco-sastre-1.0.20.tar.gz && \
    rm -fr /tmp/sastre-ansible

COPY sdwan_config_builder/ /tmp/sdwan_config_builder/
RUN pip install /tmp/sdwan_config_builder && \
    rm -fr /tmp/sdwan_config_builder

WORKDIR /ansible
