#!/bin/sh
cd input
export AWS_PAGER=""
rm -rf __pycache__
pip3 install ansible
pip3 show ansible
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common
wget -O- https://apt.releases.hashicorp.com/gpg gpg --dearmor | tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
gpg --no-default-keyring --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg --fingerprint
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/hashicorp.list
apt-get install terraform
touch ~/.bashrc
terraform -install-autocomplete
pip3 install ansible-vault
#This should set all environmental vars in the build container
./aws_env_examples.sh
#python3 vault_vars.py

