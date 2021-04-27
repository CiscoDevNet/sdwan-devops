#!/usr/bin/env bash
OPTIONS=""

if [[ ! -z "$ANSIBLE_VAULT_PASSWORD_FILE" ]]; then
   OPTIONS="--env ANSIBLE_VAULT_PASSWORD_FILE=/tmp/vault.pw -v $ANSIBLE_VAULT_PASSWORD_FILE:/tmp/vault.pw"
fi

OPTION_LIST=( \
   "VIRL_HOST" \
   "VIRL_USERNAME" \
   "VIRL_PASSWORD" \
   "VIRL_LAB" \
   "VMANAGE_HOST" \
   "VMANAGE_ORG" \
   "VMANAGE_USERNAME" \
   "VMANAGE_PASSWORD" \
   "VMANAGE1_IP" \
   "VBOND1_IP" \
   "VSMART1_IP" \
   "HQ_EDGE1_IP" \
   "SITE1_EDGE1_IP" \
   "SITE2_EDGE1_IP" \
   "VPN0_GATEWAY" \
   "TF_VAR_vsphere_user" \
   "TF_VAR_vsphere_password" \
   "TF_VAR_vsphere_server" \
   "TF_VAR_datacenter" \
   "TF_VAR_cluster" \
   "TF_VAR_folder" \
   "TF_VAR_resource_pool" \
   "TF_VAR_datastore" \
   "TF_VAR_iso_datastore" \
   "TF_VAR_iso_path" \
   "VPN0_PORTGROUP" \
   "VPN512_PORTGROUP" \
   "SERVICEVPN_PORTGROUP" \
   "IOSXE_SDWAN_IMAGE" \
   "CSR1000V_IMAGE" \
   "UBUNTU_IMAGE" \
   "VIPTELA_VERSION" \
   )

for OPTION in ${OPTION_LIST[*]}; do
   if [[ ! -z "${!OPTION}" ]]; then
      OPTIONS="$OPTIONS --env $OPTION=${!OPTION}"
   fi
done

OPTIONS="$OPTIONS --env ANSIBLE_ROLES_PATH=/ansible/roles"

docker run -it --rm -v $PWD:/ansible --env PWD="/ansible" --env USER="$USER" $OPTIONS ciscops/ansible-sdwan ansible-playbook "$@"
