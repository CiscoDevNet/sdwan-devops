#!/usr/bin/env bash

set -o pipefail

IMAGE=${IMAGE:-ghcr.io/ciscodevnet/sdwan-devops:main}

if [ -z ${PROJ_ROOT+x} ]; then echo "PROJ_ROOT is unset, please source the env script"; exit 1; else echo "PROJ_ROOT is set to '$PROJ_ROOT'"; fi

mkdir -p $PROJ_ROOT/ansible/licenses
echo "$VAULT_PASS" > $PROJ_ROOT/ansible/files/vault-password-file
docker run -it --rm -v $PROJ_ROOT/ansible:/ansible --env PWD="/ansible" $IMAGE \
    ansible-vault decrypt --vault-password-file /ansible/files/vault-password-file \
    /ansible/files/serialFile.viptela \
    --output /ansible/licenses/serialFile.viptela

docker run -it --rm -v $PROJ_ROOT/ansible:/ansible  -v $PROJ_ROOT/config:/config --env PWD="/ansible" $IMAGE \
    ansible-vault decrypt --vault-password-file /ansible/files/vault-password-file \
    /ansible/files/config.yaml \
    --output /config/config.yaml
