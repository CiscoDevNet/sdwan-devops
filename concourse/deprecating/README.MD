IMPORTANT 
=========

There are two versions of the pipeline. One builds the SDWAN using Python3 and the other Ansible and Terraform

Most companies will already have a vault and Kubernetes Cluster setup. But if you need to set that up first, its super simple and should take a few moments.
This process is automated in a separate repo which in the future will be linked to this repo.

Pipelining makes building code from multiple repos and branches very fast and easy.

To set up vault and concourse helm,  install the helm charts for vault and concourse. Refer to readme.md file in the HELM directory to find out which lines you need to edit in these files 
to update your DNS FDQN, and change password and names of local users if you desire.

Sample helm values files are included in the HELM directory of this repo

If you are using AWS DNS, once the service is ready in kubernetes, you need to create a CNAME entry in route 53 that points to the kubernetes load balancer service.

- Use Fly to Setup your team(s) in concourse. Refer to concourse documentation on how to set up teams and local access.
- Concourse can be set up to authenticate via SSO (refer to docs)

Currently local access is setup for concourse but in the near future the goal is to use github authentication.

Setup your Teams and Access Roles in Concourse.
For example, setup a team "sdwan"
Grant Access - Typically we restrict the Owner role to Devops as this role can delete pipelines. Pipelines can instantly be recreated from the pipeline file, 
however, when you delete a pipeline you lose all your build history. Therefore, typically only  Admin Role is to a few users in DEV and NONE in QA or Prod. 
Typically pipeline files remain fairly static. Its the code they process that changes rapidly.


In the configuration in this lab, under the vault mount point:concourse/sdwan is where our code will read/write variables, config files, ssh-keys etc.
Concourse/sdwan has a policy assigned to it - see sample policy under the VAULT directory in this rep

There is a token generated from this policy called "ssh-token" which is a secret under the mount point
This gets injected into the concourse pipeline - this allows jobs in the pipeline to call out to vault,
either via CLI or the REST API from within the ephemeral build containers, and in order to read/write objects into this mount point. 

It does not have access to any other mount points in the vault.


set-pipeline
========
cd concourse
fly -t sdwan set-pipeline -c pipeline-dwan.yml -p sdwan-auto -l /Users/sconrod/dev/cisco-fso-lab-gen/params/us-west-2a.yml -v aws.region=us-west-2 -v az.name=us-west-2a -v vault.addr=http://http://vault.cisco-sdwan-labs.com:8200


To Do
=====

Have it so the AWS Creds are accessed via the pipeline via the mountpoint main not under the actual team mount
{I originally set up like this but I forgot now I have to think about it}

Add an unset for the env vars after the shell script executes


Login to Concourse CICD
===========

fly --target=sdwan login --concourse-url=http://prod-ci.devops-ontap.com:8080 -n us-west-2a --username=us-west-2a --password=
(your password will be provided over cisco chat channel)

Note: I will be integrating with git SSO so local access is interim

In the future, there may be additional environments added in - in order to migrate release candidates across environments as would
occur in the real world. This will then have a symantec release in prod of the infrastructure release, and all the vars, params, configs
will be versioned in the vault to correspond to that specific infra symantec release. This allows for rollback with versions of on all objects
consumed by the pipeline. Devs will merge to dev with no PR and build pipeline from their branch, if it passes they can create a PR and get 
their code merged into DEV which should auto-kick off the DEV pipeline. Changes should roll through to Prod once tests are incorporated.

Prep
====
Until integrated with git SSO, please generate an SSH key for your git account. Step are doc'd here:
https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

You are going to add your private key to a params file initially so that when you set pipeline, you set it passing in git ssh key -
This way it can pull and push to your branch.

You should also specify your branch name in the param file. This can eventually be transitioned to vault as well but initially, let's be
aware of what branch we are building into our pipelines by forcing this step manually. 

Set Pipeline
========
fly -t sdwan set-pipeline -c pipeline-sdwan.yml -p sdwan-auto-python -l /Users/sconrod/dev/cisco-fso-lab-gen/params/us-west-2a.yml -v aws.region=us-west-2 -v az.name=us-west-2a -v vault.addr=http://http://vault.cisco-sdwan-labs.com:8200


fly switches
======
-t target = this can be any name you like, it creates a config file locally on your machine that caches your target. You can have many targets but for 
this work we just need one for now. You could have many different targets and build many different pipelines based off different branches etc.
-c config file = this is the actual pipeline config file in yaml format

-p pipeline name = you can call your pipeline whatever you like. I prefer to call mine after the code branch for consistency

-l parameters file = because we are using local auth initially, we will pass in our SSH key for git into the pipeline via this file along with 
the git branch and the git URL of the repo. You an alternatively specify these in the tasks in the pipeline if your pipeline is working from many
different repos. Sometimes people like to not even specify the git repo here, but instead, have the build container spin up and have the code do a 
fresh git clone onto the container - using vault to pass in the git ssh key etc. 

