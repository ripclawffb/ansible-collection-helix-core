"""
Unit tests for helix_core inventory plugin.

Mocks P4Python and Ansible internals to test inventory parse() logic.
Run with: pytest test/unit/test_helix_core_inventory.py -v
"""

import sys
import os
import pytest
from unittest.mock import patch, MagicMock, PropertyMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


# We need to test the helper methods and parse logic without a full ansible
# install. Import the module after mocking ansible dependencies if needed.
# The ansible package may or may not be installed, so we handle both cases.
try:
    from plugins.inventory.helix_core import InventoryModule
except ImportError:
    # If ansible is not installed, mock the required modules before importing
    import types

    # Create mock ansible module hierarchy
    ansible_mock = types.ModuleType('ansible')
    ansible_mock.errors = types.ModuleType('ansible.errors')
    ansible_mock.plugins = types.ModuleType('ansible.plugins')
    ansible_mock.plugins.inventory = types.ModuleType('ansible.plugins.inventory')

    # Create mock classes
    class MockAnsibleParserError(Exception):
        pass

    class MockBaseInventoryPlugin:
        def __init__(self):
            pass

        def verify_file(self, path):
            return True

        def parse(self, inventory, loader, path, cache=True):
            pass

        def _read_config_data(self, path):
            pass

        def get_option(self, key):
            return None

    class MockConstructable:
        def _set_composite_vars(self, *args, **kwargs):
            pass

        def _add_host_to_composed_groups(self, *args, **kwargs):
            pass

        def _add_host_to_keyed_groups(self, *args, **kwargs):
            pass

    class MockCacheable:
        pass

    ansible_mock.errors.AnsibleParserError = MockAnsibleParserError
    ansible_mock.plugins.inventory.BaseInventoryPlugin = MockBaseInventoryPlugin
    ansible_mock.plugins.inventory.Constructable = MockConstructable
    ansible_mock.plugins.inventory.Cacheable = MockCacheable

    sys.modules['ansible'] = ansible_mock
    sys.modules['ansible.errors'] = ansible_mock.errors
    sys.modules['ansible.plugins'] = ansible_mock.plugins
    sys.modules['ansible.plugins.inventory'] = ansible_mock.plugins.inventory

    from plugins.inventory.helix_core import InventoryModule


@pytest.fixture
def inventory_plugin():
    plugin = InventoryModule()
    plugin.inventory = MagicMock()
    plugin.inventory.add_group.return_value = 'test_group'
    return plugin


@pytest.fixture
def single_server():
    return [
        {
            'ServerID': 'master.1',
            'ServerAddress': 'ssl:commit.example.com:1666',
            'Services': 'commit-server',
            'Description': 'Main commit server',
        }
    ]


@pytest.fixture
def multi_servers():
    return [
        {
            'ServerID': 'master.1',
            'ServerAddress': 'ssl:commit.example.com:1666',
            'Services': 'commit-server',
            'Description': 'Main commit server',
        },
        {
            'ServerID': 'edge-chicago',
            'ServerAddress': 'ssl:edge-chi.example.com:1666',
            'Services': 'edge-server',
            'Description': 'Chicago edge server',
            'ReplicatingFrom': 'master.1',
        },
        {
            'ServerID': 'edge-london',
            'ServerAddress': 'ssl:edge-lon.example.com:1666',
            'Services': 'edge-server',
            'Description': 'London edge server',
            'ReplicatingFrom': 'master.1',
        },
    ]


class TestVerifyFile:
    def test_valid_extension_yml(self, inventory_plugin):
        assert inventory_plugin.verify_file('/path/to/inventory.helix_core.yml') is True

    def test_valid_extension_yaml(self, inventory_plugin):
        assert inventory_plugin.verify_file('/path/to/inventory.helix_core.yaml') is True

    def test_invalid_extension(self, inventory_plugin):
        assert inventory_plugin.verify_file('/path/to/inventory.yml') is False

    def test_no_extension(self, inventory_plugin):
        assert inventory_plugin.verify_file('/path/to/inventory') is False


class TestExtractHost:
    def test_ssl_host_port(self, inventory_plugin):
        assert inventory_plugin._extract_host('ssl:edge.example.com:1666') == 'edge.example.com'

    def test_host_port(self, inventory_plugin):
        assert inventory_plugin._extract_host('commit.example.com:1666') == 'commit.example.com'

    def test_host_only(self, inventory_plugin):
        assert inventory_plugin._extract_host('commit.example.com') == 'commit.example.com'

    def test_tcp_prefix(self, inventory_plugin):
        assert inventory_plugin._extract_host('tcp:server:1666') == 'server'

    def test_empty(self, inventory_plugin):
        assert inventory_plugin._extract_host('') is None

    def test_none(self, inventory_plugin):
        assert inventory_plugin._extract_host(None) is None


class TestExtractPort:
    def test_ssl_host_port(self, inventory_plugin):
        assert inventory_plugin._extract_port('ssl:edge.example.com:1666') == '1666'

    def test_host_port(self, inventory_plugin):
        assert inventory_plugin._extract_port('commit.example.com:1666') == '1666'

    def test_no_port(self, inventory_plugin):
        assert inventory_plugin._extract_port('commit.example.com') is None

    def test_empty(self, inventory_plugin):
        assert inventory_plugin._extract_port('') is None


