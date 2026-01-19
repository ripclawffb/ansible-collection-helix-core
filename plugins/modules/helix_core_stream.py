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

RETURN = r''' # '''


from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible_collections.ripclawffb.helix_core.plugins.module_utils.helix_core_connection import helix_core_connect, helix_core_disconnect


def construct_spec(module):
    # Construct a stream spec dictionary from module parameters.
    spec = {}
    spec['Stream'] = module.params['stream']
    spec['Owner'] = module.params['owner'] or module.params['user']
    spec['Name'] = module.params['name'] or module.params['stream'].split('/')[-1]
    spec['Parent'] = module.params['parent']
    spec['Type'] = module.params['type']
    spec['Description'] = module.params['description'] or f"Created by {module.params['user']}."
    spec['Options'] = module.params['options']
    spec['Paths'] = module.params['paths']
    if module.params['remapped']:
        spec['Remapped'] = module.params['remapped']
    if module.params['ignored']:
        spec['Ignored'] = module.params['ignored']
    return spec


def run_module():
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
        remapped=dict(type='list', elements='str', default=None),
        ignored=dict(type='list', elements='str', default=None),
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
            # Create or update a stream spec.
            desired_spec = construct_spec(module)
            existing_spec = p4.fetch_stream(module.params['stream'])

            # Compare the desired spec with the existing spec.
            changed = False
            if 'Update' not in existing_spec:
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
                    p4.save_stream(existing_spec)

        elif module.params['state'] == 'absent':
            # Delete a stream spec if it exists.
            existing_spec = p4.fetch_stream(module.params['stream'])
            if 'Update' in existing_spec:
                result['changed'] = True
                if not module.check_mode:
                    p4.delete_stream('-f', module.params['stream'])

    except Exception as e:
        module.fail_json(msg=f"Error: {e}", **result)
    finally:
        helix_core_disconnect(module, p4)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()