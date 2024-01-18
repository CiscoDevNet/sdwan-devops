#!/usr/bin/env bash

# Uncomment the following and define proper values (or specify as environment variables)

# GITLAB_HOST=https://gitlab.example.com
# GITLAB_USER=foo
# GITLAB_API_TOKEN=abc123
# GITLAB_PROJECT=sdwan-devops
# CML_HOST=cml.example.com
# CML_USERNAME=foo
# CML_PASSWORD=bar
# CML_LAB=sdwan-devops
# VMANAGE_ORG=your-org

# Add new project
curl --request POST -sSLk --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "$GITLAB_HOST/api/v4/projects" --form "name=$GITLAB_PROJECT"

# Add new vars
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
    curl --request POST -sSLk --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "$GITLAB_HOST/api/v4/projects/$GITLAB_USER%2f$GITLAB_PROJECT/variables" --form "key=$OPTION" --form "value=${!OPTION}"    
  fi
done

git push https://$GITLAB_USER:$GITLAB_PASSWORD@$GITLAB_HOST/$GITLAB_USER/$GITLAB_PROJECT