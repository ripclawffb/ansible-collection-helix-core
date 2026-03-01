"""
Unit tests for helix_core_ldap run_module().

Mocks P4 and AnsibleModule to test all branching logic.
Run with: pytest test/unit/test_helix_core_ldap_module.py -v
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
        'name': 'test_ldap',
        'host': 'ldap.example.com',
        'port': 389,
        'encryption': 'none',
        'bind_method': 'simple',
        'simple_pattern': '${user}@example.com',
        'search_base_dn': None,
        'search_filter': None,
        'search_bind_dn': None,
        'search_passwd': None,
        'group_search_filter': None,
        'group_base_dn': None,
        'attribute_uid': None,
        'attribute_name': None,
        'attribute_email': None,
        'options': None,
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


@pytest.fixture
def existing_ldap_spec():
    return {
        'Name': 'test_ldap',
        'Host': 'ldap.example.com',
        'Port': '389',
        'Encryption': 'none',
        'BindMethod': 'simple',
        'SimplePattern': '${user}@example.com',
        'Options': 'nodowncase nogetattrs norealminusername',
    }


@pytest.fixture
def new_ldap_spec():
    return {
        'Name': 'test_ldap',
    }


class TestLdapCreate:
    def test_create_new(self, mock_module, mock_p4, new_ldap_spec):
        mock_p4.run_ldaps.return_value = []
        mock_p4.fetch_ldap.return_value = new_ldap_spec

        with patch('plugins.modules.helix_core_ldap.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_ldap.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_ldap.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_ldap import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'created'
        assert result['ldap_spec'] is not None
        mock_p4.save_ldap.assert_called_once()

    def test_create_idempotent(self, mock_module, mock_p4, existing_ldap_spec):
        mock_p4.run_ldaps.return_value = [{'Name': 'test_ldap'}]
        mock_p4.fetch_ldap.return_value = existing_ldap_spec.copy()

        with patch('plugins.modules.helix_core_ldap.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_ldap.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_ldap.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_ldap import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert result['action'] == 'unchanged'
        mock_p4.save_ldap.assert_not_called()

    def test_create_check_mode(self, mock_module, mock_p4, new_ldap_spec):
        mock_module.check_mode = True
        mock_p4.run_ldaps.return_value = []
        mock_p4.fetch_ldap.return_value = new_ldap_spec

        with patch('plugins.modules.helix_core_ldap.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_ldap.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_ldap.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_ldap import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'created'
        mock_p4.save_ldap.assert_not_called()


class TestLdapUpdate:
    def test_field_change(self, mock_module, mock_p4, existing_ldap_spec):
        mock_module.params['host'] = 'newldap.example.com'
        mock_p4.run_ldaps.return_value = [{'Name': 'test_ldap'}]
        mock_p4.fetch_ldap.return_value = existing_ldap_spec.copy()

        with patch('plugins.modules.helix_core_ldap.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_ldap.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_ldap.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_ldap import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'updated'
        assert any(c['field'] == 'Host' for c in result['changes'])
        mock_p4.save_ldap.assert_called_once()


class TestLdapDelete:
    def test_delete_existing(self, mock_module, mock_p4, existing_ldap_spec):
        mock_module.params['state'] = 'absent'
        mock_p4.run_ldaps.return_value = [{'Name': 'test_ldap'}]
        mock_p4.fetch_ldap.return_value = existing_ldap_spec

        with patch('plugins.modules.helix_core_ldap.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_ldap.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_ldap.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_ldap import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'deleted'
        mock_p4.delete_ldap.assert_called_once_with('test_ldap')

    def test_delete_nonexistent(self, mock_module, mock_p4):
        mock_module.params['state'] = 'absent'
        mock_p4.run_ldaps.return_value = []

        with patch('plugins.modules.helix_core_ldap.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_ldap.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_ldap.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_ldap import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert result['action'] == 'unchanged'
        mock_p4.delete_ldap.assert_not_called()

    def test_delete_check_mode(self, mock_module, mock_p4, existing_ldap_spec):
        mock_module.params['state'] = 'absent'
        mock_module.check_mode = True
        mock_p4.run_ldaps.return_value = [{'Name': 'test_ldap'}]

        with patch('plugins.modules.helix_core_ldap.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_ldap.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_ldap.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_ldap import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'deleted'
        mock_p4.delete_ldap.assert_not_called()

    def test_delete_p4_error(self, mock_module, mock_p4, existing_ldap_spec):
        mock_module.params['state'] = 'absent'
        mock_p4.run_ldaps.return_value = [{'Name': 'test_ldap'}]
        mock_p4.delete_ldap.side_effect = Exception('LDAP config in use')

        with patch('plugins.modules.helix_core_ldap.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_ldap.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_ldap.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_ldap import run_module
                    with pytest.raises(AnsibleFailJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert 'LDAP config in use' in result['msg']
