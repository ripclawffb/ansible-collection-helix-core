# Ansible Collection - Perforce Helix Core

[![Build Status](https://github.com/ripclawffb/ansible-collection-helix-core/actions/workflows/github-actions-ansible.yml/badge.svg)](https://github.com/ripclawffb/ansible-collection-helix-core/actions/workflows/github-actions-ansible.yml)
[![Ansible Galaxy](https://img.shields.io/badge/ansible--galaxy-ripclawffb.helix__core-blue.svg)](https://galaxy.ansible.com/ui/repo/published/ripclawffb/helix_core/)
[![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)

This collection contains Ansible modules to install and configure Perforce Helix Core.

[Documentation](https://ripclawffb.github.io/ansible-collection-helix-core/) | [Issue Tracker](https://github.com/ripclawffb/ansible-collection-helix-core/issues) | [Galaxy Page](https://galaxy.ansible.com/ui/repo/published/ripclawffb/helix_core/)

## Requirements

- **Ansible**: 2.9+
- **Python**: 3.6+
- **P4Python**: The `p4python` pip package must be installed on the target host.

## Compatibility

This collection is tested via Molecule on the following platforms and Perforce versions:

| OS | Perforce Versions |
|----|-------------------|
| Rocky Linux 9 | 23.1, 23.2, 24.1, 24.2 |
| Ubuntu 20.04 | 23.1, 23.2 |
| Ubuntu 22.04 | 23.1, 23.2, 24.1, 24.2 |
| Ubuntu 24.04 | 23.1, 23.2, 24.1, 24.2 |

## Included Modules

| Module | Description |
|--------|-------------|
| `helix_core_client` | Manage clients/workspaces |
| `helix_core_configurable` | Manage server configurables |
| `helix_core_depot` | Manage depots |
| `helix_core_group` | Manage user groups |
| `helix_core_ldap` | Manage LDAP configurations |
| `helix_core_protect` | Manage protections table |
| `helix_core_protect_info` | Get protection table info |
| `helix_core_server` | Manage server specifications |
| `helix_core_stream` | Manage streams |
| `helix_core_trigger` | Manage triggers table |
| `helix_core_typemap` | Manage typemap table |
| `helix_core_user` | Manage users |

## Installation

### Ansible Galaxy

```bash
ansible-galaxy collection install ripclawffb.helix_core
```

### requirements.yml

```yaml
collections:
  - name: ripclawffb.helix_core
```

## Usage

Example playbook:

```yaml
---
- hosts: all
  collections:
    - ripclawffb.helix_core

  tasks:
    - name: Create a new depot
      helix_core_depot:
        state: present
        depot: projects
        type: local
        description: "Main projects depot"
        server: '1666'
        user: 'p4admin'
        password: 'changeme'

    - name: Create a user
      helix_core_user:
        state: present
        name: jdoe
        email: jdoe@example.com
        fullname: "John Doe"
        server: '1666'
        user: 'p4admin'
        password: 'changeme'
```

See the [Documentation](https://ripclawffb.github.io/ansible-collection-helix-core/) for detailed usage and examples for every module.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## License

MIT
