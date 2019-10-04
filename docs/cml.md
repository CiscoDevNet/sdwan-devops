# Cisco Modeling Labs

Both the control plane and the edge can be deployed in CML

## Dependencies

## Bringing up the Simulation

### Create a local CA

```bash
./play.sh local-ca.yml
```

### Build the topology

Run the `build-cml.yml` playbook to the build the out the control plane:

```bash
./play.sh build-cml.yml
```

This playbook will:

* Launch the lab in CML
* Wait until the VNFs are reachable

### Configure the SD-WAN fabric

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

## Clean the topology

Stops and wipes all of the nodes in the lab.

```bash
./play.sh clean-cml.yml
```

`--limit` can be used to clean individual nodes:

```bash
./play.sh clean-cml.yml --limit=site1-cedge1
```

To remove the lab completely from the VIRL server:

```bash
./play.sh clean-cml.yml --tags=destroy
```