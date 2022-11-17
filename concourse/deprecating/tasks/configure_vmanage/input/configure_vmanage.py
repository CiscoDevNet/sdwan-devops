#!/usr/bin/env python
import json, re, sys, os, json, subprocess, requests, urllib3
from subprocess import call, check_output
from vmanage.api.authentication import Authentication
from vmanage.api.device import Device
import pprint
import os
import serial
urllib3.disable_warnings()

vmanage_host = os.environ.get('VMANAGE_HOST')
vmanage_username = os.environ.get('VMANAGE_USERNAME')
vmanage_password = os.environ.get('VMANAGE_PASSWORD')

auth = Authentication(host=vmanage_host, port=443, user=vmanage_username, password=vmanage_password).login()