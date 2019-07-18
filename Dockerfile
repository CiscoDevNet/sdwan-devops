# Use an official Python runtime as a parent image
FROM ubuntu:18.04

RUN apt-get update && apt-get install -y python-pip openssh-client curl sshpass

# Install requirements.
COPY requirements.txt /tmp/requirements.txt
RUN pip install --requirement /tmp/requirements.txt
RUN pip install virlutils

# Define working directory.
ENV ANSIBLE_HOST_KEY_CHECKING false
ENV ANSIBLE_RETRY_FILES_ENABLED false
ENV ANSIBLE_SSH_PIPELINING True

WORKDIR /ansible