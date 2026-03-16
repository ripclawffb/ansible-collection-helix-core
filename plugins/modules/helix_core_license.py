#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Asif Shaikh (@ripclawffb) <ripclaw_ffb@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: helix_core_license

short_description: Deploy or remove a Perforce Helix Core license
version_added: "1.3.0"
description:
    - "Deploys or updates the server license on a Perforce Helix Core server."
    - "This module uses the C(p4 license) command. It operates on the raw text of the license file."
    - "To deploy or update a license, use C(state: present) and provide the raw text of the license file to the C(license) parameter."
    - "This module supports check mode and diff mode."

requirements:
    - "P4Python pip module is required"

seealso:
    - name: Helix Core License
      description: "Manage server license"
      link: https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_license.html
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
            - Determines if the license should be present or removed.
            - Note that removing a license may leave the server in an unlicensed state (limited to a few users/files).
        type: str
    license:
        description:
            - The raw text of the Perforce license file.
            - Required if C(state=present).
        type: str

extends_documentation_fragment:
    - ripclawffb.helix_core.helix_core_connection

author:
    - Asif Shaikh (@ripclawffb)
'''

EXAMPLES = '''
# Deploy a server license from a file
- name: Deploy server license
  ripclawffb.helix_core.helix_core_license:
    state: present
    license: "{{ lookup('file', '/path/to/license.txt') }}"
    server: '1666'
    user: superuser
    charset: auto
    password: ''
'''

RETURN = r'''
changed:
    description: Whether any changes were made to the license.
    returned: always
    type: bool
    sample: true
license_info:
    description: The current license details.
    returned: always
    type: dict
    sample:
        License: "..."
        License-Expires: "1735689600"
        Support-Expires: "1735689600"
        Customer: "Example Corp"
        Application: "Helix Core"
        IPaddress: "10.0.0.5"
        Platform: "linux26x86"
        Clients: "100"
        Users: "100"
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
    helix_core_connect, helix_core_disconnect, helix_core_connection_argspec
)


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        state=dict(type='str', default='present', choices=['present', 'absent']),
        license=dict(type='str'),
        **helix_core_connection_argspec()
    )

    result = dict(
        changed=False,
        license_info={},
        action='unchanged',
    )

    module = AnsibleModule(
        argument_spec=module_args,
        required_if=[
            ('state', 'present', ['license']),
        ],
        supports_check_mode=True
    )

    p4 = helix_core_connect(module, 'ansible')

    try:
        if module.params['state'] == 'present':
            # get current license info
            current_info = {}
            current_license_text = ""
            try:
                # `p4 license -o` returns a list of dicts with the license fields
                info_list = p4.run('license', '-o')
                if info_list:
                    current_info = info_list[0]
                    current_license_text = current_info.get('License', '')
            except Exception as e:
                # If there's an error calling p4 license -o, it might mean no license is present
                # or we don't have permission. We will proceed under the assumption it's empty.
                error_msg = str(e).lower()
                if "permission" in error_msg or "until a license is installed" in error_msg:
                    pass
                else:
                    raise

            desired_license_text = module.params['license'].strip() + "\n"
            current_clean = current_license_text.strip() + "\n" if current_license_text else ""

            if current_clean != desired_license_text:
                if module._diff:
                    result['diff'] = {
                        'before': current_clean,
                        'after': desired_license_text
                    }

                if not module.check_mode:
                    p4.input = desired_license_text
                    p4.run('license', '-i')

                result['changed'] = True
                result['action'] = 'updated' if current_license_text else 'created'
            
            # Fetch updated info to return
            try:
                info_list = p4.run('license', '-o')
                if info_list:
                    result['license_info'] = info_list[0]
            except Exception as e:
                error_msg = str(e).lower()
                if "permission" in error_msg or "until a license is installed" in error_msg:
                    pass
                else:
                    raise

        elif module.params['state'] == 'absent':
            current_info = {}
            current_license_text = ""
            try:
                info_list = p4.run('license', '-o')
                if info_list:
                    current_info = info_list[0]
                    current_license_text = current_info.get('License', '')
            except Exception as e:
                error_msg = str(e).lower()
                if "permission" in error_msg or "until a license is installed" in error_msg:
                    pass
                else:
                    raise

            if current_license_text:
                if module._diff:
                    result['diff'] = {
                        'before': current_license_text,
                        'after': ''
                    }

                if not module.check_mode:
                    p4.run('license', '-d')

                result['changed'] = True
                result['action'] = 'deleted'

    except Exception as e:
        module.fail_json(msg=f"Error: {e}", **result)

    helix_core_disconnect(module, p4)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
