#!/usr/bin/env python
#This Script creates the vmanage from AMI and the key - split out the key
import json, re, sys, os, json, subprocess, time, sys, logging, requests, urllib3
from subprocess import call, check_output
from requests.structures import CaseInsensitiveDict
urllib3.disable_warnings()

outfile_vars="vars"
lab_vars='lab_vars.py'
import lab_vars
from lab_vars import *

keypair_name=name
sg_name=name

path = os.getcwd()
print(path)
os.listdir(path)

VAULT_ADDR = os.getenv('VAULT_ADDRR')
VAULT_TOKEN = os.getenv('SSH_TOKEN') #This gets the vault token from the ephemeral build container
vpcid = os.getenv('vpcid')
vmanage_instance_id = os.getenv('vmanage_instance_id')
vol_id = os.getenv('vol_id')

#Delete first the Instance ID and poll state for terminated then delete everything else

#aws ec2 terminate-instances --instance-ids i-1234567890abcdef0
cmd_ec2_delete='aws ec2 terminate-instances --instance-ids' + " " + "{}".format(vmanage_instance_id) + " " + '--region' + "  " + "{}".format(region)
print(cmd_ec2_delete)
output = check_output("{}".format(cmd_ec2_delete), shell=True).decode().strip()
print("Output: \n{}\n".format(output))

#Poll Instance State
cmd_check_instance='aws ec2 wait instance-terminated --instance-ids' + " " + vmanage_instance_id + " " + '--region' + " " + "{}".format(region)
output = check_output("{}".format(cmd_check_instance), shell=True).decode().strip()
print("Output: \n{}\n".format(output))

'''

#Delete Volume
#aws ec2 delete-volume --volume-id vol-049df61146c4d7901
cmd_vol_delete='aws ec2 delete-volume --volume-id' + " " + "{}".format(vol_id)
print(cmd_vol_delete)
output = check_output("{}".format(cmd_vol_delete), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
'''

#Delete Secondary NIC
#aws ec2 delete-network-interface --network-interface-id eni-e5aa89a3
public_eni_id = os.getenv('public_eni_id ')
cmd_pub_eni_delete='aws ec2 delete-network-interface --network-interface-id' + " " + "{}".format(public_eni_id)
output = check_output("{}".format(cmd_pub_eni_delete), shell=True).decode().strip()
print("Output: \n{}\n".format(output))


#Delete Tertiary NIC
#aws ec2 delete-network-interface --network-interface-id eni-e5aa89a3
cluster_eni_id = os.getenv('cluster_eni_id')
cmd_cluster_eni_delete='aws ec2 delete-network-interface --network-interface-id' + " " + "{}".format(cluster_eni_id)
print(cmd_cluster_eni_delete)
output = check_output("{}".format(cmd_cluster_eni_delete), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
