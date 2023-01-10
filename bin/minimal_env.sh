#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";
export PROJ_ROOT=$SCRIPT_DIR/..

export AWS_PROFILE="default"
export AWS_ACCESS_KEY_ID=$(aws configure get $AWS_PROFILE.aws_access_key_id)
export AWS_SECRET_ACCESS_KEY=$(aws configure get $AWS_PROFILE.aws_secret_access_key)
export AWS_SESSION_TOKEN=$(aws configure get $AWS_PROFILE.aws_session_token)
export AWS_REGION="us-east-2"

# You need only one of the two following variables. The first one is best for
# local runs, and is more secure. The second one is the easiest option for CI/CD
# and other automation
# export GOOGLE_OAUTH_ACCESS_TOKEN=$(gcloud auth print-access-token)
# export GOOGLE_CREDENTIALS=$(cat key.json | tr -s '\n' ' ')

# TODO: Remove value before commit
export VAULT_PASS=


