#!/usr/bin/env python
#This Script creates the vmanage from AMI and the key - split out the key
import json, re, sys, os, json, subprocess, time, sys
from subprocess import call, check_output

outfile_vars="vars"
lab_vars='lab_vars.py'
import lab_vars
from lab_vars import *

keypair_name=name
sg_name='SDWAN'
ami_id=vmanage_ami_id

path = os.getcwd()
print(path)
os.listdir(path)

#Tag the Instance with the name vmanage
#aws ec2 create-key-pair --key-name MyKeyPair moved to aws prep

instance_type='t2.micro'
outfile_deploy_vmanage='deploy-vmanage.json'
outfile_get_vpcid='outfile_get_vpcid.json'


#Will need to add code to generate the EIPs or look for some that are availabae
inst_name="vmanage-1"
eip_mgmt='eipalloc-06d883e17a87e2338'
eip_public='eipalloc-0c78cb1a321d6de4f'

#Get VPCID
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



#get the mgmt security group id
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
    print("Printing out sgid.....")
    print(sgid)
    sgid_var=('sgid=' + "'" + "{}".format(sgid) + "'")
with open(outfile_vars, 'a+') as my_file:
    my_file.write(sgid_var + "\n")



#Get the mgmt subnetid
outfile_get_subnetid_mgmt='subnet_id_mgmt.json'
get_subnetid_mgmt='aws ec2 describe-subnets --region' + " " + "{}".format(region) + " " '--filters' + " " + '"Name=availability-zone,Values=' + "{}".format(az)  + '"' + " " + '"Name=tag:Name,Values=SUBNET_mgmt"'
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
    print("Printing out the subnetid_mgmt.....")
    print(subnetid_mgmt)
    subnetid_mgmt_var=('subnetid_mgmt=' + "'" + "{}".format(subnetid_mgmt) + "'")

with open(outfile_vars, 'a') as my_file:
    my_file.write(subnetid_mgmt_var + "\n")


#get the subnetid_public
outfile_get_subnetid_public='outfile_subnetid_public.json'
get_subnetid_public='aws ec2 describe-subnets --region' + " " + "{}".format(region) + " " '--filters' + " " + '"Name=availability-zone,Values=' + "{}".format(az) + '"' + " " + '"Name=tag:Name,Values=SUBNET_public' + '"'
print(get_subnetid_public)
output = check_output("{}".format(get_subnetid_public), shell=True).decode().strip()
print("Output: \n{}\n".format(output))

with open(outfile_get_subnetid_public, 'w') as my_file:
   my_file.write(output)
with open(outfile_get_subnetid_public) as access_json:
   read_content = json.load(access_json)
   print(read_content)
   question_access = read_content['Subnets']
   print(question_access)
   replies_access = question_access[0]
   replies_data=replies_access['SubnetId']
   subnetid_public=replies_data
   ("Printing subnetid public.....")
   print(subnetid_public)
   subnetid_public_var=('subnetid_public=' + "'" + "{}".format(subnetid_public) + "'")

with open(outfile_vars, 'a') as my_file:
   my_file.write(subnetid_public_var + "\n")



#get the subnetid_CLUSTER
outfile_get_subnetid_CLUSTER='outfile_subnetid_CLUSTER.json'
get_subnetid_CLUSTER='aws ec2 describe-subnets --region' + " " + "{}".format(region) + " " '--filters' + " " + '"Name=availability-zone,Values=' + "{}".format(az) + '"' + " " + '"Name=tag:Name,Values=SUBNET_CLUSTER' + '"'
output = check_output("{}".format(get_subnetid_CLUSTER), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_get_subnetid_CLUSTER, 'w') as my_file:
   my_file.write(output)
with open(outfile_get_subnetid_CLUSTER) as access_json:
   read_content = json.load(access_json)
   print(read_content)
   question_access = read_content['Subnets']
   print(question_access)
   replies_access = question_access[0]
   replies_data=replies_access['SubnetId']
   subnetid_CLUSTER=replies_data
   ("Printing subnetid_cluster.....")
   print(subnetid_CLUSTER)
   subnetid_CLUSTER_var=('subnetid_public=' + "'" + "{}".format(subnetid_CLUSTER) + "'")

with open(outfile_vars, 'a') as my_file:
   my_file.write(subnetid_CLUSTER_var + "\n")


