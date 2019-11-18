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
    - "A client/workspace specification defines the portion of the depot that can be accessed from that workspace and specifies where local copies of files in the depot are stored."
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
            - The directory (on the local host) relative to which all the files in the View: are specified
        required: true
        type: str
    view:
        description:
            -  Specifies the mappings between files in the depot and files in the workspace
        required: true
        elements: str
        type: list
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


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        state=dict(type='str', default='present', choices=['present', 'absent']),
        name=dict(type='str', required=True),
        description=dict(type='str'),
        host=dict(type='str'),
        root=dict(type='str'),
        view=dict(type='list', elements='str', required=True),
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

    # connect to helix
    p4 = helix_core_connect(module, 'ansible')

    try:
        # get existing client definition
        p4_client_spec = p4.fetch_client(module.params['name'])

        # if description is not given, set a default
        if module.params['description'] is None:
            module.params['description'] = "Created by {0}.".format(module.params['user'])

        # if host is not given, set a default
        if module.params['host'] is None:
            module.params['host'] = gethostname()

        # if root is not given, set a default
        if module.params['root'] is None:
            module.params['root'] = getcwd()

        if module.params['state'] == 'present':
            if 'Access' in p4_client_spec:
                # check to see if changes are detected in any of the fields
                if(p4_client_spec["Root"] == module.params['root'] and
                   p4_client_spec["Host"] == module.params['host'] and
                   p4_client_spec["Description"].rstrip() == module.params['description'] and
                   p4_client_spec["View"] == module.params['view']):

                    result['changed'] = False

                # update client with new values
                else:
                    if not module.check_mode:
                        p4_client_spec["Root"] = module.params['root']
                        p4_client_spec["Host"] = module.params['host']
                        p4_client_spec["Description"] = module.params['description']
                        p4_client_spec["View"] = module.params['view']
                        p4.save_client(p4_client_spec)

                    result['changed'] = True

            # create new client with specified values
            else:
                if not module.check_mode:
                    p4_client_spec["Root"] = module.params['root']
                    p4_client_spec["Host"] = module.params['host']
                    p4_client_spec["Description"] = module.params['description']
                    p4_client_spec["View"] = module.params['view']
                    p4.save_client(p4_client_spec)

                result['changed'] = True

        elif module.params['state'] == 'absent':
            # delete client
            if 'Access' in p4_client_spec:
                if not module.check_mode:
                    p4.delete_client('-f', module.params['name'])

                result['changed'] = True
            else:
                result['changed'] = False

    except Exception as e:
        module.fail_json(msg="Error: {0}".format(e), **result)

    helix_core_disconnect(module, p4)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
