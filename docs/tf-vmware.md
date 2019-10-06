# Building the SDWAN Control Plane on VMware with Terraform

Building out the control plane on VMware ESX is done in 2 steps:

1. Use Terraform to provision the virtual machines in vcenter
2. Run the `configure-control.yml` playbook to configure the control plane

## Build the SDWAN control plane

Clone the [Terraform SDWAN repo](https://github.com/ciscops/terraform-viptela) and follow the directios for deployment

## Configure the SD-WAN fabric

Set the name of the organization, e.g.:
```
export VMANAGE_ORG=myorgname
```

Make sure that you have a serial file in this location: `licenses/serialFile.viptela` 

Run the playbook

```bash
./play.sh configure-control.yml
```

This playbook will:

* Configure setting on vmanage
* Install Enterprise CA when required
* Add vbonds and vsmarts to vmanage
* Create CSRs for vbonds and vsmarts
* Install certificates into vmanage
* Push certificates to controllers
* Import templates if present
* Import policy if present
