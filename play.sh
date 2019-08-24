#!/bin/sh
OPTIONS=""
if [[ ! -z "$ANSIBLE_VAULT_PASSWORD_FILE" ]]; then
   OPTIONS="--env ANSIBLE_VAULT_PASSWORD_FILE=/tmp/vault.pw -v $ANSIBLE_VAULT_PASSWORD_FILE:/tmp/vault.pw"
fi

if [[ ! -z "$VIRL_HOST" ]]; then
   OPTIONS="$OPTIONS --env VIRL_SESSION=$VIRL_HOST"
fi
if [[ ! -z "$VIRL_USERNAME" ]]; then
   OPTIONS="$OPTIONS --env VIRL_SESSION=$VIRL_USERNAME"
fi
if [[ ! -z "$VIRL_PASSWORD" ]]; then
   OPTIONS="$OPTIONS --env VIRL_SESSION=$VIRL_PASSWORD"
fi
if [[ ! -z "$VIRL_SESSION" ]]; then
   OPTIONS="$OPTIONS --env VIRL_SESSION=$VIRL_SESSION"
fi

OPTIONS="$OPTIONS --env ANSIBLE_ROLES_PATH=/ansible/roles"

docker run -it --rm -v $PWD:/ansible --env PWD="/ansible" --env USER="$USER" $OPTIONS ansible-viptela ansible-playbook "$@"