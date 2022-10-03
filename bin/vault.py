#!/usr/bin/env python
import json, re, sys, os, json, time, logging, requests, urllib3
from requests.structures import CaseInsensitiveDict
urllib3.disable_warnings()
from requests.structures import CaseInsensitiveDict
import subprocess
from subprocess import call, check_output

#This allows this script to logon to the vault and write the vars under the concourse/sdwan mount point as this is the only dir that the
#policy in vault will grant this token access to read/write
VAULT_ADDR = os.getenv('VAULT_ADDRR')
VAULT_TOKEN = os.getenv('SSH_TOKEN')

#VAULT SECTION
print("Writing Generated Objects to Vault.....")

#Write PROJ_ROOT  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "PROJ_ROOT"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"PROJ_ROOT": PROJ_ROOT }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)



print("Writing Generated Objects to Vault.....")

#Write SSH_PUBKEY_BASE64  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "SSH_PUBKEY_BASE64"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"SSH_PUBKEY_BASE64": SSH_PUBKEY_BASE64 }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)


#Write SDWAN_CONTROL_INFRA  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "SDWAN_CONTROL_INFRA"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"SDWAN_CONTROL_INFRA": SDWAN_CONTROL_INFRA }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)

#Write AWS_PROFILE  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "AWS_PROFILE"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"AWS_PROFILE": AWS_PROFILE }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)


#Write AWS_ACCESS_KEY_ID  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "AWS_ACCESS_KEY_ID"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)

#Write AWS_SECRET_ACCESS_KEY  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "AWS_SECRET_ACCESS_KEY"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)

#Write AWS_REGION  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "AWS_REGION"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"AWS_REGION": AWS_REGION }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)


#Write VMANAGE_AMI  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "VMANAGE_AMI"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"VMANAGE_AMI": VMANAGE_AMI }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)

#Write VMANAGE_INSTANCE_TYPE  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "VMANAGE_INSTANCE_TYPE"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"VMANAGE_INSTANCE_TYPE": VMANAGE_INSTANCE_TYPE }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)


#Write VBOND_AMI  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "VBOND_AMI"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"VBOND_AMI": VBOND_AMI }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)


#Write VBOND_INSTANCE_TYPE  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "VBOND_INSTANCE_TYPE"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"VBOND_INSTANCE_TYPE": VBOND_INSTANCE_TYPE }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)

#Write VSMART_AMI  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "VSMART_AMI"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"VSMART_AMI": VSMART_AMI }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)


#data = f'{{"token": "{TOKEN}"}}'
data_json = {"VBOND_INSTANCE_TYPE": VBOND_INSTANCE_TYPE }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)

#Write VMANAGE_USERNAME  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "VMANAGE_USERNAME"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"VMANAGE_USERNAME": VMANAGE_USERNAME }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)

#Write VMANAGE_PASS  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "VMANAGE_PASS"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"VMANAGE_PASS": VMANAGE_PASS }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)


#Write VMANAGE_ENCRYPTED_PASS  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "VMANAGE_ENCRYPTED_PASS"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"VMANAGE_ENCRYPTED_PASS": VMANAGE_ENCRYPTED_PASS }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)


#Write export ACL_RANGES_IPV4_BASE64  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "ACL_RANGES_IPV4_BASE64"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"ACL_RANGES_IPV4_BASE64": ACL_RANGES_IPV4_BASE64 }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)

#Write export ACL_RANGES_IPV6_BASE64  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "ACL_RANGES_IPV6_BASE64"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"ACL_RANGES_IPV6_BASE64": ACL_RANGES_IPV6_BASE64 }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)

#Write export SDWAN_CA_PASSPHRASE  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "SDWAN_CA_PASSPHRASE"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"SDWAN_CA_PASSPHRASE": SDWAN_CA_PASSPHRASE }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)

#Write export SDWAN_DATACENTER  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "SDWAN_DATACENTER"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"SDWAN_DATACENTER": SDWAN_DATACENTER }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)

#Write export NETWORK_CIDR  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "NETWORK_CIDR"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"NETWORK_CIDR": NETWORK_CIDR }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)

#Write export VMANAGE1_IP  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "VMANAGE1_IP"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"VMANAGE1_IP": VMANAGE1_IP }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)


