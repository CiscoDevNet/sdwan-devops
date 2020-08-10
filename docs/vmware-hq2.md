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
    
1. Set the needed environment variables for access to your VMware infrastucture.  Replace the values below with your server and credentials.
    ```
    export TF_VAR_vsphere_user=administrator@vsphere.local
    export TF_VAR_vsphere_password=foo
    export TF_VAR_vsphere_server=vcenter.example.com
    ```

## Create/update the required inventory data

1. In `groupvars/all/local.yml` set the following variables to reflect your environment:
    * `datacenter`: the vCenter datacenter to use
    * `cluster`: the vCenter cluster to use
    * `folder`: (Optional) the folder to create in vCenter.  Provisioned VMs will be placed in this folder.  Provisioning will fail if the user does not have permissions to create VM folders in vCenter.
    * `resource_pool`: (Optional) the vCenter resource pool to use.
    * `datastore`: the datastore to use for VMs
    * `iso_datastore`: the datastore to use for cloud-init ISOs
    * `iso_path`: the path on the datastore for cloud-init ISOs
    * `vmanage_template`: the name of the vManage template in vCenter
    * `vbond_template`: the name of the vBond template in vCenter
    * `vsmart_template`: the name of the vSmart template in vCenter
    * `vedge_template`: the name of the vEdge template in vCenter
    * `cedge_template`: the name of the cEdge template in vCenter

1. In `inventory/hq2/sdwan.yml` set the following variables to reflect your environment:
    * `sdwan_vbond`: DNS name/IP address of the vbond server
    * `vpn0_portgroup`: the name of the vCenter port group to use for vpn0
    * `vpn0_gateway`: the default gateway to use for the vpn0 network
    * `vpn512_portgroup`: the name of the vCenter port group to use for vpn512
    * `vpn0_ip`: for each control plane component, set this to it's assigned static IP address
    * `servicevpn_portgroup`: the name of the vCenter port group to use for the service VPN (VPN 1)

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
