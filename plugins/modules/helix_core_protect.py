#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Asif Shaikh (@ripclawffb) <ripclaw_ffb@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: helix_core_protect

short_description: This module will allow you to manage the protection table on Perforce Helix Core

description:
    - "Manage access control via the Perforce protection table."
    - "Supports two modes: 'entry' for managing individual entries, 'replace' for whole-table management."
    - "This module supports check mode."

requirements:
    - "P4Python pip module is required"

seealso:
    - name: Helix Core Protect
      description: "Manage access permissions"
      link: https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_protect.html
    - name: P4Python Pip Module
      description: "Python module to interact with Helix Core"
      link: https://pypi.org/project/p4python/


options:
    state:
        choices:
            - present
            - absent
        default: present
        description:
            - Determines if the protection entries are added or removed
            - C(present) adds entries (mode=entry) or replaces table (mode=replace)
            - C(absent) removes matching entries (mode=entry only)
        type: str
    mode:
        choices:
            - entry
            - replace
        default: entry
        description:
            - C(entry) manages individual protection entries without affecting others
            - C(replace) replaces the entire protection table with specified entries
            - Note that C(state=absent) with C(mode=replace) is not allowed for security
        type: str
    protections:
        description:
            - List of protection entries
            - Each entry must have C(access), C(type), C(name), C(host), and C(path) keys
            - Required when state is C(present)
        type: list
        elements: dict
        suboptions:
            access:
                description:
                    - The access level (list, read, open, write, admin, super, review, =read, =open, =write, =branch)
                type: str
                required: true
            type:
                description:
                    - The type of entity (user or group)
                type: str
                required: true
                choices:
                    - user
                    - group
            name:
                description:
                    - The user or group name, or * for all
                type: str
                required: true
            host:
                description:
                    - The host IP/pattern, or * for any host
                type: str
                required: true
            path:
                description:
                    - The depot path pattern (e.g., //..., //depot/...)
                type: str
                required: true
    server:
        description:
            - The hostname/ip and port of the server (perforce:1666)
            - Can also use 'P4PORT' environment variable
        required: true
        type: str
        aliases:
            - p4port
    user:
        description:
            - A user with super user access
            - Can also use 'P4USER' environment variable
        required: true
        type: str
        aliases:
            - p4user
    password:
        description:
            - The super user password
            - Can also use 'P4PASSWD' environment variable
        required: true
        type: str
        aliases:
            - p4passwd
    charset:
        default: none
        description:
            - Character set used for translation of unicode files
            - Can also use 'P4CHARSET' environment variable
        required: false
        type: str
        aliases:
            - p4charset

author:
    - Asif Shaikh (@ripclawffb)
'''

EXAMPLES = '''
# Add individual protection entries (default mode)
- name: Add developer access
  ripclawffb.helix_core.helix_core_protect:
    state: present
    protections:
      - access: write
        type: group
        name: developers
        host: "*"
        path: //depot/...
    server: '1666'
    user: bruno
    charset: auto
    password: ''

# Remove specific protection entries
- name: Remove contractor access
  ripclawffb.helix_core.helix_core_protect:
    state: absent
    protections:
      - access: read
        type: group
        name: contractors
        host: "*"
        path: //depot/...
    server: '1666'
    user: bruno
    charset: auto
    password: ''

# Replace entire protection table
- name: Set complete protection table
  ripclawffb.helix_core.helix_core_protect:
    state: present
    mode: replace
    protections:
      - access: super
        type: user
        name: admin
        host: "*"
        path: //...
      - access: write
        type: group
        name: developers
        host: "*"
        path: //depot/...
    server: '1666'
    user: bruno
    charset: auto
    password: ''
'''

RETURN = r'''
changed:
    description: Whether any changes were made to the protection table.
    returned: always
    type: bool
    sample: true
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ripclawffb.helix_core.plugins.module_utils.helix_core_connection import (
    helix_core_connect, helix_core_disconnect, helix_core_connection_argspec
)


def protections_to_set(protect_spec):
    """Convert protection spec to a set of tuples for comparison."""
    if 'Protections' not in protect_spec or protect_spec['Protections'] is None:
        return set()
    entries = set()
    for entry in protect_spec['Protections']:
        # Each entry is a string like "access type name host path"
        parts = entry.split()
        if len(parts) >= 5:
            # Rejoin path in case it has spaces (though unusual)
            path = ' '.join(parts[4:])
            entries.add((parts[0], parts[1], parts[2], parts[3], path))
    return entries


def set_to_protections(entries):
    """Convert a set/list of tuples to protection format."""
    return ["{0} {1} {2} {3} {4}".format(e[0], e[1], e[2], e[3], e[4]) for e in entries]


def entry_to_tuple(entry):
    """Convert a dict entry to a tuple for comparison."""
    return (entry['access'], entry['type'], entry['name'], entry['host'], entry['path'])


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        state=dict(type='str', default='present', choices=['present', 'absent']),
        mode=dict(type='str', default='entry', choices=['entry', 'replace']),
        protections=dict(type='list', elements='dict', default=None, options=dict(
            access=dict(type='str', required=True),
            type=dict(type='str', required=True, choices=['user', 'group']),
            name=dict(type='str', required=True),
            host=dict(type='str', required=True),
            path=dict(type='str', required=True),
        )),
        **helix_core_connection_argspec()
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[
            ('state', 'present', ['protections']),
        ]
    )

    # Security check: block clearing entire table
    if module.params['state'] == 'absent' and module.params['mode'] == 'replace':
        module.fail_json(
            msg="Clearing the entire protection table is not allowed for security reasons. "
                "Use mode='entry' to remove specific entries, or mode='replace' with state='present' "
                "to replace the table with a new set of entries.",
            **result
        )

    # Validate protections required for absent with entry mode
    if module.params['state'] == 'absent' and module.params['mode'] == 'entry':
        if not module.params['protections']:
            module.fail_json(
                msg="protections is required when state=absent and mode=entry",
                **result
            )

    # connect to helix
    p4 = helix_core_connect(module, 'ansible')

    try:
        # get existing protection table
        p4_protect_spec = p4.fetch_protect()
        current_entries = protections_to_set(p4_protect_spec)

        if module.params['mode'] == 'entry':
            # Entry mode: add/remove individual entries
            desired_tuples = {entry_to_tuple(e) for e in module.params['protections']}

            if module.params['state'] == 'present':
                # Add entries that don't exist
                new_entries = desired_tuples - current_entries
                if new_entries:
                    if not module.check_mode:
                        updated_entries = current_entries | desired_tuples
                        p4_protect_spec['Protections'] = set_to_protections(updated_entries)
                        p4.save_protect(p4_protect_spec)
                    result['changed'] = True

            elif module.params['state'] == 'absent':
                # Remove entries that exist
                entries_to_remove = desired_tuples & current_entries
                if entries_to_remove:
                    if not module.check_mode:
                        updated_entries = current_entries - desired_tuples
                        p4_protect_spec['Protections'] = set_to_protections(updated_entries)
                        p4.save_protect(p4_protect_spec)
                    result['changed'] = True

        elif module.params['mode'] == 'replace':
            # Replace mode: replace entire table
            desired_tuples = {entry_to_tuple(e) for e in module.params['protections']}

            if current_entries != desired_tuples:
                if not module.check_mode:
                    p4_protect_spec['Protections'] = set_to_protections(desired_tuples)
                    p4.save_protect(p4_protect_spec)
                result['changed'] = True

    except Exception as e:
        module.fail_json(msg="Error: {0}".format(e), **result)

    helix_core_disconnect(module, p4)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
