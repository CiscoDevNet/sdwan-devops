#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";

#Logon to Vault here
#Pass in the public key from vault that will be used for ssh later


export PROJ_ROOT=$SCRIPT_DIR/..
#put this in the vault - local task.
#export SSH_PUBKEY_BASE64="$(cat $HOME/.ssh/id_rsa.pub | base64)"
# The below is used for adding SSH public key fingerprints to cEdges. It will only work with ssh-rsa type keys
#export SSH_PUBKEY_FP_BASE64="$(ssh-keygen -E md5 -lf ~/.ssh/id_rsa.pub | awk '{ print toupper($2) " " $3 }' | sed 's/MD5://' | sed 's/://g' | base64)"
export SDWAN_CONTROL_INFRA="aws"
export AWS_PROFILE="default"
export AWS_ACCESS_KEY_ID=$(aws configure get $AWS_PROFILE.aws_access_key_id)
export AWS_SECRET_ACCESS_KEY=$(aws configure get $AWS_PROFILE.aws_secret_access_key)
export AWS_SESSION_TOKEN=$(aws configure get $AWS_PROFILE.aws_session_token)
export AWS_REGION="us-west-2"

export VMANAGE_AMI="ami-0f727aeff8bfca1be"
export VMANAGE_INSTANCE_TYPE="t2.xlarge"
export VBOND_AMI="ami-0669c73a744a9071a"
export VBOND_INSTANCE_TYPE="t2.medium"
export VSMART_AMI="ami-0b3dcbdd1621b4819"
export VSMART_INSTANCE_TYPE="t2.medium"

# Example to generate a random password
# TODO  save it somewhere?
export VMANAGE_USERNAME="admin"
export VMANAGE_PASS="$(openssl rand -base64 12)"
export VMANAGE_ENCRYPTED_PASS="$(echo "$VMANAGE_PASS" | openssl passwd -6 -stdin)"
export SDWAN_CA_PASSPHRASE="$(openssl rand -base64 15)"

# Distinguishing single and double quotes is very important for this to work
export ACL_RANGES_IPV4_BASE64=$(echo '"0.0.0.0/1", "128.0.0.0/1"' | base64)
export ACL_RANGES_IPV6_BASE64=$(echo '"::/0"' | base64)

# SDWAN_DATACENTER is the generic variable which is the region for AWS or the
# vSphere datacenter, depending on the infra
export SDWAN_DATACENTER=$AWS_REGION
# If set, add A records for control plane element external addresses in AWS Route 53
export DNS_DOMAIN=
# Terraform for AWS has some computation built-in, hence the below values
# TODO  document static addressing
export NETWORK_CIDR=10.128.0.0/22
export VMANAGE1_IP=10.128.1.11/24
export VBOND1_IP=10.128.1.12/24
export VSMART1_IP=10.128.1.13/24
export VPN0_GATEWAY=10.128.1.1

# This should be the VPC ID eventually
#export VPN0_PORTGROUP="cpn-rtp-colab4"
#export VPN512_PORTGROUP="cpn-rtp-colab4"
#export SERVICEVPN_PORTGROUP="cpn-rtp-colab4"

export HQ_EDGE1_IP=1.1.1.4/24
export SITE1_EDGE1_IP=1.1.1.5/24
export SITE2_EDGE1_IP=1.1.1.6/24

export IOSXE_SDWAN_IMAGE=iosxe-sdwan-16.12.5

export VIPTELA_VERSION=20.8.1

export VMANAGE_ORG=CIDR_SDWAN_WORKSHOPS

export CLOUDINIT_TYPE=v2
