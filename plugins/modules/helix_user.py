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
module: helix_use

short_description: This module will allow you to manage users on Perforce Helix Core

description:
    - "Create or edit Helix server user specifications and preferences"
    - "This module supports check mode."

requirements:
    - "P4Python pip module is required. Tested with 2018.2.1743033"

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
        description:
            - One of the following: perforce or ldap
        default: perforce
        type: str
    email:
        default: user@hostname
        description:
            - The user’s email address
        type: str
    fullname:
        description:
            - The user’s full name
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
            - A user with access to create users
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
# Create a user
- name: Create a new user
  helix_user:
    state: present
    name: new_user
    email: new_user@perforce.com
    server: '1666'
    user: bruno
    charset: none
    password: ''
# Delete a user
- name: Delete a user
  helix_user:
    state: absent
    name: new_user
    server: '1666'
    user: bruno
    charset: none
    password: ''
'''

RETURN = r''' # '''


from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible_collections.ripclawffb.helix.plugins.module_utils.connection import helix_connect, helix_disconnect
from socket import gethostname


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        state=dict(type='str', default='present', choices=['present', 'absent']),
        name=dict(type='str', required=True),
        authmethod=dict(type='str', default='perforce', choices=['perforce', 'ldap']),
        email=dict(type='str'),
        fullname=dict(type='str'),
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

    # connect to helix
    p4 = helix_connect(module, 'ansible')

    try:
        # get existing user definition
        p4_user_spec = p4.fetch_user(module.params['name'])

        # if full name is not given, set a default
        if module.params['fullname'] is None:
            module.params['fullname'] = module.params['name']

        # if email is not given, set a default
        if module.params['email'] is None:
            module.params['email'] = "{0}@{1}".format(module.params['name'], gethostname())

        if module.params['state'] == 'present':
            if 'Access' in p4_user_spec:
                # check to see if changes are detected in any of the fields
                if(p4_user_spec["AuthMethod"] == module.params['authmethod'] and
                   p4_user_spec["Email"] == module.params['email'] and
                   p4_user_spec["FullName"] == module.params['fullname']):

                    result['changed'] = False

                # update user with new values
                else:
                    if not module.check_mode:
                        p4_user_spec["AuthMethod"] = module.params['authmethod']
                        p4_user_spec["Email"] = module.params['email']
                        p4_user_spec["FullName"]= module.params['fullname']
                        p4.save_user(p4_user_spec, "-f")

                    result['changed'] = True

            # create new user with specified values
            else:
                if not module.check_mode:
                    p4_user_spec["AuthMethod"] = module.params['authmethod']
                    p4_user_spec["Email"] = module.params['email']
                    p4_user_spec["FullName"]= module.params['fullname']
                    p4.save_user(p4_user_spec, "-f")

                result['changed'] = True

        elif module.params['state'] == 'absent':
            # delete user
            if 'Access' in p4_user_spec:
                if not module.check_mode:
                    p4.delete_user('-f', module.params['name'])

                result['changed'] = True
            else:
                result['changed'] = False

    except Exception as e:
        module.fail_json(msg="Error: {0}".format(e), **result)

    helix_disconnect(module, p4)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
