#!/usr/bin/env bash
# Exporting with variable names that match the Terraform convention makes it possible to use the same
# environment variables with Packer.
#The HX1 cluster is more reliable, but requires admin access, so be very careful!
#TODO, at some point, in a not too distant future, these variable names will need to be normalised across domains

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";

export PROJ_ROOT=$SCRIPT_DIR/..
export SDWAN_CONTROL_INFRA="vmware"

#export TF_VAR_vsphere_username="nsowatsk@ciscops.net"
export TF_VAR_vsphere_user="nsowatsk@ciscops.net"

export TF_VAR_vsphere_password="EZ3rZ2SMgvRqb^rI}7p["

export TF_VAR_vsphere_server="cpn-rtp-vc1.ciscops.net"
#export TF_VAR_vsphere_cluster="cpn-rtp-hx1"
export TF_VAR_cluster="cpn-rtp-hx1"

#export TF_VAR_vsphere_datacenter="RTP"
export TF_VAR_datacenter="RTP"

export TF_VAR_vsphere_content_library_datastore="cpn-rtp-hx1-datastore1"
export TF_VAR_vsphere_content_library="SD-WAN"
export TF_VAR_vsphere_network="cpn-rtp-colab4"
export TF_VAR_host_system_id="192.133.177.42"
#export TF_VAR_host_system_id="192.133.177.64"
#export TF_VAR_vsphere_datastore="cpn-rtp-hx1-datastore1"
export TF_VAR_datastore="cpn-rtp-hx1-datastore1"

#export TF_VAR_vsphere_sdwan_folder="[cpn-rtp-hx1-datastore1]/sdwan"
#export TF_VAR_vsphere_sdwan_folder="sdwan"
export TF_VAR_folder="sdwan"

#export TF_VAR_vsphere_iso_datastore="cpn-rtp-hx1-datastore1"
export TF_VAR_iso_datastore="cpn-rtp-hx1-datastore1"

#export TF_VAR_vsphere_sdwan_iso_path="cloud-init"
export TF_VAR_iso_path=cloud-init

#export TF_VAR_vsphere_resource_pool=""
export TF_VAR_resource_pool=

export TF_VAR_govc_cmd="/opt/homebrew/bin/govc"
export GOVC_USERNAME=$TF_VAR_vsphere_username
export GOVC_PASSWORD=$TF_VAR_vsphere_password
export GOVC_URL=$TF_VAR_vsphere_server
export GOVC_INSECURE=True

export VMANAGE1_IP=192.133.184.73/22
export VBOND1_IP=192.133.184.76/22
export VSMART1_IP=192.133.184.75/22
export VPN0_GATEWAY=192.133.184.1

export VPN0_PORTGROUP="cpn-rtp-colab4"
export VPN512_PORTGROUP="cpn-rtp-colab4"
export SERVICEVPN_PORTGROUP="cpn-rtp-colab4"

export HQ_EDGE1_IP=1.1.1.4/24
export SITE1_EDGE1_IP=1.1.1.5/24
export SITE2_EDGE1_IP=1.1.1.6/24

export IOSXE_SDWAN_IMAGE=iosxe-sdwan-16.12.5

export VIPTELA_VERSION=20.8.1

export VMANAGE_ORG=CIDR_SDWAN_WORKSHOPS

export CLOUDINIT_TYPE=v2