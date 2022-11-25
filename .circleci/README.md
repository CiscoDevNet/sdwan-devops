# Setting up CircleCI

## Variables

See the list of possible environment variables in the follwoing table. They can be set in the project settings, or part of an organization-wide context. Without setting the **required** variables, the pipeline will fail.

> **NOTE** The default values usually come from Terraform defaults defined in the `terraform-sdwan` submodule, not as variables defined in the Ansible code. That means that the variables themselves may not be defined at all, even if the table shows they have a default value.

| Name                    | Importance  | Default value  | Recommended value      | Notes |
|-------------------------|-------------|----------------|------------------------|-------|
| IMAGE                   | optional    | ghcr.io/ciscodevnet/sdwan-devops:cloud || Docker image to use for running the Ansible playbooks, and Terraform |
| SDWAN_CONTROL_INFRA     | optional    | aws            | -                      | This environment variable can also be set as a pipeline parameter, when triggered by the API |
| PROJ_ROOT               | required    | -              | /home/circleci/project | The directory where the repository will be checked out, may depend on the executor image |
| SDWAN_CA_PASSPHRASE     | required    | -              | -                      | |
| AWS_ACCESS_KEY_ID       | required    | -              | -                      | Only required if SDWAN_CONTROL_INFRA is aws |
| AWS_SECRET_ACCESS_KEY   | required    | -              | -                      | Only required if SDWAN_CONTROL_INFRA is aws |
| AWS_SESSION_TOKEN       | optional    | -              | -                      | Depends on how authentication on AS is set up |
| AWS_REGION              | optional    | -              | -                      | |
| SDWAN_DATACENTER        | required    | us-east-1      | -                      | Should be the same as AWS_REGION (if set) if SDWAN_CONTROL_INFRA is aws |
| DNS_DOMAIN              | optional    | -              | -                      | If set, A records for control plane elements will be added to the AWS Route 53 zone with the same name (which should be pre-configured) |
| ACL_RANGES_IPV4_BASE64  | recommended | "0.0.0.0/0"    | -                      | Only allow connections to TCP ports 22, 443, and 8443 from these IPv4 ranges. The format is a list of CIDR ranges, double quoted, separated by commas, and finally the whole string base64 encoded
| ACL_RANGES_IPV6_BASE64  | recommended | "::/0"         | -                      | Only allow connections to TCP ports 22, 443, and 8443 from these IPv6 ranges. The format is a list of CIDR ranges, double quoted, separated by commas, and finally the whole string base64 encoded
| NETWORK_CIDR            | required    | 10.128.0.0/22  | 10.128.0.0/22          | Properly handling IP addressing is still a work in progress, please use the recommended values for now |
| VMANAGE1_IP             | required    | 10.128.1.11/24 | 10.128.1.11/24         | Properly handling IP addressing is still a work in progress, please use the recommended values for now |
| VBOND1_IP               | required    | 10.128.1.12/24 | 10.128.1.12/24         | Properly handling IP addressing is still a work in progress, please use the recommended values for now |
| VSMART1_IP              | required    | 10.128.1.13/24 | 10.128.1.13/24         | Properly handling IP addressing is still a work in progress, please use the recommended values for now |
| VPN0_GATEWAY            | required    | 10.128.1.1     | 10.1281.1.1            | Properly handling IP addressing is still a work in progress, please use the recommended values for now |
| HQ_EDGE1_RANGE          | required    | -              | 10.128.4.0/23          | Properly handling IP addressing is still a work in progress, please use the recommended values for now |
| SSH_PUBKEY_BASE64       | recommended | -              | -                      | Not strictly required, but recommended for SSH login into `devbox` and SD-WAN VMs |
| SSH_PUBKEY_FP_BASE64    | recommended | -              | -                      | Used for adding SSH public key fingerprints to cEdges. It will only work with ssh-rsa type keys |
| VIPTELA_VERSION         | required    | -              | -                      | Used to choose device template (v19 or v20), and may be used in the future to auto-detect AMIs or VMware templates with standardized naming |
| CLOUDINIT_TYPE          | required    | -              | v2                     | Depends on SD_WAN version, `v1` up to 20.4.x, `v2` for later |
| VMANAGE_AMI             | required    | -              | -                      | Should be an existing AMI in the selected AWS region |
| VBOND_AMI               | required    | -              | -                      | Should be an existing AMI in the selected AWS region |
| VSMART_AMI              | required    | -              | -                      | Should be an existing AMI in the selected AWS region |
| VMANAGE_INSTANCE_TYPE   | recommended | t2.2xlarge     | t2.xlarge              | For now, only `t2` instance types are supported. `t2.xlarge` is the smallest that will allow vManage to start |
| VBOND_INSTANCE_TYPE     | optional    | t2.medium      | -                      | Not tested, but instance types othee than `t2` should be supported |
| VSMART_INSTANCE_TYPE    | optional    | t2.medium      | -                      | Not tested, but instance types othee than `t2` should be supported |
| VMANAGE_USERNAME        | required    | admin          | admin                  | It's good to have an `admin` user as some scripts may have it hardcoded or expected |
| VMANAGE_PASS            | required    | -              | -                      | The clear text password for vManage, needed for API access |
| VMANAGE_ENCRYPTED_PASS  | required    | -              | -                      | The SHA256 hashed password for vManage, needed for `user-data`. Can be obtained with `echo "$VMANAGE_PASS" | openssl passwd -6 -stdin` |
| VMANAGE_ORG             | required    | -              | CIDR_SDWAN_WORKSHOPS   | The recommended value is needed if you want to use the included `ansible/files/serialFile.viptela` (it must match the org in the `serialFile.viptela` being used) |
| VAULT_PASS              | required    | -              | -                      | The clear text password for Ansible Vault, needed to decrypt the included `ansible/files/serialFile.viptela` |

### External pipeline

| Name                       | Importance  | Notes |
|----------------------------|-------------|-------|
| CIRCLE_TOKEN               | required    | A CircleCI personal access token with rights to trigger the external pipeline |
| EXTERNAL_PIPELINE_REPOUSER | required    | The organization or username of the repository for the external pipeline |
| EXTERNAL_PIPELINE_REPONAME | required    | The external pipline repository name |
| EXTERNAL_PIPELINE_BRANCH   | required    | The Git branch on the external pipeline repository |

## Pipeline parameters

The pipeline accepts the following parameters (can be set with an API trigger, see below):

- `deploy-infra` -- the default value is `aws`, and it is the only one that works for now, but `vmware` and `azure` may come in the future
- `remove-deployment` -- whether or not to remove all resources created in AWS after a successful run (for unsuccessful runs they are removed regardless of the value of this variable). The default value is `true`. Set to `false` if you want to use the pipeline to create an SD-WAN deployment that you need to keep after the pipeline finishes. It will need to be cleaned up manually
- `wait-for-external-pipeline` -- we trigger an external pipeline (see variables above for definition) which in turn will run API calls against the deployment. This parameter controls how long we wait before initiating destruction of resources (unless `remove-deployment` is set to `false`). Default is 180 seconds

## Manual trigger

A [personal API token](https://app.circleci.com/settings/user/tokens) needs to be generated first, and its value stored in the `CIRCLE_TOKEN` environment variable. Using cURL:

    curl -X POST https://circleci.com/api/v2/project/gh/ljakab/sdwan-devops/pipeline \
        -H "Circle-Token: $CIRCLE_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"branch":"circleci","parameters":{"deploy-infra":"aws","remove-deployment":true}}'
