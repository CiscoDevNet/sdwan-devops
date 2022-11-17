#!/bin/sh
export AWS_PAGER=""
rm -rf __pycache__
python3 git-cisco-sdwan-devops/tasks/python/aws_deploy/aws_deploy_vmanage_2.py

