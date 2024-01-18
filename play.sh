#!/usr/bin/env bash
IMAGE="sdwan-devops"
OPTIONS=""

if [[ ! -z "$ANSIBLE_VAULT_PASSWORD_FILE" ]]; then
   OPTIONS="--env ANSIBLE_VAULT_PASSWORD_FILE=/tmp/vault.pw -v $ANSIBLE_VAULT_PASSWORD_FILE:/tmp/vault.pw"
fi

OPTION_LIST=( \
   "CML_HOST" \
   "CML_USERNAME" \
   "CML_PASSWORD" \
   "CML_LAB" \
   "VMANAGE_HOST" \
   "VMANAGE_ORG" \
   "VMANAGE_USERNAME" \
   "VMANAGE_PASS" \
   "VMANAGE1_IP" \
   "VBOND1_IP" \
   "VSMART1_IP" \
   "HQ_EDGE1_IP" \
   "SITE1_EDGE1_IP" \
   "SITE2_EDGE1_IP" \
   "VPN0_GATEWAY" \
   "VIPTELA_VERSION" \
   "VMANAGE_IMAGE" \
   "VSMART_IMAGE" \
   "VEDGE_IMAGE" \
   "CEDGE_IMAGE" \
   "CSR1000V_IMAGE" \
   "UBUNTU_IMAGE" \
   "CLOUDINIT_TYPE" \
   "CSR1000V_NODEDEF" \
   "UBUNTU_NODEDEF" \
   "VMANAGE_NODEDEF" \
   "VSMART_NODEDEF" \
   "VEDGE_NODEDEF" \
   "CEDGE_NODEDEF" \
   "ANSIBLE_VAULT_PASSWORD" \
   )

for OPTION in ${OPTION_LIST[*]}; do
   if [[ ! -z "${!OPTION}" ]]; then
      OPTIONS="$OPTIONS --env $OPTION=${!OPTION}"
   fi
done

OPTIONS="$OPTIONS --env ANSIBLE_ROLES_PATH=/ansible/roles"

while getopts ":dl" opt; do
  case $opt in
    d)
      docker run -it --rm -v $PWD:/ansible --env PWD="/ansible" -v $PWD/../python-viptela:/python-viptela --env USER="$USER" $OPTIONS $IMAGE /bin/ash
      exit
      ;;
    l)
      docker run -it --rm -v $PWD:/ansible --env PWD="/ansible" --env USER="$USER" $OPTIONS $IMAGE ansible-lint
      exit
      ;;
  esac
done
docker run -it --rm -v $PWD:/ansible --env PWD="/ansible" --env USER="$USER" $OPTIONS $IMAGE ansible-playbook "$@"
