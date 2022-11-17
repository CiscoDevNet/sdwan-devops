#!/bin/sh
cd input
export AWS_PAGER=""
rm -rf __pycache__
#run instance with the user data and verify it comes up correctly
apt-get update
apt-get -y install python3-pip --fix-missing
/usr/local/bin/python -m pip install --upgrade pip
pip3 six
pip3 install viptela
pip3 install viptela --upgrade
python3 -m pip install pyserial
VMANAGE_HOST="44.229.184.207"
export VMANAGE_HOST
VMANAGE_USERNAME='admin'
export VMANAGE_USERNAME
VMANAGE_PASSWORD='admin'
export VMANAGE_PASSWORD
git clone https://github.com/CiscoDevNet/python-viptela.git
cd python-viptela
pip install -e .
cd ../
python3 configure_vmanage.py
#python3 serial_test.py
