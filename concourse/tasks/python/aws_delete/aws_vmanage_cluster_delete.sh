#!/bin/sh
export AWS_PAGER=""
#This is required for vault
setcap cap_ipc_lock= /usr/bin/vault
#Logon to Vault and get: Instance IDs, volume IDs, NIC Ids and export to vars.
export NAME=$NAME
export VAULT_ADDR=$VAULT_ADDR
export VAULT_TOKEN=$SSH_TOKEN
vault login --no-print $VAULT_TOKEN
#vmanage-1
export vmanage-1_instance_id=$(vault kv get --field=vmanage_instance_id concourse/sdwan/$NAME/vmanage-1/vmanage_instance_id)
export vmanage-1_public_eni_id=$(vault kv get --field=vmanage_instance_id concourse/sdwan/$NAME/vmanage-1/public_eni_id)
export vmanage-1_cluster_eni_id=$(vault kv get --field=vmanage_instance_id concourse/sdwan/$NAME/vmanage-1/cluster_eni_id)
export vmanage-1_vol_id=$(vault kv get --field=vmanage_instance_id concourse/sdwan/$NAME/vmanage-1/vol_id)
#vmanage-2
export vmanage-2_instance_id=$(vault kv get --field=vmanage_instance_id concourse/sdwan/$NAME/vmanage-2/vmanage_instance_id)
export vmanage-2_public_eni_id=$(vault kv get --field=vmanage_instance_id concourse/sdwan/$NAME/vmanage-2/public_eni_id)
export vmanage-2_cluster_eni_id=$(vault kv get --field=vmanage_instance_id concourse/sdwan/$NAME/vmanage-2/cluster_eni_id)
export vmanage-2_vol_id=$(vault kv get --field=vmanage_instance_id concourse/sdwan/$NAME/vmanage-2/vol_id)
#vmanage-3
export vmanage-3_instance_id=$(vault kv get --field=vmanage_instance_id concourse/sdwan/$NAME/vmanage-3/vmanage_instance_id)
export vmanage-3_public_eni_id=$(vault kv get --field=vmanage_instance_id concourse/sdwan/$NAME/vmanage-3/public_eni_id)
export vmanage-3_cluster_eni_id=$(vault kv get --field=vmanage_instance_id concourse/sdwan/$NAME/vmanage-3/cluster_eni_id)
export vmanage-3_vol_id=$(vault kv get --field=vmanage_instance_id concourse/sdwan/$NAME/vmanage-3/vol_id)

printenv

#Delete Instances and Poll State.
#Delete NICs
#Delete Volumes

