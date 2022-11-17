#!/usr/bin/env python
import json, re, sys, os, json, time, logging, requests, urllib3
from requests.structures import CaseInsensitiveDict
urllib3.disable_warnings()
import subprocess
from subprocess import call, check_output

VAULT_ADDR = os.getenv('VAULT_ADDRR')
VAULT_TOKEN = os.getenv('SSH_TOKEN') #This gets the vault token from the ephemeral build container

#MAKE SURE THE AWS IS UP TO VERSION 2 ON THE BUILD CONTAINER
#GET THE DEFAULT VPC ID
outfile_vars="vars"

lab_vars='lab_vars.py'
import lab_vars
from lab_vars import *

outfile_vars="vars"
sg_name=name

#Inject the vault var vals into the ephemeral oci build container

VAULT_ADDR = os.getenv('VAULT_ADDR')
VAULT_TOKEN = os.getenv('SSH_TOKEN')
#VAULT_TOKEN = os.getenv('VAULT_TOKEN')
url = "http://http://vault.cisco-sdwan-labs.com:8200/v1/concourse/sdwan/" + name + "/" + "key_name"
headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"
#data = f'{{"token": "{TOKEN}"}}'
data_json = {"key_name": name }
resp = requests.post(url, headers=headers, json=data_json)
print(resp.status_code)


#1 - Create a Key Pair & Write it to the vault
keypair_name=name
outfile_key_pair = 'keypair_name' + '.json'
create_keypair='aws ec2 create-key-pair --key-name' + " " +  "{}".format(name) + " " + '--region' + " " + "{}".format(region) + " " + '--availability-zone' + " " + "{}".format(az)
#Write Key to Vault


#2 - CREATE THE NEW VPC AND GET VPCID
outfile = 'aws-vpc.json'
#cmd_deploy='aws ec2 create-vpc --region' + " " + "{}".format(region) + " " + '--cidr-block 10.100.0.0/22 --tag-specifications' + " " + "'ResourceType=vpc,Tags=[{Key=Name,Value=trainee1}]'"
cmd_deploy='aws ec2 create-vpc --region' + " " + "{}".format(region) + " " + '--cidr-block 10.100.0.0/22 --tag-specifications' + " " + "'ResourceType=vpc,Tags=[{Key=Name,Value=" + "{}".format(name) + '}]'"" + "'"
output = check_output("{}".format(cmd_deploy), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile, 'w') as my_file:
    my_file.write(output)
with open(outfile) as access_json:
    read_content = json.load(access_json)
    question_access = read_content['Vpc']
    replies_access = question_access['VpcId']
    vpcid = replies_access
    print(vpcid)
    vpcid_var=('vpcid=' + "'" + "{}".format(vpcid) + "'")
    print(vpcid_var)

with open(outfile_vars, 'a+') as my_file:
    my_file.write(vpcid_var + "\n")


#create the mgmt subnt
outfile_subnet_mgmt = 'aws-subnet-mgmt.json'
cmd_subnet_mgmt='aws ec2 create-subnet --vpc-id' + " " + "{}".format(vpcid) + " " + '--region' + " " + "{}".format(region) + " " + '--availability-zone' + " " + "{}".format(az) + " " + '--cidr-block 10.100.0.0/24 --tag-specifications' + " " "'ResourceType=subnet,Tags=[{Key=Name,Value=SUBNET_mgmt}]'"
print(cmd_subnet_mgmt)
output = check_output("{}".format(cmd_subnet_mgmt), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_subnet_mgmt, 'w') as my_file:
    my_file.write(output)
with open (outfile_subnet_mgmt) as access_json:
    read_content = json.load(access_json)
    question_access = read_content['Subnet']
    replies_access = question_access['SubnetId']
subnetid_mgmt = replies_access
print(subnetid_mgmt)

subnetid_mgmt_var=('subnetid_mgmt=' + "'" + "{}".format(subnetid_mgmt) + "'")

with open(outfile_vars, 'a+') as my_file:
    my_file.write(subnetid_mgmt_var + "\n")


