"""
Unit tests for helix_core_remote run_module().

Mocks P4 and AnsibleModule to test all branching logic.
Run with: pytest test/unit/test_helix_core_remote_module.py -v
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
        'remoteid': 'central-repo',
        'owner': None,
        'address': 'ssl:remoteserver:1666',
        'remoteuser': None,
        'description': 'Central repository',
        'options': None,
        'depotmap': ['//depot/... //depot/...'],
        'archivelimits': None,
        'server': '1666',
        'user': 'bruno',
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
def existing_remote_spec():
    return {
        'RemoteID': 'central-repo',
        'Description': 'Central repository',
        'Address': 'ssl:remoteserver:1666',
        'DepotMap': ['//depot/... //depot/...'],
    }


class TestRemoteCreate:
    def test_create_new_remote(self, mock_module, mock_p4, existing_remote_spec):
        mock_p4.fetch_remote.return_value = existing_remote_spec
        mock_p4.run.return_value = []  # no existing remotes

        with patch('plugins.modules.helix_core_remote.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_remote.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_remote.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_remote import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'created'
        assert result['remote_spec'] is not None
        mock_p4.save_remote.assert_called_once()

    def test_create_check_mode(self, mock_module, mock_p4, existing_remote_spec):
        mock_module.check_mode = True
        mock_p4.fetch_remote.return_value = existing_remote_spec
        mock_p4.run.return_value = []

        with patch('plugins.modules.helix_core_remote.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_remote.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_remote.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_remote import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'created'
        mock_p4.save_remote.assert_not_called()


class TestRemoteUpdate:
    def test_no_changes(self, mock_module, mock_p4, existing_remote_spec):
        mock_p4.fetch_remote.return_value = existing_remote_spec
        mock_p4.run.return_value = [{'RemoteID': 'central-repo'}]

        with patch('plugins.modules.helix_core_remote.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_remote.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_remote.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_remote import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert result['action'] == 'unchanged'
        assert result['changes'] == []
        assert result['remote_spec'] == existing_remote_spec

    def test_with_changes(self, mock_module, mock_p4, existing_remote_spec):
        mock_module.params['description'] = 'Updated remote'
        mock_p4.fetch_remote.return_value = existing_remote_spec
        mock_p4.run.return_value = [{'RemoteID': 'central-repo'}]

        with patch('plugins.modules.helix_core_remote.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_remote.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_remote.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_remote import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'updated'
        assert len(result['changes']) > 0
        assert result['changes'][0]['field'] == 'Description'
        mock_p4.save_remote.assert_called_once()


class TestRemoteDelete:
    def test_delete_existing(self, mock_module, mock_p4, existing_remote_spec):
        mock_module.params['state'] = 'absent'
        mock_p4.fetch_remote.return_value = existing_remote_spec
        mock_p4.run.return_value = [{'RemoteID': 'central-repo'}]

        with patch('plugins.modules.helix_core_remote.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_remote.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_remote.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_remote import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'deleted'
        mock_p4.delete_remote.assert_called_once_with('central-repo')

    def test_delete_nonexistent(self, mock_module, mock_p4):
        mock_module.params['state'] = 'absent'
        mock_p4.run.return_value = []

        with patch('plugins.modules.helix_core_remote.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_remote.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_remote.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_remote import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert result['action'] == 'unchanged'


class TestRemoteDiff:
    def test_update_with_diff(self, mock_module, mock_p4, existing_remote_spec):
        mock_module._diff = True
        mock_module.params['description'] = 'Updated remote'
        mock_p4.fetch_remote.return_value = existing_remote_spec
        mock_p4.run.return_value = [{'RemoteID': 'central-repo'}]

        with patch('plugins.modules.helix_core_remote.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_remote.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_remote.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_remote import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert 'diff' in result
        assert 'Central repository' in result['diff']['before']
        assert 'Updated remote' in result['diff']['after']


class TestRemoteErrors:
    def test_p4_error(self, mock_module, mock_p4, existing_remote_spec):
        mock_module.params['description'] = 'Updated remote'
        mock_p4.fetch_remote.return_value = existing_remote_spec
        mock_p4.run.return_value = [{'RemoteID': 'central-repo'}]
        mock_p4.save_remote.side_effect = Exception('Invalid remote address')

        with patch('plugins.modules.helix_core_remote.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_remote.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_remote.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_remote import run_module
                    with pytest.raises(AnsibleFailJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert 'Invalid remote address' in result['msg']