class TestGetServerType:
    def test_commit_server(self, inventory_plugin):
        assert inventory_plugin._get_server_type({'Services': 'commit-server'}) == 'commit-server'

    def test_edge_server(self, inventory_plugin):
        assert inventory_plugin._get_server_type({'Services': 'edge-server'}) == 'edge-server'

    def test_empty_services(self, inventory_plugin):
        assert inventory_plugin._get_server_type({'Services': ''}) == 'commit-server'

    def test_local_services(self, inventory_plugin):
        assert inventory_plugin._get_server_type({'Services': 'local'}) == 'commit-server'

    def test_no_services(self, inventory_plugin):
        assert inventory_plugin._get_server_type({}) == 'commit-server'


class TestParse:
    def _run_parse(self, inventory_plugin, mock_p4, servers, options_override=None):
        mock_p4.run_servers.return_value = servers

        defaults = {
            'server_types': [],
            'include_commit': True,
            'strict': False,
            'compose': {},
            'groups': {},
            'keyed_groups': [],
        }
        if options_override:
            defaults.update(options_override)

        with patch.object(inventory_plugin, '_connect', return_value=mock_p4):
            with patch.object(inventory_plugin, '_read_config_data'):
                with patch.object(inventory_plugin, 'get_option',
                                  side_effect=lambda k: defaults.get(k)):
                    inventory_plugin.parse(
                        inventory_plugin.inventory,
                        MagicMock(),
                        '/path/to/inventory.helix_core.yml'
                    )

    def test_single_server(self, inventory_plugin, single_server):
        mock_p4 = MagicMock()
        self._run_parse(inventory_plugin, mock_p4, single_server)

        inventory_plugin.inventory.add_host.assert_called_once_with('master.1')
        inventory_plugin.inventory.set_variable.assert_any_call(
            'master.1', 'ansible_host', 'commit.example.com'
        )
        inventory_plugin.inventory.set_variable.assert_any_call(
            'master.1', 'server_type', 'commit-server'
        )
        mock_p4.disconnect.assert_called_once()

    def test_multiple_servers(self, inventory_plugin, multi_servers):
        mock_p4 = MagicMock()
        self._run_parse(inventory_plugin, mock_p4, multi_servers)

        assert inventory_plugin.inventory.add_host.call_count == 3
        inventory_plugin.inventory.add_host.assert_any_call('master.1')
        inventory_plugin.inventory.add_host.assert_any_call('edge-chicago')
        inventory_plugin.inventory.add_host.assert_any_call('edge-london')

    def test_server_type_filter(self, inventory_plugin, multi_servers):
        mock_p4 = MagicMock()
        self._run_parse(inventory_plugin, mock_p4, multi_servers,
                        options_override={'server_types': ['edge-server']})

        assert inventory_plugin.inventory.add_host.call_count == 2
        inventory_plugin.inventory.add_host.assert_any_call('edge-chicago')
        inventory_plugin.inventory.add_host.assert_any_call('edge-london')

    def test_include_commit_false(self, inventory_plugin, multi_servers):
        mock_p4 = MagicMock()
        self._run_parse(inventory_plugin, mock_p4, multi_servers,
                        options_override={'include_commit': False})

        assert inventory_plugin.inventory.add_host.call_count == 2
        inventory_plugin.inventory.add_host.assert_any_call('edge-chicago')
        inventory_plugin.inventory.add_host.assert_any_call('edge-london')

    def test_connection_error(self, inventory_plugin):
        from ansible.errors import AnsibleParserError

        with patch.object(inventory_plugin, '_connect',
                          side_effect=AnsibleParserError('Connection failed')):
            with patch.object(inventory_plugin, '_read_config_data'):
                with pytest.raises(AnsibleParserError, match='Connection failed'):
                    inventory_plugin.parse(
                        inventory_plugin.inventory,
                        MagicMock(),
                        '/path/to/inventory.helix_core.yml'
                    )

    def test_host_variables(self, inventory_plugin, multi_servers):
        mock_p4 = MagicMock()
        self._run_parse(inventory_plugin, mock_p4, multi_servers)

        inventory_plugin.inventory.set_variable.assert_any_call(
            'edge-chicago', 'replicatingfrom', 'master.1'
        )
        inventory_plugin.inventory.set_variable.assert_any_call(
            'edge-chicago', 'p4_port_number', '1666'
        )

    def test_empty_server_list(self, inventory_plugin):
        mock_p4 = MagicMock()
        self._run_parse(inventory_plugin, mock_p4, [])

        inventory_plugin.inventory.add_host.assert_not_called()

    def test_server_without_id_skipped(self, inventory_plugin):
        mock_p4 = MagicMock()
        servers = [{'ServerAddress': 'ssl:host:1666', 'Services': 'edge-server'}]
        self._run_parse(inventory_plugin, mock_p4, servers)

        inventory_plugin.inventory.add_host.assert_not_called()

    def test_groups_created(self, inventory_plugin, multi_servers):
        mock_p4 = MagicMock()
        self._run_parse(inventory_plugin, mock_p4, multi_servers)

        # Should create groups for server types
        inventory_plugin.inventory.add_group.assert_any_call('commit_server')
        inventory_plugin.inventory.add_group.assert_any_call('edge_server')
