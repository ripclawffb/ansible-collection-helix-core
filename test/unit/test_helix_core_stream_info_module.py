"""
Unit tests for helix_core_stream_info run_module().

Run with: pytest test/unit/test_helix_core_stream_info_module.py -v
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


class TestStreamInfoSingle:
    def test_fetch_single_stream(self, mock_module, mock_p4):
        mock_module.params['name'] = '//Ace/main'
        spec = {'Stream': '//Ace/main', 'Type': 'mainline'}
        mock_p4.fetch_stream.return_value = spec

        with patch('plugins.modules.helix_core_stream_info.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_stream_info.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_stream_info.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_stream_info import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert result['info']['Stream'] == '//Ace/main'


class TestStreamInfoList:
    def test_list_all_streams(self, mock_module, mock_p4):
        streams = [{'Stream': '//Ace/main'}, {'Stream': '//Ace/dev'}]
        mock_p4.run_streams.return_value = streams

        with patch('plugins.modules.helix_core_stream_info.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_stream_info.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_stream_info.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_stream_info import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert len(result['info']) == 2
