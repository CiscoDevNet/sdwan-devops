# Building a CI pipeline with GitLab

The steps below will build out a CI pipeline for SD-WAN using GitLab.  These instructions assume that you are already able to run all the playbooks manually to build out the topology and configure the SD-WAN.  If you have not done that first, go back and make sure that the playbooks run successfully before trying them in GitLab CI.  

## Setup

1. Clone the repo.
    ```
    git clone https://github.com/CiscoDevNet/sdwan-devops.git
    ```

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

1. Set the version of IOS-XE image to use for edge devices.
    ```
    export IOSXE_SDWAN_IMAGE=iosxe-sdwan-16.12.2r
    ```

1. Set the version of CSR1000v image to use for underlay devices.
    ```
    export CSR1000V_IMAGE=csr1000v-170301
    ```

1. And finally, set the version of control plane to use.
    ```
    export VIPTELA_VERSION=19.2.1
    ```

>Note: This value gets appended to the image name (e.g. viptela-manage, viptela-smart, etc.) so make sure these names line up with the image definitions you have in CML.

1. Log into your GitLab instance and create a GITLAB_API_TOKEN
   - In the upper left of console, click on the symbol for your account and then Settings
   - In the left menu, click on "Access Tokens"
   - Provide a token name, expiration, the api scope, click "Create personal access token", and save the generated TOKEN for the next step

1.  Export the following variables to match your environment.
    ```
    export GITLAB_HOST=https://gitlab.example.com
    export GITLAB_USER=
    export GITLAB_API_TOKEN=
    export GITLAB_PROJECT=sdwan-devops
    ```

## Create a CI pipeline in GitLab

1. Create the GitLab project and CI/CD variables.
    ```
    extras/create-gitlab-project.sh
    ```

1. Remove the old origin, add new origin and push to GitLab.
    ```
    git remote remove origin
    git remote add origin $GITLAB_HOST/$GITLAB_USER/$GITLAB_PROJECT.git
    git config http.version HTTP/1.1
    ```

1. Commit your license file to the repo.
    ```
    git add -f licenses/serialFile.viptela
    git commit -m "Adding license file"
    ```

1. Push the repo to GitLab.
    ```
    git push --set-upstream origin master
    ```

    >Note: enter your GitLab credentials if asked

1. From the GitLab web UI, navigate to the CI/CD -> Pipelines page for the project. You should see a pipeline currently active since we committed the model-driven-devops code and we had a `.gitlab-ci.yml` file present. If that file is present, GitLab will automatically try to execute the CI pipeline defined inside.

1. Use the graphical representation of the pipeline to click through the console output of the various stages. The entire pipeline will take approximately ~8 minutes to complete. Wait until it completes to go onto the next step.

## Cleanup
1. Remove project from GitLab.
    ```
    extras/delete-gitlab-project.sh
    ```

1. Delete lab from CML.
    ```
    ./play.sh clean-virl.yml --tags "delete"
    ```
