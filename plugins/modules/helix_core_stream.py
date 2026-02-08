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
module: helix_core_stream

short_description: This module will allow you to manage streams on Perforce Helix Core

description:
    - "Create or edit an instance of a stream (also known as a stream definition)."
    - "This module supports check mode."

requirements:
    - "P4Python pip module is required. Tested with 2018.2.1743033"

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
            - A user with access to create streams
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
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ripclawffb.helix_core.plugins.module_utils.helix_core_connection import (
    helix_core_connect, helix_core_disconnect, helix_core_connection_argspec
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
            module.params['description'] = "Created by {0}.".format(module.params['user'])

        # if owner is not given, set a default
        if module.params['owner'] is None:
            module.params['owner'] = module.params['user']

        if module.params['state'] == 'present':
            # check to see if any fields have changed
            if 'Access' in p4_stream_spec:

                p4_stream_changes = []
                p4_stream_changes.append(p4_stream_spec["Description"].rstrip() == module.params['description'])
                p4_stream_changes.append(p4_stream_spec["Owner"] == module.params['owner'])
                p4_stream_changes.append(p4_stream_spec["Parent"] == module.params['parent'])
                p4_stream_changes.append(p4_stream_spec["Type"] == module.params['type'])
                p4_stream_changes.append(p4_stream_spec["Options"] == module.params['options'])
                p4_stream_changes.append(p4_stream_spec["Paths"] == module.params['paths'])

                if module.params['remapped'] is not None:
                    if 'Remapped' in p4_stream_spec:
                        p4_stream_changes.append(p4_stream_spec["Remapped"] == module.params['remapped'])
                    else:
                        p4_stream_changes.append(False)  # Remapped is being added
                elif 'Remapped' in p4_stream_spec:
                    p4_stream_changes.append(False)

                if module.params['ignored'] is not None:
                    if 'Ignored' in p4_stream_spec:
                        p4_stream_changes.append(p4_stream_spec["Ignored"] == module.params['ignored'])
                    else:
                        p4_stream_changes.append(False)  # Ignored is being added
                elif 'Ignored' in p4_stream_spec:
                    p4_stream_changes.append(False)

                # check to see if changes are detected in any of the fields
                if (all(p4_stream_changes)):

                    result['changed'] = False

                # if changes are detected, update stream with new values
                else:
                    if not module.check_mode:
                        p4_stream_spec["Description"] = module.params['description']
                        p4_stream_spec["Owner"] = module.params['owner']
                        p4_stream_spec["Parent"] = module.params['parent']
                        p4_stream_spec["Type"] = module.params['type']
                        p4_stream_spec["Options"] = module.params['options']
                        p4_stream_spec["Paths"] = module.params['paths']

                        if module.params['remapped'] is not None:
                            p4_stream_spec["Remapped"] = module.params['remapped']
                        elif 'Remapped' in p4_stream_spec:
                            del p4_stream_spec["Remapped"]

                        if module.params['ignored'] is not None:
                            p4_stream_spec["Ignored"] = module.params['ignored']
                        elif 'Ignored' in p4_stream_spec:
                            del p4_stream_spec["Ignored"]

                        p4.save_stream(p4_stream_spec)

                    result['changed'] = True

            # create new stream with specified values
            else:
                if not module.check_mode:
                    p4_stream_spec["Description"] = module.params['description']
                    p4_stream_spec["Owner"] = module.params['owner']
                    p4_stream_spec["Parent"] = module.params['parent']
                    p4_stream_spec["Type"] = module.params['type']
                    p4_stream_spec["Options"] = module.params['options']
                    p4_stream_spec["Paths"] = module.params['paths']

                    if module.params['remapped'] is not None:
                        p4_stream_spec["Remapped"] = module.params['remapped']

                    if module.params['ignored'] is not None:
                        p4_stream_spec["Ignored"] = module.params['ignored']

                    p4.save_stream(p4_stream_spec)

                result['changed'] = True

        elif module.params['state'] == 'absent':
            # delete stream
            if 'Access' in p4_stream_spec:
                if not module.check_mode:
                    p4.delete_stream('-f', module.params['stream'])

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
