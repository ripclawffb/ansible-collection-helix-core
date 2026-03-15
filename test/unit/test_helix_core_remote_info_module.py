"""
Unit tests for helix_core_remote_info run_module().

Run with: pytest test/unit/test_helix_core_remote_info_module.py -v
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
        'name': None,
        'server': '1666',
        'user': 'bruno',
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


class TestRemoteInfo:
    def test_get_all_remotes(self, mock_module, mock_p4):
        mock_p4.run_remotes.return_value = [
            {'RemoteID': 'remote1', 'Description': 'First remote'},
            {'RemoteID': 'remote2', 'Description': 'Second remote'}
        ]

        with patch('plugins.modules.helix_core_remote_info.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_remote_info.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_remote_info.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_remote_info import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert len(result['info']) == 2
        assert result['info'][0]['RemoteID'] == 'remote1'

    def test_get_specific_remote(self, mock_module, mock_p4):
        mock_module.params['name'] = 'remote1'
        mock_p4.fetch_remote.return_value = {'RemoteID': 'remote1', 'Description': 'First remote'}

        with patch('plugins.modules.helix_core_remote_info.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_remote_info.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_remote_info.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_remote_info import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert result['info']['RemoteID'] == 'remote1'

    def test_remote_p4_error(self, mock_module, mock_p4):
        mock_p4.run_remotes.side_effect = Exception('Server not available')

        with patch('plugins.modules.helix_core_remote_info.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_remote_info.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_remote_info.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_remote_info import run_module
                    with pytest.raises(AnsibleFailJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert 'Server not available' in result['msg']
