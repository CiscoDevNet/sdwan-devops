#!/bin/sh

docker run -it --rm -v $PWD:/ansible -v /tmp:/tmp --env PWD="/ansible" --env USER="$USER" --env VIRL_SESSION="$VIRL_SESSION" --env VIRL_HOST="$VIRL_HOST" --env VIRL_UERNAME="$VIRL_USERNAME" --env VIRL_PASSWORD="$VIRL_PASSWORD" ansible-viptela ansible-playbook "$@" 