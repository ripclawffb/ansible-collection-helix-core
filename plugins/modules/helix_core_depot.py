#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Asif Shaikh (@ripclawffb) <ripclaw_ffb@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: helix_core_depot

short_description: This module will allow you to manage depots on Perforce Helix Core

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
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ripclawffb.helix_core.plugins.module_utils.helix_core_connection import (
    helix_core_connect, helix_core_disconnect, helix_core_connection_argspec
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

        if module.params['map'] is None:
            module.params['map'] = "{0}/...".format(module.params['name'])

        if module.params['state'] == 'present':
            # get existing depot definition
            p4_depot_spec = p4.fetch_depot(module.params['name'])

            depots_dict = p4.run('depots')

            # look through the list of depot specs returned and see if any match the current depot
            # if a depot spec is found with the current depot name, let's look for any changes in attributes
            if any(depot_dict['name'] == module.params['name'] for depot_dict in depots_dict):

                # check to see if any fields have changed
                p4_depot_changes = []
                p4_depot_changes.append(p4_depot_spec["Description"].rstrip() == module.params['description'])
                p4_depot_changes.append(p4_depot_spec["Type"] == module.params['type'])
                p4_depot_changes.append(p4_depot_spec["Map"] == module.params['map'])

                if module.params['address'] is not None:
                    p4_depot_changes.append(p4_depot_spec["Address"] == module.params['address'])
                elif 'Address' in p4_depot_spec:
                    p4_depot_changes.append(False)

                if module.params['specmap'] is not None:
                    p4_depot_changes.append(p4_depot_spec["SpecMap"] == module.params['specmap'])
                elif 'SpecMap' in p4_depot_spec:
                    p4_depot_changes.append(False)

                if module.params['streamdepth'] is not None:
                    p4_depot_changes.append(p4_depot_spec["StreamDepth"] == module.params['streamdepth'])
                elif 'StreamDepth' in p4_depot_spec:
                    p4_depot_changes.append(False)

                if module.params['suffix'] is not None:
                    if 'Suffix' in p4_depot_spec:
                        p4_depot_changes.append(p4_depot_spec["Suffix"] == module.params['suffix'])
                    else:
                        p4_depot_changes.append(False)  # Suffix is being added
                elif 'Suffix' in p4_depot_spec:
                    p4_depot_changes.append(False)

                # check to see if changes are detected in any of the fields
                if (all(p4_depot_changes)):
                    result['changed'] = False

                # if changes are detected, update depot with new values
                else:
                    if not module.check_mode:
                        p4_depot_spec["Description"] = module.params['description']
                        p4_depot_spec["Type"] = module.params['type']
                        p4_depot_spec["Map"] = module.params['map']

                        if module.params['address'] is not None:
                            p4_depot_spec["Address"] = module.params['address']
                        elif 'Address' in p4_depot_spec:
                            del p4_depot_spec["Address"]

                        if module.params['specmap'] is not None:
                            p4_depot_spec["SpecMap"] = module.params['specmap']
                        elif 'SpecMap' in p4_depot_spec:
                            del p4_depot_spec["SpecMap"]

                        if module.params['streamdepth'] is not None:
                            p4_depot_spec["StreamDepth"] = module.params['streamdepth']
                        elif 'StreamDepth' in p4_depot_spec:
                            del p4_depot_spec["StreamDepth"]

                        if module.params['suffix'] is not None:
                            p4_depot_spec["Suffix"] = module.params['suffix']
                        elif 'Suffix' in p4_depot_spec:
                            del p4_depot_spec["Suffix"]

                        p4.save_depot(p4_depot_spec)

                    result['changed'] = True

            # create new depot with specified values
            else:
                if not module.check_mode:
                    p4_depot_spec["Description"] = module.params['description']
                    p4_depot_spec["Type"] = module.params['type']
                    p4_depot_spec["Map"] = module.params['map']

                    if module.params['address'] is not None:
                        p4_depot_spec["Address"] = module.params['address']

                    if module.params['specmap'] is not None:
                        p4_depot_spec["SpecMap"] = module.params['specmap']

                    if module.params['streamdepth'] is not None:
                        p4_depot_spec["StreamDepth"] = module.params['streamdepth']

                    if module.params['suffix'] is not None:
                        p4_depot_spec["Suffix"] = module.params['suffix']

                    p4.save_depot(p4_depot_spec)

                result['changed'] = True

        elif module.params['state'] == 'absent':
            depots_dict = p4.run('depots')

            # delete depot
            if any(depot_dict['name'] == module.params['name'] for depot_dict in depots_dict):
                if not module.check_mode:
                    p4.delete_depot('-f', module.params['name'])

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