#4- CREATE THE public SUBNET
outfile_subnet_public = 'aws-subnet-public.json'
cmd_subnet_public='aws ec2 create-subnet --vpc-id' + " " + "{}".format(vpcid) + " " + '--region' + " " + "{}".format(region) + " " + '--availability-zone' + " " + "{}".format(az) + " " + '--cidr-block 10.100.1.0/24 --tag-specifications' + " " "'ResourceType=subnet,Tags=[{Key=Name,Value=SUBNET_public}]'"
print(cmd_subnet_public)
output = check_output("{}".format(cmd_subnet_public), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_subnet_public, 'w') as my_file:
    my_file.write(output)
with open (outfile_subnet_public) as access_json:
    read_content = json.load(access_json)
    question_access = read_content['Subnet']
    replies_access = question_access['SubnetId']
    subnetid_public = replies_access
    print(subnetid_public)
    subnetid_public_var=('subnetid_public=' + "'" + "{}".format(subnetid_public) + "'")

with open(outfile_vars, 'a+') as my_file:
    my_file.write(subnetid_public_var + "\n")



#5 - CREATE INTERNET GATEWAY
outfile_ig = 'aws-ig.json'
cmd_ig='aws ec2 create-internet-gateway --region' + " " + "{}".format(region) + " " + '--tag-specifications' + " " + "'ResourceType=internet-gateway,Tags=[{Key=Name,Value=IG}]'"
print(cmd_ig)
output = check_output("{}".format(cmd_ig), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_ig, 'w') as my_file:
    my_file.write(output)
with open (outfile_ig) as access_json:
    read_content = json.load(access_json)
    print(read_content)
    question_access = read_content['InternetGateway']
    print(question_access)
    replies_access = question_access['InternetGatewayId']
    print(replies_access)
igid = replies_access
print(igid)

igid_var=('igd=' + "'" + "{}".format(igid) + "'")

with open(outfile_vars, 'a+') as my_file:
    my_file.write(igid_var + "\n")