-v variables = Right now, because there are many different labs happening in this AWS account, to keep track of stuff, I am specifying the 
region and az the lab is being deployed to so I do not get too many labs operating in the same AZ which could exhaust my AWS limits on things like
internet gateways etc. However, these are on the list to get moved into vault.

Note: these vars specified at the end of this command will be moved into vault.

fly tips
=======

get all pipelines running under your team
=====
example:

$fly -t sdwan cs

Hijack a build container before it vanishes - 3 methods:
======
Sometimes on very rare occassions its helpful to hijack a build container to debug some code.
Usually this not required since concourse prints out in detail all error messages for you.
======

fly -t $target hijack --job=pipeline/job

fly -t $target hijack -u $job_url

When running tasks, just do
fly -t $target intercept

CICD Rig Setup - This is already set up in advance - automation in progress - however steps explicitly detailed below
=======

Prep - Decide on your DNS names for vault and concourse
[]Deploy Vault - use standard vault helm chart and custom vault-values.yml file in this repo here: 
[]unseal and configure as per hashicorp standard setup procedures.
[]Create the AWS route 53 CNAME record to the LB URL generated by AWS in the LB service. $kubectl -n vault get svc
[] login into vault as root initially - create an AppRoleID and a secret for concourse. 
[] Update the concourse-values.yml file wit the vault AppRoleID and secret. Note the secret automatically is rotated every hour or as specified.
The concourse values file is located in this repo here: /Users/sconrod/dev/sdwan-devops/concourse/HELM/concourse-values.yaml
[] Update the vault URL and the concourse URL in the concourse-values.yml as well as the ci user local password. and deploy concourse. 
***Note in this lab using concourse local users but in Enterprise, Concourse will be integrated with the Corp SSO or Git SSO.****
[] Get the AWS LB service URL for concourse and create the CNAME record in AWS route 53
[] Login into concourse via CLI and set up teams. Add users to Teams with Roles. In this lab, we are giving everyone admin access to concourse so they 
can set up pipelines, modify pipelines etc.
[]Configure AWS STS for Vault using Vault IAM Policy - https://www.vaultproject.io/docs/auth/aws

Concourse can authenticate to git with integration to git. This is on the To Do List. However, right now, for it to push/pull from the repos,
it will require an SSH Key. Generate your SSH key in Git and add it to a parameters file for now. When you set pipeline, you specify the params file
that will provide the pipeline with your SSH key to push/pull from the repo. This will not be required after integration with Git.

Concourse will also need to authenticate into Dockerhub to pull the curated images and deploy the ephemeral OCI Build Containers used to build the code
For now since there is no code on our OCI images, they are public so no authentication into dockerhub is required however, it does require the location
of the images which we can specify in the params file as well.

**Important, the params file template is maintained in the repo, but the customized version since it contains your SSH key needs to be maintained
outside this repo. IF YOU PUSH AN SSH KEY TO GIT, GIT CAN DISABLE YOUR REPO*** HENCEFORTH, INTEGRATING WITH GIT IS A PRIORITY ON THE TO DO LIST

Summary
======

Things we are currently including in our params file but need to get moved to vault:
git branch - To Do move to vault
git ssh key - To Do move to vault

Idea - Developer logs into vault via cli on their mac
Developer sets pipeline using script which first will pull the SSH key from vault so this does not need to sit anywhere on their MAC
For this to work, the Developer must load vault cli onto their MAC






Considerations for the Real World
======================
In real life environments - code should only ever be deployed to a group environment such as test/dev/qa/prod via the pipeline - henceforth, 
there will be a dedicated git account that can only push to the pipelines. There should be separate auth set up so for example, it is 
impossible to accidentally config a pipeline to push code to an different environment by accident. It should be impossible for example,
for a Developer to accidentally run a pipeline build of a personal dev branch to a prod environment. 

Developers can build their branches in the pipelines and once successful, they will commit, push their PR into one of the group environments such as DEV

Setting up Concourse Team Access(Local)
===
For now, until integrated with SSO via git or other....local access is setup by Concourse Admin. When logged into
Team main as ci, run this command to create the sdwan team, then assign the local user to that team with owner role.

$fly -t sdwan set-team --team-name sdwan --local-user us-west-2a -c ./roles/owner.yml
logout of main team
test login as the user to the sdwan team

#The Developer who logs into this team will have full control over all pipelines including create and destroy pipelines.

Note for Real World:
===================
In the real world, Concourse login is integrated with Corporate SSO, usually Azure SSO, or Vault(SSO to vault via corp sso)
The user logs into a team and based on the role assigned to the user for that team they an have one of the roles assigned here:
https://concourse-ci.org/user-roles.html

Many different kinds of auth can be set up to concourse as described here:
https://concourse-ci.org/configuring-auth.html


fly -t sdwan set-pipeline -c /Users/sconrod/dev/cisco-sdwan-devops/concourse/pipeline-sdwan.yml -p sdwan-terraform -l /Users/sconrod/dev/cisco-fso-lab-gen/params/sdwan-us-west-2a.yml -v aws.region=us-west-2 -v az.name=us-west-2a -v vault.addr=http://http://vault.cisco-sdwan-labs.com:8200


