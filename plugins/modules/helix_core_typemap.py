#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Asif Shaikh (@ripclawffb) <ripclaw_ffb@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: helix_core_typemap

short_description: Manage the typemap on Perforce Helix Core

version_added: "1.1.0"

description:
    - "The typemap table associates file type modifiers with file patterns."
    - "This module manages the entire typemap table as a unit."
    - "This module supports check mode."

requirements:
    - "P4Python pip module is required"

seealso:
    - name: Helix Core Typemap
      description: "Configure file type mappings"
      link: https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_typemap.html
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
            - Determines if the typemap entries are set or cleared
            - C(present) replaces the typemap with the specified entries
            - C(absent) clears all entries from the typemap
        type: str
    typemap:
        description:
            - List of typemap entries
            - Each entry must have a C(type) and C(path) key
            - Required when state is C(present)
        type: list
        elements: dict
        suboptions:
            type:
                description:
                    - The file type to assign (e.g., binary, text+k, binary+l)
                type: str
                required: true
            path:
                description:
                    - The depot path pattern (e.g., //depot/....exe)
                type: str
                required: true

extends_documentation_fragment:
    - ripclawffb.helix_core.helix_core_connection

author:
    - Asif Shaikh (@ripclawffb)
'''

EXAMPLES = '''
# Set typemap entries
- name: Configure typemap
  ripclawffb.helix_core.helix_core_typemap:
    state: present
    typemap:
      - type: binary+l
        path: //depot/....exe
      - type: binary+l
        path: //depot/....dll
      - type: text+k
        path: //depot/....txt
    server: '1666'
    user: bruno
    charset: auto
    password: ''

# Clear all typemap entries
- name: Clear typemap
  ripclawffb.helix_core.helix_core_typemap:
    state: absent
    server: '1666'
    user: bruno
    charset: auto
    password: ''
'''

RETURN = r'''
changed:
    description: Whether any changes were made to the typemap.
    returned: always
    type: bool
    sample: true
diff:
    description: A dictionary containing 'before' and 'after' state of the resource.
    returned: when diff mode is enabled
    type: dict
    contains:
        before:
            description: The state of the resource before the action.
            type: str
        after:
            description: The state of the resource after the action.
            type: str
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ripclawffb.helix_core.plugins.module_utils.helix_core_connection import (
    helix_core_connect, helix_core_disconnect, helix_core_connection_argspec
)


def typemap_to_list(typemap_spec):
    """Convert typemap spec to a list of (type, path) tuples for comparison."""
    if 'TypeMap' not in typemap_spec or typemap_spec['TypeMap'] is None:
        return []
    entries = []
    for entry in typemap_spec['TypeMap']:
        # Each entry is a string like "binary+l //depot/....exe"
        parts = entry.split(None, 1)
        if len(parts) == 2:
            entries.append((parts[0], parts[1]))
    return entries


def list_to_typemap(entries):
    """Convert a list of dicts to typemap format."""
    return [f"{e['type']} {e['path']}" for e in entries]


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        state=dict(type='str', default='present', choices=['present', 'absent']),
        typemap=dict(type='list', elements='dict', default=None, options=dict(
            type=dict(type='str', required=True),
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
            ('state', 'present', ['typemap']),
        ]
    )

    # connect to helix
    p4 = helix_core_connect(module, 'ansible')

    try:
        # get existing typemap
        p4_typemap_spec = p4.fetch_typemap()
        current_entries = typemap_to_list(p4_typemap_spec)

        # format entries for diff
        def entries_to_diff(entries):
            return '\n'.join(f"{e[0]} {e[1]}" for e in entries) + '\n' if entries else ''

        if module.params['state'] == 'present':
            # Build desired entries list
            desired_entries = [(e['type'], e['path']) for e in module.params['typemap']]

            # Compare current vs desired
            if current_entries != desired_entries:
                before = entries_to_diff(current_entries)

                if not module.check_mode:
                    p4_typemap_spec['TypeMap'] = list_to_typemap(module.params['typemap'])
                    p4.save_typemap(p4_typemap_spec)
                result['changed'] = True

                if module._diff:
                    result['diff'] = {'before': before, 'after': entries_to_diff(desired_entries)}

        elif module.params['state'] == 'absent':
            # Clear typemap if it has entries
            if current_entries:
                before = entries_to_diff(current_entries)

                if not module.check_mode:
                    p4_typemap_spec['TypeMap'] = []
                    p4.save_typemap(p4_typemap_spec)
                result['changed'] = True

                if module._diff:
                    result['diff'] = {'before': before, 'after': ''}

    except Exception as e:
        module.fail_json(msg=f"Error: {e}", **result)

    helix_core_disconnect(module, p4)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
