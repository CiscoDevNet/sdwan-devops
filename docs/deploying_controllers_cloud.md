# Deploying Controllers on AWS

## Cloning repo

Clone the sdwan-devops repo using the cloud branch (most up to date):

- `git clone --branch cloud --single-branch --recursive https://github.com/ciscodevnet/sdwan-devops.git`

Make sure you use `--recursive` to also clone folders sdwan-edge and terraform-sdwan.

All operations are run out of the sdwan-devops directory: `cd sdwan-devops`

## License file

Generate a licence file corresponding to your org-name that will contain your device UUIDs:

- https://software.cisco.com/software/csws/ws/platform/home?locale=en_US#pnp-devices

Download and copy into `ansible/licences`

## Configure parameters

All parameters are defined in a single configuration file named **config.yaml** under folder **config**.

Go to the **config** directory

- copy `config.example.yaml` to `config.yaml`
- Update required parameters, most likely your ssh_public_key, controllers and wan-edge ami image identifiers as well as wan-edge UUIDs.

## Define environnement variables

Go to the **bin** folder.

Update your AWS profile name in file **minimal_env.sh** (if this is not "default").

Set environnement variables (make sure to use source ....)

```shell
source minimal_env.sh
```

## Config Builder

With **bin** as your current folder, build all ansible parameter files:

```shell
./config_build.sh
```

This will render parameter files for ansible playbooks based on **config/config.yaml** and **jinja templates**:

- Ansible day-1 vars: 'config/templates/day-1_local.j2' -> '../ansible/day_-1/group_vars/all/local.yml'
- Ansible day_0 vars: 'config/templates/day0_local.j2' -> '../ansible/day_0/group_vars/all/local.yml'
- Ansible day_1 vars: 'config/templates/day1_local.j2' -> '../ansible/day_1/group_vars/all/local.yml'
- Ansible SDWAN inventory: 'config/templates/sdwan_inventory.j2' -> '../ansible/inventory/sdwan_inventory.yml'

## Create CA (Day -1)

With **bin** as your current folder, run the script to create certificates:

```shell
./install_ca.sh
```

This will create a local CA in **ansible/myCA**.

## Deploy Controllers (day0)

With **bin** as your current folder, deploy and configure Control Plane:

```shell
./install_cp.sh
```

This will execute ansible playbook: **/ansible/day_0/build-control-plane.yml**

Which imports:

- /ansible/day_0/deploy-control-plane.yml
- /ansible/day_0/config-control-plane.yml
  - which in turns, imports:
    - /ansible/day_0/check-reqs.yml
    - /ansible/day_0/check-vmanage.yml
    - /ansible/day_0/config-vmanage.yml

You can also execute individual playbooks if you want to check every step of the process:

```shell
./play.sh /ansible/day_0/deploy-control-plane.yml
./play.sh /ansible/day_0/check-reqs.yml
./play.sh /ansible/day_0/check-vmanage.yml
./play.sh /ansible/day_0/config-vmanage.yml
./play.sh /ansible/day_0/config-certificates.yml
```

Notes:

- deploy-control-plane.yml: generate day0 configurations and instantiate all controllers.
- check-reqs.yml: check org-name is defined and serial file exists.
- check-vmanage.yml: check vManage is able to respond to REST API calls. Can take a while (~60 retries or 15 sec each).
- config-vmanage.yml: configure vManage settings and add vBond and vSmart controllers to vManage.
- config-certificates.yml: add certificates for all controllers.

## Deleting Controllers

With **bin** as your current folder:

```shell
./delete_cp.sh
```
