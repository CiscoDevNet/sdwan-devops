#!/bin/sh
export AWS_PAGER=""
rm -rf __pycache__
apt -y update
apt -y install jq
pip3 install vault-cli
python3 sdwan-devops/concourse/aws_key.aws_key.py
#name the pem key with the name var
#See how the pem key is named
echo $name
ls -la *.pem
cat *.pem
#PRIVATE_KEY=$name + '.pem'
#echo "echo-ing out the var $PRIVATE_KEY
echo $PRIVATE_KEY
touch ssh-key.json
awk 'NF {sub(/\r/, ""); printf "%s\\n",$0;}' *.pem > ssh-key.json
#Later iteration, set up access so that the key can be written to vault for the team, for now manually add it.
#This is where send the key to the vault under the team name
#export VAULT_API_ADDR=http://vault.devops-ontap.com:8200
vault-cli set concourse/main/ssh-cert cert=@ssh-key.json
cat ssh-key.json



