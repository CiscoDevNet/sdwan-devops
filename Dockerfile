FROM alpine:3.10

# if PyATS should be included:
# docker build -t ansible-viptela --build-arg pyats=1 .
# images size goes up from ~400 to ~800 MB!

ARG pyats

RUN echo "===> install GCC... " && \
    apk add --no-cache gcc musl-dev make && \
    \
    \
    echo "===> install Python..." && \
    apk add --no-cache python3 && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    \
    \
    echo "===> install pip..." && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    \
    \
    echo "===> Installing dependencies..."  && \
    apk --update add sshpass libffi-dev libxml2-dev libxslt-dev python3-dev openssl-dev openssh-keygen

COPY requirements.txt /tmp/requirements.txt
RUN echo "===> Installing PIP Requirements..."  && \
    pip install -r /tmp/requirements.txt

# https://github.com/pypa/pip/issues/3969#issuecomment-247381915
COPY _manylinux.py /usr/lib/python3.7/site-packages/_manylinux.py

RUN if ! [ "x$pyats" = "x" ]; then \
        echo "===> Installing PyATS / Genie requirement..."  && \
        pip install pyats[full]==19.8 ; \
    fi 

COPY files/simple_client-0.1.9b15-py3-none-any.whl /tmp/simple_client-0.1.9b15-py3-none-any.whl
RUN echo "===> Installing VIRL Client..."  && \
    pip install /tmp/simple_client-0.1.9b15-py3-none-any.whl

# Define working directory.
ENV ANSIBLE_HOST_KEY_CHECKING false
ENV ANSIBLE_RETRY_FILES_ENABLED false
ENV ANSIBLE_SSH_PIPELINING True

WORKDIR /ansible
