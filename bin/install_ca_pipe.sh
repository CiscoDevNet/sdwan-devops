#!/usr/bin/env bash
export VAULT_ADDR=$VAULT_ADDR
export VAULT_TOKEN=$SSH_TOKEN
vault login --no-print $VAULT_TOKEN
echo $SSH_TOKEN
touch serialFile.viptela
echo eeShahv3 > serialFile.viptela
LICENSE='serialFile.viptela'
vault kv put concourse/sdwan/serialFile.viptela serialFile.viptela=@$LICENSE
#require to write to the vault
./bin/play.sh "/ansible/day_-1/build-ca.yml"
