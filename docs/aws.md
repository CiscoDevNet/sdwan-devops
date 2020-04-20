# Building the Cisco SDWAN control plane in AWS

To build control plane:
```
$ ./play.sh build-aws.yml -e key_name=STEVENCA-M-C6HA -e env=customer2
```

To clean the control plane:
```
$ ./play.sh clean-aws.yml -e key_name=STEVENCA-M-C6HA -e env=customer2
```

Options are specifed as extra vars (e.g. -e <var>=<value>).  The options are:
* `env`: The name of the environment (e.g. customer name)
* `key_name`: The keypair name to use 
* `version`: The version of the viptela AMIs to create (default: 18.3.4)
* `region`: The region in which to create the protoype instances and AMIs (default: us-east-1)
* `subnet_id`: The subnet ID in which to create the protoype instances

### Requirements:
* pip: `pip install -r requirements.txt`
* AMIs in the region created with the naming convention `viptela-[vmanage,vedge,vsmart]-{{ version }}` as with in [proceedure](https://wwwin-github.cisco.com/ciscops/viptela-ops/blob/master/AMIs.md).
* `default` security groups needs to allow ssh and netconf from the control node. ([Issue #2](https://wwwin-github.cisco.com/ciscops/viptela-ops/issues/2)).
* 6 free EIPs need to be available.
* A license file located at `licenses\viptela_serial_file.viptela`
* The organization name associated with the license file set on the command like with `-e 'organization_name="<your org name>"'` or set in `inventory/group_vars/all/viptela.yml`.