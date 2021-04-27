# Building the SD-WAN control plane on VMware

The steps below will build and configure the SD-WAN control plane and edges on VMware.

> Note: the only tested reference topology for VMware is the hq2 topology.

## Create the SD-WAN images

The VMware playbooks make use of terraform to provision the control plane and edge VNFs.  Prior to running the playbooks, ensure you have the correct SD-WAN images deployed to your VMware cluster.  Follow the directions for creating the VMware images in the [terraform-sdwan](https://github.com/CiscoDevNet/terraform-sdwan) repo.

> Note: You only need to create the images.  You do not need to do any of the other steps outlined in the terraform-sdwan repo for provisioning using terraform.  The playbooks will run terraform automatically using the data specified in Ansible inventory.

## Complete the prerequisites

1. Set the organization name.  Replace the value below with your organization name.
    ```
    export VMANAGE_ORG=myorgname
    ```

1. Copy a valid license file to `licenses/serialFile.viptela`.

1. Edit `ansible.cfg` and set the inventory variable to point to hq2.
    ```
    inventory = ./inventory/hq2
    ```
    
1. Set the needed environment variables for access to your VMware infrastucture.  Replace the values below with your server, credentials and environment info.
    ```
    export TF_VAR_vsphere_user=administrator@vsphere.local
    export TF_VAR_vsphere_password=foo
    export TF_VAR_vsphere_server=vcenter.example.com
    export TF_VAR_datacenter=my_datacenter
    export TF_VAR_cluster=my_cluster
    export TF_VAR_folder=my_folder
    export TF_VAR_resource_pool=
    export TF_VAR_datastore=my_datastore
    export TF_VAR_iso_datastore=my_datastore
    export TF_VAR_iso_path=cloud-init
    ```

1. Set the IP addressing for your control plane components.  Make sure these are valid and reachable IP addresses for your environment and that they are specified in CIDR notation (except for the `VPN0_GATEWAY`).
    ```
    export VMANAGE1_IP=1.1.1.1/24
    export VBOND1_IP=1.1.1.2/24
    export VSMART1_IP=1.1.1.3/24
    export VPN0_GATEWAY=1.1.1.254
    ```

1. Set the VMware port group info for each VPN.  Use the name of the port group as seen in vCenter.
    ```
    export VPN0_PORTGROUP="Your VPN0 port group"
    export VPN512_PORTGROUP="Your VPN512 port group"
    export SERVICEVPN_PORTGROUP="Your service VPN port group"
    ```

1. Set the IP addressing for your edges.
    ```
    export HQ_EDGE1_IP=1.1.1.4/24
    export SITE1_EDGE1_IP=1.1.1.5/24
    export SITE2_EDGE1_IP=1.1.1.6/24
    ```
>Note: You do not need to supply this info if you are not going to deploy edges.

1. Set the version of IOS-XE to use for edge devices.  Set this to the name of the template you want to use in VMware
    ```
    export IOSXE_SDWAN_IMAGE=iosxe-sdwan-16.12.2r
    ```

1. And finally, set the version of control plane to use.
    ```
    export VIPTELA_VERSION=19.2.1
    ```

>Note: This value gets appended to the template name (e.g. viptela-manage, viptela-smart, etc.) so make sure these names line up with the template names you have in VMware.

## Run the playbooks

1. Create the local CA used for certificate signing.
    ```
    ./play.sh build-ca.yml
    ```

1. Build the control plane on VMWare.
    ```
    ./play.sh build-vmware.yml
    ```
    > Note: this playbook can take a long time to run.  You can verify activity by using the vCenter UI to verify provisioning and watch the VNF boot process.

    > Note: this playbook will fail if a VM folder has been specified and the user does not have rights to create VM folders in vCenter.  In this case, comment out the `folder` variable in `group_vars/all/local.yml` and all VMs will be created in the root of the datacenter.

1. Configure the SD-WAN control plane using the supplied inventory data.
    ```
    ./play.sh config-vmware.yml
    ```
    > Note: sometimes this playbook will fail because an incorrect IP address was detected for vBond.  If this happens, simply re-run the `build-vmware.yml` playbook as shown above.  This appears to be a bug in the way vBond reports IP addressing to VMware.

1. Provision and bootstrap the edges.
    ```
    ./play.sh deploy-vmware.yml
    ```
    > Note: this playbook can take a long time to run.  You can verify activity by using the vCenter UI to verify provisioning and watch the boot process.

1. Wait for the edges to sync in vManage.
    ```
    ./play.sh waitfor-sync.yml
    ```
    > Note: The `waitfor-sync.yml` playbook is useful when we want to wait until all edges are in sync and the service VPN is active.  We need to do this before validating the simulation, otherwise the validation check will fail.

1. Run the `check-sdwan.yml` playbook to validate the topology.
    ```
    ./play.sh check-sdwan.yml
    ```

## Clean the topology

To delete the entire simulation, including the control plane and edges.

```
./play.sh clean-vmware.yml
```

To delete only the edges, use the `edges` tag.

```
./play.sh clean-vwmare.yml --tags="edges"
```

To delete only the control plane, use the `control` tag.

```
./play.sh clean-vmware.yml --tags="control"
```
