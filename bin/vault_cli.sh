#!/bin/sh
export AWS_PAGER=""
#This is required for vault
setcap cap_ipc_lock= /usr/bin/vault
export VAULT_ADDR=$VAULT_ADDR
export VAULT_TOKEN=$SSH_TOKEN
vault login --no-print $VAULT_TOKEN
vault kv get --field=ssh-key concourse/sdwabn/$NAME >> sshkey.pem
SSHKEY='sshkey.pem'
#vault kv put concourse/sdwan/$NAME/ssh-key ssh-key=@$PRIVATE_KEY

