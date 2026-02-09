#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Asif Shaikh (@ripclawffb) <ripclaw_ffb@hotmail.com>
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
module: helix_core_ldap

short_description: Manage LDAP configurations on Perforce Helix Core

description:
    - "This module allows you to create, modify, or delete LDAP configurations on Perforce Helix Core."
    - "Supports various bind methods (simple, search, sasl) and encryption types."

requirements:
    - "P4Python pip module is required"

seealso:
    - name: Helix Core LDAP
      description: "Manage LDAP configurations"
      link: https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_ldap.html
    - name: P4Python Pip Module
      description: "Python module to interact with Helix Core"
      link: https://pypi.org/project/p4python/

options:
    name:
        description:
            - The name of the LDAP configuration.
        required: true
        type: str
    state:
        description:
            - Whether the LDAP configuration should exist or not.
        choices: [present, absent]
        default: present
        type: str
    host:
        description:
            - The LDAP server hostname or IP address.
        required: true
        type: str
    port:
        description:
            - The LDAP server port.
        required: true
        type: int
    encryption:
        description:
            - The encryption method used to connect to the LDAP server.
        choices: [none, ssl, tls]
        default: none
        type: str
    bind_method:
        description:
            - The method used to bind to the LDAP server.
        choices: [simple, search, sasl]
        default: simple
        type: str
    simple_pattern:
        description:
            - The pattern used for simple binding (e.g., uid=%user%,ou=users,dc=example,dc=com).
            - Required if bind_method is 'simple'.
        type: str
    search_base_dn:
        description:
            - The base DN for searching users.
            - Required if bind_method is 'search'.
        type: str
    search_filter:
        description:
            - The search filter used to find users (e.g., (uid=%user%)).
            - Required if bind_method is 'search'.
        type: str
    search_bind_dn:
        description:
            - The DN used to bind to the LDAP server for searching.
        type: str
    search_passwd:
        description:
            - The password used to bind to the LDAP server for searching.
        type: str
    group_search_filter:
        description:
            - The filter used to search for groups.
        type: str
    group_base_dn:
        description:
            - The base DN for searching groups.
        type: str
    attribute_uid:
        description:
            - The attribute used for the user ID.
        type: str
    attribute_name:
        description:
            - The attribute used for the user's full name.
        type: str
    attribute_email:
        description:
            - The attribute used for the user's email address.
        type: str
    options:
        description:
            - specific options for the LDAP configuration.
        type: list
        elements: str
        choices:
            - downcase
            - nodowncase
            - getattrs
            - nogetattrs
            - realminusername
            - norealminusername
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
            - A user with super user access
            - Can also use 'P4USER' environment variable
        required: true
        type: str
        aliases:
            - p4user
    password:
        description:
            - The super user password
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
- name: Create LDAP configuration with simple bind
  ripclawffb.helix_core.helix_core_ldap:
    name: simple_ldap
    host: ldap.example.com
    port: 389
    encryption: none
    bind_method: simple
    simple_pattern: "uid=%user%,ou=users,dc=example,dc=com"
    options:
      - nodowncase
      - getattrs
    server: '1666'
    user: bruno
    password: ''

- name: Create LDAP configuration with search bind
  ripclawffb.helix_core.helix_core_ldap:
    name: search_ldap
    host: ldap.example.com
    port: 636
    encryption: ssl
    bind_method: search
    search_base_dn: "ou=users,dc=example,dc=com"
    search_filter: "(uid=%user%)"
    search_bind_dn: "cn=admin,dc=example,dc=com"
    search_passwd: "secret_password"
    options:
      - downcase
      - getattrs
    server: '1666'
    user: bruno
    password: ''

- name: Remove LDAP configuration
  ripclawffb.helix_core.helix_core_ldap:
    name: simple_ldap
    state: absent
    host: ldap.example.com
    port: 389
    server: '1666'
    user: bruno
    password: ''
'''

RETURN = r'''
changed:
    description: Whether any changes were made to the LDAP configuration.
    returned: always
    type: bool
    sample: true
ldap_spec:
    description: The LDAP configuration specification.
    returned: always
    type: dict
    sample:
        Name: simple_ldap
        Host: ldap.example.com
        Port: 389
        Encryption: none
        BindMethod: simple
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ripclawffb.helix_core.plugins.module_utils.helix_core_connection import (
    helix_core_connect, helix_core_disconnect, helix_core_connection_argspec
)



def sync_options(existing_options, desired_options):
    """
    Sync options field.
    The spec stores options as a space-separated string.
    We convert lists to space-separated strings, preserving order is tricky so we do set comparison logic 
    but return string for spec.
    """
    if not existing_options:
        existing_options = "nodowncase nogetattrs norealminusername"
    
    current_opts = set(existing_options.split())
    
    # Process desired options
    # If user provides options, we start with defaults and override
    # Note: P4 options are pairs (downcase/nodowncase), so setting one unsets the other.
    
    # Map of option -> opposite
    opposites = {
        "downcase": "nodowncase", "nodowncase": "downcase",
        "getattrs": "nogetattrs", "nogetattrs": "getattrs",
        "realminusername": "norealminusername", "norealminusername": "realminusername"
    }

    if desired_options is None:
        return existing_options

    final_opts = current_opts.copy()
    
    for opt in desired_options:
        if opt in opposites:
            final_opts.discard(opposites[opt])
            final_opts.add(opt)
            
    return " ".join(sorted(list(final_opts)))


