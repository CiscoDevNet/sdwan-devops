#!/usr/bin/env bash

# Uncomment the following and define proper values (or specify as environment variables)

# GITLAB_HOST=https://gitlab.example.com
# GITLAB_USER=foo
# GITLAB_API_TOKEN=abc123
# GITLAB_PROJECT=sdwan-devops
# VIRL_HOST=cml.example.com
# VIRL_USERNAME=foo
# VIRL_PASSWORD=bar
# VIRL_LAB=sdwan-devops
# VMANAGE_ORG=your-org

# Add new project
curl --request POST -sSLk --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "$GITLAB_HOST/api/v4/projects" --form "name=$GITLAB_PROJECT"

# Add new vars
OPTION_LIST=( \
   "VIRL_HOST" \
   "VIRL_USERNAME" \
   "VIRL_PASSWORD" \
   "VIRL_LAB" \
   "VMANAGE_ORG" \
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
    curl --request POST -sSLk --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "$GITLAB_HOST/api/v4/projects/$GITLAB_USER%2f$GITLAB_PROJECT/variables" --form "key=$OPTION" --form "value=${!OPTION}"    
  fi
done