#6 - Attach Internet Gateway to the VPC
outfile_ig_attach_log = 'ig_attach_log.json'
cmd_ig_attach='aws ec2 attach-internet-gateway' + " " + '--region' + " " + "{}".format(region) + " " + '--internet-gateway-id' + " " + "{}".format(igid) + " " + '--vpc-id' + " " + "{}".format(vpcid)
print(cmd_ig_attach)
output = check_output("{}".format(cmd_ig_attach), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
#Do we need to add any var here to the vars.py??



# 7 - Get the route table id for the default route table for the new vpc
outfile_get_vpc_rt_id='get-vpc-rt-id.json'
get_vpc_rt_id='aws ec2 describe-route-tables' + " " + '--region' + " " + "{}".format(region) + " " + '--filters \"Name=vpc' + '-' + 'id,Values=' + "{}".format(vpcid) + '"' + " " + '--query "RouteTables[]"'
output = check_output("{}".format(get_vpc_rt_id), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_get_vpc_rt_id , 'w') as my_file:
    my_file.write(output)
with open (outfile_get_vpc_rt_id ) as access_json:
    read_content=json.load(access_json)
    question_access=read_content[0]
    replies_access=question_access['Associations']
    replies_data=replies_access[0]
    def_vpc_rt_id=replies_data['RouteTableId']
    print(def_vpc_rt_id)


def_vpc_rt_id_var=('def_vpc_rt_id=' + "'" + "{}".format(def_vpc_rt_id) + "'")
with open(outfile_vars, 'a+') as my_file:
    my_file.write(def_vpc_rt_id_var + "\n")

#Tag the default route table --resources --tags Key=Name,Value=DEFAULT_RT

#8 - aws ec2 create-tags to identify the vpc default route table
tag_def_vpc_rt='aws ec2 create-tags --resources --region' + " " + "{}".format(region) + " " + " " + "{}".format(def_vpc_rt_id) + " " + '--tags Key=Name,Value=DEFAULT_RT_' + "{}".format(name)
output = check_output("{}".format(tag_def_vpc_rt), shell=True).decode().strip()
print("Output: \n{}\n".format(output))

#9 - Add a new route to the default vpc route table requires the default vpc route table id and associated and the default gatewayid
outfile_ass_rt = 'ass_rt.json'
ass_rt_default_rt='aws ec2 create-route' + " " + '--region' + " " + "{}".format(region) + " " + '--route-table-id' + " " + "{}".format(def_vpc_rt_id) + " " + '--destination-cidr-block 0.0.0.0/0 --gateway-id' + " " + igid
output = check_output("{}".format(ass_rt_default_rt), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_ass_rt, 'w') as my_file:
    my_file.write(output)

#10 - Create mgmt Route Table
outfile_rt_mgmt = 'aws-rt-mgmt.json'
cmd_rt_mgmt='aws ec2 create-route-table --vpc-id' + " " + "{}".format(vpcid) + " " + '--region' + " " + "{}".format(region) + " " + '--tag-specifications' + " " + "'ResourceType=route-table,Tags=[{Key=Name,Value=mgmt_RT}]'"
print(cmd_rt_mgmt)
output = check_output("{}".format(cmd_rt_mgmt), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_rt_mgmt, 'w') as my_file:
    my_file.write(output)
with open (outfile_rt_mgmt) as access_json:
    read_content = json.load(access_json)
    question_access = read_content['RouteTable']
    replies_access = question_access['RouteTableId']
rt_mgmt_id = replies_access
print(rt_mgmt_id)

rt_mgmt_id_var=('rt_mgmt_id=' + "'" + "{}".format(rt_mgmt_id) + "'")
with open(outfile_vars, 'a+') as my_file:
    my_file.write(rt_mgmt_id_var + "\n")

'''

#11 - Create public Route Table
outfile_public_rt = 'aws-rt-public.json'
cmd_public_rt='aws ec2 create-route-table --vpc-id' + " " + "{}".format(vpcid) + " " + '--region' + " " + "{}".format(region) + " " + '--tag-specifications' + " " + "'ResourceType=route-table,Tags=[{Key=Name,Value=public_RT}]'"
print(cmd_public_rt)
output = check_output("{}".format(cmd_public_rt), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_public_rt, 'w') as my_file:
    my_file.write(output)
with open (outfile_public_rt) as access_json:
    read_content = json.load(access_json)
    question_access = read_content['RouteTable']
    replies_access = question_access['RouteTableId']
rt_public_id = replies_access
print(rt_public_id)

rt_public_id_var=('rt_rt_id=' + "'" + "{}".format(rt_public_id) + "'")
with open(outfile_vars, 'a+') as my_file:
    my_file.write(rt_public_id_var + "\n")
'''



#12 - ASSOCIATE THE mgmt ROUTE TABLE WITH THE mgmt SUBNET(Check with Team if there should be just one route table and this would be renamed just "main route table"
outfile_ass_mgmt_sub = 'ass_rt_mgmt_sub.json'
ass_rt_mgmt_sub='aws ec2 associate-route-table --region' + " " + "{}".format(region) + " " + '--route-table-id' + " " + "{}".format(rt_mgmt_id) + " " + '--subnet-id' + " " + "{}".format(subnetid_mgmt)
print(ass_rt_mgmt_sub)
output = check_output("{}".format(ass_rt_mgmt_sub), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_ass_mgmt_sub, 'w') as my_file:
    my_file.write(output)

#ASSOCIATE ALL THE SUBNETS WITH THE mgmt ROUTE TABLE

# - ASSOCIATE THE mgmt ROUTE TABLE WITH THE public SUBNET
outfile_ass_public_sub = 'ass_rt_mgmt_sub.json'
ass_rt_public_sub='aws ec2 associate-route-table --region' + " " + "{}".format(region) + " " + '--route-table-id' + " " + "{}".format(rt_mgmt_id) + " " + '--subnet-id' + " " + "{}".format(subnetid_public)
print(ass_rt_public_sub)
output = check_output("{}".format(ass_rt_public_sub), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_ass_public_sub, 'w') as my_file:
    my_file.write(output)


'''
#ASSOCIATE THE public ROUTE TABLE WITH THE public SUBNET
outfile_ass_public_sub = 'ass_public_sub.json'
ass_rt_public_sub='aws ec2 associate-route-table' + " " + '--region' + " " + "{}".format(region) + " " + '--route-table-id' + " " + "{}".format(rt_public_id) + " " +  '--subnet-id' + " " + "{}".format(subnetid_public)
print(ass_rt_public_sub)
output = check_output("{}".format(ass_rt_public_sub), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_ass_public_sub, 'w') as my_file:
    my_file.write(output)
'''



#Add a route to this public route table that is to the internet gateway
#Destination 0.0.0.0/0 Target: The igw for the VPC
#aws ec2 create-route --route-table-id rtb-22574640 --destination-cidr-block 0.0.0.0/0 --gateway-id igw-c0a643a9
#Need the RT ID and the GatewayID
#aws ec2 create-route --route-table-id rt_rt_id --destination-cidr-block 0.0.0.0/0 --gateway-id igid
#aws ec2 create-route --route-table-id rtb-037f6e0a9f82e1d9e --destination-cidr-block 0.0.0.0/0 --gateway-id igw-0cd42c1b9fdd2bc6d
print("Creating Router Route Table Route and Associating with Gateway")
cmd_create_router_rt_route='aws ec2 create-route --route-table-id' + " " + "{}".format(rt_mgmt_id) + " " + '--destination-cidr-block 0.0.0.0/0' + " " + '--gateway-id' + " " + igid
print(cmd_create_router_rt_route)
output = check_output("{}".format(cmd_create_router_rt_route), shell=True).decode().strip()
print("Output: \n{}\n".format(output))


#13 - Create a Security Group
out_file_sg_SDWAN='outfile-sg-public.json'
cmd_security_group='aws ec2 create-security-group --group-name --region' + " " + "{}".format(region) + " " + " " + "{}".format(sg_name) + " " + '--description' + " " + "{}".format(sg_name) + " " + '--vpc-id' + " " + "{}".format(vpcid)
output = check_output("{}".format(cmd_security_group), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(out_file_sg_SDWAN, 'w') as my_file:
    my_file.write(output)
with open (out_file_sg_SDWAN) as access_json:
    read_content = json.load(access_json)
    question_access = read_content['GroupId']
    SDWAN_sg_id=question_access
    SDWAN_sg_id_var=('SDWAN_sg_id=' + "'" + "{}".format(SDWAN_sg_id) + "'")
    print(SDWAN_sg_id_var)
with open(outfile_vars, 'a+') as my_file:
    my_file.write(SDWAN_sg_id_var + "\n")

#Create inbound rule on the security group to allow SSH
#aws ec2 authorize-security-group-ingress --group-id sg-1234567890abcdef0 --protocol tcp --port 22 --cidr 0.0.0.0/0
auth_inbound_ssh='aws ec2 authorize-security-group-ingress --region' + " " + "{}".format(region) + " " + '--group-id' + " " "{}".format(SDWAN_sg_id) + " " + '--protocol tcp --port 22 --cidr 0.0.0.0/0'
output = check_output("{}".format(auth_inbound_ssh), shell=True).decode().strip()
print("Output: \n{}\n".format(output))

#Create inbound rule on the security group to allow 8443
#aws ec2 authorize-security-group-ingress --group-id sg-1234567890abcdef0 --protocol tcp --port 22 --cidr 0.0.0.0/0
auth_inbound_ssh='aws ec2 authorize-security-group-ingress --region' + " " + "{}".format(region) + " " + '--group-id' + " " "{}".format(SDWAN_sg_id) + " " + '--protocol tcp --port 8443 --cidr 0.0.0.0/0'
output = check_output("{}".format(auth_inbound_ssh), shell=True).decode().strip()
print("Output: \n{}\n".format(output))

#Create inbound rule on the security group to allow 830
#aws ec2 authorize-security-group-ingress --group-id sg-1234567890abcdef0 --protocol tcp --port 22 --cidr 0.0.0.0/0
auth_inbound_ssh='aws ec2 authorize-security-group-ingress --region' + " " + "{}".format(region) + " " + '--group-id' + " " "{}".format(SDWAN_sg_id) + " " + '--protocol tcp --port 830 --cidr 0.0.0.0/0'
output = check_output("{}".format(auth_inbound_ssh), shell=True).decode().strip()
print("Output: \n{}\n".format(output))



#Create inbound rule on the security group to allow 830
#aws ec2 authorize-security-group-ingress --group-id sg-1234567890abcdef0 --protocol tcp --port 22 --cidr 0.0.0.0/0
auth_inbound_ssh='aws ec2 authorize-security-group-ingress --region' + " " + "{}".format(region) + " " + '--group-id' + " " "{}".format(SDWAN_sg_id) + " " + '--ip-permissions IpProtocol=tcp,FromPort=23456,ToPort=24156,IpRanges=' + "'[{CidrIp=0.0.0.0/0}]'''"
print(auth_inbound_ssh)
output = check_output("{}".format(auth_inbound_ssh), shell=True).decode().strip()
print("Output: \n{}\n".format(output))

#aws ec2 authorize-security-group-ingress --group-id sg-1234567890abcdef0 --protocol tcp --port 22 --cidr 0.0.0.0/0
auth_inbound_ssh='aws ec2 authorize-security-group-ingress --region' + " " + "{}".format(region) + " " + '--group-id' + " " "{}".format(SDWAN_sg_id) + " " + '--ip-permissions IpProtocol=udp,FromPort=12346,ToPort=13046,IpRanges=' + "'[{CidrIp=0.0.0.0/0}]'''"
output = check_output("{}".format(auth_inbound_ssh), shell=True).decode().strip()
print("Output: \n{}\n".format(output))


#VAULT SECTION

#Write Key to vault

#Write vpcid  to the vault
url = "http://http://vault.cisco-sdwan-labs.com:8200/v1/concourse/sdwan/" + name + "/" + "vpcid"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"vpcid": vpcid }

resp = requests.post(url, headers=headers, json=data_json)
print(resp.status_code)


#3 Write the subnetid_public to the vault

url = "http://http://vault.cisco-sdwan-labs.com:8200/v1/concourse/sdwan/" + name + "/" + "subnetid_public"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"subnetid_public": subnetid_public }

