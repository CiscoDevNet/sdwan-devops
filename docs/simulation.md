# PS-CRN Simulation

This is Simulation compentent of the [Public Sector Cloud Read Network](crn_overview.md) DevOps bundle.  It consists of
a dynamically generated VIRL topology and the automation tooling to completely configre it.

## Topology

![Alt Text](images/virl_topology.png)

> The default username/password for network devices is `admin/admin`

> The default username/password for the control and test nodes is `virl/admin`

*See the [requirements](requirements.md) for running these playbooks first!*

## Bringing up the Simulation

### Deploy the topology

Run the `build` playbook to the build the topology:

```bash
ansible-playbook build.yml
```

This playbook will:

* Launch the topology file
* Wait until they show as reachable in VIRL

> **Extra Vars**
>
> * `virl_tag`: Set the tag used for the topology (Default: username)
> 
> ```bash
> ansible-playbook build.yml -e virl_tag=test1
> ```

### License the VNFs in the environment

```bash
ansible-playbook configure-licensing.yml
```

### Configure the SD-WAN fabric

```bash
ansible-playbook configure.yml
```

> **Extra Vars**
>
> * `CA`: only create the private CA
> * `control`: only provision the Viptela control plane
> * `vedge`: only provision the Viptela vEdges
> * `check_control`: check connectivity of the control plane
> * `check_edge`: check connectivity of the edge
> * `check_all`: check full connectivity of the overlay

### Wait for the vEdges to sync:

```shell
ansible-playbook waitfor-sync.yml
```

### Import templates

```shell
ansible-playbook import-templates.yml
```

> **Extra Vars**
>
> * `vmanage_ip`
>
> To specify the IP address of the vManage server into which to import the templates:
>
> ```bash
> ansible-playbook import-templates.yml -e vmanage_ip=1.2.3.4
> ```

### Attach templates to devices

```bash
ansible-playbook attach_templates.yml
```

> To attach a template to a limited set of devices:
>
> ```bash
> ansible-playbook attach_templates.yml --limit=east-rtr1,west-rtr1
> ```

### Import Policy

```shell
ansible-playbook import-policy.yml
```

> **Extra Vars**
>
> * `vmanage_ip`
>
> To specify the IP address of the vManage server into which to import the templates:
>
> ```bash
> ansible-playbook import-policy.yml -e vmanage_ip=1.2.3.4
> ```

### Activate Central Policy

```bash
ansible-playbook activate-central-policy.yml
```

## Other Operations

### Export templates

```bash
ansible-playbook export-templates.yml
```

> **Extra Vars**
>
> * `vmanage_ip`
>
> To specify the IP address of the vManage server from which to export the templates:
> 
> ```bash
> ansible-playbook export-temapltes.yml -e vmanage_ip=1.2.3.4
> ```

### Detach templates from devices
```yaml
ansible-playbook detach_templates.yml
```

## Clean the topology

```bash
ansible-playbook clean.yml
```
