#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Asif Shaikh (@ripclawffb) <ripclaw_ffb@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: helix_core_group

short_description: Manage groups on Perforce Helix Core

version_added: "1.0.0"

description:
    - "Add or delete users from a group, or set the maxresults, maxscanrows, maxlocktime, and timeout limits for the members of a group"
    - "This module supports check mode."

requirements:
    - "P4Python pip module is required"

seealso:
    - name: Helix Core Group
      description: "Add or delete users from a group, or set the maxresults, maxscanrows, maxlocktime, and timeout limits for the members of a group"
      link: https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_group.html
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
            - Determines if the group is present or deleted
        type: str
    name:
        description:
            - The name of the group that needs to be managed
        required: true
        type: str
        aliases:
            - group
    ldapconfig:
        description:
            - The LDAP configuration to use when populating the group’s user list from an LDAP query
        type: str
    ldapsearchquery:
        description:
            - The LDAP query used to identify the members of the group
        type: str
    ldapuserattribute:
        description:
            - The LDAP attribute that represents the user’s username
        type: str
    maxlocktime:
        default: unset
        description:
            - The maximum length of time (in milliseconds) that any one operation can lock any database table when scanning data
        type: str
    maxopenfiles:
        default: unset
        description:
            - The maximum number of files that a member of a group can open using a single command
        type: str
    maxresults:
        default: unset
        description:
            - The maximum number of results that members of this group can access from the service from a single command
        type: str
    maxscanrows:
        default: unset
        description:
            - The maximum number of rows that members of this group can scan from the service from a single command
        type: str
    owners:
        description:
            - Names of other Helix server users
        elements: str
        type: list
    passwordtimeout:
        default: unset
        description:
            - The length of time (in seconds) for which passwords for users in this group remain valid
        type: str
    subgroups:
        description:
            - Names of other Helix server groups
        elements: str
        type: list
    timeout:
        default: 43200
        description:
            - The duration (in seconds) of the validity of a session ticket created by p4 login
        type: str
    users:
        description:
            - The Helix server usernames of the group members
        elements: str
        type: list

extends_documentation_fragment:
    - ripclawffb.helix_core.helix_core_connection

author:
    - Asif Shaikh (@ripclawffb)
'''

EXAMPLES = '''
# Create a group
- name: Create a new group
  helix_core_group:
    state: present
    name: group1
    users:
        - root
    server: '1666'
    user: bruno
    charset: none
    password: ''

# Delete a group
- name: Delete a group
  helix_core_group:
    state: absent
    name: new_user
    server: '1666'
    user: bruno
    charset: none
    password: ''
'''

RETURN = r'''
changed:
    description: Whether any changes were made to the group.
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
from ansible_collections.ripclawffb.helix_core.plugins.module_utils._helix_core_connection import (
    helix_core_connect, helix_core_disconnect, helix_core_connection_argspec, spec_to_string
)
from ansible_collections.ripclawffb.helix_core.plugins.module_utils._helix_core_spec import (
    build_after_spec, check_spec, update_spec
)


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        state=dict(type='str', default='present', choices=['present', 'absent']),
        name=dict(type='str', required=True, aliases=['group']),
        ldapconfig=dict(type='str', default=None),
        ldapsearchquery=dict(type='str', default=None),
        ldapuserattribute=dict(type='str', default=None),
        maxlocktime=dict(type='str', default='unset'),
        maxopenfiles=dict(type='str', default='unset'),
        maxresults=dict(type='str', default='unset'),
        maxscanrows=dict(type='str', default='unset'),
        owners=dict(type='list', elements='str', default=None),
        passwordtimeout=dict(type='str', default='unset'),
        subgroups=dict(type='list', elements='str', default=None),
        timeout=dict(type='str', default='43200'),
        users=dict(type='list', elements='str', default=None),
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
        # get existing group definition
        p4_group_spec = p4.fetch_group(module.params['name'])

        # field mapping: spec key -> module param key
        mapping = {
            'Group': 'name',
            'MaxLockTime': 'maxlocktime',
            'MaxResults': 'maxresults',
            'MaxOpenFiles': 'maxopenfiles',
            'MaxScanRows': 'maxscanrows',
            'PasswordTimeout': 'passwordtimeout',
            'Timeout': 'timeout',
            'LdapConfig': 'ldapconfig',
            'LdapSearchQuery': 'ldapsearchquery',
            'LdapUserAttribute': 'ldapuserattribute',
            'Owners': 'owners',
            'Subgroups': 'subgroups',
            'Users': 'users',
        }

        # fields to track for diff
        diff_fields = list(mapping.keys())

        if module.params['state'] == 'present':

            # build after_spec once for diff (used in both update and create paths)
            if module._diff:
                after_spec = build_after_spec(module.params, mapping)

            if 'Users' in p4_group_spec:

                # capture before state for diff
                if module._diff:
                    before = spec_to_string(p4_group_spec, diff_fields)

                # check to see if changes are detected in any of the fields
                if not check_spec(p4_group_spec, module.params, mapping, rstrip_fields=['MaxResults']):
                    result['changed'] = False

                # if changes are detected, update group with new values
                else:
                    if not module.check_mode:
                        update_spec(p4_group_spec, module.params, mapping)
                        p4.save_group(p4_group_spec)

                    result['changed'] = True

                    if module._diff:
                        result['diff'] = {'before': before, 'after': spec_to_string(after_spec, diff_fields)}

            # create new user with specified values
            else:
                if not module.check_mode:
                    update_spec(p4_group_spec, module.params, mapping)
                    p4.save_group(p4_group_spec)

                result['changed'] = True

                if module._diff:
                    result['diff'] = {'before': '', 'after': spec_to_string(after_spec, diff_fields)}

        elif module.params['state'] == 'absent':
            # delete group
            if 'Users' in p4_group_spec:
                if module._diff:
                    before = spec_to_string(p4_group_spec, diff_fields)

                if not module.check_mode:
                    p4.delete_group(module.params['name'])

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
