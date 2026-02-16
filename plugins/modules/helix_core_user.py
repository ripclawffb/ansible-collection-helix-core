#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Asif Shaikh (@ripclawffb) <ripclaw_ffb@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: helix_core_user

short_description: Manage users on Perforce Helix Core

version_added: "1.0.0"

description:
    - "Create or edit Helix server user specifications and preferences"
    - "This module supports check mode."

requirements:
    - "P4Python pip module is required"

seealso:
    - name: Helix Core User
      description: "Create, edit, or delete Helix server user specifications and preferences"
      link: https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_user.html
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
            - Determines if the user is present or deleted
        type: str
    name:
        description:
            - The name of the user that needs to be managed
        required: true
        type: str
    authmethod:
        choices:
            - perforce
            - ldap
        default: perforce
        description:
            - One of the following, perforce or ldap
        type: str
    email:
        default: user@hostname
        description:
            - The user’s email address
        type: str
    fullname:
        default: name
        description:
            - The user’s full name
        type: str

extends_documentation_fragment:
    - ripclawffb.helix_core.helix_core_connection

author:
    - Asif Shaikh (@ripclawffb)
'''

EXAMPLES = '''
# Create a user
- name: Create a new user
  helix_core_user:
    state: present
    name: new_user
    email: new_user@perforce.com
    server: '1666'
    user: bruno
    charset: none
    password: ''

# Delete a user
- name: Delete a user
  helix_core_user:
    state: absent
    name: new_user
    server: '1666'
    user: bruno
    charset: none
    password: ''
'''

RETURN = r'''
changed:
    description: Whether any changes were made to the user.
    returned: always
    type: bool
    sample: true
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
from ansible_collections.ripclawffb.helix_core.plugins.module_utils.helix_core_connection import (
    helix_core_connect, helix_core_disconnect, helix_core_connection_argspec, spec_to_string
)
from socket import gethostname


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        state=dict(type='str', default='present', choices=['present', 'absent']),
        name=dict(type='str', required=True),
        authmethod=dict(type='str', default='perforce', choices=['perforce', 'ldap']),
        email=dict(type='str'),
        fullname=dict(type='str'),
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
        # get existing user definition
        p4_user_spec = p4.fetch_user(module.params['name'])

        # if full name is not given, set a default
        if module.params['fullname'] is None:
            module.params['fullname'] = module.params['name']

        # if email is not given, set a default
        if module.params['email'] is None:
            module.params['email'] = f"{module.params['name']}@{gethostname()}"

        # capture before state for diff
        diff_fields = ['AuthMethod', 'Email', 'FullName']
        if module._diff:
            if 'Access' in p4_user_spec:
                before = spec_to_string(p4_user_spec, diff_fields)
            else:
                before = ''

        if module.params['state'] == 'present':
            if module._diff:
                after = spec_to_string({
                    'AuthMethod': module.params['authmethod'],
                    'Email': module.params['email'],
                    'FullName': module.params['fullname'],
                }, diff_fields)

            if 'Access' in p4_user_spec:
                # check to see if changes are detected in any of the fields
                if (p4_user_spec["AuthMethod"] == module.params['authmethod']
                   and p4_user_spec["Email"] == module.params['email']
                   and p4_user_spec["FullName"] == module.params['fullname']):

                    result['changed'] = False

                # update user with new values
                else:
                    if not module.check_mode:
                        p4_user_spec["AuthMethod"] = module.params['authmethod']
                        p4_user_spec["Email"] = module.params['email']
                        p4_user_spec["FullName"] = module.params['fullname']
                        p4.save_user(p4_user_spec, "-f")

                    result['changed'] = True

                    if module._diff:
                        result['diff'] = {'before': before, 'after': after}

            # create new user with specified values
            else:
                if not module.check_mode:
                    p4_user_spec["AuthMethod"] = module.params['authmethod']
                    p4_user_spec["Email"] = module.params['email']
                    p4_user_spec["FullName"] = module.params['fullname']
                    p4.save_user(p4_user_spec, "-f")

                result['changed'] = True

                if module._diff:
                    result['diff'] = {'before': '', 'after': after}

        elif module.params['state'] == 'absent':
            # delete user
            if 'Access' in p4_user_spec:
                if not module.check_mode:
                    p4.delete_user('-f', module.params['name'])

                result['changed'] = True

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
