#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Asif Shaikh (@ripclawffb) <ripclaw_ffb@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: helix_core_server

short_description: Manage server spec on Perforce Helix Core

version_added: "1.0.0"

description:
    - "A server specification describes the high-level configuration and intended usage of a
       Helix Server. For installations with only one Helix Server, the server specification is optional."
    - "This module supports check mode."

requirements:
    - "P4Python pip module is required"

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
    address:
        description: The P4PORT used by this server
        type: str
    allowedaddresses:
        description:
            - A list of addresses that are valid this server
        elements: str
        type: list
    archivedatafilter:
        description:
            - For a replica server, this optional field can contain one or more patterns describing the policy
              for automatically scheduling the replication of file content. If this field is present, only those
              files described by the pattern are automatically transferred to the replica; other files are not
              transferred until they are referenced by a replica command that needs the file content.
        elements: str
        type: list
    clientdatafilter:
        description:
            - For a replica server, this optional field can contain one or more patterns describing how active
              client workspace metadata is to be filtered. Active client workspace data includes have lists,
              working records, and pending resolves.
        elements: str
        type: list
    description:
        default: Created by user.
        description:
            - A textual description of the server
        type: str
    distributedconfig:
        description:
            - For all server types, this field shows a line for each configurable that is set to a non-default value.
              In this field, the admin can edit certain values, add a new line to set certain configurables to a
              non-default value, or delete a line to reset certain configurables to their default value.
        elements: str
        type: list
    externaladdress:
        description:
            - This field contains the external address the commit server requires for connection to the edge server
        type: str
    name:
        description:
            - The P4NAME associated with this server. You can leave this blank or you can set it to the same value as the serverid.
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
    revisiondatafilter:
        description:
            - For a replica server, this optional field can contain one or more patterns describing how submitted
              revision metadata is to be filtered. Submitted revision data includes revision records, integration
              records, label contents, and the files listed in submitted changelists.
        elements: str
        type: list
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
    serviceuser:
        description:
            - The service user name used by the server (this is the user field in server spec)
        type: str
    type:
        default: server
        description:
            - Server executable type
        type: str
    updatedcachedrepos:
        description:
            - Beginning in 2019.2, this optional field can contain a list of repos to be updated, with each repo name on a separate line
        type: str

extends_documentation_fragment:
    - ripclawffb.helix_core.helix_core_connection

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

# Create a filtered edge server spec
- name: Create filtered edge server
  helix_core_server:
    state: present
    serverid: edge_replica
    description: 'Created by root.'
    archivedatafilter:
      - //depot1/...
      - -//depot2/...
    clientdatafilter:
      - -//workstation1/...
    revisiondatafilter:
      - //depot1/...
      - -//depot2/...
    services: edge-server
    server: '1666'
    user: bruno
    charset: auto
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

