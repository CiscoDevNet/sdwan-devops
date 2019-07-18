## Build Topology

_NOTE: The Topology requires images for vmanage, vbond, vsmart, vedge, and CSR1000v_

### Step1

Cloning the workshop repo repo:

``` shell
git clone --recursive https://github.com/ciscodevnet/ps-crn.git
```
>For more help with git, see DevNet's [A Brief Introduction to Git](https://learninglabs.cisco.com/lab/git-basic-workflows/step/1)

### Step 2

Navigate to the `ps-crn` directory.

``` shell
$ cd ps-crn/
```

>Note: All subsequent exercises will be in this directory unless otherwise noted.

### Step 3

Install requirements with pip:

```
pip install -r requirements.txt
```

Install sshpass (see [pre-requisites](../../pre-requisites.md)).

### Step 4

Deploy Topology:

Create a file named `.virlrc` in the `ps-crn` directory:
``` shell
VIRL_USERNAME=guest
VIRL_PASSWORD=guest
VIRL_HOST=your.virl.server
```

>Note: your values will be different.

Run the `build` playbook to the build the topology:
``` shell
ansible-playbook build.yml
```

>Note: The username is used in the session ID by default.  A different tag can be specified by adding `-e virl_tag=<tag name>`.

This playbook will:
* Launch the topology file
* Wait until they show as reachable in VIRL

#### Extra Vars
* `topo_name`: Set the name of the topo

```yaml
ansible-playbook build.yml -e topo_name=test1
```

### License the VNFs in the environment:
```yaml
ansible-playbook configure-licensing.yml
```