#!/bin/sh
export AWS_PAGER=""
#This is required for vault
setcap cap_ipc_lock= /usr/bin/vault
wget https://releases.hashicorp.com/vault/1.11.3/vault_1.11.3_linux_amd64.zip
unzip vault_1.11.3_linux_amd64.zip
mv vault /usr/bin
export NAME=$NAME
export VAULT_ADDR=$VAULT_ADDR
export VAULT_TOKEN=$SSH_TOKEN
vault login --no-print $VAULT_TOKEN
vault kv get --field=ssh-key concourse/sdwan/$NAME/ssh-ed25529-private-key >> input/ed25519
cd input
chmod 400 ed25519
#copy the public key to each instance - get the instance_id for each of the 3 instances from the  vault
#vault kv get --field=vmanage_instance_id concourse/sdwan/$NAME/vmanage/vmanage_instance_id >> instance_id
#REQUIRE UPDATE TO DEPLOY SCRIPT TO WRITE THE ELASTIC IP OF THE MGMT NIC TO THE VAULT
#vault kv get --field=vmanage_instance_id concourse/sdwan/$NAME/vmanage/vmanage_instance_id >> instance_id
export INSTANCE_1_ID=$(cat instance_id)
REGION='us-west-2'
export REGION
export ip='44.229.184.207'
python3 input/configure_vmanage.py

#aws ec2-instance-connect send-serial-console-ssh-public-key --instance-id i-0f678cce2a4fc9ae7 --serial-port 0 --ssh-public-key file://id_ed25519.pub --region us-west-2
#ssh -i id_ed25519 i-0f678cce2a4fc9ae7.port0@serial-console.ec2-instance-connect.us-west-2.aws




