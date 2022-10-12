#!/usr/bin/env python
import json, re, sys, os, json, subprocess, requests, urllib3
from subprocess import call, check_output
from vmanage.api.authentication import Authentication
from vmanage.api.device import Device
import pprint
import os
urllib3.disable_warnings()

vmanage_host = os.environ.get('VMANAGE_HOST')
vmanage_username = os.environ.get('VMANAGE_USERNAME')
vmanage_password = os.environ.get('VMANAGE_PASSWORD')
pp = pprint.PrettyPrinter(indent=2)

auth = Authentication(host=vmanage_host, user=vmanage_username,
                      password=vmanage_password).login()
vmanage_device = Device(auth, vmanage_host)

device_config_list = vmanage_device.get_device_config_list('all')
pp.pprint(device_config_list)