# Ansible Collection - Perforce Helix Core

[![Build Status](https://travis-ci.org/ripclawffb/ansible-collection-helix-core.svg?branch=master)](https://travis-ci.org/ripclawffb/ansible-collection-helix-core)

This collection contains modules to install and configure Perforce Helix Core.

## Usage

Install the collection:

    ansible-galaxy collection install ripclawffb.helix_core -p ./collections

Then you can use the modules from the collection in your playbooks:

```yaml
---
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
        p4user: 'p4admin'
        p4passwd: 'changeme'
        p4charset: auto

    - name: Create new client
      helix_core_client:
        state: present
        name: bruno_new_client
        description: 'New client for Bruno'
        host: workstation01
        root: /tmp/bruno_new_client
        view:
          - //depot/... //bruno_new_client/depot/...
        server: '1666'
        user: bruno
        charset: auto
        password: ''

    - name: Create new user
      helix_core_user:
        state: present
        name: new_user
        email: new_user@perforce.com
        server: '1666'
        user: bruno
        charset: auto
        password: ''

    - name: Create new group
      helix_core_group:
        state: present
        name: new_group
        users:
          - new_user
        maxlocktime: '300'
        timeout: '86400'
        server: '1666'
        user: bruno
        charset: auto
        password: ''

    - name: Create a new server spec
      helix_core_server:
        state: present
        serverid: commit
        description: 'Commit server'
        services: standard
        server: '1666'
        user: bruno
        charset: auto
        password: ''

    - name: Create filtered edge server spec
      helix_core_server:
        state: present
        serverid: edge_replica
        description: 'Created by root.'
        archivedatafilter:
          - //depot1/...
          - -//depot2/...
        clientdatafilter:
          - -//workstation1/...
        revisiondatafilter:
          - //depot1/...
          - -//depot2/...
        services: edge-server
        server: '1666'
        user: bruno
        charset: auto
        password: ''

    - name: Create a new depot
      helix_core_depot:
        state: present
        depot: bruno
        type: local
        description: Bruno's depot
        p4port: '1666'
        p4user: 'bruno'
        p4passwd: ''
        p4charset: auto
      register: create_depot
```

## Author

This collection was created in 2019 by Asif Shaikh
