#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Asif Shaikh (@ripclawffb) <ripclaw_ffb@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: helix_core_configurable_info

short_description: Get configurable settings from Perforce Helix Core

version_added: "1.1.0"

description:
    - "Retrieves configurable settings from Perforce Helix Core."
    - "When C(name) is provided, returns the value of a specific configurable."
    - "When C(name) is omitted, returns all configurable settings."
    - "This is a read-only module that does not make any changes."

requirements:
    - "P4Python pip module is required"

seealso:
    - name: Helix Core Configurables
      description: "List of supported configurables"
      link: https://www.perforce.com/manuals/cmdref/Content/CmdRef/appendix.configurables.html
    - name: P4Python Pip Module
      description: "Python module to interact with Helix Core"
      link: https://pypi.org/project/p4python/


options:
    name:
        description:
            - The name of the configurable to retrieve.
            - If omitted, all configurables are returned.
        required: false
        type: str
    serverid:
        description:
            - The server ID to filter configurables by.
            - Defaults to C(any) which shows all server IDs.
        default: any
        required: false
        type: str

extends_documentation_fragment:
    - ripclawffb.helix_core.helix_core_connection

author:
    - Asif Shaikh (@ripclawffb)
'''

EXAMPLES = '''
# Get a specific configurable
- name: Get auth.id configurable
  ripclawffb.helix_core.helix_core_configurable_info:
    name: auth.id
    server: '1666'
    user: bruno
    charset: auto
    password: ''
  register: config_info

# Get all configurables
- name: Get all configurables
  ripclawffb.helix_core.helix_core_configurable_info:
    server: '1666'
    user: bruno
    charset: auto
    password: ''
  register: all_configs

# Get configurables for a specific server
- name: Get configurables for master.1
  ripclawffb.helix_core.helix_core_configurable_info:
    serverid: master.1
    server: '1666'
    user: bruno
    charset: auto
    password: ''
  register: server_configs
'''

RETURN = r'''
changed:
    description: Always False as this is a read-only module.
    returned: always
    type: bool
    sample: false
info:
    description:
        - When C(name) is provided, a list of matching configurable entries.
        - When C(name) is omitted, a list of all configurable entries.
        - Each entry contains Name, Value, and ServerName.
    returned: success
    type: list
    elements: dict
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ripclawffb.helix_core.plugins.module_utils._helix_core_connection import (
    helix_core_connect, helix_core_disconnect, helix_core_connection_argspec
)


def run_module():
    module_args = dict(
        name=dict(type='str', required=False, default=None),
        serverid=dict(type='str', default='any'),
        **helix_core_connection_argspec()
    )

    result = dict(
        changed=False,
        info=[]
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    p4 = helix_core_connect(module, 'ansible')

    try:
        p4_configs = p4.run('configure', 'show', 'allservers')

        configs = []
        for config in p4_configs:
            # Filter by serverid if not 'any'
            if module.params['serverid'] != 'any':
                if config.get('ServerName') != module.params['serverid']:
                    continue

            # Filter by name if provided
            if module.params['name']:
                if config.get('Name') != module.params['name']:
                    continue

            configs.append(config)

        result['info'] = configs

    except Exception as e:
        module.fail_json(msg=f"Error: {e}", **result)

    helix_core_disconnect(module, p4)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
