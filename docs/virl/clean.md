## Clean the topology

### Step 1

Now that we are done with the workshop, let's clean up the environment:

```shell
ansible-playbook clean.yml
```

This playbook will:
* De-register hosts from Smart Licensing
* Remove topology devices from the `known_hosts` file
* Remove the `myCA` directory
* Destroy the topology specified in `.virl/default/id`