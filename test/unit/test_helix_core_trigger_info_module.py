"""
Unit tests for helix_core_trigger_info run_module().

Run with: pytest test/unit/test_helix_core_trigger_info_module.py -v
"""

import sys
import os
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


class AnsibleExitJson(Exception):
    pass


def exit_json_side_effect(**kwargs):
    raise AnsibleExitJson(kwargs)


@pytest.fixture
def mock_module():
    module = MagicMock()
    module.params = {
        'server': '1666',
        'user': 'admin',
        'password': 'pass',
        'charset': 'none',
    }
    module.check_mode = True
    module._diff = False
    module.exit_json = MagicMock(side_effect=exit_json_side_effect)
    module.fail_json = MagicMock(side_effect=exit_json_side_effect)
    return module


@pytest.fixture
def mock_p4():
    p4 = MagicMock()
    p4.connected.return_value = True
    return p4


class TestTriggerInfo:
    def test_returns_triggers(self, mock_module, mock_p4):
        mock_p4.fetch_triggers.return_value = {
            'Triggers': [
                'check_submit change-submit //depot/... /scripts/validate.sh',
            ]
        }

        with patch('plugins.modules.helix_core_trigger_info.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_trigger_info.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_trigger_info.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_trigger_info import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert len(result['triggers']) == 1

    def test_empty_triggers(self, mock_module, mock_p4):
        mock_p4.fetch_triggers.return_value = {'Triggers': []}

        with patch('plugins.modules.helix_core_trigger_info.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_trigger_info.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_trigger_info.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_trigger_info import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['triggers'] == []

    def test_missing_triggers_key(self, mock_module, mock_p4):
        mock_p4.fetch_triggers.return_value = {}

        with patch('plugins.modules.helix_core_trigger_info.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_trigger_info.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_trigger_info.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_trigger_info import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['triggers'] == []
