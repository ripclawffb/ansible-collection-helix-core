"""
Unit tests for helix_core_protect run_module() — absent/entry scenarios.

Mocks P4 and AnsibleModule to test state=absent branching logic.
Run with: pytest test/unit/test_helix_core_protect_module.py -v
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
        'state': 'absent',
        'mode': 'entry',
        'position': 'end',
        'protections': [
            {'access': 'write', 'type': 'user', 'name': 'alice', 'host': '*', 'path': '//...'},
        ],
        'server': '1666',
        'user': 'admin',
        'password': 'pass',
        'charset': 'none',
    }
    module.check_mode = False
    module._diff = False
    module.exit_json = MagicMock(side_effect=exit_json_side_effect)
    module.fail_json = MagicMock(side_effect=fail_json_side_effect)
    module.warn = MagicMock()
    return module


@pytest.fixture
def mock_p4():
    p4 = MagicMock()
    p4.connected.return_value = True
    return p4


class TestProtectAbsentEntry:
    def test_remove_existing_entry(self, mock_module, mock_p4):
        mock_p4.fetch_protect.return_value = {
            'Protections': [
                'write user alice * //...',
                'read user bob * //...',
            ]
        }

        with patch('plugins.modules.helix_core_protect.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_protect.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_protect.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_protect import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'updated'
        assert len(result['changes']['removed']) == 1
        assert result['changes']['removed'][0]['name'] == 'alice'
        mock_p4.save_protect.assert_called_once()

    def test_remove_nonexistent_entry(self, mock_module, mock_p4):
        """Removing an entry that doesn't exist should be idempotent."""
        mock_p4.fetch_protect.return_value = {
            'Protections': [
                'read user bob * //...',
            ]
        }

        with patch('plugins.modules.helix_core_protect.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_protect.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_protect.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_protect import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert result['action'] == 'unchanged'
        mock_p4.save_protect.assert_not_called()

    def test_remove_check_mode(self, mock_module, mock_p4):
        mock_module.check_mode = True
        mock_p4.fetch_protect.return_value = {
            'Protections': [
                'write user alice * //...',
                'read user bob * //...',
            ]
        }

        with patch('plugins.modules.helix_core_protect.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_protect.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_protect.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_protect import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'updated'
        mock_p4.save_protect.assert_not_called()

    def test_remove_p4_error(self, mock_module, mock_p4):
        mock_p4.fetch_protect.return_value = {
            'Protections': [
                'write user alice * //...',
            ]
        }
        mock_p4.save_protect.side_effect = Exception('Permission denied')

        with patch('plugins.modules.helix_core_protect.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_protect.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_protect.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_protect import run_module
                    with pytest.raises(AnsibleFailJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert 'Permission denied' in result['msg']


class TestProtectAbsentReplaceDenied:
    def test_replace_absent_blocked(self, mock_module, mock_p4):
        """state=absent + mode=replace should be blocked for security."""
        mock_module.params['mode'] = 'replace'

        with patch('plugins.modules.helix_core_protect.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_protect.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_protect.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_protect import run_module
                    with pytest.raises(AnsibleFailJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert 'not allowed for security reasons' in result['msg']
