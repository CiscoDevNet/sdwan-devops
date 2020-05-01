#!/usr/bin/env python

import os
import sys
import json
import argparse


STATE_FILES = [
    './terraform-sdwan/vmware/terraform.tfstate.d/control/terraform.tfstate',
    './terraform-sdwan/vmware/terraform.tfstate.d/edges/terraform.tfstate'
]

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--list', action='store_true',
                        help='List host records from NIOS for use in Ansible')

    parser.add_argument('--host',
                        help='List meta data about single host (not used)')

    return parser.parse_args()


def main():
    args = parse_args()
    hostvars = {}
    all_hosts = []

    inventory = {
        '_meta': {
            'hostvars': hostvars
        },
        'all': {
            'hosts': all_hosts,
        },
        'vmware_hosts': {
            'hosts': all_hosts,
        }
    }

    for state_file in STATE_FILES:
        try: 
        # with open(state_file) as state:
            state = open(state_file)
            data = json.load(state)
            default_ip_addresses = data['outputs']['default_ip_addresses']['value']
            for item in default_ip_addresses:
                all_hosts.append(item['name'])
                hostvars[item['name']] = {'ansible_host': item['default_ip_address']}
        except:
            pass
    sys.stdout.write(json.dumps(inventory, indent=4))
    sys.exit(0)


if __name__ == '__main__':
    main()
