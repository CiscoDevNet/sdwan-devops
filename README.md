# SDWAN DevOps

This repo contains a set of tools to create automated workflows and CI/CD pipelines for Cisco SDWAN.

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
docker build -t ansible-viptela .
```

#### Running the the playbooks in the docker container

In order to make this easier, a bash script has also been provided:

```bash
./play.sh <playbook> <options>
```

### Licensing Requirements

* A Viptela license file and the Organization name associated with that license file in `licenses/serialFile.viptela`.
* The Organization name associated with the serial file
* A Cisco Smart License token that point to an account with ASAv licensing (when licensing is required)

The easiest way to provide this information to the playbooks is to create `inventory/group_vars/all/local.yml` and specify the following:

```yaml
organization_name: "<your org name>"
license_token: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

## Inventories/Topologies

This repo comes with several built-in topologies and more can be added.  In order to switch between
topologies, either edit `ansible.cfg` and point `inventory` to the proper directory (e.g. `inventory/hq1`)
or specify `-i` with every command (e.g. `./play.sh -i inventory/hq1 build-cml.yml)

## Infrastructure

This tooling is capable of deploying on different infrastructure:
* [Cisco Modelling Labs](docs/cml.md)
* [Vmware](docs/vmware.md)
* AWS
* Azure