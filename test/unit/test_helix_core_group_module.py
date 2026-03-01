"""
Unit tests for helix_core_group run_module().

Mocks P4 and AnsibleModule to test all branching logic.
Run with: pytest test/unit/test_helix_core_group_module.py -v
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
        'name': 'dev_team',
        'ldapconfig': None,
        'ldapsearchquery': None,
        'ldapuserattribute': None,
        'maxlocktime': 'unset',
        'maxopenfiles': 'unset',
        'maxresults': 'unset',
        'maxscanrows': 'unset',
        'owners': None,
        'passwordtimeout': 'unset',
        'subgroups': None,
        'timeout': '43200',
        'users': ['alice', 'bob'],
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
def existing_group_spec():
    return {
        'Group': 'dev_team',
        'MaxLockTime': 'unset',
        'MaxResults': 'unset',
        'MaxOpenFiles': 'unset',
        'MaxScanRows': 'unset',
        'PasswordTimeout': 'unset',
        'Timeout': '43200',
        'Users': ['alice', 'bob'],
    }


@pytest.fixture
def new_group_spec():
    return {'Group': 'dev_team'}


class TestGroupCreate:
    def test_create_new_group(self, mock_module, mock_p4, new_group_spec):
        mock_p4.fetch_group.return_value = new_group_spec

        with patch('plugins.modules.helix_core_group.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_group.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_group.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_group import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        mock_p4.save_group.assert_called_once()

    def test_create_check_mode(self, mock_module, mock_p4, new_group_spec):
        mock_module.check_mode = True
        mock_p4.fetch_group.return_value = new_group_spec

        with patch('plugins.modules.helix_core_group.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_group.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_group.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_group import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        mock_p4.save_group.assert_not_called()


class TestGroupUpdate:
    def test_no_changes(self, mock_module, mock_p4, existing_group_spec):
        mock_p4.fetch_group.return_value = existing_group_spec

        with patch('plugins.modules.helix_core_group.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_group.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_group.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_group import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False

    def test_with_changes(self, mock_module, mock_p4, existing_group_spec):
        mock_module.params['users'] = ['alice', 'bob', 'charlie']
        mock_p4.fetch_group.return_value = existing_group_spec

        with patch('plugins.modules.helix_core_group.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_group.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_group.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_group import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        mock_p4.save_group.assert_called_once()


class TestGroupDelete:
    def test_delete_existing(self, mock_module, mock_p4, existing_group_spec):
        mock_module.params['state'] = 'absent'
        mock_p4.fetch_group.return_value = existing_group_spec

        with patch('plugins.modules.helix_core_group.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_group.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_group.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_group import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        mock_p4.delete_group.assert_called_once_with('dev_team')

    def test_delete_nonexistent(self, mock_module, mock_p4, new_group_spec):
        mock_module.params['state'] = 'absent'
        mock_p4.fetch_group.return_value = new_group_spec

        with patch('plugins.modules.helix_core_group.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_group.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_group.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_group import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        mock_p4.delete_group.assert_not_called()

    def test_delete_check_mode(self, mock_module, mock_p4, existing_group_spec):
        mock_module.params['state'] = 'absent'
        mock_module.check_mode = True
        mock_p4.fetch_group.return_value = existing_group_spec

        with patch('plugins.modules.helix_core_group.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_group.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_group.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_group import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        mock_p4.delete_group.assert_not_called()
