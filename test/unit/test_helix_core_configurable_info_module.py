"""
Unit tests for helix_core_configurable_info run_module().

Run with: pytest test/unit/test_helix_core_configurable_info_module.py -v
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
        'name': None,
        'serverid': 'any',
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


class TestConfigurableInfoAll:
    def test_list_all_configurables(self, mock_module, mock_p4):
        configs = [
            {'ServerName': 'any', 'Name': 'auth.id', 'Value': 'master.1'},
            {'ServerName': 'any', 'Name': 'security', 'Value': '3'},
        ]
        mock_p4.run.return_value = configs

        with patch('plugins.modules.helix_core_configurable_info.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_configurable_info.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_configurable_info.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_configurable_info import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert len(result['info']) == 2


class TestConfigurableInfoFiltered:
    def test_filter_by_name(self, mock_module, mock_p4):
        mock_module.params['name'] = 'auth.id'
        configs = [
            {'ServerName': 'any', 'Name': 'auth.id', 'Value': 'master.1'},
            {'ServerName': 'any', 'Name': 'security', 'Value': '3'},
        ]
        mock_p4.run.return_value = configs

        with patch('plugins.modules.helix_core_configurable_info.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_configurable_info.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_configurable_info.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_configurable_info import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert len(result['info']) == 1
        assert result['info'][0]['Name'] == 'auth.id'

    def test_filter_by_serverid(self, mock_module, mock_p4):
        mock_module.params['serverid'] = 'commit'
        configs = [
            {'ServerName': 'commit', 'Name': 'auth.id', 'Value': 'master.1'},
            {'ServerName': 'any', 'Name': 'security', 'Value': '3'},
        ]
        mock_p4.run.return_value = configs

        with patch('plugins.modules.helix_core_configurable_info.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_configurable_info.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_configurable_info.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_configurable_info import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert len(result['info']) == 1
        assert result['info'][0]['ServerName'] == 'commit'
