#!/usr/bin/env python
import json, re, sys, os, json, subprocess, time
from subprocess import call, check_output

outfile_vars="vars"
lab_vars='lab_vars.py'
from lab_vars import *

sg_name=name
keypair_name=name

print('Printing out the Name of the Region')
print(region)

#Create the vmanage router subnet tools instance
vmanage_ami_id=vmanage_ami_id
instance_type='t2.medium'

outfile_get_vpcid='outfile_get_vpcid.json'
get_vpcid='aws ec2 describe-vpcs --region' + " " + "{}".format(region) + " " + '--filters Name=tag:Name,Values=' + "{}".format(name)
output = check_output("{}".format(get_vpcid), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_get_vpcid, 'w') as my_file:
    my_file.write(output)
with open (outfile_get_vpcid) as access_json:
    read_content = json.load(access_json)
    question_access = read_content['Vpcs']
    question_data=question_access[0]
    replies_access=question_data['VpcId']
    vpcid=replies_access
    print(vpcid)
    vpcid_var=('vpcid=' + "'" + "{}".format(vpcid) + "'")

with open(outfile_vars, 'w') as my_file:
    my_file.write(vpcid_var + "\n")



#get the router security group id
#aws ec2 describe-security-groups --filters "Name=vpc-id,Values=vpc-01bdad153448ce387" --filters "Name=group-name,Values=sg01
#get_sgid='aws ec2 describe-security-groups --region' + " " + "{}".format(region) + " " + '--filters "Name=group-name,Values=' + "{}".format(sg_name) + '"' + " " + '"Name=availability-zone,Values=' + "{}".format(az) + '"'
outfile_get_sgid='outfile_sgid.json'
get_sgid='aws ec2 describe-security-groups --region' + " " + "{}".format(region) + " " + '--filters "Name=group-name,Values=' + "{}".format(sg_name) + '"'
output = check_output("{}".format(get_sgid), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_get_sgid, 'w') as my_file:
    my_file.write(output)
with open (outfile_get_sgid) as access_json:
    read_content = json.load(access_json)
    question_access = read_content['SecurityGroups']
    question_replies=question_access[0]
    question_data=question_replies['GroupId']
    sgid=question_data
    print(sgid)
    sgid_var=('sgid=' + "'" + "{}".format(sgid) + "'")
with open(outfile_vars, 'a+') as my_file:
    my_file.write(sgid_var + "\n")



#Get the router subnetid
outfile_get_subnetid_mgmt='subnet_id_mgmt.json'
get_subnetid_mgmt='aws ec2 describe-subnets --region' + " " + "{}".format(region) + " " '--filters' + " " + '"Name=availability-zone,Values=' + "{}".format(az)  + '"' + " " + '"Name=tag:Name,Values=SUBNET_MGMT"'
output = check_output("{}".format(get_subnetid_mgmt), shell=True).decode().strip()
print("Output: \n{}\n".format(output))

with open(outfile_get_subnetid_mgmt, 'w') as my_file:
    my_file.write(output)
with open(outfile_get_subnetid_mgmt) as access_json:
    read_content = json.load(access_json)
    print(read_content)
    question_access = read_content['Subnets']
    print(question_access)
    replies_access = question_access[0]
    print(replies_access)
    replies_data=replies_access['SubnetId']
    subnetid_mgmt=replies_data
    print(subnetid_mgmt)
    subnetid_mgmt_var=('subnetid_mgmt=' + "'" + "{}".format(subnetid_mgmt) + "'")

with open(outfile_vars, 'a') as my_file:
    my_file.write(subnetid_mgmt_var + "\n")

#get the subnetid_lan
outfile_get_subnetid_tunnel='outfile_subnetid_tunnel.json'
get_subnetid_tunnel='aws ec2 describe-subnets --region' + " " + "{}".format(region) + " " '--filters' + " " + '"Name=availability-zone,Values=' + "{}".format(az) + '"' + " " + '"Name=tag:Name,Values=SUBNET_TUNNEL' + '"'
output = check_output("{}".format(get_subnetid_tunnel), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_get_subnetid_tunnel, 'w') as my_file:
    my_file.write(output)
