#!/bin/sh
cd input
chmod 400 *.pem
export AWS_PAGER=""
rm -rf __pycache__
#run instance with the user data and verify it comes up correctly
aws ec2 run instances --image-id ami-0f727aeff8bfca1be --subnet-id  subnet-0452e6a65a00efdd8 --key-name us-west-2a --security-group-ids sg-0128fedae52fe69ba --user-data file://vmanage.user_data
