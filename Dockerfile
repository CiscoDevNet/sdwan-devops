FROM alpine:3.11

ARG build_date=unspecified
ARG terraform_version=0.12.24
ARG virl2_client_pkg=virl2_client-0.8.2+b4d055d25-py3-none-any.whl

LABEL org.opencontainers.image.title="Cisco-SDWAN" \
      org.opencontainers.image.description="Cisco SDWAN DevOps" \
      org.opencontainers.image.vendor="Cisco Systems" \
      org.opencontainers.image.created="${build_date}" \
      org.opencontainers.image.url="https://github.com/CiscoDevNet/sdwan-devops"

COPY requirements.txt /tmp/requirements.txt
COPY files/${virl2_client_pkg} /tmp/${virl2_client_pkg}

RUN echo "===> Installing GCC <===" && \
    apk add --no-cache gcc musl-dev make && \
    \
    \
    echo "===> Installing Python <===" && \
    apk add --no-cache python3 && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    \
    \
    echo "===> Installing pip <===" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    \
    \
    echo "===> Installing dependancies <==="  && \
    apk --update add sshpass libffi-dev libxml2-dev libxslt-dev python3-dev openssl-dev openssh-keygen && \
    \
    \
    echo "===> Installing PIP Requirements <==="  && \
    pip install -r /tmp/requirements.txt && \
    \
    \
    echo "===> Installing Terraform <===" && \
    apk --update add wget unzip cdrkit curl && \
    \
    \
    wget --quiet https://releases.hashicorp.com/terraform/${terraform_version}/terraform_${terraform_version}_linux_amd64.zip && \
    unzip terraform_${terraform_version}_linux_amd64.zip && \
    mv terraform /usr/bin && \
    rm terraform_${terraform_version}_linux_amd64.zip

ENV ANSIBLE_HOST_KEY_CHECKING=false \
    ANSIBLE_RETRY_FILES_ENABLED=false \
    ANSIBLE_SSH_PIPELINING=true

WORKDIR /ansible
