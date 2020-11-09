From the root of this collection, create a symlink in your default collections path so Ansible can find this collection.

```
ln -s $(pwd) ~/.ansible/collections/ansible_collections/ripclawffb/helix_core
```

Sample playbook for testing your changes:

```
- name: Update perforce servers
  hosts: localhost
  remote_user: root
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
```
