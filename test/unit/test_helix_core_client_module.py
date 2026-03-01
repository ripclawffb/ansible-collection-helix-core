"""
Unit tests for helix_core_client run_module().

Mocks P4 and AnsibleModule to test all branching logic.
Run with: pytest test/unit/test_helix_core_client_module.py -v
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
        'name': 'test_client',
        'description': 'Test client',
        'host': 'workstation01',
        'root': '/tmp/test_client',
        'altroots': None,
        'view': ['//depot/... //test_client/depot/...'],
        'lineend': 'local',
        'options': 'noallwrite noclobber nocompress unlocked nomodtime normdir',
        'submitoptions': 'submitunchanged',
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
def existing_client_spec():
    return {
        'Client': 'test_client',
        'Access': '2024/01/01 00:00:00',
        'Description': 'Test client',
        'Host': 'workstation01',
        'Root': '/tmp/test_client',
        'View': ['//depot/... //test_client/depot/...'],
        'LineEnd': 'local',
        'Options': 'noallwrite noclobber nocompress unlocked nomodtime normdir',
        'SubmitOptions': 'submitunchanged',
    }


@pytest.fixture
def new_client_spec():
    return {
        'Client': 'test_client',
        'Description': 'Test client',
        'Host': 'workstation01',
        'Root': '/tmp/test_client',
    }


class TestClientCreate:
    def test_create_new_client(self, mock_module, mock_p4, new_client_spec):
        mock_p4.fetch_client.return_value = new_client_spec

        with patch('plugins.modules.helix_core_client.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_client.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_client.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_client import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'created'
        assert result['client_spec'] is not None
        mock_p4.save_client.assert_called_once()

    def test_create_check_mode(self, mock_module, mock_p4, new_client_spec):
        mock_module.check_mode = True
        mock_p4.fetch_client.return_value = new_client_spec

        with patch('plugins.modules.helix_core_client.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_client.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_client.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_client import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'created'
        mock_p4.save_client.assert_not_called()


class TestClientUpdate:
    def test_no_changes(self, mock_module, mock_p4, existing_client_spec):
        mock_p4.fetch_client.return_value = existing_client_spec

        with patch('plugins.modules.helix_core_client.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_client.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_client.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_client import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert result['action'] == 'unchanged'
        assert result['changes'] == []
        assert result['client_spec'] == existing_client_spec
        mock_p4.save_client.assert_not_called()

    def test_with_changes(self, mock_module, mock_p4, existing_client_spec):
        mock_module.params['description'] = 'Updated description'
        mock_p4.fetch_client.return_value = existing_client_spec

        with patch('plugins.modules.helix_core_client.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_client.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_client.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_client import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'updated'
        assert len(result['changes']) > 0
        assert result['changes'][0]['field'] == 'Description'
        mock_p4.save_client.assert_called_once()

    def test_with_changes_check_mode(self, mock_module, mock_p4, existing_client_spec):
        mock_module.check_mode = True
        mock_module.params['description'] = 'Updated description'
        mock_p4.fetch_client.return_value = existing_client_spec

        with patch('plugins.modules.helix_core_client.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_client.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_client.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_client import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'updated'
        assert len(result['changes']) > 0
        mock_p4.save_client.assert_not_called()

    def test_noaltsync_option_idempotency(self, mock_module, mock_p4, existing_client_spec):
        """Helix Core 23.1+ adds noaltsync to Options — should still be idempotent."""
        existing_client_spec['Options'] = 'noallwrite noclobber nocompress unlocked nomodtime normdir noaltsync'
        mock_p4.fetch_client.return_value = existing_client_spec

        with patch('plugins.modules.helix_core_client.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_client.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_client.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_client import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert result['action'] == 'unchanged'
        assert result['changes'] == []


class TestClientDelete:
    def test_delete_existing(self, mock_module, mock_p4, existing_client_spec):
        mock_module.params['state'] = 'absent'
        mock_p4.fetch_client.return_value = existing_client_spec

        with patch('plugins.modules.helix_core_client.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_client.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_client.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_client import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'deleted'
        mock_p4.delete_client.assert_called_once_with('-f', 'test_client')

    def test_delete_nonexistent(self, mock_module, mock_p4, new_client_spec):
        mock_module.params['state'] = 'absent'
        mock_p4.fetch_client.return_value = new_client_spec

        with patch('plugins.modules.helix_core_client.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_client.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_client.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_client import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert result['action'] == 'unchanged'
        mock_p4.delete_client.assert_not_called()

    def test_delete_check_mode(self, mock_module, mock_p4, existing_client_spec):
        mock_module.params['state'] = 'absent'
        mock_module.check_mode = True
        mock_p4.fetch_client.return_value = existing_client_spec

        with patch('plugins.modules.helix_core_client.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_client.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_client.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_client import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'deleted'
        mock_p4.delete_client.assert_not_called()
