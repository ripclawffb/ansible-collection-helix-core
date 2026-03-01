"""
Unit tests for helix_core_configurable run_module().

Mocks P4 and AnsibleModule to test all branching logic.
Run with: pytest test/unit/test_helix_core_configurable_module.py -v
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
        'name': 'auth.id',
        'value': 'master.1',
        'serverid': 'any',
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


class TestConfigurableSet:
    def test_set_new_configurable(self, mock_module, mock_p4):
        mock_p4.run.return_value = []  # no existing configs

        with patch('plugins.modules.helix_core_configurable.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_configurable.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_configurable.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_configurable import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'created'
        assert result['configurable'] == {'name': 'auth.id', 'value': 'master.1', 'serverid': 'any'}
        assert len(result['changes']) == 1
        assert result['changes'][0]['field'] == 'value'

    def test_set_same_value_idempotent(self, mock_module, mock_p4):
        mock_p4.run.return_value = [
            {'ServerName': 'any', 'Name': 'auth.id', 'Value': 'master.1'},
        ]

        with patch('plugins.modules.helix_core_configurable.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_configurable.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_configurable.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_configurable import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert result['action'] == 'unchanged'
        assert result['changes'] == []
        assert result['configurable'] == {'name': 'auth.id', 'value': 'master.1', 'serverid': 'any'}

    def test_set_different_value(self, mock_module, mock_p4):
        mock_p4.run.return_value = [
            {'ServerName': 'any', 'Name': 'auth.id', 'Value': 'old_value'},
        ]

        with patch('plugins.modules.helix_core_configurable.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_configurable.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_configurable.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_configurable import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'updated'
        assert len(result['changes']) == 1
        assert result['changes'][0]['before'] == 'old_value'
        assert result['changes'][0]['after'] == 'master.1'

    def test_set_check_mode(self, mock_module, mock_p4):
        mock_module.check_mode = True
        mock_p4.run.return_value = []

        with patch('plugins.modules.helix_core_configurable.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_configurable.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_configurable.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_configurable import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'created'
        # p4.run should only be called once (for 'configure show'), not for 'configure set'
        assert mock_p4.run.call_count == 1


class TestConfigurableUnset:
    def test_unset_existing(self, mock_module, mock_p4):
        mock_module.params['state'] = 'absent'
        mock_p4.run.return_value = [
            {'ServerName': 'any', 'Name': 'auth.id', 'Value': 'master.1'},
        ]

        with patch('plugins.modules.helix_core_configurable.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_configurable.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_configurable.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_configurable import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'deleted'
        assert len(result['changes']) == 1
        assert result['changes'][0]['before'] == 'master.1'
        assert result['changes'][0]['after'] is None

    def test_unset_nonexistent(self, mock_module, mock_p4):
        mock_module.params['state'] = 'absent'
        mock_p4.run.return_value = []

        with patch('plugins.modules.helix_core_configurable.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_configurable.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_configurable.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_configurable import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert result['action'] == 'unchanged'
        assert result['changes'] == []

    def test_unset_check_mode(self, mock_module, mock_p4):
        mock_module.params['state'] = 'absent'
        mock_module.check_mode = True
        mock_p4.run.return_value = [
            {'ServerName': 'any', 'Name': 'auth.id', 'Value': 'master.1'},
        ]

        with patch('plugins.modules.helix_core_configurable.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_configurable.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_configurable.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_configurable import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'deleted'
        assert mock_p4.run.call_count == 1


class TestConfigurableDiff:
    def test_set_with_diff(self, mock_module, mock_p4):
        mock_module._diff = True
        mock_p4.run.return_value = []

        with patch('plugins.modules.helix_core_configurable.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_configurable.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_configurable.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_configurable import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert 'diff' in result
        assert 'auth.id' in result['diff']['after']

    def test_unset_with_diff(self, mock_module, mock_p4):
        mock_module._diff = True
        mock_module.params['state'] = 'absent'
        mock_p4.run.return_value = [
            {'ServerName': 'any', 'Name': 'auth.id', 'Value': 'master.1'},
        ]

        with patch('plugins.modules.helix_core_configurable.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_configurable.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_configurable.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_configurable import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert 'diff' in result
        assert result['diff']['after'] == ''

    def test_no_diff_when_disabled(self, mock_module, mock_p4):
        mock_module._diff = False
        mock_p4.run.return_value = []

        with patch('plugins.modules.helix_core_configurable.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_configurable.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_configurable.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_configurable import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert 'diff' not in result

    def test_check_mode_set_with_diff(self, mock_module, mock_p4):
        mock_module._diff = True
        mock_module.check_mode = True
        mock_p4.run.return_value = []

        with patch('plugins.modules.helix_core_configurable.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_configurable.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_configurable.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_configurable import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert 'diff' in result
        assert 'auth.id' in result['diff']['after']
        # Should only call 'configure show', not 'configure set'
        assert mock_p4.run.call_count == 1

