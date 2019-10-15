
# SDWAN DevOps

This repo contains a set of tools to automate workflows and build CI/CD pipelines for Cisco SDWAN.

## Installation

## Cloning the repo

``` shell
git clone --recursive https://github.com/ciscodevnet/sdwan-devops.git
```

All operations are run out of the `sdwan-devops` directory:

```bash
cd sdwan-devops
```

### Software Dependancies

* [ansible-viptela](https://github.com/CiscoDevNet/ansible-viptela) (Delivered as part of the repo when `--recursive` is used when cloning)
* Python 3 with the dependencies listed in requirements.txt
* sshpass


### Running with Docker

The easiest way to address the python and sshpass dependencies is to use the Dockerfile packaged in the repo.  All development and testing uses this Dockerfile, so it is the best way to guarantee that the tooling will run as designed

#### Build the Docker container

To build the docker container, run:

```bash
docker build -t ansible-sdwan .
```

#### Running the the playbooks in the docker container

In order to make this easier, a bash script has also been provided:

```bash
./play.sh <playbook> <options>
```

### Licensing Requirements

* A Viptela license file and the Organization name associated with that license file in `licenses/serialFile.viptela`.
* The Organization name associated with the serial file
* A Cisco Smart License token that point to an account with ASAv licensing (when licensing non-SD-WAN VNFs is required)

Set the name of the organization, e.g.:
```
export VMANAGE_ORG=myorgname
```

**Note:** This value can be set permanently in `group_vars/all/local.yml`

```yaml
organization_name: "<your org name>"
license_token: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

**Note:** Edge devices in the topologies must be updated to reflect the one from the `serialFile.viptela` provided.  This is done by updated `sdwan_uuid` in the `sdwan.yml` inventory file in the `host_vars` directory corresponding to the edge device (e.g. `inventory/hq1/host_vars/hq-cedge1/sdwan.yml`).  See the `Variables` section for more information.

## Structure

The repo contains a set of playbooks, roles, templates, and inventories.

### Inventories

This repo comes with several built-in topologies located in the inventory and more can be added.  In order to switch between topologies, either edit `ansible.cfg` and point `inventory` to the proper directory:

For example, change:
```
inventory = ./inventory/hq1
```
to
```
inventory = ./inventory/crn1
```

or specify `-i` with every command (e.g. `./play.sh -i inventory/hq1 build-cml.yml`)

The local defaults for all inventories are set in `sdwan-devops\group_vars/all/local/yml`

### Variables

The following variables are used by the playbooks and must be set somewhere in the inventory:

```yaml
sdwan_system_ip: 192.168.255.13
sdwan_site_id: 1
sdwan_vbond: 10.0.0.11
sdwan_model: 'vedge-CSR-1000v'
sdwan_uuid: 'CSR-82DEC3C6-3A28-B866-6F4A-40BEA274CA00'
sdwan_personality: vedge
sdwan_template:
  name: 'hq-csr1000v'
  variables:
    'vpn512_interface': GigabitEthernet1
    'vpn0_internet_ipv4_address': 10.0.0.13/24
    'vpn0_default_gateway': 10.0.0.1
    'vpn0_interface': GigabitEthernet2
    'vpn1_ipv4_address': 10.0.255.6/30
    'vpn1_interface': GigabitEthernet3
    'vpn1_ospf_interface': GigabitEthernet3
    'system_latitude': 37.411343
    'system_longitude': -121.938803
    'system_site_id': 1
    'system_host_name': hq-cedge1
    'system_system_ip': 192.168.255.13
    'banner_login': "{{ login_banner }}"
    'banner_motd': Welcome to hq-cedge1!
```

## Playbooks

### `configure-control.yml`
* Configure setting on vmanage
* Install Enterprise CA when required
* Add vbonds and vsmarts to vmanage
* Create CSRs for vbonds and vsmarts
* Install certificates into vmanage
* Push certificates to controllers
* Import templates if present
* Import policy if present

### `build-ca.yml`
* Creates a local CA

Infrastructure specific playbooks for building the control plane and deploying vedges are described in the specific infrastructure instructions below

## Infrastructure

This tooling is capable of deploying on different infrastructure:
* [VIRL](docs/virl.md)
* [Vmware](docs/tf-vmware.md)
* AWS
* Azure

