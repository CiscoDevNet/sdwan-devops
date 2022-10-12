#!/usr/bin/env python
import json, re, sys, os, json, subprocess
from subprocess import call, check_output
import netmiko
from netmiko import *


from netmiko import ConnectHandler


key_file='us-west-1a.pem'
username='ec2-user'
#update the csr router ip here
ip='54.177.168.254'

net_connect = netmiko.ConnectHandler(ip=ip, device_type="cisco_ios", username="ec2-user", key_file=key_file)

print(net_connect.send_command("sh ip int brief"))

output = net_connect.send_command("end")
print(output)

output= net_connect.send_config_set("exec-timeout 0 0")
print(output)

output = net_connect.send_command("end")
print(output)

output= net_connect.send_config_set("no ip domain-lookup")
print(output)

output = net_connect.send_command("end")
print(output)

output = net_connect.send_config_set("host csr1000v")
print(output)

output = net_connect.send_command("end")
print(output)

output = net_connect.send_command("wr")
print(output)

output = net_connect.send_command("show ip int brief")
print(output)

output = net_connect.send_config_set("iox")
print(output)

output = net_connect.send_command("end")
print(output)

output = net_connect.send_command("wr")
print(output)

output = net_connect.send_command("show iox-service")
print(output)

output = net_connect.send_command("guestshell")
print(output)

output = net_connect.send_config_set("app-hosting appid guestshell")
print(output)


config_commands= [ 'interface VirtualPortGroup1',
                   'ip address 192.168.1.1 255.255.255.0',
                   'no shut']
output = net_connect.send_config_set(config_commands)
print(output)
output = net_connect.send_command("end")
print(output)


config_commands= [ 'app-hosting appid guestshell',
                   'vnic gateway1 virtualportgroup 0 guest-interface 0 guest-ipaddress 192.168.1.2 netmask 255.255.255.0 gateway 192.168.1.1 name-server 8.8.8.8']
output = net_connect.send_config_set(config_commands)
print(output)

output = net_connect.send_command("end")
print(output)

config_commands= [ 'interface VirtualPortGroup0',
                   'ip nat inside',
                   'exit',
                   'interface GigabitEthernet1',
                   'ip nat outside',
                   'exit',
                   'ip access-list extended NAT-ACL',
                   'permit ip 192.168.1.0 0.0.0.255 any',
                   'exit',
                   'ip nat inside source list NAT-ACL interface GigabitEthernet1 overload',
                   'end']

output = net_connect.send_config_set(config_commands)
print(output)
output = net_connect.send_command("end")
print(output)

config_commands= ['int gig 2',
                  'ip address 10.10.20.100 255.255.255.0',
                  'no shut']

output = net_connect.send_config_set(config_commands)
print(output)
output = net_connect.send_command("end")
print(output)


