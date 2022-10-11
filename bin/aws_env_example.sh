#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";

#Logon to Vault here
export NAME=$NAME
export VAULT_ADDR=$VAULT_ADDR
export VAULT_TOKEN=$SSH_TOKEN
vault login --no-print $VAULT_TOKEN
#Pass in the public key from vault that will be used for ssh later


export PROJ_ROOT=$SCRIPT_DIR/..
#put this in the vault - local task.
#export SSH_PUBKEY_BASE64="$(cat $HOME/.ssh/id_rsa.pub | base64)"
export SDWAN_CONTROL_INFRA="aws"
vault kv put concourse/sdwan/$NAME/SDWAN_CONTROL_INFRA SDWAN_CONTROL_INFRA=$SDWAN_CONTROL_INFRA
export AWS_PROFILE="default"
#export AWS_ACCESS_KEY_ID=$(aws configure get $AWS_PROFILE.aws_access_key_id)
#Right now this is in the container but will change
export AWS_ACCESS_KEY_ID=$AWS_KEY_ID
#export AWS_SECRET_ACCESS_KEY=$(aws configure get $AWS_PROFILE.aws_secret_access_key)
export AWS_SECRET_ACCESS_KEY=$AWS_KEY
#export AWS_SESSION_TOKEN=$(aws configure get $AWS_PROFILE.aws_session_token)
export AWS_REGION="us-west-2"

export VMANAGE_AMI="ami-0f727aeff8bfca1be"
vault kv put concourse/sdwan/$NAME/VMANAGE_AMI VMANAGE_AMI=$VMANAGE_AMI
export VMANAGE_INSTANCE_TYPE="t2.xlarge"
vault kv put concourse/sdwan/$NAME/VMANAGE_INSTANCE_TYPE VMANAGE_INSTANCE_TYPE=$VMANAGE_INSTANCE_TYPE
export VBOND_AMI="ami-0669c73a744a9071a"
vault kv put concourse/sdwan/$NAME/VBOND_AMI VBOND_AMI=$VBOND_AMI
export VBOND_INSTANCE_TYPE="t2.medium"
vault kv put concourse/sdwan/$NAME/VBOND_INSTANCE_TYPE VBOND_INSTANCE_TYPE=$VBOND_INSTANCE_TYPE
export VSMART_AMI="ami-0b3dcbdd1621b4819"
vault kv put concourse/sdwan/$NAME/VSMART_AMI VSMART_AMI=$VSMART_AMI
export VSMART_INSTANCE_TYPE="t2.medium"
vault kv put concourse/sdwan/$NAME/VSMART_INSTANCE_TYPE VSMART_INSTANCE_TYPE=$VSMART_INSTANCE_TYPE

# Example to generate a random password
# TODO  save it somewhere?
export VMANAGE_USERNAME="admin"
vault kv put concourse/sdwan/$NAME/VMANAGE_USERNAME VMANAGE_USERNAME=$VMANAGE_USERNAME
export VMANAGE_PASS="$(openssl rand -base64 12)"
vault kv put concourse/sdwan/$NAME/VMANAGE_PASS VMANAGE_PASS=$VMANAGE_PASS
export VMANAGE_ENCRYPTED_PASS="$(echo "$VMANAGE_PASS" | openssl passwd -6 -stdin)"
vault kv put concourse/sdwan/$NAME/VMANAGE_ENCRYPTED_PASSS VMANAGE_ENCRYPTED_PASS=$VMANAGE_ENCRYPTED_PASS
export SDWAN_CA_PASSPHRASE="$(openssl rand -base64 15)"
vault kv put concourse/sdwan/$NAME/SDWAN_CA_PASSPHRASES SDWAN_CA_PASSPHRASE=$SDWAN_CA_PASSPHRASE

# Distinguishing single and double quotes is very important for this to work
export ACL_RANGES_IPV4_BASE64=$(echo '"0.0.0.0/1", "128.0.0.0/1"' | base64)
vault kv put concourse/sdwan/$NAME/ACL_RANGES_IPV4_BASE64 ACL_RANGES_IPV4_BASE64=$ACL_RANGES_IPV4_BASE64
export ACL_RANGES_IPV6_BASE64=$(echo '"::/0"' | base64)
vault kv put concourse/sdwan/$NAME/ACL_RANGES_IPV6_BASE644 ACL_RANGES_IPV6_BASE64=$ACL_RANGES_IPV6_BASE64

# SDWAN_DATACENTER is the generic variable which is the region for AWS or the
# vSphere datacenter, depending on the infra
export SDWAN_DATACENTER=$AWS_REGION
vault kv put concourse/sdwan/$NAME/SDWAN_DATACENTER SDWAN_DATACENTER=$SDWAN_DATACENTER
# Terraform for AWS has some computation built-in, hence the below values
# TODO  document static addressing
export NETWORK_CIDR=10.128.0.0/22
vault kv put concourse/sdwan/$NAME/NETWORK_CIDR NETWORK_CIDR=$NETWORK_CIDR
export VMANAGE1_IP=10.128.1.11/24
vault kv put concourse/sdwan/$NAME/MANAGE1_IP VMANAGE1_IP=$MANAGE1_IP
export VBOND1_IP=10.128.1.12/24
vault kv put concourse/sdwan/$NAME/VBOND1_IP VBOND1_IP=$VBOND1_IP
export VSMART1_IP=10.128.1.13/24
vault kv put concourse/sdwan/$NAME/VSMART1_IP VSMART1_IP=$VSMART1_IP
export VPN0_GATEWAY=10.128.1.1
vault kv put concourse/sdwan/$NAME/VPN0_GATEWAY VPN0_GATEWAY=$VPN0_GATEWAY

# This should be the VPC ID eventually
#export VPN0_PORTGROUP="cpn-rtp-colab4"
#export VPN512_PORTGROUP="cpn-rtp-colab4"
#export SERVICEVPN_PORTGROUP="cpn-rtp-colab4"

export HQ_EDGE1_IP=1.1.1.4/24
vault kv put concourse/sdwan/$NAME/HQ_EDGE1_IPY HQ_EDGE1_IP=$HQ_EDGE1_IP
export SITE1_EDGE1_IP=1.1.1.5/24
vault kv put concourse/sdwan/$NAME/SITE1_EDGE1_IPY SITE1_EDGE1_IP=$SITE1_EDGE1_IP
export SITE2_EDGE1_IP=1.1.1.6/24
vault kv put concourse/sdwan/$NAME/SITE2_EDGE1_IP SITE2_EDGE1_IP=$SITE2_EDGE1_IP

export IOSXE_SDWAN_IMAGE=iosxe-sdwan-16.12.5
vault kv put concourse/sdwan/$NAME/IOSXE_SDWAN_IMAGEP IOSXE_SDWAN_IMAGE=$IOSXE_SDWAN_IMAGE

export VIPTELA_VERSION=20.8.1
vault kv put concourse/sdwan/$NAME/VIPTELA_VERSION VIPTELA_VERSION=$VIPTELA_VERSION

export VMANAGE_ORG=CIDR_SDWAN_WORKSHOPS
vault kv put concourse/sdwan/$NAME/VMANAGE_ORGN VMANAGE_ORG=$VMANAGE_ORG

export CLOUDINIT_TYPE=v2
vault kv put concourse/sdwan/$NAME/CLOUDINIT_TYPE CLOUDINIT_TYPE=$CLOUDINIT_TYPE
