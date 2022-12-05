#!/usr/bin/env bash

# If you're on a Mac and used Hombrew to install OpenSSL 3, uncomment the
# following line (if you want to take advantage of the password hashing ability)
#export PATH="/opt/homebrew/opt/openssl@3/bin:$PATH"

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";

export VIPTELA_VERSION=20.8.1
export IOSXE_VERSION=17.08.01a
export IOSXE_VERSION_DASHES=17-08-01a

export PROJ_ROOT=$SCRIPT_DIR/..
export SSH_PUBKEY_BASE64="$(cat $HOME/.ssh/id_rsa.pub | base64)"
# The below is used for adding SSH public key fingerprints to cEdges. It will only work with ssh-rsa type keys
export SSH_PUBKEY_FP_BASE64="$(ssh-keygen -E md5 -lf ~/.ssh/id_rsa.pub | awk '{ print toupper($2) " " $3 }' | sed 's/MD5://' | sed 's/://g' | base64)"
export SDWAN_CONTROL_INFRA="aws"
export AWS_PROFILE="default"
export AWS_ACCESS_KEY_ID=$(aws configure get $AWS_PROFILE.aws_access_key_id)
export AWS_SECRET_ACCESS_KEY=$(aws configure get $AWS_PROFILE.aws_secret_access_key)
export AWS_SESSION_TOKEN=$(aws configure get $AWS_PROFILE.aws_session_token)
export AWS_REGION="us-east-2"

export VMANAGE_AMI="ami-00383691e06a97ec6"
export VMANAGE_INSTANCE_TYPE="t2.xlarge"
export VBOND_AMI="ami-081b3a108aa230f88"
export VBOND_INSTANCE_TYPE="t2.medium"
export VSMART_AMI="ami-063f1b59c2694a7ef"
export VSMART_INSTANCE_TYPE="t2.medium"

export CEDGE_AMI=$(aws ec2 describe-images --filters "Name=name,Values=Cisco-C8K-${IOSXE_VERSION}-42cb6e93-8d9d-490b-a73c-e3e56077ffd1" --query "reverse(sort_by(Images,&CreationDate))[0].ImageId" --output text --region $AWS_REGION)
export CEDGE_AWS_INSTANCE_TYPE="t3.medium"

export CEDGE_GCP_IMAGE_ID="cisco-public/cisco-c8k-${IOSXE_VERSION_DASHES}"
export CEDGE_GCP_INSTANCE_TYPE="n1-standard-4"
export GCP_PROJECT=
# You need only one of the two following variables. The first one is best for
# local runs, and is more secure. The second one is the easiest option for CI/CD
# and other automation
#export GOOGLE_OAUTH_ACCESS_TOKEN=$(gcloud auth print-access-token)
#export GOOGLE_CREDENTIALS=$(cat key.json | tr -s '\n' ' ')

# Example to generate a random password
# TODO  save it somewhere?
export VMANAGE_USERNAME="admin"
export VMANAGE_PASS="$(openssl rand -base64 12)"
export VMANAGE_ENCRYPTED_PASS="$(echo "$VMANAGE_PASS" | openssl passwd -6 -stdin)"
export SDWAN_CA_PASSPHRASE="$(openssl rand -base64 15)"
export VAULT_PASS=

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

# Each site is expected to have a /23, as Ansible will compute static addresses based on this assumption
export HQ_EDGE1_RANGE=10.128.4.0/23
export SITE1_EDGE1_RANGE=10.128.6.0/23
export SITE2_EDGE1_RANGE=10.128.8.0/23

export IOSXE_SDWAN_IMAGE=iosxe-sdwan-${IOSXE_VERSION}

export VMANAGE_ORG="Cisco CX Canada"

export CLOUDINIT_TYPE=v2
