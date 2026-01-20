#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Asif Shaikh (@ripclawffb) <ripclaw_ffb@hotmail.com>
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
module: helix_core_depot

short_description: This module will allow you to manage depots on Perforce Helix Core

description:
    - "Create or edit a depot specification."
    - "This module supports check mode."

requirements:
    - "P4Python pip module is required. Tested with 2018.2.1743033"

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
            - A user with access to create depots
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

RETURN = r''' # '''


from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible_collections.ripclawffb.helix_core.plugins.module_utils.helix_core_connection import helix_core_connect, helix_core_disconnect


def construct_spec(module):
    # Construct a depot spec dictionary from module parameters.
    spec = {}
    spec['Description'] = module.params['description'] or f"Created by {module.params['user']}."
    spec['Type'] = module.params['type']
    spec['Map'] = module.params['map'] or f"{module.params['name']}/..."
    if module.params['address']:
        spec['Address'] = module.params['address']
    if module.params['specmap']:
        spec['SpecMap'] = module.params['specmap']
    if module.params['streamdepth']:
        spec['StreamDepth'] = module.params['streamdepth']
    if module.params['suffix']:
        spec['Suffix'] = module.params['suffix']
    return spec


def run_module():
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

    p4 = helix_core_connect(module, 'ansible')

    try:
        if module.params['state'] == 'present':
            # Create or update a depot spec.
            desired_spec = construct_spec(module)
            existing_spec = p4.fetch_depot(module.params['name'])

            # Compare the desired spec with the existing spec.
            changed = False
            if not existing_spec:
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
                    p4.save_depot(existing_spec)

        elif module.params['state'] == 'absent':
            # Delete a depot spec if it exists.
            depots_dict = p4.run('depots')
            if any(d['name'] == module.params['name'] for d in depots_dict):
                result['changed'] = True
                if not module.check_mode:
                    p4.delete_depot('-f', module.params['name'])

    except Exception as e:
        module.fail_json(msg=f"Error: {e}", **result)
    finally:
        helix_core_disconnect(module, p4)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()