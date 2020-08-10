
# SDWAN DevOps

This repo contains a set of tools to automate workflows and build CI/CD pipelines for Cisco SDWAN.

> Note: The tools in this repo only work from a Unix environment with Docker (e.g. Linux, MacOS, etc.) due to issues with Ansible and file permissions mapping between Windows and the Linux container used in `play.sh`.  WSL2 may fix this issue and we will revisit when WSL2 is released.

> Note: This repo is tested against CML^2 and VMware vCenter 6.7.

## Cloning the repo

``` bash
git clone --recursive https://github.com/ciscodevnet/sdwan-devops.git
```

All operations are run out of the `sdwan-devops` directory:

```bash
cd sdwan-devops
```

## Quick start instructions

If you want to skip all the info and documentation below and just run the automation, use the following links, otherwise read on for more details.

- [Build the hq1 topology in CML](docs/virl-hq1.md)
- [Build the hq2 topology in CML](docs/virl-hq2.md)
- [Build the hq2 topology in VMware](docs/vmware-hq2.md)

## Software Dependancies

All software dependencies have been rolled into a Docker container.  Ansible playbooks are launched via the container using the `play.sh` shell script.  The `Dockerfile` included in this repo is used to automatically build the [ansible-sdwan](https://hub.docker.com/repository/docker/ciscops/ansible-sdwan) container image on Docker Hub.

For a detailed list of the dependencies required to run the playbooks, refer to the `Dockerfile`.

## Licensing Requirements

The following licensing-related tasks need to be completed prior to running the playbooks:
1. Copy a valid Viptela license file into `licenses/serialFile.viptela`
1. Set organization name as an environment variable using `export VMANAGE_ORG=myorgname`.

These values can also be set permanently in `group_vars/all/local.yml` if desired.

```yaml
organization_name: "<your org name>"
license_token: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

> Note: Edge device UUIDs must be updated to reflect the ones from the `serialFile.viptela` provided.  This is done by updating `sdwan_uuid` value for each edge in the `sdwan.yml` inventory file (e.g. `inventory/hq1/sdwan.yml`).  See the `Variables` section for more information.

## Capabilities

### Running playbooks via the Docker container

To run playbooks in this repo, use the `play.sh` shell script as shown below:

```bash
./play.sh <playbook> <options>
```

### Simulation

Simulation can be used for developing new deployments as well as testing changes to current deployments.  Simulation capabilities are provided by CML^2 or VMware.  The [Ansible CML^2 Modules](https://github.com/ciscodevnet/ansible-virl) are used to automate deployments in CML^2.  The [Terraform Modules](https://github.com/CiscoDevNet/terraform-sdwan) are used to automate deployments in VMware.

### Automation Playbooks

* `build-ca.yml`
  * Create a local CA in `./myCA`
* `build-virl.yml` or `build-vmware.yml`
  * Creates Day0 config for VNFs based on the data in the `sdwan.yml` file
  * Provision and start VNFs on virtual infrastructure
* `config-virl.yml` or `config-vmware.yml`
  * Configure setting on vmanage
  * Install Enterprise CA when required
  * Add vbonds and vsmarts to vmanage
  * Create CSRs for vbonds and vsmarts
  * Install certificates into vmanage
  * Push certificates to controllers
  * Import templates if present
  * Import policy if present
* `deploy-virl.yml` or `deploy-vmware.yml`
  * Create Day0 config for edge VNFs
  * Provision and boot edge VNFs on virtual infrastructure
* `import-templates.yml`
  * Imports device and feature templates into vManage
* `attach-templates.yml`
  * Attaches templates to devices as specified in the `sdwan.yml` file
* `import-policy.yml`
  * Imports policy into vManage
* `activate-policy.yml`
  * Activates policy 
* `waitfor-sync.yml`
  * Waits until all edge devices are in sync on vManage

### Validation Playbooks
* `check-sdwan.yml`
  * Check overlay connectivity using ping
  * Can check for things that should, or should not, work

### Testing

Jenkins CI is used for automatic and manual testing.  The various Jenkinsfiles in use are in the `jenkins` directory.  A `gitlab-ci.yml` file is also included for running CI from GitLab.

## Structure

### Inventories

The repo contains a set of playbooks, roles, and templates that are fed from the included inventories. Several built-in topologies located in the inventory and more can be added.  There are two topologies that are provided in the `inventory` directory:

* `hq1` builds only on CML^2 and includes an underlay network, SD-WAN control plane and SD-WAN edges (see [hq1.png](docs/images/hq1.png))
* `hq2` builds on CML^2 and VMware and includes the SD-WAN control plane and SD-WAN edges in a flat network (see [hq2.png](docs/images/hq2.png))

To switch between topologies, either edit `ansible.cfg` and point `inventory` to the proper directory:

For example, change:
```
inventory = ./inventory/hq1
```
to
```
inventory = ./inventory/hq2
```

or specify `-i` with every command (e.g. `./play.sh -i inventory/hq1 build-virl.yml`)

The local defaults for all inventories are set in `sdwan-devops/group_vars/all/local.yml`

### Variables

There are a set of required variables that must be set for each device in the topology.  An example for a typical edge device is shown below.  Note that in the case of the `hq1` inventory, you don't need to modify any of these values if you just want to test out the automation.  However, the `hq2

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
