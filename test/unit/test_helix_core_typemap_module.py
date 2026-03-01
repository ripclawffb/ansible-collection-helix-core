"""
Unit tests for helix_core_typemap run_module() — absent/clear scenarios.

Mocks P4 and AnsibleModule to test state=absent branching logic.
Run with: pytest test/unit/test_helix_core_typemap_module.py -v
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
        'typemap': None,
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


class TestTypemapAbsent:
    def test_clear_existing_typemap(self, mock_module, mock_p4):
        mock_p4.fetch_typemap.return_value = {
            'TypeMap': ['text //....txt', 'binary //....exe']
        }

        with patch('plugins.modules.helix_core_typemap.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_typemap.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_typemap.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_typemap import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'cleared'
        mock_p4.save_typemap.assert_called_once()

    def test_clear_already_empty(self, mock_module, mock_p4):
        mock_p4.fetch_typemap.return_value = {}

        with patch('plugins.modules.helix_core_typemap.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_typemap.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_typemap.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_typemap import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert result['action'] == 'unchanged'
        mock_p4.save_typemap.assert_not_called()

    def test_clear_check_mode(self, mock_module, mock_p4):
        mock_module.check_mode = True
        mock_p4.fetch_typemap.return_value = {
            'TypeMap': ['text //....txt']
        }

        with patch('plugins.modules.helix_core_typemap.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_typemap.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_typemap.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_typemap import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'cleared'
        mock_p4.save_typemap.assert_not_called()

    def test_clear_p4_error(self, mock_module, mock_p4):
        mock_p4.fetch_typemap.return_value = {
            'TypeMap': ['text //....txt']
        }
        mock_p4.save_typemap.side_effect = Exception('Permission denied')

        with patch('plugins.modules.helix_core_typemap.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_typemap.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_typemap.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_typemap import run_module
                    with pytest.raises(AnsibleFailJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert 'Permission denied' in result['msg']
