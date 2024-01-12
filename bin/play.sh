#!/usr/bin/env bash
IMAGE=${IMAGE:-ghcr.io/ciscodevnet/sdwan-devops:main}
OPTIONS=""

if [[ ! -z "$ANSIBLE_VAULT_PASSWORD_FILE" ]]; then
   OPTIONS="--env ANSIBLE_VAULT_PASSWORD_FILE=/tmp/vault.pw -v $ANSIBLE_VAULT_PASSWORD_FILE:/tmp/vault.pw"
fi

OPTION_LIST=( \
   "AWS_ACCESS_KEY_ID" \
   "AWS_SECRET_ACCESS_KEY" \
   "AWS_SESSION_TOKEN" \
   "ARM_CLIENT_ID" \
   "ARM_CLIENT_SECRET" \
   "ARM_SUBSCRIPTION_ID" \
   "ARM_TENANT_ID" \
   "GOOGLE_OAUTH_ACCESS_TOKEN" \
   "GCP_PROJECT" \
   "PROJ_ROOT" \
   "CONFIG_BUILDER_METADATA"
   )

for OPTION in ${OPTION_LIST[*]}; do
   if [[ ! -z "${!OPTION}" ]]; then
      OPTIONS="$OPTIONS --env $OPTION=${!OPTION}"
   fi
done

OPTIONS="$OPTIONS --env ANSIBLE_ROLES_PATH=/ansible/roles --env ANSIBLE_STDOUT_CALLBACK=debug"

while getopts ":dlc" opt; do
   case $opt in
   d)
      docker run -it --rm -v $PROJ_ROOT/ansible:/ansible \
      -v $PROJ_ROOT/terraform-sdwan:/terraform-sdwan \
      -v $PROJ_ROOT/sdwan-edge:/sdwan-edge \
      -v $PROJ_ROOT/config:/config \
      -v $PWD/../python-viptela:/python-viptela \
      --env PWD="/ansible" \
      --env USER="$USER" \
      $OPTIONS \
      $IMAGE /bin/bash
      exit
      ;;
   l)
      docker run -it --rm -v $PROJ_ROOT/ansible:/ansible \
         --env PWD="/ansible" \
         --env USER="$USER" \
         $OPTIONS \
         $IMAGE ansible-lint --offline
      exit
      ;;
   c)
      shift $((OPTIND-1))
      docker run -it --rm -v $PROJ_ROOT/ansible:/ansible \
         -v $PROJ_ROOT/terraform-sdwan:/terraform-sdwan \
         -v $PROJ_ROOT/sdwan-edge:/sdwan-edge \
         -v $PROJ_ROOT/config:/config \
         --env PWD="/ansible" \
         --env USER="$USER" \
         $OPTIONS \
         $IMAGE sdwan_config_build "$@"
      exit
      ;;
  esac
done
docker run -it --rm -v $PROJ_ROOT/ansible:/ansible \
   -v $PROJ_ROOT/terraform-sdwan:/terraform-sdwan \
   -v $PROJ_ROOT/sdwan-edge:/sdwan-edge \
   `# Uncomment the following line if you are using a container image with the Azure CLI included and want to deploy a cEdge on Azure` \
   `#-v $HOME/.azure:/root/.azure` \
   --env PWD="/ansible" \
   --env USER="$USER" \
   --env GOOGLE_CREDENTIALS="$GOOGLE_CREDENTIALS" \
   $OPTIONS \
   $IMAGE ansible-playbook "$@"
