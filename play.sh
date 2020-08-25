#!/usr/bin/env bash
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
if [[ ! -z "$VMANAGE1_IP" ]]; then
   OPTIONS="$OPTIONS --env VMANAGE1_IP=$VMANAGE1_IP"
fi
if [[ ! -z "$VBOND1_IP" ]]; then
   OPTIONS="$OPTIONS --env VBOND1_IP=$VBOND1_IP"
fi
if [[ ! -z "$VSMART1_IP" ]]; then
   OPTIONS="$OPTIONS --env VSMART1_IP=$VSMART1_IP"
fi
if [[ ! -z "$VPN0_GATEWAY" ]]; then
   OPTIONS="$OPTIONS --env VPN0_GATEWAY=$VPN0_GATEWAY"
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
if [[ ! -z "$VPN0_PORTGROUP" ]]; then
   OPTIONS="$OPTIONS --env VPN0_PORTGROUP=$VPN0_PORTGROUP"
fi
if [[ ! -z "$VPN512_PORTGROUP" ]]; then
   OPTIONS="$OPTIONS --env VPN512_PORTGROUP=$VPN512_PORTGROUP"
fi
if [[ ! -z "$SERVICEVPN_PORTGROUP" ]]; then
   OPTIONS="$OPTIONS --env SERVICEVPN_PORTGROUP=$SERVICEVPN_PORTGROUP"
fi


OPTIONS="$OPTIONS --env ANSIBLE_ROLES_PATH=/ansible/roles"

docker run -it --rm -v $PWD:/ansible --env PWD="/ansible" --env USER="$USER" $OPTIONS ciscops/ansible-sdwan ansible-playbook "$@"
