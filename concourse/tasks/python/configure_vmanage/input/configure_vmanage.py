#!/usr/bin/env python
import json, re, sys, os, subprocess
from subprocess import call, check_output
import netmiko
from netmiko import *
from netmiko.cisco_base_connection import CiscoSSHConnection
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
from paramiko.ssh_exception import SSHException

vmanage_host = os.environ.get('VMANAGE_HOST')
vmanage_username = os.environ.get('VMANAGE_USERNAME')
vmanage_password = os.environ.get('VMANAGE_PASSWORD')
#auth = Authentication(host=vmanage_host, user=vmanage_username, password=vmanage_password).login()

key_file='ed25519'
username='admin'
ip='44.229.184.207'

net_connect = netmiko.ConnectHandler(ip=ip, device_type="linux", username="admin", key_file=key_file, password='admin')

print(net_connect.send_command("show interface"))