def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent']),
        host=dict(type='str'),
        port=dict(type='int'),
        encryption=dict(type='str', default='none', choices=['none', 'ssl', 'tls']),
        bind_method=dict(type='str', default='simple', choices=['simple', 'search', 'sasl']),
        simple_pattern=dict(type='str'),
        search_base_dn=dict(type='str'),
        search_filter=dict(type='str'),
        search_bind_dn=dict(type='str'),
        search_passwd=dict(type='str', no_log=True),
        group_search_filter=dict(type='str'),
        group_base_dn=dict(type='str'),
        attribute_uid=dict(type='str'),
        attribute_name=dict(type='str'),
        attribute_email=dict(type='str'),
        options=dict(type='list', elements='str', choices=[
            'downcase', 'nodowncase',
            'getattrs', 'nogetattrs',
            'realminusername', 'norealminusername'
        ]),
        **helix_core_connection_argspec()
    )

    result = dict(
        changed=False,
        ldap_spec={}
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[
            ('state', 'present', ['host', 'port']),
        ]
    )

    p4 = helix_core_connect(module, 'ansible')

    try:
        ldap_name = module.params['name']
        state = module.params['state']
        
        # Check if LDAP config exists by iterating all ldaps
        try:
            exists = False
            all_ldaps = p4.run_ldaps()
            for l in all_ldaps:
                if l['Name'] == ldap_name:
                    exists = True
                    break
        except Exception:
            exists = False

        if state == 'present':
            # Fields logic
            spec = p4.fetch_ldap(ldap_name) # start with fresh/current spec
            
            changes = []
            
            # Helper to check and set fields only if they differ
            def check_set(field, param_name=None, value=None, type_conv=str):
                # Determine value to set: either from module params or direct value
                if value is None and param_name:
                    value = module.params.get(param_name)
                
                # If value is provided (even empty string), compare and set
                if value is not None:
                    # If current spec value differs from desired value
                    if str(spec.get(field, '')) != str(value):
                        changes.append(field)
                        spec[field] = type_conv(value)

            check_set('Host', 'host')
            check_set('Port', 'port')
            check_set('Encryption', 'encryption')
            check_set('BindMethod', 'bind_method')
            
            # Set relevant fields and clear irrelevant ones based on bind method
            if module.params['bind_method'] == 'simple':
                check_set('SimplePattern', 'simple_pattern')
                # Clear search fields
                check_set('SearchBaseDN', value='')
                check_set('SearchFilter', value='')
                check_set('SearchBindDN', value='')
                check_set('SearchPasswd', value='')
                
            elif module.params['bind_method'] == 'search':
                # Clear simple pattern
                check_set('SimplePattern', value='')
                # Set search fields
                check_set('SearchBaseDN', 'search_base_dn')
                check_set('SearchFilter', 'search_filter')
                check_set('SearchBindDN', 'search_bind_dn')
                check_set('SearchPasswd', 'search_passwd')
                
            elif module.params['bind_method'] == 'sasl':
                # Clear both simple and search fields
                check_set('SimplePattern', value='')
                check_set('SearchBaseDN', value='')
                check_set('SearchFilter', value='')
                check_set('SearchBindDN', value='')
                check_set('SearchPasswd', value='')
                
            check_set('GroupSearchFilter', 'group_search_filter')
            check_set('GroupBaseDN', 'group_base_dn')
            check_set('AttributeUid', 'attribute_uid')
            check_set('AttributeName', 'attribute_name')
            check_set('AttributeEmail', 'attribute_email')
            
            # Handle Options
            if module.params['options'] is not None:
                new_opts = sync_options(spec.get('Options', ''), module.params['options'])
                # Compare as sets to ignore order differences
                current_opts_set = set(spec.get('Options', '').split()) if spec.get('Options', '') else set()
                new_opts_set = set(new_opts.split()) if new_opts else set()
                if current_opts_set != new_opts_set:
                    changes.append('Options')
                    spec['Options'] = new_opts
                    
            if not exists:
                changes.append('Creation')
            
            if changes:
                if not module.check_mode:
                    p4.save_ldap(spec)
                result['changed'] = True

            # Always return the spec
            result['ldap_spec'] = spec

        elif state == 'absent':
            if exists:
                if not module.check_mode:
                    p4.delete_ldap(ldap_name)
                result['changed'] = True

    except Exception as e:
        module.fail_json(msg="Error: {0}".format(e), **result)

    helix_core_disconnect(module, p4)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
