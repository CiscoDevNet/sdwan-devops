#!/usr/bin/env python
import json, re, sys, os, json, time, logging, requests, urllib3
from requests.structures import CaseInsensitiveDict
urllib3.disable_warnings()
from requests.structures import CaseInsensitiveDict
import subprocess
from subprocess import call, check_output

#Passing in env vars from build container
VAULT_ADDR = os.getenv('VAULT_ADDRR')
VAULT_TOKEN = os.getenv('SSH_TOKEN') #This gets the vault token from the ephemeral build container

vars='vars.py'
import vars
from vars import *

outfile_vars="vars"
sg_name=name

#1 - Create a Key Pair
keypair_name=name
outfile_key_pair = 'keypair_name' + '.json'

#Inject the vault var vals into the ephemeral oci build container

VAULT_ADDR = os.getenv('VAULT_ADDR')
VAULT_TOKEN = os.getenv('SSH_TOKEN')
#VAULT_TOKEN = os.getenv('VAULT_TOKEN')
#Writing the AWS SSH Key to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/sdwan/" + name + "/" + "key_name"
headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"
#data = f'{{"token": "{TOKEN}"}}'
data_json = {"key_name": name }
resp = requests.post(url, headers=headers, json=data_json)
print(resp.status_code)



