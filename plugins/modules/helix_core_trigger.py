#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Asif Shaikh (@ripclawffb) <ripclaw_ffb@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: helix_core_trigger

short_description: Manage triggers on Perforce Helix Core

description:
    - "Triggers are user-defined scripts executed by the Perforce server when specific operations occur."
    - "This module manages the entire triggers table as a unit."
    - "This module supports check mode."

requirements:
    - "P4Python pip module is required"

seealso:
    - name: Helix Core Triggers
      description: "Configure trigger definitions"
      link: https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_triggers.html
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
            - Determines if the trigger entries are set or cleared
            - C(present) replaces the triggers with the specified entries
            - C(absent) clears all entries from the triggers table
        type: str
    triggers:
        description:
            - List of trigger entries
            - Each entry must have C(name), C(type), C(path), and C(command) keys
            - Required when state is C(present)
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - A unique name for the trigger
                type: str
                required: true
            type:
                description:
                    - The trigger type (e.g., change-submit, change-content, change-commit, form-save, auth-check)
                type: str
                required: true
            path:
                description:
                    - The depot path pattern for changelist triggers, or form type for form triggers
                type: str
                required: true
            command:
                description:
                    - The command to execute when the trigger fires
                type: str
                required: true

extends_documentation_fragment:
    - ripclawffb.helix_core.helix_core_connection

author:
    - Asif Shaikh (@ripclawffb)
'''

EXAMPLES = '''
# Set trigger entries
- name: Configure triggers
  ripclawffb.helix_core.helix_core_trigger:
    state: present
    triggers:
      - name: check_submit
        type: change-submit
        path: //depot/...
        command: "/scripts/validate.sh %changelist%"
      - name: notify_commit
        type: change-commit
        path: //depot/...
        command: "/scripts/notify.sh %changelist% %user%"
    server: '1666'
    user: bruno
    charset: auto
    password: ''

# Clear all trigger entries
- name: Clear triggers
  ripclawffb.helix_core.helix_core_trigger:
    state: absent
    server: '1666'
    user: bruno
    charset: auto
    password: ''
'''

RETURN = r'''
changed:
    description: Whether any changes were made to the triggers.
    returned: always
    type: bool
    sample: true
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ripclawffb.helix_core.plugins.module_utils.helix_core_connection import (
    helix_core_connect, helix_core_disconnect, helix_core_connection_argspec
)


def triggers_to_list(triggers_spec):
    """Convert triggers spec to a list of tuples for comparison."""
    if 'Triggers' not in triggers_spec or triggers_spec['Triggers'] is None:
        return []
    entries = []
    for entry in triggers_spec['Triggers']:
        # Each entry is a string like "name type path command"
        # Format: "name type path command" where command can contain spaces and be quoted
        parts = entry.split(None, 3)
        if len(parts) >= 4:
            command = parts[3]
            # Strip quotes from command if present
            if command.startswith('"') and command.endswith('"'):
                command = command[1:-1]
            entries.append((parts[0], parts[1], parts[2], command))
        elif len(parts) == 3:
            # Some triggers may not have a command with spaces
            entries.append((parts[0], parts[1], parts[2], ''))
    return entries


def list_to_triggers(entries):
    """Convert a list of dicts to triggers format."""
    result = []
    for e in entries:
        command = e['command']
        # Quote command if it contains spaces
        if ' ' in command and not (command.startswith('"') and command.endswith('"')):
            command = '"{0}"'.format(command)
        result.append("{0} {1} {2} {3}".format(e['name'], e['type'], e['path'], command))
    return result


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        state=dict(type='str', default='present', choices=['present', 'absent']),
        triggers=dict(type='list', elements='dict', default=None, options=dict(
            name=dict(type='str', required=True),
            type=dict(type='str', required=True),
            path=dict(type='str', required=True),
            command=dict(type='str', required=True),
        )),
        **helix_core_connection_argspec()
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,

        required_if=[
            ('state', 'present', ['triggers']),
        ]
    )

    # connect to helix
    p4 = helix_core_connect(module, 'ansible')

    try:
        # get existing triggers
        p4_triggers_spec = p4.fetch_triggers()
        current_entries = triggers_to_list(p4_triggers_spec)

        # format entries for diff
        def entries_to_diff(entries):
            return '\n'.join('{0} {1} {2} {3}'.format(*e) for e in entries) + '\n' if entries else ''

        if module.params['state'] == 'present':
            # Build desired entries list
            desired_entries = [(e['name'], e['type'], e['path'], e['command']) for e in module.params['triggers']]

            # Compare current vs desired
            if current_entries != desired_entries:
                before = entries_to_diff(current_entries)

                if not module.check_mode:
                    p4_triggers_spec['Triggers'] = list_to_triggers(module.params['triggers'])
                    p4.save_triggers(p4_triggers_spec)
                result['changed'] = True

                if module._diff:
                    result['diff'] = {'before': before, 'after': entries_to_diff(desired_entries)}

        elif module.params['state'] == 'absent':
            # Clear triggers if it has entries
            if current_entries:
                before = entries_to_diff(current_entries)

                if not module.check_mode:
                    p4_triggers_spec['Triggers'] = []
                    p4.save_triggers(p4_triggers_spec)
                result['changed'] = True

                if module._diff:
                    result['diff'] = {'before': before, 'after': ''}

    except Exception as e:
        module.fail_json(msg="Error: {0}".format(e), **result)

    helix_core_disconnect(module, p4)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
