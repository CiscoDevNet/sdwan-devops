# Deploying C8000v on Cloud (AWS, Azure and GCP)

Details in [Deploying C8000v](https://github.com/CiscoDevNet/sdwan-edge/blob/main/README.md)

## Cloning repo

Clone the sdwan-devops repo using the main branch (default: origin/main):

```shell
git clone --single-branch --recursive https://github.com/ciscodevnet/sdwan-devops.git
```

Make sure you use `--recursive` to also clone folders sdwan-edge and terraform-sdwan.

All operations are run out of the sdwan-devops directory: `cd sdwan-devops`

## C8000v AWS AMI

To find Image id:

- Go to the [AWS Marketplace](https://aws.amazon.com/marketplace/) page
- search for the image called: 'Cisco Catalyst 8000V Edge Software - BYOL'
- Click on the image title.
- Click **Continue to Subscribe** button.
- Click **Continue to Configuration** button.
- Verify **Fulfillment Option**, **Software Version**, and **Region** values. Changing any of these can change the **Ami Id**.
- Find and save the **Ami Id** - this will be used in the config.yml configuration file in the next section.

## Configure parameters

All parameters are defined in a single configuration file named **config.yaml** under folder **config**.

Go to the **config** directory

- copy `config.example.yaml` to `config.yaml`
- Update required parameters, most likely your ssh_public_key, controllers and wan-edge ami image identifiers as well as wan-edge UUIDs.

## Define environnement variables

Go to the **bin** folder.

Update your credentials in file **minimal_env.sh**.

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

## Deploy C8000v

With **bin** as your current folder, deploy the C8000v:

```shell
install_edges.sh
```

which invokes: `./play.sh /ansible/day_0/onboard-edges.yml`

that uses the following playbooks:

- get-bootstrap.yml
- terraform-apply-edges.yml
- terraform-apply-edges.yml

Note:

- If no template is attached to the UUIDs specified, a basic day0 configuration will be used.
- If a template is attached, the vManage generated configuration will be used as day0 config.

## Deleting C8000v

With **bin** as your current folder:

```shell
./delete_edges.sh
```
