FROM alpine:3.16

ARG build_date=unspecified
ARG terraform_version=1.3.1
ARG arch=amd64

LABEL org.opencontainers.image.title="Cisco-SDWAN" \
      org.opencontainers.image.description="Cisco SDWAN DevOps" \
      org.opencontainers.image.vendor="Cisco Systems" \
      org.opencontainers.image.created="${build_date}" \
      org.opencontainers.image.url="https://github.com/CiscoDevNet/sdwan-devops"

RUN apk --update add wget unzip cdrkit curl
RUN wget https://releases.hashicorp.com/terraform/${terraform_version}/terraform_${terraform_version}_linux_${arch}.zip
RUN unzip terraform_${terraform_version}_linux_${arch}.zip
RUN mv terraform /usr/bin
RUN rm terraform_${terraform_version}_linux_${arch}.zip

RUN apk add --no-cache gcc musl-dev make


RUN apk add --no-cache python3
RUN if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi

RUN python3 -m ensurepip
# RUN rm -r /usr/lib/python*/ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools wheel
# RUN if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi

RUN apk --update add git sshpass libffi-dev libxml2-dev libxslt-dev python3-dev openssl-dev openssh-keygen

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ENV ANSIBLE_HOST_KEY_CHECKING=false
ENV ANSIBLE_RETRY_FILES_ENABLED=false
ENV ANSIBLE_SSH_PIPELINING=true
ENV ANSIBLE_LOCAL_TMP=/tmp
ENV ANSIBLE_REMOTE_TMP=/tmp

WORKDIR /ansible
