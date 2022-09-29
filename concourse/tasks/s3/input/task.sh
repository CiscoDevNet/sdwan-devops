#!/bin/sh
export AWS_PAGER=""
export VAULT_ADDR=$VAULT_ADDR
export VAULT_TOKEN=$SSH_TOKEN
#create s3 bucket, policy and role.
aws s3api create-bucket --bucket sdwan-images --region $region
#get the arn of the S3 bucket and write to vault
#Update the policy.json to create the policy