#Create the Instance
#aws ec2 run-instances --image-id ami-067c66abd840abc24 --instance-type t2.medium --subnet-id subnet-008617eb0c9782f55 --security-group-ids sg-0b0384b66d7d692f9 --PrivateIpAddress "10.10.10.100" --associate-public-ip-address --key-name blitz-user-1
cmd_deploy_vmanage='aws ec2 run-instances --region' + " " + "{}".format(region) + " " + '--image-id' + " " + "{}".format(ami_id) + " " + '--instance-type' + " " + "{}".format(instance_type) + " " + '--subnet-id' + " " + "{}".format(subnetid_mgmt) +  " " + '--security-group-ids' + " " + "{}".format(sgid) + " " + '--key-name' + " " + "{}".format(keypair_name) + " " + '--placement AvailabilityZone=' + "{}".format(az)
#print(cmd_deploy_vmanage)
output = check_output("{}".format(cmd_deploy_vmanage), shell=True).decode().strip()
print("Output: \n{}\n".format(output))

with open(outfile_deploy_vmanage, 'w') as my_file:
   my_file.write(output)

with open (outfile_deploy_vmanage) as access_json:
   read_content = json.load(access_json)
   question_access_vmanage = read_content['Instances']
   replies_access_vmanage = question_access_vmanage[0]
   replies_data_vmanage=replies_access_vmanage['InstanceId']
   print(replies_data_vmanage)
   vmanage_instance_id=replies_data_vmanage #add this to the vars file
   print(vmanage_instance_id)
   vmanage_instance_id_var=('vmanage_instance_id=' + "'" + "{}".format(vmanage_instance_id) + "'")
   vmanage_int_ip_addr=replies_access_vmanage['PrivateIpAddress']
   print(vmanage_int_ip_addr)

with open(outfile_vars, 'a+') as my_file:
   my_file.write(vmanage_instance_id_var + "\n")



#Capture the instance_id and write to the var file or vault
vmanage_instance_id_var=('vmanage_instance_id=' + "'" + "{}".format(vmanage_instance_id) + "'")
print(vmanage_instance_id_var)
with open(outfile_vars, 'a') as my_file:
   my_file.write(vmanage_instance_id_var + "\n")


#tag the vmanage instance
#tag_vmanage='aws ec2 create-tags --resources' + " " + "{}".format(vmanage_instance_id) '--tags "'Key="[Name]",Value=vmanage'"
vmanage_tag_inst='aws ec2 create-tags --region' + " " + "{}".format(region) + " " + '--resources' + " " +  "{}".format(vmanage_instance_id) + " " + '--tags' + " " + "'" + 'Key="Name",Value=vmanage-1.0' + "'"
output = check_output("{}".format(vmanage_tag_inst), shell=True).decode().strip()
print("Output: \n{}\n".format(output))


#Capture the network interface id from the instance_id
# aws ec2 describe-instances --instance-id i-0253ef13177c9cc75 --query 'Reservations[].Instances[].NetworkInterfaces[*].NetworkInterfaceId'
cmd_vmanage_mgmt_eni_id='aws ec2 describe-instances --instance-id' + " " + vmanage_instance_id + " " + '--query' + " " + 'Reservations[].Instances[].NetworkInterfaces[*].NetworkInterfaceId'
print(cmd_vmanage_mgmt_eni_id)
output = check_output("{}".format(cmd_vmanage_mgmt_eni_id), shell=True).decode().strip()
print("Output: \n{}\n".format(output))

outfile_get_mgmt_eni_id='outfile_get_mgmt_eni_id.json'
with open(outfile_get_mgmt_eni_id, 'w') as my_file:
   my_file.write(output)
with open (outfile_get_mgmt_eni_id) as access_json:
   read_content = json.load(access_json)
   print(read_content)
   question_access = read_content[0]
   print(question_access)
   mgmt_eni_id=question_access[0]
   print(mgmt_eni_id)



#tag the vmanage_mgmt_eni_id
#write the eip to the vault

#Pole until the instance is created....
##!!HERE WE NEED TO POLL AND WAIT UNTIL THE INSTANCE IS IN AN INITIALIZED STATE -
#aws ec2 wait instance-status-ok --instance-ids vmanage_instance_id
cmd_check_instance='aws ec2 wait instance-running --instance-ids' + " " + vmanage_instance_id + " " + '--region' + " " + "{}".format(region)
output = check_output("{}".format(cmd_check_instance), shell=True).decode().strip()
print("Output: \n{}\n".format(output))

