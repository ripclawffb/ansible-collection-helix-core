"""
Unit tests for helix_core_trigger run_module() — absent/clear scenarios.

Mocks P4 and AnsibleModule to test state=absent branching logic.
Run with: pytest test/unit/test_helix_core_trigger_module.py -v
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
        'triggers': None,
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


class TestTriggerAbsent:
    def test_clear_existing_triggers(self, mock_module, mock_p4):
        mock_p4.fetch_triggers.return_value = {
            'Triggers': ['my_trigger change-submit //... "/usr/bin/script"']
        }

        with patch('plugins.modules.helix_core_trigger.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_trigger.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_trigger.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_trigger import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'cleared'
        mock_p4.save_triggers.assert_called_once()

    def test_clear_already_empty(self, mock_module, mock_p4):
        mock_p4.fetch_triggers.return_value = {}

        with patch('plugins.modules.helix_core_trigger.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_trigger.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_trigger.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_trigger import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert result['action'] == 'unchanged'
        mock_p4.save_triggers.assert_not_called()

    def test_clear_check_mode(self, mock_module, mock_p4):
        mock_module.check_mode = True
        mock_p4.fetch_triggers.return_value = {
            'Triggers': ['my_trigger change-submit //... "/usr/bin/script"']
        }

        with patch('plugins.modules.helix_core_trigger.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_trigger.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_trigger.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_trigger import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'cleared'
        mock_p4.save_triggers.assert_not_called()

    def test_clear_p4_error(self, mock_module, mock_p4):
        mock_p4.fetch_triggers.return_value = {
            'Triggers': ['my_trigger change-submit //... "/usr/bin/script"']
        }
        mock_p4.save_triggers.side_effect = Exception('Permission denied')

        with patch('plugins.modules.helix_core_trigger.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_trigger.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_trigger.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_trigger import run_module
                    with pytest.raises(AnsibleFailJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert 'Permission denied' in result['msg']
