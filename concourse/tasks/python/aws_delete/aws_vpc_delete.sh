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

echo "deleting security group...."
SDWAN_sg_id=$(vault kv get --field=SDWAN_sg_id concourse/sdwan/$NAME/SDWAN_sg_id)
export SDWAN_sg_id=$SDWAN_sg_id
echo $SDWAN_sg_id
aws ec2 delete-security-group --group-id $SDWAN_sg_id

echo "Deleting All Subnets...."
subnetid_public=$(vault kv get --field=subnetid_public concourse/sdwan/$NAME/subnetid_public)
export subnetid_public=$subnetid_public
aws ec2 delete-subnet --subnet-id $subnetid_public

subnetid_mgmt=$(vault kv get --field=subnetid_mgmt concourse/sdwan/$NAME/subnetid_mgmt)
export subnetid_mgmt=$subnetid_mgmt
aws ec2 delete-subnet --subnet-id $subnetid_mgmt

subnetid_cluster=$(vault kv get --field=subnetid_cluster concourse/sdwan/$NAME/subnetid_cluster)
export subnetid_cluster=$subnetid_cluster
aws ec2 delete-subnet --subnet-id $subnetid_cluster

vpcid=$(vault kv get --field=vpcid concourse/sdwan/$NAME/vpcid)
export vpcid=$vpcid


echo "Deleting the mgmt route table"
rt_mgmt_id=$(vault kv get --field=rt_mgmt_id concourse/sdwan/$NAME/rt_mgmt_id)
export rt_mgmt_id=$rt_mgmt_id
aws ec2 delete-route-table --route-table-id $rt_mgmt_id

echo "Deleting the cluster route table"
rt_cluster_id=$(vault kv get --field=rt_cluster_id concourse/sdwan/$NAME/rt_cluster_id)
export rt_cluster_id=$rt_cluster_id
aws ec2 delete-route-table --route-table-id $rt_cluster_id

echo "Detaching Internet Gateway......"
vpcid=$(vault kv get --field=vpcid concourse/sdwan/$NAME/vpcid)
export vpcid=$vpcid
igid=$(vault kv get --field=igid concourse/sdwan/$NAME/igid)
export igid=$igid
aws ec2 delete-internet-gateway --internet-gateway-id $igid
aws ec2 detach-internet-gateway --internet-gateway-id $igid --vpc-id $vpcid


echo "Deleting Internet Gateway....."
igid=$(vault kv get --field=igid concourse/sdwan/$NAME/igid)
export igid=$igid
aws ec2 delete-internet-gateway --internet-gateway-id $igid

echo "Deleting the VPC..."
echo "Deleting Internet Gateway....."
vpcid=$(vault kv get --field=vpcid concourse/sdwan/$NAME/vpcid)
export vpcid=$vpcid
aws ec2 delete-vpc --vpc-id $vpcid