FROM alpine:3.10

COPY requirements.txt /tmp/requirements.txt
RUN echo "===> install GCC ****" && \
    apk add --no-cache gcc musl-dev make && \
    \
    \
    echo "===> install Python ****" && \
    apk add --no-cache python3 && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    \
    \
    echo "**** install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    \
    \
    echo "===> Installing dependancies..."  && \
    apk --update add sshpass libffi-dev libxml2-dev libxslt-dev python3-dev openssl-dev && \
    \
    \
    echo "===> Installing PIP Requirements..."  && \
    pip install -r /tmp/requirements.txt

COPY files/simple_client-0.1.9b7-py3-none-any.whl /tmp/simple_client-0.1.9b7-py3-none-any.whl
RUN echo "===> Installing VIRL Client..."  && \
    pip install /tmp/simple_client-0.1.9b7-py3-none-any.whl

# Define working directory.
ENV ANSIBLE_HOST_KEY_CHECKING false
ENV ANSIBLE_RETRY_FILES_ENABLED false
ENV ANSIBLE_SSH_PIPELINING True

WORKDIR /ansible
