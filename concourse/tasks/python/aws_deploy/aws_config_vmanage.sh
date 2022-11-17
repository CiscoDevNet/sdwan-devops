#!/bin/sh
export AWS_PAGER=""
#This is required for vault
setcap cap_ipc_lock= /usr/bin/vault
export NAME=$NAME
export VAULT_ADDR=$VAULT_ADDR
export VAULT_TOKEN=$SSH_TOKEN
vault login --no-print $VAULT_TOKEN
#Get the EDSA priv and pub key from vault and set as env vars to be used in python script that will use AWS CLI to copy them up
cd aws_deploy
ssh-keygen -t ed25519 -q -f "ed25519" -N ""
EDSA_PRIVATE_KEY=$(ls ed25519)
EDSA_PUBLIC_KEY=$(ls ed25519.pub)
export EDSA_PRIVATE_KEY
export EDSA_PUBLIC_KEY
vault kv put concourse/sdwan/$NAME/ssh-ed25519-private-key ssh-key=@$EDSA_PRIVATE_KEY
vault kv put concourse/sdwan/$NAME/ssh-ed25519-public-key ssh-key=@$EDSA_PUBLIC_KEY
#vault kv get --field=ssh-key concourse/sdwan/$NAME/ssh-ed25529-private-key >> ed25519
#vault kv get --field=ssh-key concourse/sdwan/$NAME/ssh-ed25519-public-key >> ed25519.pub
#vault kv get --field=vmanage_user_data concourse/sdwan/vmanage_user_data >> /git-cisco-sdwan-devops/tasks/python/aws_deploy/vmanage_user_data
#copy the public key to each instance - get the instance_id for each of the 3 instances from the  vault
vault kv get --field=vmanage_instance_id concourse/sdwan/$NAME/vmanage/vmanage_instance_id >> instance_id
export INSTANCE_1_ID=$(cat instance_id)
aws ec2-instance-connect send-serial-console-ssh-public-key --instance-id $INSTANCE_1_ID --serial-port 0 --ssh-public-key file://ed25519.pub --region $REGION

#aws ec2-instance-connect send-serial-console-ssh-public-key --instance-id i-0f678cce2a4fc9ae7 --serial-port 0 --ssh-public-key file://id_ed25519.pub --region us-west-2
#ssh -i id_ed25519 i-0f678cce2a4fc9ae7.port0@serial-console.ec2-instance-connect.us-west-2.aws