'''
#Get the external public address assigned to the vmanage and write it to the var file or vault
outfile_vmanage_pub_ip='vmanage_pub_ip.json'
cmd_get_vmanage_pub_ip='aws ec2 describe-instances --region' + " " + "{}".format(region) + " " '--instance-id' + " " + "{}".format(vmanage_instance_id) + " " + '--query "Reservations[*].Instances[*].publicIpAddress"'
output = check_output("{}".format(cmd_get_vmanage_pub_ip), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_vmanage_pub_ip, 'w') as my_file:
   my_file.write(output)

outfile_vmanage_pub_ip='vmanage_pub_ip.json'
with open(outfile_vmanage_pub_ip) as access_json:
   read_content = json.load(access_json)
   question_access = read_content[0]
   print(read_content)
   question_data=question_access[0]
   vmanage_pub_ip=question_data
   print(vmanage_pub_ip)


#Capture the External IP address and write it to the var file or vault
vmanage_pub_ip_var=('vmanage_pub_ip=' + "'" + "{}".format(vmanage_pub_ip) + "'")
print(vmanage_pub_ip_var)
with open(outfile_vars, 'a') as my_file:
   my_file.write(vmanage_pub_ip_var + "\n")

'''

#associate an eip with the default nic
cmd_associate_eip_mgmt='aws ec2 associate-address --allocation-id' + " " +  eip_mgmt + " " + '--network-interface-id' + " " + mgmt_eni_id
print(cmd_associate_eip_mgmt)
output = check_output("{}".format(cmd_associate_eip_mgmt), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
print("Associating eip with the mgmt nic")

#Create a Secondary NIC and assign to the public subnet
#cmd_add_nic_mgmt='aws ec2 create-network-interface --subnet-id' + " " + "{}".format(subnetid_public) + " " + '--description "vmanage_nic"' + " " + '--groups' + " " + "{}".format(mgmt_sg_id) + " " + '--private-ip-address 10.10.20.100'
outfile_add_vmanage_nic='add-vmanage-nic.json'
cmd_add_vmanage_nic='aws ec2 create-network-interface --region' + " " "{}".format(region) + " " + '--subnet-id' + " " + "{}".format(subnetid_public) + " " + '--description "vmanage_nic_public_sub"' + " " + '--groups' + " " + "{}".format(sgid) + " " + '--tag-specifications' + " " + "'ResourceType=network-interface,Tags=[{Key=Name,Value=" + "{}".format(name) + '}]'"" + "'"
output = check_output("{}".format(cmd_add_vmanage_nic), shell=True).decode().strip()
("Creating Secondary NIC on public Subne....t")
print("Output: \n{}\n".format(output))
with open(outfile_add_vmanage_nic, 'w') as my_file:
   my_file.write(output)

#Capture the secondary public eni_id out of the json output

with open(outfile_add_vmanage_nic) as access_json:
   read_content = json.load(access_json)
   print(read_content)
   question_access=read_content['NetworkInterface']
   question_data=question_access['NetworkInterfaceId']
   public_eni_id=question_data
#write the interface eni out to the vars file will  need it to attach it
   public_eni_id_var=('eni_id=' + "'" + "{}".format(public_eni_id) + "'")
   print(public_eni_id_var)
with open(outfile_vars, 'a') as my_file:
   my_file.write(public_eni_id_var + "\n")


outfile_attach_vmanage_nic='attach-vmanage-nic.json'
cmd_attach_vmanage_nic='aws ec2 attach-network-interface --region' + " " + "{}".format(region) + " " +  '--network-interface-id' + " " + "{}".format(public_eni_id) + " " + '--instance-id' + " " + "{}".format(vmanage_instance_id) + " " + '--device-index 1'
output = check_output("{}".format(cmd_attach_vmanage_nic), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_attach_vmanage_nic, 'w') as my_file:
   my_file.write(output)


#assign an elastic ip to the secondary nic
#aws ec2 associate-address --allocation-id eipalloc-06a51c0591881f9cf --network-interface-id eni-1a2b3c4d
outfile_associate_eip_public='associate_eip_public.json'
cmd_associate_eip_public='aws ec2 associate-address --allocation-id' + " " + eip_public + " " +  '--network-interface-id' + " " + public_eni_id
print(cmd_associate_eip_public)
output = check_output("{}".format(cmd_associate_eip_public), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_associate_eip_public, 'w') as my_file:
   my_file.write(output)


#Add additional SSD of 1 TB to the instance
#Create the volume and get the volume id - /dev/sdf
outfile_volume='volume.json'
cmd_create_volume='aws ec2 create-volume --volume-type gp2 --size 1000 --availability-zone' + " " + az + " " + '--tag-specifications' + " " + 'ResourceType=volume,Tags=[{Key=Description,Value=vmanage-vol}]'
output = check_output("{}".format(cmd_create_volume), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_volume, 'a') as my_file:
    my_file.write(output + "\n")

with open(outfile_volume) as access_json:
    read_content = json.load(access_json)
    print(read_content)
    question_access=read_content['VolumeId']
    print(question_access)
    vol_id=question_access
    print(vol_id)

#Attach the volume to the instance
#aws ec2 attach-volume --volume-id vol-1234567890abcdef0 --instance-id i-01474ef662b89480 --device /dev/sdf
cmd_attach_vol='aws ec2 attach-volume --volume-id' + " " + vol_id + " " + '--instance-id' + " " + vmanage_instance_id + " " + '--device /dev/sdf'
output = check_output("{}".format(cmd_attach_vol), shell=True).decode().strip()
print("Output: \n{}\n".format(output))


#######CREATE THE THIRD NIC AND ATTACH IT AND THEN ASSIGN THE ELASTIC IP

#Create a Tertiary NIC and assign to the CLUSTER subnet
#cmd_add_nic_mgmt='aws ec2 create-network-interface --subnet-id' + " " + "{}".format(subnetid_public) + " " + '--description "vmanage_nic"' + " " + '--groups' + " " + "{}".format(mgmt_sg_id) + " " + '--private-ip-address 10.10.20.100'
outfile_add_vmanage_cluster_nic='add-vmanage-cluster-nic.json'
cmd_add_cluster_nic='aws ec2 create-network-interface --region' + " " "{}".format(region) + " " + '--subnet-id' + " " + "{}".format(subnetid_CLUSTER) + " " + '--description "vmanage_nic_CLUSTER_sub"' + " " + '--groups' + " " + "{}".format(sgid) + " " + '--tag-specifications' + " " + "'ResourceType=network-interface,Tags=[{Key=Name,Value=" + "{}".format(name) + '}]'"" + "'"
output = check_output("{}".format(cmd_add_cluster_nic), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_add_vmanage_cluster_nic, 'w') as my_file:
   my_file.write(output)

#Capture the tertiary CLUSTER eni_id out of the json output

with open(outfile_add_vmanage_cluster_nic) as access_json:
   read_content = json.load(access_json)
   question_access=read_content['NetworkInterface']
   question_data=question_access['NetworkInterfaceId']
   cluster_eni_id=question_data
   #write the interface eni out to the vars file will  need it to attach it
   cluster_eni_id_var=('eni_id=' + "'" + "{}".format(cluster_eni_id) + "'")
   print(cluster_eni_id_var)
with open(outfile_vars, 'a') as my_file:
   my_file.write(cluster_eni_id_var + "\n")


outfile_attach_vmanage_nic='attach-cluster-nic.json'
cmd_attach_cluster_nic='aws ec2 attach-network-interface --region' + " " + "{}".format(region) + " " +  '--network-interface-id' + " " + "{}".format(cluster_eni_id) + " " + '--instance-id' + " " + "{}".format(vmanage_instance_id) + " " + '--device-index 2'
output = check_output("{}".format(cmd_attach_cluster_nic), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_attach_vmanage_nic, 'w') as my_file:
   my_file.write(output)

#assign an elastic ip to the tertiary nic
#aws ec2 associate-address --allocation-id eipalloc-06a51c0591881f9cf --network-interface-id eni-1a2b3c4d
outfile_associate_eip_CLUSTER='associate_eip_CLUSTER.json'
cmd_associate_eip_CLUSTER='aws ec2 associate-address --allocation-id' + " " +  eip_cluster + " " + '--network-interface-id' + " " + cluster_eni_id
print(cmd_associate_eip_CLUSTER)
output = check_output("{}".format(cmd_associate_eip_CLUSTER), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_associate_eip_CLUSTER, 'w') as my_file:
   my_file.write(output)

#Wait to check the instance is initialized
#Check that the instance is initialized
cmd_check_instance='aws ec2 wait instance-status-ok --instance-ids' + " " + vmanage_instance_id + " " + '--region' + " " + "{}".format(region)
output = check_output("{}".format(cmd_check_instance), shell=True).decode().strip()
print("Output: \n{}\n".format(output))

'''

#To Do
#Do an EC2 instance describe and get the enid of the first nic deployed to the mgmt subnet
#get the eni_id of the first nic
#consider instead of associating public ip with first nic on mgmt subnet, instead associate elastic ip
#fix up code so that you can first enter in the elastic ip reservation ids into the vault and call from there

'''
