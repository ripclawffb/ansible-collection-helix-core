#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Asif Shaikh (@ripclawffb) <ripclaw_ffb@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: helix_core_protect_info

short_description: Get the current protection table from Perforce Helix Core

version_added: "1.1.0"

description:
    - "Retrieves the current protection table entries from Perforce Helix Core."
    - "This is a read-only module that does not make any changes."

requirements:
    - "P4Python pip module is required"

seealso:
    - name: Helix Core Protect
      description: "Manage access permissions"
      link: https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_protect.html
    - name: P4Python Pip Module
      description: "Python module to interact with Helix Core"
      link: https://pypi.org/project/p4python/


extends_documentation_fragment:
    - ripclawffb.helix_core.helix_core_connection

author:
    - Asif Shaikh (@ripclawffb)
'''

EXAMPLES = '''
# Get the current protection table
- name: Get protection table
  ripclawffb.helix_core.helix_core_protect_info:
    server: '1666'
    user: bruno
    charset: auto
    password: ''
  register: protect_info

- name: Display protections
  ansible.builtin.debug:
    var: protect_info.protections
'''

RETURN = r'''
changed:
    description: Always False as this is a read-only module.
    returned: always
    type: bool
    sample: false
protections:
    description: List of protection entries found.
    returned: success
    type: list
    elements: dict
    contains:
        access:
            description: Access level (e.g., read, write, super).
            type: str
        type:
            description: Type of entity (user or group).
            type: str
        name:
            description: Name of the user or group.
            type: str
        host:
            description: Host IP address or wildcard.
            type: str
        path:
            description: Depot path for the protection entry.
            type: str
    sample:
      - access: write
        type: user
        name: "*"
        host: "*"
        path: "//..."
      - access: super
        type: user
        name: bruno
        host: "*"
        path: "//..."
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ripclawffb.helix_core.plugins.module_utils.helix_core_connection import (
    helix_core_connect, helix_core_disconnect, helix_core_connection_argspec
)


def parse_protection_entry(entry):
    """Parse a protection entry string into a dict."""
    parts = entry.split()
    if len(parts) >= 5:
        # Rejoin path in case it has spaces
        path = ' '.join(parts[4:])
        return {
            'access': parts[0],
            'type': parts[1],
            'name': parts[2],
            'host': parts[3],
            'path': path
        }
    return None


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        **helix_core_connection_argspec()
    )

    result = dict(
        changed=False,
        protections=[]
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # connect to helix
    p4 = helix_core_connect(module, 'ansible')

    try:
        # get protection table
        p4_protect_spec = p4.fetch_protect()

        if 'Protections' in p4_protect_spec and p4_protect_spec['Protections']:
            for entry in p4_protect_spec['Protections']:
                parsed = parse_protection_entry(entry)
                if parsed:
                    result['protections'].append(parsed)

    except Exception as e:
        module.fail_json(msg=f"Error: {e}", **result)

    helix_core_disconnect(module, p4)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
