#!/bin/sh
export AWS_PAGER=""
rm -rf __pycache__
echo "Until OCI Build Container is updated with Terraform and Ansible - installing it now on the container....."
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
chmod a+x sdwan-devops/bin/aws_env_example_pipe.sh
./sdwan-devops/bin/aws_env_example.sh
#Step 1 - manual task to write all VARS to vault.

#chmod a+x sdwan-devops/bin/initialize.sh
#./sdwan-devops/bin/initialize.sh










