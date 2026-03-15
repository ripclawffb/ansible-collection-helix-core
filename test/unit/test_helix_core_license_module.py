"""
Unit tests for helix_core_license run_module().

Run with: pytest test/unit/test_helix_core_license_module.py -v
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
        'license': 'License:\n\tmy-license-string-xyz123\n',
        'server': '1666',
        'user': 'super',
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


class TestLicenseDeploy:
    def test_create_new_license(self, mock_module, mock_p4):
        # Simulation: -o returns no license initially, then returns info after update
        mock_p4.run.side_effect = [
            [], # initially empty from -o
            [], # result of -i
            [{'License': 'License:\n\tmy-license-string-xyz123\n', 'Users': '10'}] # after save from -o
        ]

        with patch('plugins.modules.helix_core_license.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_license.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_license.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_license import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'created'
        assert result['license_info']['Users'] == '10'
        # Check that -i was called
        mock_p4.run.assert_any_call('license', '-i')
        p4_input = mock_p4.input
        assert 'my-license-string' in p4_input

    def test_update_existing_license(self, mock_module, mock_p4):
        mock_p4.run.side_effect = [
            [{'License': 'License:\n\told-license-111\n'}], # current
            mock_p4.DEFAULT, # p4 license -i
            [{'License': 'License:\n\tmy-license-string-xyz123\n'}] # after save
        ]

        with patch('plugins.modules.helix_core_license.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_license.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_license.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_license import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'updated'
        mock_p4.run.assert_any_call('license', '-i')

    def test_idempotent_license(self, mock_module, mock_p4):
        # The license matches the desired license
        mock_p4.run.side_effect = [
            [{'License': 'License:\n\tmy-license-string-xyz123\n'}], # current
            [{'License': 'License:\n\tmy-license-string-xyz123\n'}] # refresh
        ]

        with patch('plugins.modules.helix_core_license.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_license.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_license.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_license import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert result['action'] == 'unchanged'

    def test_check_mode(self, mock_module, mock_p4):
        mock_module.check_mode = True
        mock_p4.run.side_effect = [
            [], # initially empty
            [] # refresh
        ]

        with patch('plugins.modules.helix_core_license.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_license.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_license.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_license import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'created'
        
        # Verify -i was not called
        assert 'license, -i' not in str(mock_p4.run.call_args_list)


class TestLicenseDelete:
    def test_delete_existing(self, mock_module, mock_p4):
        mock_module.params['state'] = 'absent'
        mock_p4.run.side_effect = [
            [{'License': 'License:\n\told-license-111\n'}], # current 
            [] # delete result
        ]

        with patch('plugins.modules.helix_core_license.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_license.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_license.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_license import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'deleted'
        mock_p4.run.assert_any_call('license', '-d')

    def test_delete_nonexistent(self, mock_module, mock_p4):
        mock_module.params['state'] = 'absent'
        mock_p4.run.side_effect = [
            [{'License': ''}] # empty
        ]

        with patch('plugins.modules.helix_core_license.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_license.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_license.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_license import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert result['action'] == 'unchanged'


class TestLicenseDiff:
    def test_update_with_diff(self, mock_module, mock_p4):
        mock_module._diff = True
        mock_p4.run.side_effect = [
            [{'License': 'License: old\n'}], # current
            mock_p4.DEFAULT, # p4 license -i
            [{'License': 'License:\n\tmy-license-string-xyz123\n'}] # refresh
        ]

        with patch('plugins.modules.helix_core_license.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_license.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_license.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_license import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert 'diff' in result
        assert 'License: old' in result['diff']['before']
        assert 'xyz123' in result['diff']['after']


class TestLicenseErrors:
    def test_p4_error_on_save(self, mock_module, mock_p4):
        def p4_run_side_effect(*args):
            if args == ('license', '-i'):
                raise Exception('Invalid license')
            return [{'License': 'old'}]
            
        mock_p4.run.side_effect = p4_run_side_effect

        with patch('plugins.modules.helix_core_license.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_license.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_license.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_license import run_module
                    with pytest.raises(AnsibleFailJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert 'Invalid license' in result['msg']
