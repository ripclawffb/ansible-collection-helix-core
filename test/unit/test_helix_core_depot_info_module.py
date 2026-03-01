"""
Unit tests for helix_core_depot_info run_module().

Run with: pytest test/unit/test_helix_core_depot_info_module.py -v
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


class TestDepotInfoSingle:
    def test_fetch_single_depot(self, mock_module, mock_p4):
        mock_module.params['name'] = 'depot1'
        spec = {'Depot': 'depot1', 'Type': 'local'}
        mock_p4.fetch_depot.return_value = spec

        with patch('plugins.modules.helix_core_depot_info.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_depot_info.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_depot_info.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_depot_info import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert result['info']['Depot'] == 'depot1'


class TestDepotInfoList:
    def test_list_all_depots(self, mock_module, mock_p4):
        depots = [{'name': 'd1'}, {'name': 'd2'}]
        mock_p4.run_depots.return_value = depots

        with patch('plugins.modules.helix_core_depot_info.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_depot_info.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_depot_info.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_depot_info import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert len(result['info']) == 2
