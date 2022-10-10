#!/bin/sh
export AWS_PAGER=""
cp config ~/.aws
rm -rf __pycache__
python3 vmanage_deploy.py