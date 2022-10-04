#!/usr/bin/env python
SDWAN_CONTROL_INFRA="aws"
AWS_PROFILE="default"
REGION=$REGION

#amis are for us-west-2
VMANAGE_AMI="ami-0f727aeff8bfca1be"
VMANAGE_INSTANCE_TYPE="t2.xlarge"
VBOND_AMI="ami-0669c73a744a9071a"
VBOND_INSTANCE_TYPE="t2.medium"
VSMART_AMI="ami-0b3dcbdd1621b4819"
VSMART_INSTANCE_TYPE="t2.medium"

# Example to generate a random password
# TODO  save it somewhere?
VMANAGE_USERNAME="admin"
VMANAGE_PASS="$(openssl rand -base64 12)"
VMANAGE_ENCRYPTED_PASS="$(echo "$VMANAGE_PASS" | openssl passwd -6 -stdin)"
SDWAN_CA_PASSPHRASE="$(openssl rand -base64 15)"

# Distinguishing single and double quotes is very important for this to work
ACL_RANGES_IPV4_BASE64='"0.0.0.0/1", "128.0.0.0/1"'
ACL_RANGES_IPV6_BASE64=echo '"::/0"'

# SDWAN_DATACENTER is the generic variable which is the region for AWS or the
# vSphere datacenter, depending on the infra
SDWAN_DATACENTER=$AWS_REGION
# Terraform for AWS has some computation built-in, hence the below values
# TODO  document static addressing
NETWORK_CIDR=10.128.0.0/22
VMANAGE1_IP=10.128.1.11/24
VBOND1_IP=10.128.1.12/24
VSMART1_IP=10.128.1.13/24
VPN0_GATEWAY=10.128.1.1

# This should be the VPC ID eventually
#VPN0_PORTGROUP="cpn-rtp-colab4"
#VPN512_PORTGROUP="cpn-rtp-colab4"
#SERVICEVPN_PORTGROUP="cpn-rtp-colab4"

HQ_EDGE1_IP="1.1.1.4/24"
SITE1_EDGE1_IP="1.1.1.5/24"
SITE2_EDGE1_IP="1.1.1.6/24"

IOSXE_SDWAN_IMAGE="iosxe-sdwan-16.12.5"

VIPTELA_VERSION="20.8.1"

VMANAGE_ORG="CIDR_SDWAN_WORKSHOPS"

CLOUDINIT_TYPE="v2"
