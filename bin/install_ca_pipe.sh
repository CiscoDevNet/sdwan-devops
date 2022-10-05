#!/usr/bin/env bash
pip3 install ansible-vault
set -o pipefail

if [ -z ${PROJ_ROOT+x} ]; then echo "PROJ_ROOT is unset, please source the env script"; exit 1; else echo "PROJ_ROOT is set to '$PROJ_ROOT'"; fi

PROJ_ROOT="bin/"
LICENSE_DIR=$PROJ_ROOT/ansible/licenses
rm -rf $PROJ_ROOT/myCA
rm -rf $LICENSE_DIR
mkdir $LICENSE_DIR
echo eeShahv3 > $LICENSE_DIR/vault-password-file
#TODO is this the right location for the serialFile? Should the serialFile be in a different directory on its own?
ansible-vault decrypt --vault-password-file $LICENSE_DIR/vault-password-file $PROJ_ROOT/ansible/files/serialFile.viptela --output $LICENSE_DIR/serialFile.viptela
#require to write to the vault
./play.sh "/ansible/day_-1/build-ca.yml"
