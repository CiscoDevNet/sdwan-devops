#!/bin/sh
export AWS_PAGER=""
rm -rf __pycache__
python3 git-cisco-sdwan-devops/tasks/python/aws_deploy/aws_deploy_vmanage_1.py

#copy the ed25519 key to the instance
