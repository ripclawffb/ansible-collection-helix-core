"""
Unit tests for helix_core_server run_module().

Mocks P4 and AnsibleModule to test all branching logic.
Run with: pytest test/unit/test_helix_core_server_module.py -v
"""

import sys
import os
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


class AnsibleExitJson(Exception):
    pass


class AnsibleFailJson(Exception):
    pass


def exit_json_side_effect(**kwargs):
    raise AnsibleExitJson(kwargs)


def fail_json_side_effect(**kwargs):
    raise AnsibleFailJson(kwargs)


@pytest.fixture
def mock_module():
    module = MagicMock()
    module.params = {
        'state': 'present',
        'serverid': 'commit',
        'description': 'Commit server',
        'services': 'standard',
        'type': 'server',
        'options': 'nomandatory',
        'address': None,
        'allowedaddresses': None,
        'archivedatafilter': None,
        'clientdatafilter': None,
        'distributedconfig': None,
        'externaladdress': None,
        'name': None,
        'replicatingfrom': None,
        'revisiondatafilter': None,
        'serviceuser': None,
        'updatedcachedrepos': None,
        'server': '1666',
        'user': 'admin',
        'password': 'pass',
        'charset': 'none',
    }
    module.check_mode = False
    module._diff = False
    module.exit_json = MagicMock(side_effect=exit_json_side_effect)
    module.fail_json = MagicMock(side_effect=fail_json_side_effect)
    return module


@pytest.fixture
def mock_p4():
    p4 = MagicMock()
    p4.connected.return_value = True
    return p4


@pytest.fixture
def existing_server_spec():
    return {
        'ServerID': 'commit',
        'Description': 'Commit server',
        'Services': 'standard',
        'Type': 'server',
        'Options': 'nomandatory',
    }


class TestServerCreate:
    def test_create_new_server(self, mock_module, mock_p4, existing_server_spec):
        mock_p4.fetch_server.return_value = existing_server_spec
        mock_p4.run.return_value = []  # no existing servers

        with patch('plugins.modules.helix_core_server.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_server.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_server.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_server import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'created'
        assert result['server_spec'] is not None
        mock_p4.save_server.assert_called_once()

    def test_create_check_mode(self, mock_module, mock_p4, existing_server_spec):
        mock_module.check_mode = True
        mock_p4.fetch_server.return_value = existing_server_spec
        mock_p4.run.return_value = []

        with patch('plugins.modules.helix_core_server.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_server.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_server.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_server import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'created'
        mock_p4.save_server.assert_not_called()


class TestServerUpdate:
    def test_no_changes(self, mock_module, mock_p4, existing_server_spec):
        mock_p4.fetch_server.return_value = existing_server_spec
        mock_p4.run.return_value = [{'ServerID': 'commit'}]

        with patch('plugins.modules.helix_core_server.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_server.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_server.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_server import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert result['action'] == 'unchanged'
        assert result['changes'] == []
        assert result['server_spec'] == existing_server_spec

    def test_with_changes(self, mock_module, mock_p4, existing_server_spec):
        mock_module.params['description'] = 'Updated server'
        mock_p4.fetch_server.return_value = existing_server_spec
        mock_p4.run.return_value = [{'ServerID': 'commit'}]

        with patch('plugins.modules.helix_core_server.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_server.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_server.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_server import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'updated'
        assert len(result['changes']) > 0
        assert result['changes'][0]['field'] == 'Description'
        mock_p4.save_server.assert_called_once()


class TestServerDelete:
    def test_delete_existing(self, mock_module, mock_p4, existing_server_spec):
        mock_module.params['state'] = 'absent'
        mock_p4.fetch_server.return_value = existing_server_spec
        mock_p4.run.return_value = [{'ServerID': 'commit'}]

        with patch('plugins.modules.helix_core_server.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_server.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_server.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_server import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'deleted'
        mock_p4.delete_server.assert_called_once_with('commit')

    def test_delete_nonexistent(self, mock_module, mock_p4):
        mock_module.params['state'] = 'absent'
        mock_p4.run.return_value = []

        with patch('plugins.modules.helix_core_server.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_server.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_server.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_server import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert result['action'] == 'unchanged'

    def test_delete_check_mode(self, mock_module, mock_p4, existing_server_spec):
        mock_module.params['state'] = 'absent'
        mock_module.check_mode = True
        mock_p4.fetch_server.return_value = existing_server_spec
        mock_p4.run.return_value = [{'ServerID': 'commit'}]

        with patch('plugins.modules.helix_core_server.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_server.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_server.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_server import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'deleted'
        mock_p4.delete_server.assert_not_called()


class TestServerDiff:
    def test_create_with_diff(self, mock_module, mock_p4, existing_server_spec):
        mock_module._diff = True
        mock_p4.fetch_server.return_value = existing_server_spec
        mock_p4.run.return_value = []

        with patch('plugins.modules.helix_core_server.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_server.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_server.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_server import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert 'diff' in result
        assert result['diff']['before'] == ''
        assert 'Description' in result['diff']['after']

    def test_update_with_diff(self, mock_module, mock_p4, existing_server_spec):
        mock_module._diff = True
        mock_module.params['description'] = 'Updated server'
        mock_p4.fetch_server.return_value = existing_server_spec
        mock_p4.run.return_value = [{'ServerID': 'commit'}]

        with patch('plugins.modules.helix_core_server.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_server.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_server.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_server import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert 'diff' in result
        assert 'Commit server' in result['diff']['before']
        assert 'Updated server' in result['diff']['after']

    def test_delete_with_diff(self, mock_module, mock_p4, existing_server_spec):
        mock_module._diff = True
        mock_module.params['state'] = 'absent'
        mock_p4.fetch_server.return_value = existing_server_spec
        mock_p4.run.return_value = [{'ServerID': 'commit'}]

        with patch('plugins.modules.helix_core_server.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_server.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_server.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_server import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert 'diff' in result
        assert 'Description' in result['diff']['before']
        assert result['diff']['after'] == ''

    def test_no_diff_when_disabled(self, mock_module, mock_p4, existing_server_spec):
        mock_module._diff = False
        mock_p4.fetch_server.return_value = existing_server_spec
        mock_p4.run.return_value = []

        with patch('plugins.modules.helix_core_server.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_server.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_server.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_server import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert 'diff' not in result

    def test_check_mode_create_with_diff(self, mock_module, mock_p4, existing_server_spec):
        mock_module._diff = True
        mock_module.check_mode = True
        mock_p4.fetch_server.return_value = existing_server_spec
        mock_p4.run.return_value = []

        with patch('plugins.modules.helix_core_server.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_server.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_server.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_server import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert 'diff' in result
        assert result['diff']['before'] == ''
        mock_p4.save_server.assert_not_called()

    def test_check_mode_update_with_diff(self, mock_module, mock_p4, existing_server_spec):
        mock_module._diff = True
        mock_module.check_mode = True
        mock_module.params['description'] = 'Updated server'
        mock_p4.fetch_server.return_value = existing_server_spec
        mock_p4.run.return_value = [{'ServerID': 'commit'}]

        with patch('plugins.modules.helix_core_server.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_server.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_server.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_server import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert 'diff' in result
        assert 'Commit server' in result['diff']['before']
        assert 'Updated server' in result['diff']['after']
        mock_p4.save_server.assert_not_called()

