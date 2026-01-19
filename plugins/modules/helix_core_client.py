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
module: helix_core_client

short_description: This module will allow you to manage client/workspace on Perforce Helix Core

description:
    - "A client/workspace specification defines the portion of the depot that can be accessed from that
       workspace and specifies where local copies of files in the depot are stored."
    - "This module supports check mode."

requirements:
    - "P4Python pip module is required. Tested with 2018.2.1743033"

seealso:
    - name: Helix Core Client
      description: "Create or edit a client workspace specification and its view"
      link: https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_client.html
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
            - Determines if the client is present or deleted
        type: str
    name:
        description:
            - The name of the client that needs to be managed
        required: true
        type: str
    description:
        default: Created by user.
        description:
            - A textual description of the workspace
        type: str
    host:
        default: hostname
        description:
            - The name of the workstation on which this workspace resides
        type: str
    root:
        description:
            - The directory (on the local host) relative to which all the files in the View are specified
        required: true
        type: str
    altroots:
        default: None
        description:
            - Up to two optional alternate client workspace roots
        elements: str
        type: list
    view:
        description:
            -  Specifies the mappings between files in the depot and files in the workspace
        required: true
        elements: str
        type: list
    lineend:
        choices:
            - local
            - unix
            - mac
            - win
            - share
        default: local
        description:
            - Configure carriage-return/linefeed (CR/LF) conversion
        type: str
    options:
        default: noallwrite noclobber nocompress unlocked nomodtime normdir
        description:
            - A set of switches that control particular workspace options
        type: str
    submitoptions:
        default: submitunchanged
        description:
            - Options to govern the default behavior of p4 submit
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
            - A user with access to create clients/workspaces
            - Can also use 'P4USER' environment variable
        required: true
        type: str
        aliases:
            - p4user
    password:
        description:
            - The user password
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
# Create a client
- name: Create a new client
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
    charset: none
    password: ''

# Delete a client
- name: Delete a client
  helix_core_client:
    state: absent
    name: bruno_new_client
    server: '1666'
    user: bruno
    charset: none
    password: ''
'''

RETURN = r''' # '''


from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible_collections.ripclawffb.helix_core.plugins.module_utils.helix_core_connection import helix_core_connect, helix_core_disconnect
from os import getcwd
from socket import gethostname


def construct_spec(module):
    # Construct a client spec dictionary from module parameters.
    spec = {}
    spec['Root'] = module.params['root'] or getcwd()
    spec['Host'] = module.params['host'] or gethostname()
    spec['Description'] = module.params['description'] or f"Created by {module.params['user']}."
    spec['View'] = module.params['view']
    spec['LineEnd'] = module.params['lineend']
    spec['Options'] = module.params['options']
    spec['SubmitOptions'] = module.params['submitoptions']
    if module.params['altroots']:
        spec['AltRoots'] = module.params['altroots']
    return spec


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        state=dict(type='str', default='present', choices=['present', 'absent']),
        name=dict(type='str', required=True),
        description=dict(type='str'),
        host=dict(type='str'),
        root=dict(type='str'),
        altroots=dict(type='list', elements='str', default=None),
        view=dict(type='list', elements='str', default=None),
        lineend=dict(type='str', default='local', choices=['local', 'unix', 'mac', 'win', 'share']),
        options=dict(type='str', default='noallwrite noclobber nocompress unlocked nomodtime normdir'),
        submitoptions=dict(type='str', default='submitunchanged'),
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
        if module.params['state'] == 'present':
            # Create or update a client spec.
            desired_spec = construct_spec(module)
            existing_spec = p4.fetch_client(module.params['name'])

            # Required for idempotency for Helix Core 23.1 or newer.
            if 'noaltsync' in existing_spec.get("Options", ""):
                desired_spec['Options'] = f'{desired_spec["Options"]} noaltsync'

            # Compare the desired spec with the existing spec.
            changed = False
            if 'Access' not in existing_spec:
                changed = True
            else:
                for key, value in desired_spec.items():
                    if key == 'Description':
                        if existing_spec.get(key, '').rstrip() != value:
                            changed = True
                            break
                    elif existing_spec.get(key) != value:
                        changed = True
                        break
            
            if changed:
                result['changed'] = True
                if not module.check_mode:
                    # Apply the desired spec to the existing spec and save.
                    for key, value in desired_spec.items():
                        existing_spec[key] = value
                    p4.save_client(existing_spec)

        elif module.params['state'] == 'absent':
            # Delete a client spec if it exists.
            existing_spec = p4.fetch_client(module.params['name'])
            if 'Access' in existing_spec:
                result['changed'] = True
                if not module.check_mode:
                    p4.delete_client('-f', module.params['name'])

    except Exception as e:
        module.fail_json(msg=f"Error: {e}", **result)

    finally:
        helix_core_disconnect(module, p4)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()