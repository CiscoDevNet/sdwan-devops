#!/bin/sh
export AWS_PAGER=""
rm -rf __pycache__
echo "Working Directory...."
ls -la
cd git-cisco-sdwan-devops/tasks/python/aws_deploy
python3 aws_deploy_vmanage.py

