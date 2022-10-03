To set pipeline
===========

This pipeline takes your docker file and generates and OCI complian build container to be used in the concourse pipelines for sdwan
From time to time, we add new tools or upgrade our OCI Build containers. This is rare actually, but its important to bump the version
When you bump the version of your OCI container to docker, you can then bump the image tag version in the pipleine and build pipeline to ensure there are no issues
with a new revision of your build container.

Note: You can just retain all of the vars in the vault if you like. I am passing via params file.

Example
======

fly -t <target name> set-pipeline -c <pipeline config file> -p <name of your pipeline> -l ~./<this is the full path to your params file which needs to be kept outside repo>.yml
fly -t sdwan set-pipeline -c /Users/sconrod/dev/cisco/sdwan-devops/concourse/OCI-Docker-Builds/python-aws/python-aws-build-docker-pipeline.yml -p oci-python-aws -l /Users/sconrod/dev/cisco-fso-lab-gen/params/Docker.yml
