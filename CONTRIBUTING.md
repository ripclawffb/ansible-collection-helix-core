To contribute to this project, you'll need access to a Perforce server for testing.

To setup your environment you'll need to run `pipenv install`, `pipenv shell`

To install a collection from a branch run:

`ansible-galaxy collection install git+https://github.com/ripclawffb/ansible-collection-helix-core.git,<branch_name>`

To run Ansible playbook, run: `ansible-playbook -i inventory playbook.yml`

Example inventory:

```
localhost-py3 ansible_host=localhost ansible_connection=local ansible_python_interpreter=/usr/bin/python3

[py3-hosts]
localhost

[py3-hosts:vars]
ansible_python_interpreter=/usr/bin/python3
```

Example test playbook you can use for testing. If developing a new module replace or add a task to use that module.

```
- hosts: all

  collections:
    - ripclawffb.helix_core

  tasks:
    - name: Set auth.id for any server id
      helix_core_configurable:
        state: present
        name: auth.id
        value: master.1
        p4port: '1666'
        p4user: ''
        p4passwd: ''
        p4charset: none
    - name: Create a new server spec
      helix_core_server:
        state: present
        description: Created by user.
        archivedatafilter:
            - //depot1/...
            - -//depot2/...
        revisiondatafilter:
            - //depot1/...
            - -//depot2/...
        serverid: edge
        services: edge-server
        type: server
        server: '1666'
        p4user: ''
        p4passwd: ''
        charset: none
    - name: Create a edge server spec
      helix_core_server:
        state: present
        description: Created by user.
        externaladdress: 127.0.0.1
        archivedatafilter:
            - //depot1/...
            - -//depot2/...
        revisiondatafilter:
            - //depot1/...
            - -//depot2/...
        serverid: edge2
        services: edge-server
        type: server
        server: '1666'
        p4user: ''
        p4passwd: ''
        charset: none
    - name: Create a new group
      helix_core_group:
        state: present
        name: xyz
        users:
            - root
        server: '1666'
        p4user: ''
        p4passwd: ''
        charset: none
```
