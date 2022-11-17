#!/bin/sh
export AWS_PAGER=""
export VAULT_ADDR=$VAULT_ADDR
export VAULT_TOKEN=$SSH_TOKEN
python3 git-cisco-sdwan-devops/tasks/python/aws_deploy/aws_env_deploy.py
