# Building the SDWAN Control Plane on VMware with Terraform

Building out the control plane on VMware ESX is done in 2 steps:

1. Use Terraform to provision the virtual machines in vcenter
2. Run the `configure-control.yml` playbook to configure the control plane

## Build the SDWAN control plane

Clone the [Terraform SDWAN repo](https://github.com/ciscops/terraform-viptela) and follow the directions for deployment

## Create the local CA

If you are using a local CA, create it:

```bash
./play.sh build-ca.yml
```

## Configure the SD-WAN fabric

Set the name of the organization, e.g.:

```bash
export VMANAGE_ORG=myorgname
```

Make sure that you have a serial file in this location: `licenses/serialFile.viptela` 

## Create/update the inventory

You can start with the examples in `inventory/deployments` (e.g. `sdwan1.yml`):

```yaml
all:
  vars:
    sdwan_vbond: 192.133.179.13
  children:
    sdwan:
      children:
        sdwan_control:
          children:
            vmanage_hosts:
              vars:
                sdwan_personality: vmanage
                sdwan_device_model: vmanage
              hosts:
                cpn-rtp-vmanage1:
                  sdwan_system_ip: 1.1.1.1
                  sdwan_transport_ip: 192.168.179.11
                  ansible_host: "{{ sdwan_transport_ip }}"
                  sdwan_site_id: 1
            vbond_hosts:
              vars:
                sdwan_personality: vbond
                sdwan_device_model: vbond
              hosts:
                cpn-rtp-vbond1:
                  sdwan_system_ip: 1.1.3.1
                  sdwan_transport_ip: 192.168.179.13
                  ansible_host: "{{ sdwan_transport_ip }}"
                  sdwan_site_id: 3
            vsmart_hosts:
              vars:
                sdwan_personality: vsmart
                sdwan_device_model: vsmart
              hosts:
                cpn-rtp-vsmart1:
                  sdwan_system_ip: 1.1.2.1
                  sdwan_transport_ip: 192.168.179.12
                  ansible_host: "{{ sdwan_transport_ip }}"
                  sdwan_site_id: 2
```

The following items need to be set to reflect the specifics of your environment:

* `sdwan_vbond`: DNS name/IP address of the vbond server
* `system_ip`: The system IP of that control plane member
* `transport_ip`: The VPN0 address that the control plane members will communicate with each other
* `ansible_host`: This is the address that Ansible will use to configure the control plane members.  If the `inventory_hostname` is resolvable, then it is not needed. If it is the VPN0 address, it can be specified as `"{{ sdwan_transport_ip }}"`, otherwise, it is DNS name/IP address Ansible should use.

## Configure the SD-WAN Control Plane

Run the playbook

```bash
./play.sh configure-control.yml -i inventory/deployments/sdwan1.yml
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