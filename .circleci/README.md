# Setting up CircleCI

## Variables

See the list of possible environment variables in the follwoing table. They can be set in the project settings, or part of an organization-wide context. Without setting the **required** variables, the pipeline will fail.

> **NOTE** The default values usually come from Terraform defaults defined in the `terraform-sdwan` submodule, not as variables defined in the Ansible code. That means that the variables themselves may not be defined at all, even if the table shows they have a default value.

| Name                    | Importance  | Default value  | Recommended value      | Notes |
|-------------------------|-------------|----------------|------------------------|-------|
| IMAGE                   | optional    | ghcr.io/ciscodevnet/sdwan-devops:cloud || Docker image to use for running the Ansible playbooks, and Terraform |
| PROJ_ROOT               | required    | -              | /home/circleci/project | The directory where the repository will be checked out, may depend on the executor image |
| VAULT_PASS              | required    | -              | -                      | The clear text password for Ansible Vault, needed to decrypt the included `ansible/files/serialFile.viptela` |
| AWS_ACCESS_KEY_ID       | required    | -              | -                      | Required if deploying something on AWS |
| AWS_SECRET_ACCESS_KEY   | required    | -              | -                      | Required if deploying something on AWS |
| AWS_SESSION_TOKEN       | optional    | -              | -                      | Alternative to the above two, depending on how authentication on AWS is set up |
| GOOGLE_CREDENTIALS      | required    | -              | -                      | Contents (not the path) of a GCP service account key file in JSON format (without newline characters), for deploying a cEdge on GCP |
|GOOGLE_OAUTH_ACCESS_TOKEN| optional    | -              | -                      | Alternative to the above two, depending on how authentication on GCP is set up |
| ARM_CLIENT_ID           | optional    | -              | -                      | Required if deploying something on Azure |
| ARM_CLIENT_SECRET       | optional    | -              | -                      | Required if deploying something on Azure |
| ARM_SUBSCRIPTION_ID     | optional    | -              | -                      | Required if deploying something on Azure |
| ARM_TENANT_ID           | optional    | -              | -                      | Required if deploying something on Azure |
| CONFIG_BUILDER_METADATA | required    | -              | ../config/metadata.yaml| Configure the sdwan_config_builder |
| VPN_GW                  | optional    | -              | -                      | OpenConnect compatible VPN gateway hostname, for setting up an OpenConnect VPN (used for on-prem access) |
| VPN_USER                | optional    | -              | -                      | VPN gateway username |
| VPN_PASS                | optional    | -              | -                      | VPN gateway password |
| VPN_HOST                | optional    | -              | -                      | DC host to ping to check connectivity |

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

A [personal API token](https://app.circleci.com/settings/user/tokens) needs to be generated first, and its value stored in the `CIRCLE_TOKEN` environment variable. One can check CircleCI API access with:

    curl https://circleci.com/api/v2/me --header "Circle-Token: $CIRCLE_TOKEN"

To trigger the pipeline:

    curl -X POST https://circleci.com/api/v2/project/gh/ljakab/sdwan-devops/pipeline \
        -H "Circle-Token: $CIRCLE_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"branch":"cloud","parameters":{"deploy-infra":"aws","remove-deployment":true}}'
