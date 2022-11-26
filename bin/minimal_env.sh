#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";

export PROJ_ROOT=$SCRIPT_DIR/..
export AWS_PROFILE="default"
export AWS_ACCESS_KEY_ID=$(aws configure get $AWS_PROFILE.aws_access_key_id)
export AWS_SECRET_ACCESS_KEY=$(aws configure get $AWS_PROFILE.aws_secret_access_key)
export AWS_SESSION_TOKEN=$(aws configure get $AWS_PROFILE.aws_session_token)
export AWS_REGION="us-east-2"

# export IOSXE_VERSION=17.08.01a
# export CEDGE_AMI=$(aws ec2 describe-images --filters "Name=name,Values=Cisco-C8K-${IOSXE_VERSION}-42cb6e93-8d9d-490b-a73c-e3e56077ffd1" --query "reverse(sort_by(Images,&CreationDate))[0].ImageId" --output text --region $AWS_REGION)

# Terraform for AWS has some computation built-in, hence the below values
export NETWORK_CIDR=10.128.0.0/22
export VMANAGE1_IP=10.128.1.11/24
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

# TODO: Remove value before commit
export VAULT_PASS="Cisc0123"