#Write export VBOND1_IP  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "VBOND1_IP"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"VBOND1_IP": VBOND1_IP }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)

#Write export VSMART1_IP  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "VSMART1_IP"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = { "VBOND1_IP": VSMART1_IP }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)


#Write export VPN0_GATEWAY  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "VPN0_GATEWAY"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = { "VPN0_GATEWAY": VPN0_GATEWAY }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)

#Write export HQ_EDGE1_IP  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "HQ_EDGE1_IP"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = { "HQ_EDGE1_IP": HQ_EDGE1_IP }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)


#Write export IOSXE_SDWAN_IMAGE  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "IOSXE_SDWAN_IMAGE"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = { "IOSXE_SDWAN_IMAGE": IOSXE_SDWAN_IMAGE }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)

#Write export VMANAGE_ORG  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "VMANAGE_ORG"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = { "VMANAGE_ORG": VMANAGE_ORG }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)

#Write export VMANAGE_ORG  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "VMANAGE_ORG"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = { "VMANAGE_ORG": VMANAGE_ORG }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)



#Write export CLOUDINIT_TYPE  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "CLOUDINIT_TYPE"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = { "CLOUDINIT_TYPE": CLOUDINIT_TYPE }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)

=====
export PROJ_ROOT=$SCRIPT_DIR/..
export SSH_PUBKEY_BASE64="$(cat $HOME/.ssh/id_rsa.pub | base64)"
export SDWAN_CONTROL_INFRA="aws"
export AWS_PROFILE="default"
export AWS_ACCESS_KEY_ID=$(aws configure get $AWS_PROFILE.aws_access_key_id)
export AWS_SECRET_ACCESS_KEY=$(aws configure get $AWS_PROFILE.aws_secret_access_key)
export AWS_SESSION_TOKEN=$(aws configure get $AWS_PROFILE.aws_session_token)
export AWS_REGION="us-west-2"

export VMANAGE_AMI="ami-0f727aeff8bfca1be"
export VMANAGE_INSTANCE_TYPE="t2.xlarge"
export VBOND_AMI="ami-0669c73a744a9071a"
export VBOND_INSTANCE_TYPE="t2.medium"
export VSMART_AMI="ami-0b3dcbdd1621b4819"
export VSMART_INSTANCE_TYPE="t2.medium"

# Example to generate a random password
# TODO  save it somewhere?
export VMANAGE_USERNAME="admin"
export VMANAGE_PASS="$(openssl rand -base64 12)"
export VMANAGE_ENCRYPTED_PASS="$(echo "$VMANAGE_PASS" | openssl passwd -6 -stdin)"
export SDWAN_CA_PASSPHRASE="$(openssl rand -base64 15)"

# Distinguishing single and double quotes is very important for this to work
export ACL_RANGES_IPV4_BASE64=$(echo '"0.0.0.0/1", "128.0.0.0/1"' | base64)
export ACL_RANGES_IPV6_BASE64=$(echo '"::/0"' | base64)

# SDWAN_DATACENTER is the generic variable which is the region for AWS or the
# vSphere datacenter, depending on the infra
export SDWAN_DATACENTER=$AWS_REGION
# Terraform for AWS has some computation built-in, hence the below values
# TODO  document static addressing
export NETWORK_CIDR=10.128.0.0/22
export VMANAGE1_IP=10.128.1.11/24
export VBOND1_IP=10.128.1.12/24
export VSMART1_IP=10.128.1.13/24
export VPN0_GATEWAY=10.128.1.1

# This should be the VPC ID eventually
#export VPN0_PORTGROUP="cpn-rtp-colab4"
#export VPN512_PORTGROUP="cpn-rtp-colab4"
#export SERVICEVPN_PORTGROUP="cpn-rtp-colab4"

export HQ_EDGE1_IP=1.1.1.4/24
export SITE1_EDGE1_IP=1.1.1.5/24
export SITE2_EDGE1_IP=1.1.1.6/24

export IOSXE_SDWAN_IMAGE=iosxe-sdwan-16.12.5

export VIPTELA_VERSION=20.8.1

export VMANAGE_ORG=CIDR_SDWAN_WORKSHOPS

export CLOUDINIT_TYPE=v2