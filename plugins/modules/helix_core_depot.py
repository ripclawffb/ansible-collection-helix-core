#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Asif Shaikh (@ripclawffb) <ripclaw_ffb@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: helix_core_depot

short_description: Manage depots on Perforce Helix Core

version_added: "1.0.0"

description:
    - "Create or edit a depot specification."
    - "This module supports check mode."

requirements:
    - "P4Python pip module is required"

seealso:
    - name: Helix Core Depot
      description: "Create or edit a depot"
      link: https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_depot.html
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
            - Determines if the depot is present or deleted
        type: str
    depot:
        description:
            - The name of the depot that needs to be managed
        required: true
        type: str
    address:
        description:
            - If the Type is remote, the address should be the P4PORT address of the remote server
        type: str
    description:
        default: Created by user.
        description:
            - A textual description of the depot
        type: str
    map:
        description:
            - For a local depot, the Map field specifies the filesystem location of the archive contents for files in the depot
        type: str
    specmap:
        description:
            - For spec depots, an optional description of which specs should be saved, expressed as a view
        type: str
    streamdepth:
        default: 1
        description:
            - The default is one level below the name of the depot
        type: str
    suffix:
        default: .p4s
        description:
            -  If the Type is spec, this field holds an optional suffix for generated paths to objects in the spec depot
        required: true
        type: str
    type:
        choices:
            - local
            - remote
            - stream
            - spec
            - unload
            - archive
            - tangent
            - graph
        default: local
        description:
            - The type of depot
        type: str

extends_documentation_fragment:
    - ripclawffb.helix_core.helix_core_connection

author:
    - Asif Shaikh (@ripclawffb)
'''

EXAMPLES = '''
# Create a depot
- name: Create a new depot
  helix_core_depot:
    state: present
    name: bruno_new_depot
    description: 'New depot for Bruno'
    server: '1666'
    user: bruno
    charset: none
    password: ''

# Delete a depot
- name: Delete a depot
  helix_core_depot:
    state: absent
    name: bruno_new_depot
    server: '1666'
    user: bruno
    charset: none
    password: ''
'''

RETURN = r'''
changed:
    description: Whether any changes were made to the depot.
    returned: always
    type: bool
    sample: true
depot_spec:
    description: The depot specification after the operation.
    returned: always
    type: dict
    sample:
        Depot: my_depot
        Description: My depot
        Type: local
action:
    description: The action performed on the resource.
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
        name=dict(type='str', required=True, aliases=['depot']),
        description=dict(type='str'),
        address=dict(type='str', default=None),
        map=dict(type='str'),
        specmap=dict(type='str', default=None),
        streamdepth=dict(type='str', default=None),
        suffix=dict(type='str', default=None),
        type=dict(type='str', default='local', choices=['local', 'remote', 'stream', 'spec', 'unload', 'archive', 'tangent', 'graph']),
        **helix_core_connection_argspec()
    )

    result = dict(
        changed=False,
        depot_spec={},
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

        if module.params['map'] is None:
            module.params['map'] = f"{module.params['name']}/..."

        # field mapping: spec key -> module param key
        mapping = {
            'Description': 'description',
            'Type': 'type',
            'Map': 'map',
            'Address': 'address',
            'SpecMap': 'specmap',
            'StreamDepth': 'streamdepth',
            'Suffix': 'suffix',
        }

        # fields to track for diff
        diff_fields = list(mapping.keys())

        if module.params['state'] == 'present':
            # get existing depot definition
            p4_depot_spec = p4.fetch_depot(module.params['name'])

            depots_dict = p4.run('depots')

            # build after_spec once for diff (used in both update and create paths)
            if module._diff:
                after_spec = build_after_spec(module.params, mapping)

            # look through the list of depot specs returned and see if any match the current depot
            # if a depot spec is found with the current depot name, let's look for any changes in attributes
            if any(depot_dict['name'] == module.params['name'] for depot_dict in depots_dict):

                # capture before state for diff
                if module._diff:
                    before = spec_to_string(p4_depot_spec, diff_fields)

                # detect per-field changes
                field_changes = changed_fields(p4_depot_spec, module.params, mapping, rstrip_fields=['Description'])

                if not field_changes:
                    result['changed'] = False

                # if changes are detected, update depot with new values
                else:
                    if not module.check_mode:
                        update_spec(p4_depot_spec, module.params, mapping)
                        p4.save_depot(p4_depot_spec)

                    result['changed'] = True
                    result['action'] = 'updated'
                    result['changes'] = field_changes

                    if module._diff:
                        result['diff'] = {'before': before, 'after': spec_to_string(after_spec, diff_fields)}

            # create new depot with specified values
            else:
                if not module.check_mode:
                    update_spec(p4_depot_spec, module.params, mapping)
                    p4.save_depot(p4_depot_spec)

                result['changed'] = True
                result['action'] = 'created'

                if module._diff:
                    result['diff'] = {'before': '', 'after': spec_to_string(after_spec, diff_fields)}

            # always return the spec for present state
            result['depot_spec'] = p4_depot_spec

        elif module.params['state'] == 'absent':
            depots_dict = p4.run('depots')

            # delete depot
            if any(depot_dict['name'] == module.params['name'] for depot_dict in depots_dict):
                p4_depot_spec = p4.fetch_depot(module.params['name'])
                if module._diff:
                    before = spec_to_string(p4_depot_spec, diff_fields)

                if not module.check_mode:
                    p4.delete_depot('-f', module.params['name'])

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
