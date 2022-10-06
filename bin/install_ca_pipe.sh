#!/usr/bin/env bash
export VAULT_ADDR=$VAULT_ADDR
export VAULT_TOKEN=$SSH_TOKEN
vault login --no-print $VAULT_TOKEN
echo $SSH_TOKEN
touch serialFile.viptela
LICENSE=(echo eeShahv3 > serialFile.viptela)
export LICENSE
vault kv put concourse/sdwan/serialFile.viptela serialFile.viptela=@$LICENSE
#require to write to the vault
#./play.sh "/ansible/day_-1/build-ca.yml"