resp = requests.post(url, headers=headers, json=data_json)
print(resp.status_code)

#4 Write the subnetid_mgmt to the vault

url = "http://http://vault.cisco-sdwan-labs.com:8200/v1/concourse/sdwan/" + name + "/" + "subnetid_mgmt"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"subnetid_mgmt": subnetid_mgmt }

resp = requests.post(url, headers=headers, json=data_json)
print(resp.status_code)

#5 Write the igid to the vault

url = "http://http://vault.cisco-sdwan-labs.com:8200/v1/concourse/sdwan/" + name + "/" + "igid"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"igid": igid }

resp = requests.post(url, headers=headers, json=data_json)
print(resp.status_code)

#10 - Write rt_mgmt_id to the vault

url = "http://http://vault.cisco-sdwan-labs.com:8200/v1/concourse/sdwan/" + name + "/" + "rt_mgmt_id"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"rt_mgmt_id": rt_mgmt_id }

resp = requests.post(url, headers=headers, json=data_json)
print(resp.status_code)

#11 - Write rt_mgmt_id to the vault
url = "http://http://vault.cisco-sdwan-labs.com:8200/v1/concourse/sdwan/" + name + "/" + "rt_mgmt_id"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"rt_mgmt_id": rt_mgmt_id }

resp = requests.post(url, headers=headers, json=data_json)
print(resp.status_code)

#13 - Write the SDWAN_sg_id to the vault

url = "http://http://vault.cisco-sdwan-labs.com:8200/v1/concourse/sdwan/" + name + "/" + "SDWAN_sg_id"
print(url)

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"SDWAN_sg_id": SDWAN_sg_id }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)
print(name)

#Add in Here Allocate EIPs and write to vault
#aws ec2 allocate-address