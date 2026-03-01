#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Asif Shaikh (@ripclawffb) <ripclaw_ffb@hotmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
name: helix_core
short_description: Perforce Helix Core dynamic inventory plugin
description:
    - Discovers Perforce server topology by querying C(p4 servers).
    - Each registered server becomes an Ansible host, keyed by its C(ServerID).
    - Hosts are automatically grouped by server type (commit, edge, replica, etc.).
    - Supports Constructable features like C(compose), C(keyed_groups), and C(groups).
    - Ideal for federated Perforce environments with commit + edge/replica servers.
version_added: "1.3.0"
requirements:
    - P4Python pip module is required
extends_documentation_fragment:
    - constructed
options:
    plugin:
        description: Token to ensure this is an inventory plugin file.
        required: true
        choices: ['ripclawffb.helix_core.helix_core']
    server:
        description:
            - The hostname/ip and port of the Perforce server (e.g. C(ssl:perforce:1666)).
            - Can also use C(P4PORT) environment variable.
        required: true
        type: str
        env:
            - name: P4PORT
    user:
        description:
            - A Perforce user with permission to run C(p4 servers).
            - Can also use C(P4USER) environment variable.
        required: true
        type: str
        env:
            - name: P4USER
    password:
        description:
            - The login password for the Perforce user.
            - Can also use C(P4PASSWD) environment variable.
        required: true
        type: str
        env:
            - name: P4PASSWD
    charset:
        description:
            - Character set used for translation of unicode files.
            - Can also use C(P4CHARSET) environment variable.
        default: none
        type: str
        env:
            - name: P4CHARSET
    server_types:
        description:
            - Optional list of server types to include in the inventory.
            - Valid types include C(commit-server), C(edge-server), C(replica),
              C(forwarding-replica), C(build-server), C(depot-master), etc.
            - If omitted, all server types are included.
        type: list
        elements: str
        default: []
    include_commit:
        description:
            - Whether to include the commit server itself in the inventory.
            - Only relevant when the commit server has a registered server spec.
        type: bool
        default: true
'''

EXAMPLES = r'''
# Minimal inventory file — discover all servers
# inventory.helix_core.yml
plugin: ripclawffb.helix_core.helix_core
server: ssl:commit-server:1666
user: admin
password: "{{ vault_p4_password }}"

# Filter to only edge servers and group by type
plugin: ripclawffb.helix_core.helix_core
server: ssl:commit-server:1666
user: admin
password: "{{ vault_p4_password }}"
server_types:
  - edge-server
  - commit-server
keyed_groups:
  - key: server_type
    prefix: p4
    separator: "_"

# Use compose to set ansible_host from the server address
plugin: ripclawffb.helix_core.helix_core
server: ssl:commit-server:1666
user: admin
password: "{{ vault_p4_password }}"
compose:
  ansible_port: 22
'''

import re
import traceback

from ansible.errors import AnsibleParserError
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable

try:
    from P4 import P4
    HAS_P4 = True
except ImportError:
    P4_IMP_ERR = traceback.format_exc()
    HAS_P4 = False


class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):
    """Perforce Helix Core dynamic inventory plugin."""

    NAME = 'ripclawffb.helix_core.helix_core'

    def verify_file(self, path):
        """Verify that the inventory source file is valid."""
        valid = False
        if super().verify_file(path):
            if path.endswith(('.helix_core.yml', '.helix_core.yaml')):
                valid = True
        return valid

    def _connect(self):
        """Create a standalone P4 connection (not coupled to AnsibleModule)."""
        if not HAS_P4:
            raise AnsibleParserError(
                'The P4Python library is required. '
                'Install it with: pip install p4python'
            )

        try:
            p4 = P4()
            p4.prog = 'ansible-inventory'
            p4.port = self.get_option('server')
            p4.user = self.get_option('user')
            p4.password = self.get_option('password')
            p4.charset = self.get_option('charset')
            p4.connect()
            p4.run_login()
            return p4
        except Exception as e:
            raise AnsibleParserError(
                f'Failed to connect to Perforce server: {e}'
            )

    def _extract_host(self, address):
        """Extract hostname from a P4 ServerAddress like 'ssl:host.example.com:1666'."""
        if not address:
            return None

        # Handle formats: ssl:host:port, host:port, host
        # Strip protocol prefix (ssl:, tcp:, etc.)
        match = re.match(r'^(?:\w+:)?([^:]+)(?::(\d+))?$', address)
        if match:
            return match.group(1)
        return address

    def _extract_port(self, address):
        """Extract port from a P4 ServerAddress like 'ssl:host.example.com:1666'."""
        if not address:
            return None

        match = re.match(r'^(?:\w+:)?[^:]+:(\d+)$', address)
        if match:
            return match.group(1)
        return None

    def _get_server_type(self, server):
        """Determine the server type from the Services field."""
        services = server.get('Services', '')
        if not services or services == 'local':
            return 'commit-server'
        return services

    def parse(self, inventory, loader, path, cache=True):
        """Parse the inventory source and populate the inventory."""
        super().parse(inventory, loader, path, cache)
        self._read_config_data(path)

        p4 = self._connect()

        try:
            servers = p4.run_servers()
        except Exception as e:
            raise AnsibleParserError(
                f'Failed to retrieve server list: {e}'
            )
        finally:
            try:
                p4.disconnect()
            except Exception:
                pass

        server_types_filter = self.get_option('server_types')
        include_commit = self.get_option('include_commit')

        for server in servers:
            server_id = server.get('ServerID', '')
            if not server_id:
                continue

            server_type = self._get_server_type(server)

            # Apply server_types filter
            if server_types_filter and server_type not in server_types_filter:
                continue

            # Apply include_commit filter
            if not include_commit and server_type == 'commit-server':
                continue

            address = server.get('ServerAddress', '')
            hostname = self._extract_host(address)
            port = self._extract_port(address)

            # Add host to inventory
            self.inventory.add_host(server_id)

            # Set ansible_host from the server address
            if hostname:
                self.inventory.set_variable(server_id, 'ansible_host', hostname)

            # Set host variables
            variables = {
                'server_id': server_id,
                'server_address': address,
                'server_type': server_type,
                'services': server.get('Services', ''),
                'description': server.get('Description', ''),
                'p4port': address,
            }

            # Add optional fields if present
            for field in ['ReplicatingFrom', 'Type', 'Name', 'ExternalAddress',
                          'DistributedConfig']:
                if field in server:
                    variables[field.lower()] = server[field]

            if port:
                variables['p4_port_number'] = port

            for var_name, var_val in variables.items():
                self.inventory.set_variable(server_id, var_name, var_val)

            # Add to server type group
            group_name = self.inventory.add_group(server_type.replace('-', '_'))
            self.inventory.add_child(group_name, server_id)

            # Support Constructable features (compose, keyed_groups, groups)
            strict = self.get_option('strict')

            self._set_composite_vars(
                self.get_option('compose'),
                variables,
                server_id,
                strict=strict,
            )

            self._add_host_to_composed_groups(
                self.get_option('groups'),
                variables,
                server_id,
                strict=strict,
            )

            self._add_host_to_keyed_groups(
                self.get_option('keyed_groups'),
                variables,
                server_id,
                strict=strict,
            )
