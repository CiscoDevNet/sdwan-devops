# Building the SDWAN Control Plane on VMware with Terraform

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

## Clean the SDWAN control plane

Stops and wipes all of the nodes in the lab.

```bash
./play.sh clean-control.yml
```