#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Asif Shaikh (@ripclawffb) <ripclaw_ffb@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: helix_core_license_info

short_description: Get server license information from Perforce Helix Core

version_added: "1.3.0"

description:
    - "Retrieves server licensing information from Perforce Helix Core."
    - "Returns the details of the active license and its usage limits."
    - "This is a read-only module that does not make any changes."

requirements:
    - "P4Python pip module is required"

seealso:
    - name: Helix Core License
      description: "Manage server license"
      link: https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_license.html
    - name: P4Python Pip Module
      description: "Python module to interact with Helix Core"
      link: https://pypi.org/project/p4python/

options: {}

extends_documentation_fragment:
    - ripclawffb.helix_core.helix_core_connection

author:
    - Asif Shaikh (@ripclawffb)
'''

EXAMPLES = '''
# Get license info
- name: Get license info
  ripclawffb.helix_core.helix_core_license_info:
    server: '1666'
    user: bruno
    charset: auto
    password: ''
  register: license_info
'''

RETURN = r'''
changed:
    description: Always False as this is a read-only module.
    returned: always
    type: bool
    sample: false
info:
    description:
        - A dict with the current license details.
        - Contains usage info if the server supports it and the user has admin or super privileges.
    returned: success
    type: dict
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ripclawffb.helix_core.plugins.module_utils._helix_core_connection import (
    helix_core_connect, helix_core_disconnect, helix_core_connection_argspec
)


def run_module():
    module_args = dict(
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
        # First, try to get usage info (-u) which requires admin privileges
        try:
            usage_info_list = p4.run('license', '-u')
            for info in usage_info_list:
                result['info'].update(info)
        except Exception as e:
            # Fall back to -o if -u fails due to permissions or missing license
            error_msg = str(e).lower()
            if "permission" in error_msg or "until a license is installed" in error_msg:
                pass
            else:
                raise
        
        # Also grab the raw license info from -o
        try:
            info_list = p4.run('license', '-o')
            if info_list:
                result['info'].update(info_list[0])
        except Exception as e:
            # -o fails on fully unlicensed servers with "Only 'p4 license -i', 'p4 license -L' and 'p4 license -u' may be used until a license is installed."
            error_msg = str(e).lower()
            if "until a license is installed" in error_msg:
                pass
            else:
                raise

    except Exception as e:
        module.fail_json(msg=f"Error: {e}", **result)

    helix_core_disconnect(module, p4)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
