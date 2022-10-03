#!/usr/bin/env bash
IMAGE="ghcr.io/ciscodevnet/sdwan-devops:0.0.6"
OPTIONS=""

if [[ ! -z "$ANSIBLE_VAULT_PASSWORD_FILE" ]]; then
   OPTIONS="--env ANSIBLE_VAULT_PASSWORD_FILE=/tmp/vault.pw -v $ANSIBLE_VAULT_PASSWORD_FILE:/tmp/vault.pw"
fi

OPTION_LIST=( \
   "SSH_PUBKEY_BASE64" \
   "AWS_ACCESS_KEY_ID" \
   "AWS_SECRET_ACCESS_KEY" \
   "AWS_SESSION_TOKEN" \
   "AWS_REGION" \
   "VMANAGE_AMI" \
   "VMANAGE_INSTANCE_TYPE" \
   "VBOND_AMI" \
   "VBOND_INSTANCE_TYPE" \
   "VSMART_AMI" \
   "VSMART_INSTANCE_TYPE"
   "SDWAN_CONTROL_INFRA" \
   "SDWAN_DATACENTER" \
   "ACL_RANGES_IPV4_BASE64" \
   "ACL_RANGES_IPV6_BASE64" \
   "VIRL_HOST" \
   "VIRL_USERNAME" \
   "VIRL_PASSWORD" \
   "VIRL_LAB" \
   "VMANAGE_HOST" \
   "VMANAGE_ORG" \
   "VMANAGE_USERNAME" \
   "VMANAGE_PASS" \
   "VMANAGE_ENCRYPTED_PASS" \
   "SDWAN_CA_PASSPHRASE" \
   "NETWORK_CIDR" \
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
   "CLOUDINIT_TYPE"
   )

for OPTION in ${OPTION_LIST[*]}; do
   if [[ ! -z "${!OPTION}" ]]; then
      OPTIONS="$OPTIONS --env $OPTION=${!OPTION}"
   fi
done

OPTIONS="$OPTIONS --env ANSIBLE_ROLES_PATH=/ansible/roles --env ANSIBLE_STDOUT_CALLBACK=debug"

while getopts ":dl" opt; do
  case $opt in
    d)
      docker run -it --rm -v $PROJ_ROOT/ansible:/ansible --env PWD="/ansible" -v $PWD/../python-viptela:/python-viptela --env USER="$USER" $OPTIONS $IMAGE /bin/ash
      exit
      ;;
    l)
      docker run -it --rm -v $PROJ_ROOT/ansible:/ansible --env PWD="/ansible" --env USER="$USER" $OPTIONS $IMAGE ansible-lint
      exit
      ;;
  esac
done
docker run -it --rm -v $PROJ_ROOT/ansible:/ansible -v $PROJ_ROOT/terraform-sdwan:/terraform-sdwan --env PWD="/ansible" --env USER="$USER" $OPTIONS $IMAGE ansible-playbook "$@"
