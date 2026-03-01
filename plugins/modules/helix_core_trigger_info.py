#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Asif Shaikh (@ripclawffb) <ripclaw_ffb@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: helix_core_trigger_info

short_description: Get the current trigger table from Perforce Helix Core

version_added: "1.2.0"

description:
    - "Retrieves the current trigger table entries from Perforce Helix Core."
    - "This is a read-only module that does not make any changes."

requirements:
    - "P4Python pip module is required"

seealso:
    - name: Helix Core Triggers
      description: "Configure trigger definitions"
      link: https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_triggers.html
    - name: P4Python Pip Module
      description: "Python module to interact with Helix Core"
      link: https://pypi.org/project/p4python/


extends_documentation_fragment:
    - ripclawffb.helix_core.helix_core_connection

author:
    - Asif Shaikh (@ripclawffb)
'''

EXAMPLES = '''
# Get the current trigger table
- name: Get trigger table
  ripclawffb.helix_core.helix_core_trigger_info:
    server: '1666'
    user: bruno
    charset: auto
    password: ''
  register: trigger_info

- name: Display triggers
  ansible.builtin.debug:
    var: trigger_info.triggers
'''

RETURN = r'''
changed:
    description: Always False as this is a read-only module.
    returned: always
    type: bool
    sample: false
triggers:
    description: List of trigger entries.
    returned: success
    type: list
    elements: dict
    contains:
        name:
            description: The trigger name.
            type: str
        type:
            description: The trigger type.
            type: str
        path:
            description: The depot path pattern or form type.
            type: str
        command:
            description: The command to execute.
            type: str
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ripclawffb.helix_core.plugins.module_utils._helix_core_connection import (
    helix_core_connect, helix_core_disconnect, helix_core_connection_argspec
)


def parse_trigger_entry(entry):
    """Parse a trigger entry string into a dict."""
    parts = entry.split(None, 3)
    if len(parts) >= 4:
        command = parts[3]
        if command.startswith('"') and command.endswith('"'):
            command = command[1:-1]
        return {
            'name': parts[0],
            'type': parts[1],
            'path': parts[2],
            'command': command
        }
    elif len(parts) == 3:
        return {
            'name': parts[0],
            'type': parts[1],
            'path': parts[2],
            'command': ''
        }
    return None


def run_module():
    module_args = dict(
        **helix_core_connection_argspec()
    )

    result = dict(
        changed=False,
        triggers=[]
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    p4 = helix_core_connect(module, 'ansible')

    try:
        p4_triggers_spec = p4.fetch_triggers()

        if 'Triggers' in p4_triggers_spec and p4_triggers_spec['Triggers']:
            for entry in p4_triggers_spec['Triggers']:
                parsed = parse_trigger_entry(entry)
                if parsed:
                    result['triggers'].append(parsed)

    except Exception as e:
        module.fail_json(msg=f"Error: {e}", **result)

    helix_core_disconnect(module, p4)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
