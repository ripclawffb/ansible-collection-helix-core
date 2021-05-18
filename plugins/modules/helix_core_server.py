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
    - "A server specification describes the high-level configuration and intended usage of a
       Helix Server. For installations with only one Helix Server, the server specification is optional."
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
        descripton:
            - The service user name used by the server (this is the user: field in server spec)
        type: str
    type:
        default: server
        description:
            - Server executable type
        type: str
    updatecachedrepos:
        description:
            - Beginning in 2019.2, this optional field can contain a list of repos to be updated, with each repo name on a separate line
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

RETURN = r''' # '''


from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible_collections.ripclawffb.helix_core.plugins.module_utils.helix_core_connection import helix_core_connect, helix_core_disconnect


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
        # if description is not given, set a default
        if module.params['description'] is None:
            module.params['description'] = "Created by {0}.".format(module.params['user'])

        if module.params['state'] == 'present':
            # get server definition
            p4_server_spec = p4.fetch_server(module.params['serverid'])

            servers_dict = p4.run('servers')

            # look through the list of servers specs returned and see if any match the current server id
            # if a server spec is found with the current server id, let's look for any changes in attributes
            if any(server_dict['ServerID'] == module.params['serverid'] for server_dict in servers_dict):

                # check to see if any fields have changed
                p4_server_changes = []
                p4_server_changes.append(p4_server_spec["Description"].rstrip() == module.params['description'])
                p4_server_changes.append(p4_server_spec["Options"] == module.params['options'])
                p4_server_changes.append(p4_server_spec["Services"] == module.params['services'])
                p4_server_changes.append(p4_server_spec["Type"] == module.params['type'])

                if module.params['address'] is not None:
                    p4_server_changes.append(p4_server_spec["Address"] == module.params['address'])
                elif 'Address' in p4_server_spec:
                    p4_server_changes.append(False)

                if module.params['allowedaddresses'] is not None:
                    p4_server_changes.append(p4_server_spec["AllowedAddresses"] == module.params['allowedaddresses'])
                elif 'AllowedAddresses' in p4_server_spec:
                    p4_server_changes.append(False)

                if module.params['archivedatafilter'] is not None:
                    p4_server_changes.append(p4_server_spec["ArchiveDataFilter"] == module.params['archivedatafilter'])
                elif 'ArchiveDataFilter' in p4_server_spec:
                    p4_server_changes.append(False)

                if module.params['clientdatafilter'] is not None:
                    p4_server_changes.append(p4_server_spec["ClientDataFilter"] == module.params['clientdatafilter'])
                elif 'ClientDataFilter' in p4_server_spec:
                    p4_server_changes.append(False)

                # ToDo - figure out how to get current configurables for this server id and compare to this if not provided
                # if module.params['distributedconfig'] is not None:
                #    p4_server_changes.append(p4_server_spec["DistributedConfig"] == module.params['distributedconfig'])
                # elif 'DistributedConfig' in p4_server_spec:
                #     p4_server_changes.append(False)

                if module.params['externaladdress'] is not None:
                    p4_server_changes.append(p4_server_spec["ExternalAddress"] == module.params['externaladdress'])
                elif 'ExternalAddress' in p4_server_spec:
                    p4_server_changes.append(False)

                if module.params['name'] is not None:
                    p4_server_changes.append(p4_server_spec["Name"] == module.params['name'])
                elif 'Name' in p4_server_spec:
                    p4_server_changes.append(False)

                if module.params['replicatingfrom'] is not None:
                    p4_server_changes.append(p4_server_spec["ReplicatingFrom"] == module.params['replicatingfrom'])
                elif 'ReplicatingFrom' in p4_server_spec:
                    p4_server_changes.append(False)

                if module.params['revisiondatafilter'] is not None:
                    p4_server_changes.append(p4_server_spec["RevisionDataFilter"] == module.params['revisiondatafilter'])
                elif 'RevisionDataFilter' in p4_server_spec:
                    p4_server_changes.append(False)

                if module.params['updatedcachedrepos'] is not None:
                    p4_server_changes.append(p4_server_spec["UpdatedCachedRepos"] == module.params['updatedcachedrepos'])
                elif 'UpdatedCachedRepos' in p4_server_spec:
                    p4_server_changes.append(False)

                if module.params['serviceuser'] is not None:
                    p4_server_changes.append(p4_server_spec["User"] == module.params['serviceuser'])
                elif 'User' in p4_server_spec:
                    p4_server_changes.append(False)

                # check to see if changes are detected in any of the fields
                if(all(p4_server_changes)):

                    result['changed'] = False

                # if changes are detected, update server spec with new values
                else:
                    if not module.check_mode:
                        p4_server_spec["Description"] = module.params['description']
                        p4_server_spec["Options"] = module.params['options']
                        p4_server_spec["Services"] = module.params['services']
                        p4_server_spec["Type"] = module.params['type']

                        if module.params['address'] is not None:
                            p4_server_spec["Address"] = module.params['address']
                        elif 'Address' in p4_server_spec:
                            del p4_server_spec["Address"]

                        if module.params['allowedaddresses'] is not None:
                            p4_server_spec["AllowedAddresses"] = module.params['allowedaddresses']
                        elif 'AllowedAddresses' in p4_server_spec:
                            del p4_server_spec["AllowedAddresses"]

                        if module.params['archivedatafilter'] is not None:
                            p4_server_spec["ArchiveDataFilter"] = module.params['archivedatafilter']
                        elif 'ArchiveDataFilter' in p4_server_spec:
                            del p4_server_spec["ArchiveDataFilter"]

                        if module.params['clientdatafilter'] is not None:
                            p4_server_spec["ClientDataFilter"] = module.params['clientdatafilter']
                        elif 'ClientDataFilter' in p4_server_spec:
                            del p4_server_spec["ClientDataFilter"]

                        if module.params['distributedconfig'] is not None:
                            p4_server_spec["DistributedConfig"] = module.params['distributedconfig']
                        elif 'DistributedConfig' in p4_server_spec:
                            del p4_server_spec["DistributedConfig"]

                        if module.params['externaladdress'] is not None:
                            p4_server_spec["ExternalAddress"] = module.params['externaladdress']
                        elif 'ExternalAddress' in p4_server_spec:
                            del p4_server_spec["ExternalAddress"]

                        if module.params['name'] is not None:
                            p4_server_spec["Name"] = module.params['name']
                        elif 'Name' in p4_server_spec:
                            del p4_server_spec["Name"]

                        if module.params['replicatingfrom'] is not None:
                            p4_server_spec["ReplicatingFrom"] = module.params['replicatingfrom']
                        elif 'ReplicatingFrom' in p4_server_spec:
                            del p4_server_spec["ReplicatingFrom"]

                        if module.params['revisiondatafilter'] is not None:
                            p4_server_spec["RevisionDataFilter"] = module.params['revisiondatafilter']
                        elif 'RevisionDataFilter' in p4_server_spec:
                            del p4_server_spec["RevisionDataFilter"]

                        if module.params['serviceuser'] is not None:
                            p4_server_spec["User"] = module.params['serviceuser']
                        elif 'User' in p4_server_spec:
                            del p4_server_spec["User"]

                        if module.params['updatedcachedrepos'] is not None:
                            p4_server_spec["UpdatedCachedRepos"] = module.params['updatedcachedrepos']
                        elif 'UpdatedCachedRepos' in p4_server_spec:
                            del p4_server_spec["UpdatedCachedRepos"]

                        p4.save_server(p4_server_spec)

                    result['changed'] = True

            # create new server spec with specified values
            else:
                if not module.check_mode:
                    p4_server_spec["ServerID"] = module.params['serverid']
                    p4_server_spec["Description"] = module.params['description']
                    p4_server_spec["Options"] = module.params['options']
                    p4_server_spec["Services"] = module.params['services']
                    p4_server_spec["Type"] = module.params['type']

                    if module.params['address'] is not None:
                        p4_server_spec["Address"] = module.params['address']

                    if module.params['allowedaddresses'] is not None:
                        p4_server_spec["AllowedAddresses"] = module.params['allowedaddresses']

                    if module.params['archivedatafilter'] is not None:
                        p4_server_spec["ArchiveDataFilter"] = module.params['archivedatafilter']

                    if module.params['clientdatafilter'] is not None:
                        p4_server_spec["ClientDataFilter"] = module.params['clientdatafilter']

                    if module.params['distributedconfig'] is not None:
                        p4_server_spec["DistributedConfig"] = module.params['distributedconfig']

                    if module.params['externaladdress'] is not None:
                        p4_server_spec["ExternalAddress"] = module.params['externaladdress']

                    if module.params['name'] is not None:
                        p4_server_spec["Name"] = module.params['name']

                    if module.params['replicatingfrom'] is not None:
                        p4_server_spec["ReplicatingFrom"] = module.params['replicatingfrom']

                    if module.params['revisiondatafilter'] is not None:
                        p4_server_spec["RevisionDataFilter"] = module.params['revisiondatafilter']

                    if module.params['serviceuser'] is not None:
                        p4_server_spec["User"] = module.params['serviceuser']

                    if module.params['updatedcachedrepos'] is not None:
                        p4_server_spec["UpdatedCachedRepos"] = module.params['updatedcachedrepos']

                    p4.save_server(p4_server_spec)

                result['changed'] = True

        elif module.params['state'] == 'absent':
            servers_dict = p4.run('servers')

            # delete server spec
            if any(server_dict['ServerID'] == module.params['serverid'] for server_dict in servers_dict):
                if not module.check_mode:
                    p4.delete_server(module.params['serverid'])

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
