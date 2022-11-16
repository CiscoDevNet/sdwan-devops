#!/bin/sh
export AWS_PAGER=""
#This is required for vault
setcap cap_ipc_lock= /usr/bin/vault
export NAME=$NAME
export VAULT_ADDR=$VAULT_ADDR
export VAULT_TOKEN=$SSH_TOKEN
vault login --no-print $VAULT_TOKEN
#This is by team, so if logged into main you need the ssh-token that has the sdwan policy.
ssh-keygen -t ed25519 -q -f "ed25519" -N ""
EDSA_PRIVATE_KEY=$(ls ed25519)
EDSA_PUBLIC_KEY=$(ls ed25519.pub)
export EDSA_PRIVATE_KEY
export EDSA_PUBLIC_KEY
vault kv put concourse/sdwan/$NAME/ssh-ed25519-private-key ssh-key=@$EDSA_PRIVATE_KEY
vault kv put concourse/sdwan/$NAME/ssh-ed25519-public-key ssh-key=@$EDSA_PUBLIC_KEY






