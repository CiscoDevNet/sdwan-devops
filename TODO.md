# TODO for sdwan-devops

There's a LOT to be worked on to make SD-WAN insfratructure-as-code a reality first, and as streamlined as possible eventually. Feel free to add more tasks or specific sub-tasks, and put your name to some you'd like to work on.

Some of the tasks listed here relate to the `terraform-sdwan` submodule

## Tasks

### Generic

- [ ] **Update README to cover changes**
- [ ] Switch to the public [sdwan-edge](https://github.com/CiscoDevNet/sdwan-edge/) code (imported as a Git submodule) for deploying cEdges.
- [ ] Fix the network interface detection issue
- [ ] Fix the `deviceIP` issue affecting 20.9.1 (and DHCP deployments) in the `config-sdwan.yml` play
- [ ] Discuss Ansible variable approach with some Ansible experts from the team
- [x] Support for specifying password and encoding it
- [ ] Static addressing has some conflicting configurations, clean that up
- [x] Update Docker container (pull in Nathan's work)
- [x] Split out day 1 automation (pull in Marcelo's work)
- [ ] Decouple serial file management from certificate authority, as it is related to edge deployment

### Generic multi-infra support

We should be able to use the same Ansible workflow to deploy both on-prem and all public clouds.

- [x] Add generic support for bastion hosts / proxies so that we can deploy behind NAT (or firewalls) with static IPs
- [x] Create infra specific Jinja templates as necessary, with the infra name in the file name, and defined as a variable in the inventory file
- [ ] Adapt the AWS code to use the inventory approach of `control.tfvars` to define the VMs to be deployed and their `user-data` (terraform-sdwan).
  - [x] **Alternatively, create an AWS specific `control.tfvars`, once the infra specific Jinja task is done.** (Lori)
- [x] Add support for *optional* VPC/network creation
  - [x] Pick up terraform outputs from VPC creation as Ansible facts
- [ ] Support deploying into existing VPC
- [x] Support for ACLs or adding IP ranges to the security group
- [ ] On AWS, if possible, use the APIs to check if quotas are enough for VPC and elastic IP before attempting to deploy. For bonus points, request quota increase automatically

### Integrations with SaaS tools

- [ ] [Terraform Cloud](https://app.terraform.io/) integration (for remote state management, multi-tenancy and better CI/CD integration)
- [ ] [CircleCI](https://app.circleci.com/) integration (Lori)
  - [ ] Build the Docker container
  - [ ] Test the Docker container (how?)
  - [ ] Publish the Docker container (besaed on branch and Git tag: different flavors, dev, release)

## Questions

- [ ] Where do we get licenses from?
- [ ] Why are the playbooks not in a `playbooks` directory?
- [ ] Why is there not a script to set all env variables?
- [ ] Why are the top level steps in, for exampe, virl-hq1.md, not in a script?
- [ ] Can we replace `inventory = ./inventory/hq1` with an environment variable?
- [ ] Is `./ansible/inventory/hq2/terraform.py` used by anything, or is it just a leftover from the early days of the repo?
- [x] What is the equivalent of TF destroy?
  - That would be `./play.sh /ansible/day_0/clean-vmware.yml`, which does a bit more than just TF destroy, but it fits the bill.
