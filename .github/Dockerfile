FROM summerwind/actions-runner:v2.287.1-ubuntu-20.04
  
ARG build_date=unspecified

LABEL org.opencontainers.image.title="Cisco-SDWAN" \
      org.opencontainers.image.description="Cisco SDWAN DevOps" \
      org.opencontainers.image.vendor="Cisco Systems" \
      org.opencontainers.image.created="${build_date}" \
      org.opencontainers.image.url="https://github.com/CiscoDevNet/sdwan-devops"

RUN sudo apt-get update && sudo apt-get install -y \
      sshpass \
      python3-dev \
      libffi-dev \
      libxml2-dev \
      libxslt-dev \
      mkisofs

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /tmp
ARG terraform_version=0.13.7
RUN wget --quiet https://releases.hashicorp.com/terraform/${terraform_version}/terraform_${terraform_version}_linux_amd64.zip
RUN unzip terraform_${terraform_version}_linux_amd64.zip
RUN sudo mv terraform /usr/bin
RUN rm terraform_${terraform_version}_linux_amd64.zip

ENV ANSIBLE_HOST_KEY_CHECKING=false
ENV ANSIBLE_RETRY_FILES_ENABLED=false
ENV ANSIBLE_SSH_PIPELINING=true
ENV ANSIBLE_LOCAL_TMP=/tmp
ENV ANSIBLE_REMOTE_TMP=/tmp

WORKDIR /ansible
