#!/bin/sh
export AWS_PAGER=""
#This is required for vault
setcap cap_ipc_lock= /usr/bin/vault
python3 git-resource/tasks/aws_deploy/aws_key.py
cat *.pem
rm sshkey.pem
PRIVATE_KEY=$(ls *.pem)
echo $PRIVATE_KEY
export VAULT_ADDR=$VAULT_ADDR
export VAULT_TOKEN=$SSH_TOKEN
vault login --no-print $VAULT_TOKEN
#This is by team, so if logged into main you need the ssh-token that has the sdwan policy.
vault kv put concourse/sdwan/ssh-key ssh-key=@$PRIVATE_KEY






