FROM alpine:3.10

COPY requirements.txt /tmp/requirements.txt
RUN echo "===> Installing GCC ****" && \
    apk add --no-cache gcc musl-dev make && \
    \
    \
    echo "===> Installing Python ****" && \
    apk add --no-cache python3 && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    \
    \
    echo "**** Installing pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    \
    \
    echo "===> Installing dependancies..."  && \
    apk --update add sshpass libffi-dev libxml2-dev libxslt-dev python3-dev openssl-dev openssh-keygen && \
    \
    \
    echo "===> Installing PIP Requirements..."  && \
    pip install -r /tmp/requirements.txt

COPY files/virl2_client-0.8.2+b4d055d25-py3-none-any.whl /tmp/virl2_client-0.8.2+b4d055d25-py3-none-any.whl
RUN echo "===> Installing VIRL Client..."  && \
    pip install /tmp/virl2_client-0.8.2+b4d055d25-py3-none-any.whl

RUN echo "===> Installing Terraform ****" && \
    apk --update add wget unzip cdrkit curl && \
    \
    \
    wget --quiet https://releases.hashicorp.com/terraform/0.12.12/terraform_0.12.12_linux_amd64.zip && \
    unzip terraform_0.12.12_linux_amd64.zip && \
    mv terraform /usr/bin && \
    rm terraform_0.12.12_linux_amd64.zip

# Define working directory.
ENV ANSIBLE_HOST_KEY_CHECKING false
ENV ANSIBLE_RETRY_FILES_ENABLED false
ENV ANSIBLE_SSH_PIPELINING True

WORKDIR /ansible
