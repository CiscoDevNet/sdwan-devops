#!/usr/bin/env bash

set -o pipefail

IMAGE=${IMAGE:-ghcr.io/ciscodevnet/sdwan-devops:cloud}

if [ -z ${PROJ_ROOT+x} ]; then echo "PROJ_ROOT is unset, please source the env script"; exit 1; else echo "PROJ_ROOT is set to '$PROJ_ROOT'"; fi

LICENSE_DIR=ansible/licenses
rm -rf $PROJ_ROOT/myCA
rm -rf $PROJ_ROOT/$LICENSE_DIR
mkdir $PROJ_ROOT/$LICENSE_DIR
echo "$VAULT_PASS" > $PROJ_ROOT/$LICENSE_DIR/vault-password-file
#TODO is this the right location for the serialFile? Should the serialFile be in a different directory on its own?
#ansible-vault decrypt --vault-password-file $LICENSE_DIR/vault-password-file $PROJ_ROOT/ansible/files/serialFile.viptela --output $LICENSE_DIR/serialFile.viptela
docker run -it --rm -v $PROJ_ROOT/ansible:/ansible --env PWD="/ansible" $IMAGE ansible-vault decrypt --vault-password-file /$LICENSE_DIR/vault-password-file /ansible/files/serialFile.viptela --output /$LICENSE_DIR/serialFile.viptela
#require to write to the vault
./play.sh "/ansible/day_-1/build-ca.yml"
