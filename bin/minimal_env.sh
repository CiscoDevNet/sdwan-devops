#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";

export PROJ_ROOT=$SCRIPT_DIR/..
export AWS_PROFILE="default"
export AWS_ACCESS_KEY_ID=$(aws configure get $AWS_PROFILE.aws_access_key_id)
export AWS_SECRET_ACCESS_KEY=$(aws configure get $AWS_PROFILE.aws_secret_access_key)
export AWS_SESSION_TOKEN=$(aws configure get $AWS_PROFILE.aws_session_token)
export AWS_REGION="us-east-2"

# This should be the VPC ID eventually
#export VPN0_PORTGROUP="cpn-rtp-colab4"
#export VPN512_PORTGROUP="cpn-rtp-colab4"
#export SERVICEVPN_PORTGROUP="cpn-rtp-colab4"

# TODO: Remove value before commit
export VAULT_PASS=

# export GCP_PROJECT="gcp-sdwaniac-nprd-84677"

