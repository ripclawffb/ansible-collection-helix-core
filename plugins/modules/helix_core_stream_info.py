#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Asif Shaikh (@ripclawffb) <ripclaw_ffb@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: helix_core_stream_info

short_description: Get stream information from Perforce Helix Core

version_added: "1.1.0"

description:
    - "Retrieves stream specifications from Perforce Helix Core."
    - "When C(name) is provided, returns a single stream spec."
    - "When C(name) is omitted, returns a list of all streams."
    - "This is a read-only module that does not make any changes."

requirements:
    - "P4Python pip module is required"

seealso:
    - name: Helix Core Stream
      description: "Manage streams"
      link: https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_stream.html
    - name: P4Python Pip Module
      description: "Python module to interact with Helix Core"
      link: https://pypi.org/project/p4python/


options:
    name:
        description:
            - The stream depot path to retrieve (e.g., C(//Ace/main)).
            - If omitted, all streams are listed.
        required: false
        type: str

extends_documentation_fragment:
    - ripclawffb.helix_core.helix_core_connection

author:
    - Asif Shaikh (@ripclawffb)
'''

EXAMPLES = '''
# Get a specific stream
- name: Get stream info
  ripclawffb.helix_core.helix_core_stream_info:
    name: //Ace/main
    server: '1666'
    user: bruno
    charset: auto
    password: ''
  register: stream_info

# List all streams
- name: List all streams
  ripclawffb.helix_core.helix_core_stream_info:
    server: '1666'
    user: bruno
    charset: auto
    password: ''
  register: all_streams
'''

RETURN = r'''
changed:
    description: Always False as this is a read-only module.
    returned: always
    type: bool
    sample: false
info:
    description:
        - When C(name) is provided, a dict with the stream spec fields.
        - When C(name) is omitted, a list of stream summary dicts.
    returned: success
    type: raw
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ripclawffb.helix_core.plugins.module_utils._helix_core_connection import (
    helix_core_connect, helix_core_disconnect, helix_core_connection_argspec
)


def run_module():
    module_args = dict(
        name=dict(type='str', required=False, default=None),
        **helix_core_connection_argspec()
    )

    result = dict(
        changed=False,
        info={}
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    p4 = helix_core_connect(module, 'ansible')

    try:
        if module.params['name']:
            spec = p4.fetch_stream(module.params['name'])
            result['info'] = dict(spec)
        else:
            result['info'] = p4.run_streams('//...')

    except Exception as e:
        module.fail_json(msg=f"Error: {e}", **result)

    helix_core_disconnect(module, p4)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
