#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Asif Shaikh (@ripclawffb) <ripclaw_ffb@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: helix_core_configurable

short_description: This module will allow you to set config options on Perforce Helix Core

description:
    - "Configurables allow you to customize a Perforce service. Configurable settings might affect the server, the client, or a proxy."
    - "This module supports check mode."

requirements:
    - "P4Python pip module is required. Tested with 2018.2.1743033"

seealso:
    - name: Helix Core Configurables
      description: "List of supported configurables"
      link: https://www.perforce.com/manuals/cmdref/Content/CmdRef/appendix.configurables.html
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
            - Determines if the configurable is set or removed
        type: str
    name:
        description:
            - The name of the configurable that needs to be set
        required: true
        type: str
    value:
        description:
            - The value of named configurable
        required: true
        type: str
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
    serverid:
        default: any
        description:
            - The server ID of the helix server
        required: false
        type: str

author:
    - Asif Shaikh (@ripclawffb)
'''

EXAMPLES = '''
# Set auth.id configurable for any server
- name: Set auth.id
  helix_core_configurable:
    state: present
    name: auth.id
    value: master.1
    server: '1666'
    user: bruno
    charset: none
    password: ''

# Unset auth.id configurable for specific server
- name: Unset auth.id
  helix_core_configurable:
    state: absent
    name: auth.id
    value: master.1
    serverid: master.1
    server: '1666'
    user: bruno
    password: ''
    charset: auto
'''

RETURN = r''' # '''


from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible_collections.ripclawffb.helix_core.plugins.module_utils.helix_core_connection import helix_core_connect, helix_core_disconnect


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        state=dict(type='str', default='present', choices=['present', 'absent']),
        name=dict(type='str', required=True),
        value=dict(type='str', required=True),
        server=dict(type='str', required=True, aliases=['p4port'], fallback=(env_fallback, ['P4PORT'])),
        user=dict(type='str', required=True, aliases=['p4user'], fallback=(env_fallback, ['P4USER'])),
        password=dict(type='str', required=True, aliases=['p4passwd'], fallback=(env_fallback, ['P4PASSWD']), no_log=True),
        charset=dict(type='str', default='none', aliases=['p4charset'], fallback=(env_fallback, ['P4CHARSET'])),
        serverid=dict(type='str', default='any')
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    p4 = helix_core_connect(module, 'ansible')

    try:
        # Get all current server configurations.
        p4_current_configs = p4.run('configure', 'show', 'allservers')
        # Find the value of the specified configurable for the given server ID.
        p4_current_value = next((c['Value'] for c in p4_current_configs if c["ServerName"] == module.params['serverid'] and c["Name"] == module.params['name']), None)

        if module.params['state'] == 'present':
            # Set the configurable if it's not already set to the desired value.
            if p4_current_value != module.params['value']:
                result['changed'] = True
                if not module.check_mode:
                    p4.run('configure', 'set', f"{module.params['serverid']}#{module.params['name']}={module.params['value']}")
        elif module.params['state'] == 'absent':
            # Unset the configurable if it's currently set.
            if p4_current_value is not None:
                result['changed'] = True
                if not module.check_mode:
                    p4.run('configure', 'unset', f"{module.params['serverid']}#{module.params['name']}")
    except Exception as e:
        module.fail_json(msg=f"Error: {e}", **result)
    finally:
        helix_core_disconnect(module, p4)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()