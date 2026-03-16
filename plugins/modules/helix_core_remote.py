#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Asif Shaikh (@ripclawffb) <ripclaw_ffb@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: helix_core_remote

short_description: Manage remote specs on Perforce Helix Core
version_added: "1.3.0"
description:
    - "A remote specification describes the shared server that your server cooperates with."
    - "Uses the C(p4 remote) command to create, modify, or delete a remote specification."
    - "This module supports check mode."

requirements:
    - "P4Python pip module is required"

seealso:
    - name: Helix Core Remote
      description: "Create or edit a remote spec"
      link: https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_remote.html
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
            - Determines if the remote spec is present or deleted.
        type: str
    remoteid:
        description:
            - The name of the remote spec to manage.
        required: true
        type: str
    owner:
        description:
            - The name of the user who owns the remote spec. By default, this is the user who creates it.
        type: str
    address:
        description:
            - The P4PORT for the shared server.
        type: str
    remoteuser:
        description:
            - Specifies the identity (user) P4 Server uses to authenticate against this remote server when pushing and fetching.
        type: str
    description:
        default: 'Created by user.'
        description:
            - A description of the remote spec.
        type: str
    options:
        default: 'unlocked nocompress copyrcs'
        description:
            - Flags to change the remote spec behavior.
        type: str
    depotmap:
        description:
            - A list of one or more lines describing the mapping from the shared server's files to your personal server's files.
        elements: str
        type: list
    archivelimits:
        description:
            - One or more entries specifying how many revisions of file archives to store locally when the files are fetched.
        elements: str
        type: list

extends_documentation_fragment:
    - ripclawffb.helix_core.helix_core_connection

author:
    - Asif Shaikh (@ripclawffb)
'''

EXAMPLES = '''
# Create a new remote spec
- name: Create remote spec
  ripclawffb.helix_core.helix_core_remote:
    state: present
    remoteid: central-repo
    description: "Central repository shared server"
    address: "ssl:central-perforce:1666"
    depotmap:
      - "//depot/... //depot/..."
    server: '1666'
    user: bruno
    charset: auto
    password: ''
'''

RETURN = r'''
changed:
    description: Whether any changes were made to the remote spec.
    returned: always
    type: bool
    sample: true
remote_spec:
    description: The remote specification after the operation.
    returned: always
    type: dict
    sample:
        RemoteID: central-repo
        Address: ssl:central-perforce:1666
        Description: Central repository shared server
action:
    description: The action performed.
    returned: always
    type: str
    sample: created
    choices:
        - created
        - updated
        - deleted
        - unchanged
changes:
    description: List of fields that were changed.
    returned: always
    type: list
    elements: dict
    sample:
        - field: Description
          before: Old description
          after: New description
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
    build_after_spec, changed_fields, update_spec
)


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        state=dict(type='str', default='present', choices=['present', 'absent']),
        remoteid=dict(type='str', required=True),
        owner=dict(type='str', default=None),
        address=dict(type='str', default=None),
        remoteuser=dict(type='str', default=None),
        description=dict(type='str'),
        options=dict(type='str', default='unlocked nocompress copyrcs'),
        depotmap=dict(type='list', elements='str', default=None),
        archivelimits=dict(type='list', elements='str', default=None),
        **helix_core_connection_argspec()
    )

    result = dict(
        changed=False,
        remote_spec={},
        action='unchanged',
        changes=[],
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

        # field mapping: spec key -> module param key
        mapping = {
            'Owner': 'owner',
            'Description': 'description',
            'Address': 'address',
            'RemoteUser': 'remoteuser',
            'Options': 'options',
            'DepotMap': 'depotmap',
            'ArchiveLimits': 'archivelimits',
        }

        # fields to track for diff
        diff_fields = ['RemoteID', 'Owner', 'Description', 'Address', 'RemoteUser', 'Options', 'DepotMap', 'ArchiveLimits']

        if module.params['state'] == 'present':
            # get remote definition
            p4_remote_spec = p4.fetch_remote(module.params['remoteid'])

            remotes_dict = p4.run('remotes')

            # build after_spec once for diff (used in both update and create paths)
            if module._diff:
                after_spec = build_after_spec(module.params, mapping)
                after_spec['RemoteID'] = module.params['remoteid']

            # look through the list of remote specs returned and see if any match the current remote id
            if any(remote_dict['RemoteID'] == module.params['remoteid'] for remote_dict in remotes_dict):

                # capture before state for diff
                if module._diff:
                    before = spec_to_string(p4_remote_spec, diff_fields)

                # detect per-field changes
                field_changes = changed_fields(p4_remote_spec, module.params, mapping, rstrip_fields=['Description'])

                if not field_changes:
                    result['changed'] = False

                # if changes are detected, update remote spec with new values
                else:
                    if not module.check_mode:
                        update_spec(p4_remote_spec, module.params, mapping)
                        p4.save_remote(p4_remote_spec)

                    result['changed'] = True
                    result['action'] = 'updated'
                    result['changes'] = field_changes

                    if module._diff:
                        result['diff'] = {'before': before, 'after': spec_to_string(after_spec, diff_fields)}

            # create new remote spec with specified values
            else:
                if not module.check_mode:
                    p4_remote_spec["RemoteID"] = module.params['remoteid']
                    update_spec(p4_remote_spec, module.params, mapping)
                    p4.save_remote(p4_remote_spec)

                result['changed'] = True
                result['action'] = 'created'

                if module._diff:
                    result['diff'] = {'before': '', 'after': spec_to_string(after_spec, diff_fields)}

            # always return the spec for present state
            result['remote_spec'] = p4_remote_spec

        elif module.params['state'] == 'absent':
            remotes_dict = p4.run('remotes')

            # delete remote spec
            if any(remote_dict['RemoteID'] == module.params['remoteid'] for remote_dict in remotes_dict):
                p4_remote_spec = p4.fetch_remote(module.params['remoteid'])
                if module._diff:
                    before = spec_to_string(p4_remote_spec, diff_fields)

                if not module.check_mode:
                    p4.delete_remote(module.params['remoteid'])

                result['changed'] = True
                result['action'] = 'deleted'

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
