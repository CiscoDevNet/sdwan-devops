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
    inventory = ./inventory/hq1
    ```
    
1. Set the needed environment variables for access to your CML infrastucture.  Replace the values below with your server, credentials and lab name.
    ```
    export VIRL_HOST=myvirlhost.example.com
    export VIRL_USERNAME=myusername
    export VIRL_PASSWORD=mypasword
    export VIRL_LAB=myusername_sdwan
    ```

## Run the playbooks

1. Create the local CA used for certificate signing.
    ```
    ./play.sh build-ca.yml
    ```

1. Build out the underlay and control plane.
    ```
    ./play.sh build-virl.yml
    ```

1. Configure the SD-WAN control plane using the supplied inventory data.
    ```
    ./play.sh config-virl.yml
    ```

1. Provision and bootstrap the edges.
    ```
    ./play.sh deploy-virl.yml
    ```

1. Wait for the edges to sync in vManage.
    ```
    ./play.sh waitfor-sync.yml
    ```
    > Note: The `waitfor-sync.yml` playbook is useful when we want to wait until all edges are in sync and the service VPN is active.  We need to do this before validating the simulation, otherwise the validation check will fail.

1. Get inventory information.
    ```
    ./play.sh virl-inventory.yml
    ```

1. Get detailed inventory information for a single host.
    ```
    ./play.sh virl-inventory.yml --tags=detail --limit=vmanage1
    ```

1. Run the `check-sdwan.yml` playbook to validate the topology.
    ```
    ./play.sh check-sdwan.yml
    ```

## Clean the topology

To stop and wipe all of the nodes in the lab.
```
./play.sh clean-virl.yml
```

To clean individual nodes, use `--limit`.
```
./play.sh clean-virl.yml --limit=site1-cedge1
```

To remove the lab completely from the VIRL server.
```
./play.sh clean-virl.yml --tags=delete
```