RETURN = r'''
changed:
    description: Whether any changes were made to the server spec.
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
from ansible_collections.ripclawffb.helix_core.plugins.module_utils._helix_core_connection import (
    helix_core_connect, helix_core_disconnect, helix_core_connection_argspec, spec_to_string
)
from ansible_collections.ripclawffb.helix_core.plugins.module_utils._helix_core_spec import (
    build_after_spec, check_spec, update_spec
)


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        state=dict(type='str', default='present', choices=['present', 'absent']),
        address=dict(type='str', default=None),
        allowedaddresses=dict(type='list', elements='str', default=None),
        archivedatafilter=dict(type='list', elements='str', default=None),
        clientdatafilter=dict(type='list', elements='str', default=None),
        description=dict(type='str'),
        distributedconfig=dict(type='list', elements='str', default=None),
        externaladdress=dict(type='str', default=None),
        options=dict(type='str', default='nomandatory'),
        replicatingfrom=dict(type='str', default=None),
        revisiondatafilter=dict(type='list', elements='str', default=None),
        name=dict(type='str', default=None),
        serverid=dict(type='str', required=True),
        services=dict(type='str', default='standard', choices=['standard', 'replica', 'forwarding-replica', 'commit-server', 'edge-server', 'build-server',
                                                               'standby', 'forwarding-standby', 'local', 'P4AUTH', 'P4CHANGE']),
        serviceuser=dict(type='str', default=None),
        type=dict(type='str', default='server'),
        updatedcachedrepos=dict(type='str', default=None),
        **helix_core_connection_argspec()
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
        # if description is not given, set a default
        if module.params['description'] is None:
            module.params['description'] = f"Created by {module.params['user']}."

        # field mapping for comparison (excludes DistributedConfig, which is intentionally
        # not compared — see ToDo comment in original code)
        check_mapping = {
            'Description': 'description',
            'Options': 'options',
            'Services': 'services',
            'Type': 'type',
            'Address': 'address',
            'AllowedAddresses': 'allowedaddresses',
            'ArchiveDataFilter': 'archivedatafilter',
            'ClientDataFilter': 'clientdatafilter',
            'ExternalAddress': 'externaladdress',
            'Name': 'name',
            'ReplicatingFrom': 'replicatingfrom',
            'RevisionDataFilter': 'revisiondatafilter',
            'User': 'serviceuser',
            'UpdatedCachedRepos': 'updatedcachedrepos',
        }

        # full mapping for updates (includes DistributedConfig)
        update_mapping = dict(check_mapping)
        update_mapping['DistributedConfig'] = 'distributedconfig'

        # fields to track for diff
        diff_fields = ['Description', 'Options', 'Services', 'Type', 'Address',
                       'AllowedAddresses', 'ArchiveDataFilter', 'ClientDataFilter',
                       'DistributedConfig', 'ExternalAddress', 'Name',
                       'ReplicatingFrom', 'RevisionDataFilter', 'User', 'UpdatedCachedRepos']

        if module.params['state'] == 'present':
            # get server definition
            p4_server_spec = p4.fetch_server(module.params['serverid'])

            servers_dict = p4.run('servers')

            # build after_spec once for diff (used in both update and create paths)
            if module._diff:
                after_spec = build_after_spec(module.params, update_mapping)

            # look through the list of servers specs returned and see if any match the current server id
            # if a server spec is found with the current server id, let's look for any changes in attributes
            if any(server_dict['ServerID'] == module.params['serverid'] for server_dict in servers_dict):

                # capture before state for diff
                if module._diff:
                    before = spec_to_string(p4_server_spec, diff_fields)

                # check to see if any fields have changed
                if not check_spec(p4_server_spec, module.params, check_mapping, rstrip_fields=['Description']):
                    result['changed'] = False

                # if changes are detected, update server spec with new values
                else:
                    if not module.check_mode:
                        update_spec(p4_server_spec, module.params, update_mapping)
                        p4.save_server(p4_server_spec)

                    result['changed'] = True

                    if module._diff:
                        result['diff'] = {'before': before, 'after': spec_to_string(after_spec, diff_fields)}

            # create new server spec with specified values
            else:
                if not module.check_mode:
                    p4_server_spec["ServerID"] = module.params['serverid']
                    update_spec(p4_server_spec, module.params, update_mapping)
                    p4.save_server(p4_server_spec)

                result['changed'] = True

                if module._diff:
                    result['diff'] = {'before': '', 'after': spec_to_string(after_spec, diff_fields)}

        elif module.params['state'] == 'absent':
            servers_dict = p4.run('servers')

            # delete server spec
            if any(server_dict['ServerID'] == module.params['serverid'] for server_dict in servers_dict):
                p4_server_spec = p4.fetch_server(module.params['serverid'])
                if module._diff:
                    before = spec_to_string(p4_server_spec, diff_fields)

                if not module.check_mode:
                    p4.delete_server(module.params['serverid'])

                result['changed'] = True

                if module._diff:
                    result['diff'] = {'before': before, 'after': ''}
            else:
                result['changed'] = False

    except Exception as e:
        module.fail_json(msg=f"Error: {e}", **result)

    helix_core_disconnect(module, p4)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
