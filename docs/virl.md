# VIRL

Both the control plane and the edge can be deployed in virl

## Dependencies

Set the name of the lab, e.g.:
```
export VIRL_HOST=myvirlhost
export VIRL_USERNAME=myusername
export VIRL_PASSWORD=mypasword
export VIRL_LAB=myusername_sdwan
```

These values can be set permanently in the `virl.yml` file in the inventory by adding:
```
host: myvirlhost
username: myusername
password: mypasword
lab: myusername_sdwan
```

## Lab files

The files that define the labs are located in `{{ playbook_dir }}/files`.  The `build-virl.yml` playbooks builds the lab specified in the `virl_lab_file` fact located in `inventory/<topology_name>/group_vars/all/virl.yml`

## Bringing up the Simulation

### Create a local CA

```bash
./play.sh local-ca.yml
```

### Build the topology

Run the `build-virl.yml` playbook to the build the out the control plane:

```bash
./play.sh build-virl.yml
```

This playbook will:

* Launch the lab in virl
* Wait until the VNFs are reachable

`--limit` can be used to build individual nodes:

```bash
./play.sh build-virl.yml --limit=site1-cedge1
```

### Configure the SD-WAN fabric

Set the name of the organization, e.g.:
```
export VMANAGE_ORG=myorgname
```

>Note: This value can be set permanently in `group_vars/all/local.yml`

Make sure that you have a serial file in this location: `licenses/serialFile.viptela` 

Run the playbook

```bash
./play.sh configure-control.yml
```

This playbook will:

* Configure setting on vmanage
* Install Enterprise CA when required
* Add vbonds and vsmarts to vmanage
* Create CSRs for vbonds and vsmarts
* Install certificates into vmanage
* Push certificates to controllers
* Import templates if present
* Import policy if present

### Deploy the SD-WAN edges

```bash
./play.sh deploy-virl.yml
```

## Clean the topology

Stops and wipes all of the nodes in the lab.

```bash
./play.sh clean-virl.yml
```

`--limit` can be used to clean individual nodes:

```bash
./play.sh clean-virl.yml --limit=site1-cedge1
```

To remove the lab completely from the VIRL server:

```bash
./play.sh clean-virl.yml --tags=destroy
```