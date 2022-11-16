#!/bin/sh
export AWS_PAGER=""
rm -rf __pycache__
echo "Working Directory...."
ls -la
cd git-resource/tasks/aws_deploy
python3 aws_deploy_vmanage.py

