"""
Unit tests for helix_core_license_info run_module().

Run with: pytest test/unit/test_helix_core_license_info_module.py -v
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
        'server': '1666',
        'user': 'super',
        'password': 'pass',
        'charset': 'none',
    }
    module.check_mode = False
    module.exit_json = MagicMock(side_effect=exit_json_side_effect)
    module.fail_json = MagicMock(side_effect=fail_json_side_effect)
    return module


@pytest.fixture
def mock_p4():
    p4 = MagicMock()
    p4.connected.return_value = True
    return p4


class TestLicenseInfo:
    def test_get_license_info(self, mock_module, mock_p4):
        def p4_run_side_effect(*args):
            if args == ('license', '-u'):
                return [{'userCount': '5', 'clientCount': '10'}]
            elif args == ('license', '-o'):
                return [{'License': 'LicData', 'Customer': 'TestInc'}]
            return []
            
        mock_p4.run.side_effect = p4_run_side_effect

        with patch('plugins.modules.helix_core_license_info.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_license_info.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_license_info.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_license_info import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert result['info']['Customer'] == 'TestInc'
        assert result['info']['userCount'] == '5'

    def test_get_license_info_no_u_access(self, mock_module, mock_p4):
        def p4_run_side_effect(*args):
            if args == ('license', '-u'):
                raise Exception('You do not have permission.')
            elif args == ('license', '-o'):
                return [{'License': 'LicData', 'Customer': 'TestInc'}]
            return []
            
        mock_p4.run.side_effect = p4_run_side_effect

        with patch('plugins.modules.helix_core_license_info.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_license_info.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_license_info.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_license_info import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert result['info']['Customer'] == 'TestInc'
        assert 'userCount' not in result['info']

    def test_p4_error(self, mock_module, mock_p4):
        mock_p4.run.side_effect = Exception('Server not responding')

        with patch('plugins.modules.helix_core_license_info.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_license_info.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_license_info.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_license_info import run_module
                    with pytest.raises(AnsibleFailJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert 'Server not responding' in result['msg']
