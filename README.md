# Ansible Collection - Perforce Helix

[![Build Status](https://travis-ci.org/ripclawffb/ansible-collection-helix.svg?branch=master)](https://travis-ci.org/ripclawffb/ansible-collection-helix)

This collection contains modules to install and configure Perforce Helix Core.

## Usage

Install the collection:

    ansible-galaxy collection install ripclawffb.helix -p ./collections

Then you can use the modules from the collection in your playbooks:

```yaml
---
- hosts: all

    collections:
    - ripclawffb.helix

    tasks:
    - name: Set auth.id for any server id
        helix_configurable:
        state: present
        name: auth.id
        value: master.1
        p4port: '1666'
        p4user: 'p4admin'
        p4passwd: 'changeme'
        p4charset: auto
        register: auth_set_configurable
        delegate_to: localhost
```

## Author

This collection was created in 2019 by Asif Shaikh
