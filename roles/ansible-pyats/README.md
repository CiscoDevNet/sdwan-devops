ansible-pyats
=========

ansible-genie is a implementation of the [pyATS](https://developer.cisco.com/pyats/) network testing framework in an
Ansible role.  It contains modules, filters, and tasks:
* Run a command and get structured output
* "snapshot" the output of a command and save it to a file
* Compare the current output of a command to a previous "snapshot"

## Modules

In addition to tasks to accomplish these things, `ansible-pyats` contains to filters:
* `pyats_parser`: provides structured data from unstructured command output
* `pyats_diff`: provides the difference between two data structures

## Requirements


* pyats
* genie

## Example Playbooks


### Run a command and retrieve the structured output
```yaml
- hosts: router
  connection: network_cli
  gather_facts: no
  roles:
    - ansible-pyats
  tasks:
    - pyats_parse_command:
        command: show ip route bgp
      register: output

    - debug:
        var: output.structured
```

### Snapshot the output of a command to a file
```yaml
- hosts: router
  connection: network_cli
  gather_facts: no
  roles:
    - ansible-pyats
  tasks:
    - include_role:
        name: ansible-pyats
        tasks_from: snapshot_command
      vars:
        command: show ip route
        file: "{{ inventory_hostname }}_routes.json"
```

#### Role Variables

* `command`: the command to run on the device
* `file`: the name of the file in which to store the command "shapshot"

### Compare the output of a command with a previous snapshot
```yaml
- hosts: router
  connection: network_cli
  gather_facts: no
  roles:
    - ansible-pyats
  tasks:
    - include_role:
        name: ansible-pyats
        tasks_from: compare_command
      vars:
        command: show ip route
        file: "{{ inventory_hostname }}_routes.json"
```

#### Role Variables

* `command`: the command to run on the device
* `file`: the name of the file in which to store the command "shapshot"

### Using the `pyats_parser` filter directly
```yaml
- hosts: router
  connection: network_cli
  gather_facts: no
  roles:
    - ansible-pyats
  tasks:
    - name: Run command
      cli_command:
        command: show ip route
      register: cli_output
    
    - name: Parsing output
      set_fact:
        parsed_output: "{{ cli_output.stdout | pyats_parser('show ip route', 'iosxe') }}"
```

### Using the `genie_diff` filter directly
```yaml
- name: Diff current and snapshot
  set_fact:
    diff_output: "{{ current_output | pyats_diff(previous_output) }}"
```

License
-------

Cisco Sample License

