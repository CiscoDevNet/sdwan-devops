# Deploying Controllers on AWS

## Define environnement variables

With `sdwan-devops/bin` as your current folder, copy `aws_env_example.sh` to `aws_env.sh`

Edit it based on your requirements:
- profile: update with your own profile name
- region: specify the AWS region where you want to deploy your controllers. 
- org-name: make sure you put the correct org-name (very important, this cannot be changed once deployed)
- ami: you can deploy Cisco SD-WAN controllers in an AWS account using AMI images. Refer to [Deploy Cisco SD-WAN Controllers in the AWS Cloud](https://www.cisco.com/c/en/us/td/docs/routers/sdwan/configuration/sdwan-xe-gs-book/controller-aws.html) to request controllers AMIs.

Here is an example:

```
export PATH="/opt/homebrew/opt/openssl@3/bin:$PATH"

export AWS_PROFILE="ciscotme"
export AWS_REGION="eu-west-3"

export VMANAGE_AMI="ami-083e92d69763aae94"
export VBOND_AMI="ami-0ff04c1fcefbe2973"
export VSMART_AMI="ami-091a4348dbc1a39e3"

export VMANAGE_USERNAME="admin"
export VMANAGE_PASS="Cisco123#"
export SDWAN_CA_PASSPHRASE="Cisco123#"

export VIPTELA_VERSION=20.9.1
export VMANAGE_ORG=ciscotme
```

Set environnement variables
  - Set environnement variables (make sure to use source ....)
  - `source aws_env.sh`


## Create CA

Initialize
- `./install_ca.sh`

This will create a local CA in `./myCA`


## Deploy Controllers 

With sdwan-devops/bin as your current folder:

Deploy Control Plane:
- `./play.sh /ansible/day_0/build-control-plane.yml`

Finalize configuration:
- `./play.sh /ansible/day_0/config-sdwan.yml`

