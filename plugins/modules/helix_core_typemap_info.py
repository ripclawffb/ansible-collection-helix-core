#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Asif Shaikh (@ripclawffb) <ripclaw_ffb@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: helix_core_typemap_info

short_description: Get the current typemap from Perforce Helix Core

version_added: "1.1.0"

description:
    - "Retrieves the current typemap entries from Perforce Helix Core."
    - "This is a read-only module that does not make any changes."

requirements:
    - "P4Python pip module is required"

seealso:
    - name: Helix Core Typemap
      description: "Configure file type mappings"
      link: https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_typemap.html
    - name: P4Python Pip Module
      description: "Python module to interact with Helix Core"
      link: https://pypi.org/project/p4python/


extends_documentation_fragment:
    - ripclawffb.helix_core.helix_core_connection

author:
    - Asif Shaikh (@ripclawffb)
'''

EXAMPLES = '''
# Get the current typemap
- name: Get typemap
  ripclawffb.helix_core.helix_core_typemap_info:
    server: '1666'
    user: bruno
    charset: auto
    password: ''
  register: typemap_info

- name: Display typemap entries
  ansible.builtin.debug:
    var: typemap_info.typemap
'''

RETURN = r'''
changed:
    description: Always False as this is a read-only module.
    returned: always
    type: bool
    sample: false
typemap:
    description: List of typemap entries.
    returned: success
    type: list
    elements: dict
    contains:
        type:
            description: The file type (e.g., binary+l, text+k).
            type: str
        path:
            description: The depot path pattern (e.g., //depot/....exe).
            type: str
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ripclawffb.helix_core.plugins.module_utils._helix_core_connection import (
    helix_core_connect, helix_core_disconnect, helix_core_connection_argspec
)


def parse_typemap_entry(entry):
    """Parse a typemap entry string into a dict."""
    parts = entry.split(None, 1)
    if len(parts) == 2:
        return {
            'type': parts[0],
            'path': parts[1]
        }
    return None


def run_module():
    module_args = dict(
        **helix_core_connection_argspec()
    )

    result = dict(
        changed=False,
        typemap=[]
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    p4 = helix_core_connect(module, 'ansible')

    try:
        p4_typemap_spec = p4.fetch_typemap()

        if 'TypeMap' in p4_typemap_spec and p4_typemap_spec['TypeMap']:
            for entry in p4_typemap_spec['TypeMap']:
                parsed = parse_typemap_entry(entry)
                if parsed:
                    result['typemap'].append(parsed)

    except Exception as e:
        module.fail_json(msg=f"Error: {e}", **result)

    helix_core_disconnect(module, p4)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
