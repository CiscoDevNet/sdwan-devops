# Building the SD-WAN control plane on CML

The steps below will build and configure the SD-WAN control plane and edges on CML.

>Note: The repo is designed for CML2.

## Create the SD-WAN images

If your CML server does not have the SD-WAN images installed, follow the steps [here](https://github.com/CiscoSE/virl-howtos/blob/master/virl2-sdwan-images/virl2-sdwan-devops.md) to create the proper node definitions and upload the images.

## Complete the prerequisites

1. Set the organization name.  Replace the value below with your organization name.
    ```
    export VMANAGE_ORG=myorgname
    ```

1. Copy a valid license file to `licenses/serialFile.viptela`.

1. Edit `ansible.cfg` and set the inventory variable to point to hq1.
    ```
    inventory = ./inventory/hq2
    ```
    
1. Set the needed environment variables for access to your CML infrastucture.  Replace the values below with your server, credentials and lab name.
    ```
    export CML_HOST=mycmlhost.example.com
    export CML_USERNAME=myusername
    export CML_PASSWORD=mypasword
    export CML_LAB=myusername_sdwan
    ```

1. Set the node definitions IDs used for control plane and edge devices.
    ```
    export VMANAGE_NODEDEF=viptela-manage
    export VSMART_NODEDEF=viptela-smart
    export VEDGE_NODEDEF=viptela-edge
    export CEDGE_NODEDEF=viptela-cedge
    ```

1. Set the image IDs to use for control plane and edge devices.
    ```
    export VMANAGE_IMAGE=viptela-manage-20.9.3.2
    export VSMART_IMAGE=viptela-smart-20.9.3.1
    export VEDGE_IMAGE=viptela-edge-20.9.3.1
    export CEDGE_IMAGE=iosxe-sdwan-17.3.5
    ```

1. Set the IP addressing for your control plane components.  Make sure these are valid and reachable IP addresses for your environment and that they are specified in CIDR notation (except for the `VPN0_GATEWAY`).
    ```
    export VMANAGE1_IP=1.1.1.1/24
    export VBOND1_IP=1.1.1.2/24
    export VSMART1_IP=1.1.1.3/24
    export VPN0_GATEWAY=1.1.1.254
    ```

1. Set the IP addressing for your edges.
    ```
    export HQ_EDGE1_IP=1.1.1.4/24
    export SITE1_EDGE1_IP=1.1.1.5/24
    export SITE2_EDGE1_IP=1.1.1.6/24
    ```
>Note: You do not need to supply this info if you are not going to deploy edges.

1. Set the cloud-init format as needed.  `v2` for later versions of vmanage and `v1` for earlier versions.
    ```
    export CLOUDINIT_TYPE=v2
    ```

1. And finally, set the version of control plane to use.
    ```
    export VIPTELA_VERSION=20.9.3
    ```

>Note: This value gets used to determine which version of device and feature templates to import into vManage.

## Run the playbooks

1. Create the local CA used for certificate signing.
    ```
    ./play.sh build-ca.yml
    ```

1. Build out the underlay and control plane.
    ```
    ./play.sh build-cml.yml
    ```

1. Configure the SD-WAN control plane using the supplied inventory data.
    ```
    ./play.sh config-sdwan.yml
    ```

1. Provision and bootstrap the edges.
    ```
    ./play.sh deploy-cml.yml
    ```

1. Wait for the edges to sync in vManage.
    ```
    ./play.sh waitfor-sync.yml
    ```
    > Note: The `waitfor-sync.yml` playbook is useful when we want to wait until all edges are in sync and the service VPN is active.  We need to do this before validating the simulation, otherwise the validation check will fail.

1. Get inventory information.
    ```
    ./play.sh cisco.cml.inventory.yml
    ```

1. Get inventory information for a single host.
    ```
    ./play.sh cisco.cml.inventory.yml --limit=vmanage1
    ```

1. Run the `check-sdwan.yml` playbook to validate the topology.
    ```
    ./play.sh check-sdwan.yml
    ```

## Clean the topology

To stop and wipe all of the nodes in the lab.
```
./play.sh clean-cml.yml
```

To clean individual nodes, use `--limit`.
```
./play.sh clean-cml.yml --limit=site1-cedge1
```
