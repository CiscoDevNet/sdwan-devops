Logon to Concourse
==================
$fly --target=cisco-sdwan-labs login --concourse-url=http://ci.cisco-sdwan-labs.com:8080 -n main --username= --password=

If you do not specify a password at the command line, it will automatically open your default browser - after authenticating
it will provide you with a token to paste into command line.

Set pipeline (you only need to do this part once unless you want to change the pipeline setup)
=========
$fly -t cisco-sdwan-labs set-pipeline -c sdwan-pipeline-python.yml -p sdwan-python -l [your params file].yml
The params file contains your git account SSH key and you can also specify the branch you want to build from
or you can also specify this in your tasks file(recommended). There is a params template file in this dir.

