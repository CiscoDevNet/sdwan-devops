#!/bin/sh
export AWS_PAGER=""
#This is required for vault
setcap cap_ipc_lock= /usr/bin/vault
export NAME=$NAME
export VAULT_ADDR=$VAULT_ADDR
export VAULT_TOKEN=$SSH_TOKEN
vault login --no-print $VAULT_TOKEN
#Get vpcid from vault
vpcid=$(vault kv get --field=vpcid concourse/sdwan/$NAME/vpcid)
export vpcid=$vpcid
echo $vpcid
#Get instance id from vault
vmanage_instance_id=$(vault kv get --field=vmanage_instance_id concourse/sdwan/$NAME/vmanage/vmanage_instance_id)
export vmanage_instance_id=$vmanage_instance_id
echo $vmanage_instance_id
echo "Terminating the vmanage instance..."
aws ec2 terminate-instances --instance-ids $vmanage_instance_id
aws ec2 wait instance-terminated --instance-ids $vmanage_instance_id
echo "Deleting the volume....."
#Get vol_id from vault
vol_id=$(vault kv get --field=vol_id concourse/sdwan/$NAME/vmanage/vol_id)
export vol_id=$vol_id
echo $vol_id
aws ec2 delete-volume --volume-id $vol_id
echo "Deleting the secondary network card"
#Get public eni id from vault
public_eni_id=$(vault kv get --field=public_eni_id concourse/sdwan/$NAME/vmanage/public_eni_id)
export public_eni_id=$public_eni_id
echo $public_eni_id
aws ec2 delete-network-interface --network-interface-id $public_eni_id --region $REGION
