#!/bin/sh
export AWS_PAGER=""
export AWS_PAGER=""
#This is required for vault
setcap cap_ipc_lock= /usr/bin/vault
export VAULT_ADDR=$VAULT_ADDR
export VAULT_TOKEN=$SSH_TOKEN
vault login --no-print $VAULT_TOKEN
export NAME=$NAME
export REGION=$REGION
#Get the EDSA priv and pub key from vault and set as env vars to be used in python script that will use AWS CLI to copy them up
vault kv get --field=ssh-key concourse/sdwan/$NAME/ssh-ed25519-private-key >> aws_deploy/ed25519
vault kv get --field=ssh-key concourse/sdwan/$NAME/ssh-ed25519-public-key >> aws_deploy/ed25519.pub
#copy the public key to each instance - get the instance_id for each of the 3 instances from the  vault
cd aws_deploy
vault kv get --field=vmanage_instance_id concourse/sdwan/$NAME/vmanage-1/vmanage_instance_id >> instance_id_1
export INSTANCE_1_ID=$(cat instance_id_1)
echo $INSTANCE_1_ID
aws ec2-instance-connect send-serial-console-ssh-public-key --instance-id $INSTANCE_1_ID --serial-port 0 --ssh-public-key file://ed25519.pub --region $REGION ---cli-connect-timeout 5

vault kv get --field=vmanage_instance_id concourse/sdwan/$NAME/vmanage-2/vmanage_instance_id >> instance_id_2
export INSTANCE_2_ID=$(cat instance_id_2)
echo $INSTANCE_2_ID
aws ec2-instance-connect send-serial-console-ssh-public-key --instance-id $INSTANCE_2_ID --serial-port 0 --ssh-public-key file://ed25519.pub --region $REGION --cli-connect-timeout 5

vault kv get --field=vmanage_instance_id concourse/sdwan/$NAME/vmanage-3/vmanage_instance_id >> instance_id_3
export INSTANCE_3_ID=$(cat instance_id_3)
echo $INSTANCE_3_ID
aws ec2-instance-connect send-serial-console-ssh-public-key --instance-id $INSTANCE_3_ID --serial-port 0 --ssh-public-key file://ed25519.pub --region $REGION --cli-connect-timeout 5







