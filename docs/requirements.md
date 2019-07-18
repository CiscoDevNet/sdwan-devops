# Requirements

There are two sets of requirements of for this repo:

* The software dependancies required to build the simulation and use the automation
* The Viptela and ASAv licensing required to operate the simulation

Cloning the workshop repo repo:

``` shell
git clone --recursive https://github.com/ciscodevnet/ps-crn.git
```

>For more help with git, see DevNet's [A Brief Introduction to Git](https://learninglabs.cisco.com/lab/git-basic-workflows/step/1)

All operations are run out of the `ps-crn` directory:

```bash
cd ps-crn
```

## Software Dependancies

* VIRL setup with Cisco SD-WAN, ASAv, and CSR1000v images.
* [ansible-viptela](https://github.com/CiscoDevNet/ansible-viptela) (Delivered as part of the repo when `--recursive` is used when cloning)
* Python dependancies listed in requirements.txt
* sshpass

### VIRL

The ASAv and CSR1000v images are available within VIRL.  In order to add the Cisco SD-WAN images, download the qcows from software.cisco.com
and use [these](https://github.com/CiscoSE/virl-howtos) directions to add them to VIRL.

In order provide the hostname of the VIRL server and the username and password of the use, create a file named `.virlrc` in the `ps-crn` directory:

```bash
VIRL_USERNAME=guest
VIRL_PASSWORD=guest
VIRL_HOST=your.virl.server
```

### Running with Docker

The easiest way to address the python and sshpass dependacies is to use the Dockerfile packaged in the repo.  All development and testing
uses this Dockerfile, so it is the best way to garuntee that the tooling will run as designed

#### Build the Docker container

To build the docker container, run:

```bash
docker build -t ansible-viptela .
```

#### Running the the playbooks in the docker container

To run the playbooks in the docker container:

```bash
docker run -it --rm -v $PWD:/ansible --env PWD="/ansible" --env USER="$USER" ansible-viptela ansible-playbook <playbook> <options>
```

In order to make this easier, a bash script has also been provided:

```bash
./play.sh <playbook> <options>
```

## Licensing Requirements

* A Viptela license file and the Organization name associated with that license file in `licenses/serialFile.viptela`.
* The Organization name assocated with the serial file
* A Cisco Smart License token that point to an account with ASAv licensing

The easiest way to provide this information to the playbooks is to create `inventory/group_vars/all/local.yml` and specify the following:

```yaml
organization_name: "<your org name>"
license_token: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```
