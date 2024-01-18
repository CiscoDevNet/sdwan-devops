FROM alpine:3.19

ARG build_date=unspecified

LABEL org.opencontainers.image.title="Cisco-SDWAN" \
      org.opencontainers.image.description="Cisco SDWAN DevOps" \
      org.opencontainers.image.vendor="Cisco Systems" \
      org.opencontainers.image.created="${build_date}" \
      org.opencontainers.image.url="https://github.com/CiscoDevNet/sdwan-devops"

# Add required gcc and python tools
RUN apk add --no-cache gcc musl-dev make python3 python3-dev py3-pip py3-setuptools py3-wheel

#RUN apk add --no-cache python3 py3-pip py3-setuptools py3-wheel
#RUN if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi

#RUN python3 -m ensurepip
# RUN rm -r /usr/lib/python*/ensurepip
# RUN pip install --no-cache --upgrade pip setuptools wheel
# RUN if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi

# Add requirement packages for sdwan-devops
RUN apk --update add git sshpass libffi-dev libxml2-dev libxslt-dev openssl-dev openssh-keygen

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt --break-system-packages

COPY requirements.yml /tmp/requirements.yml
RUN ansible-galaxy collection install -r /tmp/requirements.yml

# ARG terraform_version=0.13.7

# RUN apk --update add wget unzip cdrkit curl
# RUN wget --quiet https://releases.hashicorp.com/terraform/${terraform_version}/terraform_${terraform_version}_linux_amd64.zip
# RUN unzip terraform_${terraform_version}_linux_amd64.zip
# RUN mv terraform /usr/bin
# RUN rm terraform_${terraform_version}_linux_amd64.zip

ENV ANSIBLE_HOST_KEY_CHECKING=false
ENV ANSIBLE_RETRY_FILES_ENABLED=false
ENV ANSIBLE_SSH_PIPELINING=true
ENV ANSIBLE_LOCAL_TMP=/tmp
ENV ANSIBLE_REMOTE_TMP=/tmp
ENV ANSIBLE_ASYNC_DIR=/tmp/.ansible_async

WORKDIR /ansible
