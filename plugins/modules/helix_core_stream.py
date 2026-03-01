#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Asif Shaikh (@ripclawffb) <ripclaw_ffb@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: helix_core_stream

short_description: Manage streams on Perforce Helix Core

version_added: "1.0.0"

description:
    - "Create or edit an instance of a stream (also known as a stream definition)."
    - "This module supports check mode."

requirements:
    - "P4Python pip module is required"

seealso:
    - name: Helix Core Stream
      description: "Create or edit an instance of a stream (also known as a stream definition)."
      link: https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_stream.html
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
            - Determines if the stream is present or deleted
        type: str
    name:
        description:
            - Display name of the stream
        type: str
    description:
        default: Created by user.
        description:
            - Description of the stream
        type: str
    owner:
        description:
            - The Helix server user or group who owns the stream
        type: str
    stream:
        description:
            - Specifies the stream’s name (permanent identifier) and its path in the stream depot, in the form //depotname/streamname
        required: true
        type: str
    parent:
        default: none
        description:
            - The parent of this stream
        type: str
    parentview:
        default: inherit
        description:
            - Defines whether the stream inherits a view from its parent
        type: str
    type:
        choices:
            - mainline
            - development
            - release
            - virtual
            - task
        default: development
        description:
            - The stream’s type determines the expected flow of change. Valid stream types are mainline, development, release, virtual, andtask.
        type: str
    options:
        default: allsubmit unlocked toparent fromparent mergedown
        description:
            - Settings that configure stream behavior
        type: str
    paths:
        default:
            - share ...
        description:
            -  Paths define how files are incorporated into the stream structure
        elements: str
        type: list
    remapped:
        description:
            -  Reassigns the location of workspace files
        elements: str
        type: list
    ignored:
        description:
            -  A list of file or directory names to be ignored
        elements: str
        type: list

extends_documentation_fragment:
    - ripclawffb.helix_core.helix_core_connection

author:
    - Asif Shaikh (@ripclawffb)
'''

EXAMPLES = '''
# Create a stream
- name: Create a new stream
  helix_core_stream:
    state: present
    stream: //depotname/streamname
    description: 'Development Stream'
    type: development
    paths:
      - share ...
    server: '1666'
    user: bruno
    charset: none
    password: ''

# Delete a stream
- name: Delete a stream
  helix_core_stream:
    state: absent
    name: //depotname/streamname
    server: '1666'
    user: bruno
    charset: none
    password: ''
'''

RETURN = r'''
changed:
    description: Whether any changes were made to the stream.
    returned: always
    type: bool
    sample: true
stream_spec:
    description: The stream specification after the operation.
    returned: always
    type: dict
    sample:
        Stream: //depot/main
        Description: Main stream
        Type: mainline
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
        name=dict(type='str'),
        description=dict(type='str'),
        owner=dict(type='str'),
        stream=dict(type='str', required=True),
        parent=dict(type='str', default='none'),
        parentview=dict(type='str', default='inherit'),
        type=dict(type='str', default='development', choices=['mainline', 'development', 'release', 'virtual', 'task']),
        options=dict(type='str', default='allsubmit unlocked toparent fromparent mergedown'),
        paths=dict(type='list', default=['share ...'], elements='str'),
        remapped=dict(type='list', elements='str'),
        ignored=dict(type='list', elements='str'),
        **helix_core_connection_argspec()
    )

    result = dict(
        changed=False,
        stream_spec={},
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
        # get existing stream definition
        p4_stream_spec = p4.fetch_stream(module.params['stream'])

        # if description is not given, set a default
        if module.params['description'] is None:
            module.params['description'] = f"Created by {module.params['user']}."

        # if owner is not given, set a default
        if module.params['owner'] is None:
            module.params['owner'] = module.params['user']

        # field mapping: spec key -> module param key
        mapping = {
            'Description': 'description',
            'Owner': 'owner',
            'Parent': 'parent',
            'Type': 'type',
            'Options': 'options',
            'Paths': 'paths',
            'Remapped': 'remapped',
            'Ignored': 'ignored',
        }

        # fields to track for diff
        diff_fields = list(mapping.keys())

        if module.params['state'] == 'present':
            # build after_spec once for diff (used in both update and create paths)
            if module._diff:
                after_spec = build_after_spec(module.params, mapping)

            # check to see if any fields have changed
            if 'Access' in p4_stream_spec:

                # capture before state for diff
                if module._diff:
                    before = spec_to_string(p4_stream_spec, diff_fields)

                # detect per-field changes
                field_changes = changed_fields(p4_stream_spec, module.params, mapping, rstrip_fields=['Description'])

                if not field_changes:
                    result['changed'] = False

                # if changes are detected, update stream with new values
                else:
                    if not module.check_mode:
                        update_spec(p4_stream_spec, module.params, mapping)
                        p4.save_stream(p4_stream_spec)

                    result['changed'] = True
                    result['action'] = 'updated'
                    result['changes'] = field_changes

                    if module._diff:
                        result['diff'] = {'before': before, 'after': spec_to_string(after_spec, diff_fields)}

            # create new stream with specified values
            else:
                if not module.check_mode:
                    update_spec(p4_stream_spec, module.params, mapping)
                    p4.save_stream(p4_stream_spec)

                result['changed'] = True
                result['action'] = 'created'

                if module._diff:
                    result['diff'] = {'before': '', 'after': spec_to_string(after_spec, diff_fields)}

            # always return the spec for present state
            result['stream_spec'] = p4_stream_spec

        elif module.params['state'] == 'absent':
            # delete stream
            if 'Access' in p4_stream_spec:
                if module._diff:
                    before = spec_to_string(p4_stream_spec, diff_fields)

                if not module.check_mode:
                    p4.delete_stream('-f', module.params['stream'])

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
