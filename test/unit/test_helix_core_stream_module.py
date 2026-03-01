"""
Unit tests for helix_core_stream run_module().

Mocks P4 and AnsibleModule to test all branching logic.
Run with: pytest test/unit/test_helix_core_stream_module.py -v
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
        'stream': '//Ace/main',
        'name': None,
        'description': 'Main branch',
        'owner': None,
        'type': 'mainline',
        'options': 'allsubmit unlocked toparent fromparent mergedown',
        'parent': 'none',
        'parentview': 'inherit',
        'paths': ['share ...'],
        'remapped': None,
        'ignored': None,
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
def existing_stream_spec():
    return {
        'Stream': '//Ace/main',
        'Access': '2024/01/01 00:00:00',
        'Description': 'Main branch',
        'Owner': 'admin',
        'Type': 'mainline',
        'Options': 'allsubmit unlocked toparent fromparent mergedown',
        'Parent': 'none',
        'Paths': ['share ...'],
    }


@pytest.fixture
def new_stream_spec():
    return {'Stream': '//Ace/main'}


class TestStreamCreate:
    def test_create_new_stream(self, mock_module, mock_p4, new_stream_spec):
        mock_p4.fetch_stream.return_value = new_stream_spec

        with patch('plugins.modules.helix_core_stream.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_stream.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_stream.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_stream import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'created'
        assert result['stream_spec'] is not None
        mock_p4.save_stream.assert_called_once()

    def test_create_check_mode(self, mock_module, mock_p4, new_stream_spec):
        mock_module.check_mode = True
        mock_p4.fetch_stream.return_value = new_stream_spec

        with patch('plugins.modules.helix_core_stream.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_stream.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_stream.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_stream import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'created'
        mock_p4.save_stream.assert_not_called()


class TestStreamUpdate:
    def test_no_changes(self, mock_module, mock_p4, existing_stream_spec):
        mock_p4.fetch_stream.return_value = existing_stream_spec

        with patch('plugins.modules.helix_core_stream.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_stream.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_stream.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_stream import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert result['action'] == 'unchanged'
        assert result['changes'] == []
        assert result['stream_spec'] == existing_stream_spec

    def test_with_changes(self, mock_module, mock_p4, existing_stream_spec):
        mock_module.params['description'] = 'Updated branch'
        mock_p4.fetch_stream.return_value = existing_stream_spec

        with patch('plugins.modules.helix_core_stream.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_stream.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_stream.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_stream import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'updated'
        assert len(result['changes']) > 0
        assert result['changes'][0]['field'] == 'Description'
        mock_p4.save_stream.assert_called_once()


class TestStreamDelete:
    def test_delete_existing(self, mock_module, mock_p4, existing_stream_spec):
        mock_module.params['state'] = 'absent'
        mock_p4.fetch_stream.return_value = existing_stream_spec

        with patch('plugins.modules.helix_core_stream.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_stream.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_stream.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_stream import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'deleted'
        mock_p4.delete_stream.assert_called_once_with('-f', '//Ace/main')

    def test_delete_nonexistent(self, mock_module, mock_p4, new_stream_spec):
        mock_module.params['state'] = 'absent'
        mock_p4.fetch_stream.return_value = new_stream_spec

        with patch('plugins.modules.helix_core_stream.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_stream.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_stream.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_stream import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert result['action'] == 'unchanged'

    def test_delete_check_mode(self, mock_module, mock_p4, existing_stream_spec):
        mock_module.params['state'] = 'absent'
        mock_module.check_mode = True
        mock_p4.fetch_stream.return_value = existing_stream_spec

        with patch('plugins.modules.helix_core_stream.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_stream.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_stream.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_stream import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'deleted'
        mock_p4.delete_stream.assert_not_called()


class TestStreamDiff:
    def test_create_with_diff(self, mock_module, mock_p4, new_stream_spec):
        mock_module._diff = True
        mock_p4.fetch_stream.return_value = new_stream_spec

        with patch('plugins.modules.helix_core_stream.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_stream.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_stream.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_stream import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert 'diff' in result
        assert result['diff']['before'] == ''
        assert 'Description' in result['diff']['after']

    def test_update_with_diff(self, mock_module, mock_p4, existing_stream_spec):
        mock_module._diff = True
        mock_module.params['description'] = 'Updated branch'
        mock_p4.fetch_stream.return_value = existing_stream_spec

        with patch('plugins.modules.helix_core_stream.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_stream.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_stream.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_stream import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert 'diff' in result
        assert 'Main branch' in result['diff']['before']
        assert 'Updated branch' in result['diff']['after']

    def test_delete_with_diff(self, mock_module, mock_p4, existing_stream_spec):
        mock_module._diff = True
        mock_module.params['state'] = 'absent'
        mock_p4.fetch_stream.return_value = existing_stream_spec

        with patch('plugins.modules.helix_core_stream.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_stream.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_stream.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_stream import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert 'diff' in result
        assert 'Description' in result['diff']['before']
        assert result['diff']['after'] == ''

    def test_no_diff_when_disabled(self, mock_module, mock_p4, new_stream_spec):
        mock_module._diff = False
        mock_p4.fetch_stream.return_value = new_stream_spec

        with patch('plugins.modules.helix_core_stream.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_stream.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_stream.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_stream import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert 'diff' not in result

    def test_check_mode_create_with_diff(self, mock_module, mock_p4, new_stream_spec):
        mock_module._diff = True
        mock_module.check_mode = True
        mock_p4.fetch_stream.return_value = new_stream_spec

        with patch('plugins.modules.helix_core_stream.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_stream.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_stream.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_stream import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert 'diff' in result
        assert result['diff']['before'] == ''
        mock_p4.save_stream.assert_not_called()

    def test_check_mode_update_with_diff(self, mock_module, mock_p4, existing_stream_spec):
        mock_module._diff = True
        mock_module.check_mode = True
        mock_module.params['description'] = 'Updated branch'
        mock_p4.fetch_stream.return_value = existing_stream_spec

        with patch('plugins.modules.helix_core_stream.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_stream.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_stream.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_stream import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert 'diff' in result
        assert 'Main branch' in result['diff']['before']
        assert 'Updated branch' in result['diff']['after']
        mock_p4.save_stream.assert_not_called()

