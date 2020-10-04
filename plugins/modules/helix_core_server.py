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
module: helix_core_server

short_description: This module will allow you to manage server spec on Perforce Helix Core

description:
    - "A server specification describes the high-level configuration and intended usage of a Helix Server. For installations with only one Helix Server, the server specification is optional."
    - "This module supports check mode."

requirements:
    - "P4Python pip module is required. Tested with 2018.2.1743033"

seealso:
    - name: Helix Core Server
      description: "Create, modify, or delete a Helix server specification"
      link: https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_server.html
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
            - Determines if the server spec is present or deleted
        type: str
    description:
        default: Created by user.
        description:
            - A textual description of the server
        type: str
    options:
        default: nomandatory
        description:
            - Controls how metadata is replicated to replicas
        type: str
    replicatingfrom:
        description:
            - Server ID of the server from which this server is replicating or journalcopy'ing
        type: str
    serverid:
        description:
            - A unique identifier for this server
        required: true
        type: str
    services:
        default: standard
        description:
            - The server type server provides
        type: str
    type:
        default: server
        description:
            - Server executable type
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
# Create a server spec
- name: Create a new server spec
  helix_core_server:
    state: present
    serverid: commit
    description: 'Commit server'
    services: standard
    server: '1666'
    user: bruno
    charset: none
    password: ''
# Delete a server spec
- name: Delete a server spec
  helix_core_server:
    state: absent
    serverid: commit
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
        serverid=dict(type='str', required=True),
        description=dict(type='str'),
        services=dict(type='str', default='standard', choices = ['standard', 'replica', 'forwarding-replica', 'commit-server', 'edge-server', 'build-server', 'standby', 'forwarding-standby', 'local', 'P4AUTH', 'P4CHANGE']),
        type=dict(type='str', default='server'),
        options=dict(type='str', default='nomandatory'),
        replicatingfrom=dict(type='str', default=None),
        name=dict(type='str', default=None),
        server=dict(type='str', required=True, aliases=['p4port'], fallback=(env_fallback, ['P4PORT'])),
        user=dict(type='str', required=True, aliases=['p4user'], fallback=(env_fallback, ['P4USER'])),
        password=dict(type='str', required=True, aliases=['p4passwd'], fallback=(env_fallback, ['P4PASSWD']), no_log=True),
        charset=dict(type='str', default='none', aliases=['p4charset'], fallback=(env_fallback, ['P4CHARSET'])),
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
        # get existing server definition
        p4_server_spec = p4.fetch_server(module.params['serverid'])

        # if description is not given, set a default
        if module.params['description'] is None:
            module.params['description'] = "Created by {0}.".format(module.params['user'])

        if module.params['state'] == 'present':
            # check to see if any fields have changed
            if 'ServerID' in p4_server_spec:

                p4_server_changes = []
                p4_server_changes.append(p4_server_spec["Description"].rstrip() == module.params['description'])
                p4_server_changes.append(p4_server_spec["Services"] == module.params['services'])
                p4_server_changes.append(p4_server_spec["Type"] == module.params['type'])
                p4_server_changes.append(p4_server_spec["Options"] == module.params['options'])

                if module.params['replicatingfrom'] is not None:
                   p4_server_changes.append(p4_server_spec["ReplicatingFrom"] == module.params['replicatingfrom'])
                elif 'ReplicatingFrom' in p4_server_spec:
                    p4_server_changes.append(False)

                # check to see if changes are detected in any of the fields
                if(all(p4_server_changes)):

                    result['changed'] = False

                # if changes are detected, update server spec with new values
                else:
                    if not module.check_mode:
                        p4_server_spec["Description"] = module.params['description']
                        p4_server_spec["Services"] = module.params['services']
                        p4_server_spec["Type"] = module.params['type']
                        p4_server_spec["Options"] = module.params['options'])

                        if module.params['replicatingfrom'] is not None:
                            p4_server_spec["ReplicatingFrom"] = module.params['replicatingfrom']
                        elif 'ReplicatingFrom' in p4_server_spec:
                            del p4_server_spec["ReplicatingFrom"]

                        p4.save_server(p4_server_spec)

                    result['changed'] = True

            # create new server spec with specified values
            else:
                if not module.check_mode:
                    p4_server_spec["ServerID"] = module.params['serverid']
                    p4_server_spec["Description"] = module.params['description']
                    p4_server_spec["Services"] = module.params['services']
                    p4_server_spec["Type"] = module.params['type']

                    if module.params['replicatingfrom'] is not None:
                        p4_server_spec["ReplicatingFrom"] = module.params['replicatingfrom']

                    p4.save_server(p4_server_spec)

                result['changed'] = True

        elif module.params['state'] == 'absent':
            # delete server spec
            if 'ServerID' in p4_server_spec:
                if not module.check_mode:
                    p4.delete_server('-f', module.params['serverid'])

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
