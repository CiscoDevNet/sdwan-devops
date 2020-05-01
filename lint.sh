#!/bin/sh
OPTIONS=""
if [[ ! -z "$ANSIBLE_VAULT_PASSWORD_FILE" ]]; then
   OPTIONS="--env ANSIBLE_VAULT_PASSWORD_FILE=/tmp/vault.pw -v $ANSIBLE_VAULT_PASSWORD_FILE:/tmp/vault.pw"
fi

if [[ ! -z "$VIRL_HOST" ]]; then
   OPTIONS="$OPTIONS --env VIRL_HOST=$VIRL_HOST"
fi
if [[ ! -z "$VIRL_USERNAME" ]]; then
   OPTIONS="$OPTIONS --env VIRL_USERNAME=$VIRL_USERNAME"
fi
if [[ ! -z "$VIRL_PASSWORD" ]]; then
   OPTIONS="$OPTIONS --env VIRL_PASSWORD=$VIRL_PASSWORD"
fi
if [[ ! -z "$VIRL_LAB" ]]; then
   OPTIONS="$OPTIONS --env VIRL_LAB=$VIRL_LAB"
fi
if [[ ! -z "$VMANAGE_HOST" ]]; then
   OPTIONS="$OPTIONS --env VMANAGE_HOST=$VMANAGE_HOST"
fi
if [[ ! -z "$VMANAGE_ORG" ]]; then
   OPTIONS="$OPTIONS --env VMANAGE_ORG=$VMANAGE_ORG"
fi
if [[ ! -z "$VMANAGE_USERNAME" ]]; then
   OPTIONS="$OPTIONS --env VMANAGE_SESSION=$VMANAGE_USERNAME"
fi
if [[ ! -z "$VMANAGE_PASSWORD" ]]; then
   OPTIONS="$OPTIONS --env VIRL_SESSION=$VMANAGE_PASSWORD"
fi
if [[ ! -z "$TF_VAR_vsphere_user" ]]; then
   OPTIONS="$OPTIONS --env TF_VAR_vsphere_user=$TF_VAR_vsphere_user"
fi
if [[ ! -z "$TF_VAR_vsphere_password" ]]; then
   OPTIONS="$OPTIONS --env TF_VAR_vsphere_password=$TF_VAR_vsphere_password"
fi
if [[ ! -z "$TF_VAR_vsphere_server" ]]; then
   OPTIONS="$OPTIONS --env TF_VAR_vsphere_server=$TF_VAR_vsphere_server"
fi

OPTIONS="$OPTIONS --env ANSIBLE_ROLES_PATH=/ansible/roles"

docker run -it --rm -v $PWD:/ansible --env PWD="/ansible" --env USER="$USER" $OPTIONS ansible-sdwan ansible-lint "$@"
