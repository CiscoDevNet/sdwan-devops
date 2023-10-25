# SDWAN DevOps

This repo contains a set of tools to automate workflows and build CI/CD pipelines for Cisco SDWAN.

> Note: The tools in this repo only work from a Unix environment with Docker (e.g. Linux, MacOS, etc.) due to issues with Ansible and file permissions mapping between Windows and the Linux container used in play.sh. WSL2 may fix this issue and we will revisit when WSL2 is released.

All operations are run out of the sdwan-devops directory: `cd sdwan-devops`

The folder `sdwan-edge` allows the deployment of C8000v in AWS, Azure, GCP. Openstack and VMware.

The folder `sdwan-terraform` allows the deployment of SDWAN Controllers in AWS, Azure and VMware.

A video demonstration of the use of this repository is available on [Vidcast](https://app.vidcast.io/share/1e934c26-ece4-4167-a986-4db17f125423).

## Clone repository

Clone the sdwan-devops repo using the main branch (default: origin/main):

```shell
git clone --single-branch --recursive https://github.com/ciscodevnet/sdwan-devops.git
```

Make sure you use `--recursive` to also clone folders sdwan-edge and terraform-sdwan.

## Openssl version3

If you are on a Mac: we need openssl version3, while on mac this is LibreSSL.

Upgrade openssl:

```shell
brew install openssl@3
```

## Software Dependencies

All software dependencies have been rolled into a Docker container. Ansible playbooks are launched via the container using the play.sh shell script.

All you need is a valid installation of docker on your system.

> Note: The Dockerfile included in this repo is used to automatically build the sdwan-devops container image and publish it to the GitHub Container Registry. For a detailed list of the dependencies required to run the playbooks, refer to the Dockerfile.

## Running playbooks via the Docker container

To run playbooks in this repo, use the play.sh shell script as shown below:

- `./play.sh <playbook> <options>`

This will start the docker container published in the GitHub Container Registry, run the playbooks inside the container and remove it once finished.

## Deploying Controllers on AWS

The sdwan-devops can be used to instantiates controllers on AWS.

[Deploying Controllers on AWS](docs/deploying_controllers_cloud.md)

- Deploy vBond, vSmart and vManage controllers in a VPC
- Provides bootstrap configuration

## Deploying C8000v

C8000v can be deployed in a transit VPC/VNET in AWS, Azure and GCP, and can also be deployed on VMware and Openstack.

[Deploying C8000v](docs/deploying_edges_cloud.md)

- Generates bootstrap configuration (cloud-init format)
- Creates transit VPC if required
- Deploy C8000v

## Simulation

Simulation can be used for developing new deployments as well as testing changes to current deployments.  Simulation capabilities are provided by CML^2 or VMware.  The [Ansible CML^2 Modules](https://github.com/ciscodevnet/ansible-virl) are used to automate deployments in CML^2.  The [Terraform Modules](https://github.com/CiscoDevNet/terraform-sdwan) are used to automate deployments in VMware.

[Simulation](docs/simulation.md)
