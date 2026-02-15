#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Asif Shaikh (@ripclawffb) <ripclaw_ffb@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: helix_core_group

short_description: This module will allow you to manage groups on Perforce Helix Core

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
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ripclawffb.helix_core.plugins.module_utils.helix_core_connection import (
    helix_core_connect, helix_core_disconnect, helix_core_connection_argspec
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

        if module.params['state'] == 'present':
            if 'Users' in p4_group_spec:

                # check to see if any fields have changed
                p4_group_changes = []
                p4_group_changes.append(p4_group_spec['Group'] == module.params['name'])
                p4_group_changes.append(p4_group_spec['MaxLockTime'] == module.params['maxlocktime'])
                p4_group_changes.append(p4_group_spec['MaxResults'].rstrip() == module.params['maxresults'])
                p4_group_changes.append(p4_group_spec['MaxOpenFiles'] == module.params['maxopenfiles'])
                p4_group_changes.append(p4_group_spec['MaxScanRows'] == module.params['maxscanrows'])
                p4_group_changes.append(p4_group_spec['PasswordTimeout'] == module.params['passwordtimeout'])
                p4_group_changes.append(p4_group_spec['Timeout'] == module.params['timeout'])

                if module.params['ldapconfig'] is not None:
                    p4_group_changes.append(p4_group_spec['LdapConfig'] == module.params['ldapconfig'])
                elif 'LdapConfig' in p4_group_spec:
                    p4_group_changes.append(False)

                if module.params['ldapsearchquery'] is not None:
                    p4_group_changes.append(p4_group_spec['LdapSearchQuery'] == module.params['ldapsearchquery'])
                elif 'LdapSearchQuery' in p4_group_spec:
                    p4_group_changes.append(False)

                if module.params['ldapuserattribute'] is not None:
                    p4_group_changes.append(p4_group_spec['LdapUserAttribute'] == module.params['ldapuserattribute'])
                elif 'LdapUserAttribute' in p4_group_spec:
                    p4_group_changes.append(False)

                if module.params['owners'] is not None:
                    if 'Owners' in p4_group_spec:
                        p4_group_changes.append(p4_group_spec['Owners'] == module.params['owners'])
                    else:
                        # owners param provided but spec has no Owners - need to add them
                        p4_group_changes.append(len(module.params['owners']) == 0)
                elif 'Owners' in p4_group_spec:
                    p4_group_changes.append(False)

                if module.params['subgroups'] is not None:
                    if 'Subgroups' in p4_group_spec:
                        p4_group_changes.append(p4_group_spec['Subgroups'] == module.params['subgroups'])
                    else:
                        # subgroups param provided but spec has no Subgroups - need to add them
                        p4_group_changes.append(len(module.params['subgroups']) == 0)
                elif 'Subgroups' in p4_group_spec:
                    p4_group_changes.append(False)

                if module.params['users'] is not None:
                    p4_group_changes.append(p4_group_spec['Users'] == module.params['users'])
                elif 'Users' in p4_group_spec:
                    p4_group_changes.append(False)

                # check to see if changes are detected in any of the fields
                if (all(p4_group_changes)):

                    result['changed'] = False

                # if changes are detected, update group with new values
                else:
                    if not module.check_mode:
                        p4_group_spec['Group'] = module.params['name']
                        p4_group_spec['MaxLockTime'] = module.params['maxlocktime']
                        p4_group_spec['MaxResults'] = module.params['maxresults']
                        p4_group_spec['MaxOpenFiles'] = module.params['maxopenfiles']
                        p4_group_spec['MaxScanRows'] = module.params['maxscanrows']
                        p4_group_spec['PasswordTimeout'] = module.params['passwordtimeout']
                        p4_group_spec['Timeout'] = module.params['timeout']

                        if module.params['ldapconfig'] is not None:
                            p4_group_spec['LdapConfig'] = module.params['ldapconfig']
                        elif 'LdapConfig' in p4_group_spec:
                            del p4_group_spec['LdapConfig']

                        if module.params['ldapsearchquery'] is not None:
                            p4_group_spec['LdapSearchQuery'] = module.params['ldapsearchquery']
                        elif 'LdapSearchQuery' in p4_group_spec:
                            del p4_group_spec['LdapSearchQuery']

                        if module.params['ldapuserattribute'] is not None:
                            p4_group_spec['LdapUserAttribute'] = module.params['ldapuserattribute']
                        elif 'LdapUserAttribute' in p4_group_spec:
                            del p4_group_spec['LdapUserAttribute']

                        if module.params['owners'] is not None:
                            p4_group_spec['Owners'] = module.params['owners']
                        elif 'Owners' in p4_group_spec:
                            del p4_group_spec['Owners']

                        if module.params['subgroups'] is not None:
                            p4_group_spec['Subgroups'] = module.params['subgroups']
                        elif 'Subgroups' in p4_group_spec:
                            del p4_group_spec['Subgroups']

                        if module.params['users'] is not None:
                            p4_group_spec['Users'] = module.params['users']
                        elif 'Users' in p4_group_spec:
                            del p4_group_spec['Users']

                        p4.save_group(p4_group_spec)

                    result['changed'] = True

            # create new user with specified values
            else:
                if not module.check_mode:
                    p4_group_spec['Group'] = module.params['name']
                    p4_group_spec['MaxLockTime'] = module.params['maxlocktime']
                    p4_group_spec['MaxResults'] = module.params['maxresults']
                    p4_group_spec['MaxOpenFiles'] = module.params['maxopenfiles']
                    p4_group_spec['MaxScanRows'] = module.params['maxscanrows']
                    p4_group_spec['PasswordTimeout'] = module.params['passwordtimeout']
                    p4_group_spec['Timeout'] = module.params['timeout']

                    if module.params['ldapconfig'] is not None:
                        p4_group_spec['LdapConfig'] = module.params['ldapconfig']

                    if module.params['ldapsearchquery'] is not None:
                        p4_group_spec['LdapSearchQuery'] = module.params['ldapsearchquery']

                    if module.params['ldapuserattribute'] is not None:
                        p4_group_spec['LdapUserAttribute'] = module.params['ldapuserattribute']

                    if module.params['owners'] is not None:
                        p4_group_spec['Owners'] = module.params['owners']

                    if module.params['subgroups'] is not None:
                        p4_group_spec['Subgroups'] = module.params['subgroups']

                    if module.params['users'] is not None:
                        p4_group_spec['Users'] = module.params['users']

                    p4.save_group(p4_group_spec)

                result['changed'] = True

        elif module.params['state'] == 'absent':
            # delete group
            if 'Users' in p4_group_spec:
                if not module.check_mode:
                    p4.delete_group(module.params['name'])

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