with open(outfile_get_subnetid_tunnel) as access_json:
    read_content = json.load(access_json)
    print(read_content)
    question_access = read_content['Subnets']
    print(question_access)
    replies_access = question_access[0]
    replies_data=replies_access['SubnetId']
    subnetid_tunnel=replies_data
    print(subnetid_tunnel)
    subnetid_tunnel_var=('subnetid_tunnel=' + "'" + "{}".format(subnetid_tunnel) + "'")

with open(outfile_vars, 'a') as my_file:
    my_file.write(subnetid_tunnel_var + "\n")

outfile_deploy_vmanage_router='deploy-vmanage-router.json'
#aws ec2 run-instances --image-id ami-067c66abd840abc24 --instance-type t2.medium --subnet-id subnet-008617eb0c9782f55 --security-group-ids sg-0b0384b66d7d692f9 --associate-public-ip-address --key-name blitz-user-1
cmd_deploy_vmanage_router='aws ec2 run-instances --region' + " " + "{}".format(region) + " " + '--image-id' + " " + "{}".format(vmanage_ami_id) + " " + '--instance-type' + " " + "{}".format(instance_type) + " " + '--subnet-id' + " " + "{}".format(subnetid_mgmt) + " " + '--security-group-ids' + " " + "{}".format(sgid) + " " + '--associate-public-ip-address' + " " + '--key-name' + " " + "{}".format(keypair_name) + " " + '--placement AvailabilityZone=' + "{}".format(az)
print(cmd_deploy_vmanage_router)

output = check_output("{}".format(cmd_deploy_vmanage_router), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_deploy_vmanage_router, 'w') as my_file:
    my_file.write(output)
#Get the instance ID and write it to the vars file
with open (outfile_deploy_vmanage_router) as access_json:
    read_content = json.load(access_json)
    question_access = read_content['Instances']
    replies_access = question_access[0]
    replies_data=replies_access['InstanceId']
    print(replies_data)
    vmanage_router_instance_id=replies_data

#Wait to check the instance is initialized
#Check that the instance is initialized
cmd_check_instance='aws ec2 wait instance-status-ok --instance-ids' + " " + vmanage_router_instance_id + " " + '--region' + " " + "{}".format(region)
output = check_output("{}".format(cmd_check_instance), shell=True).decode().strip()
print("Output: \n{}\n".format(output))


#tag the instance
vmanage_router_tag='aws ec2 create-tags --region' + " " + "{}".format(region) + " " + '--resources' + " " +  "{}".format(vmanage_router_instance_id) + " " + '--tags' + " " + "'" + 'Key="Name",Value=vmanage_router' + "'"
output = check_output("{}".format(vmanage_router_tag), shell=True).decode().strip()
print("Output: \n{}\n".format(output))

#Get the external public address assigned to the router ec2 instance and write it to the var file or vault
outfile_router_pub_ip='router_pub_ip.json'
cmd_get_router_pub_ip='aws ec2 describe-instances --region' + " " + "{}".format(region) + " " '--instance-id' + " " + "{}".format(vmanage_router_instance_id) + " " + '--query "Reservations[*].Instances[*].PublicIpAddress"'
output = check_output("{}".format(cmd_get_router_pub_ip), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_router_pub_ip, 'w') as my_file:
    my_file.write(output)

outfile_router_pub_ip='router_pub_ip.json'
with open(outfile_router_pub_ip) as access_json:
    read_content = json.load(access_json)
    question_access = read_content[0]
    print(read_content)
    question_data=question_access[0]
    router_pub_ip=question_data
    print('The External IP Address is:')
    print(router_pub_ip)


#ssh to the instance using the key and do an apt-get update && apt-get upgrade
#install vault client