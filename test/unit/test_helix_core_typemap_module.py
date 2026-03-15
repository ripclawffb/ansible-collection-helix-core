"""
Comprehensive unit tests for helix_core_typemap run_module().

Covers state=present (set/replace/idempotent), state=absent (clear),
check mode, diff mode, and edge cases.

Run with: pytest test/unit/test_helix_core_typemap_module.py -v
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


def make_module(state='present', typemap=None, check_mode=False, diff=False):
    """Build a mock AnsibleModule with the given params."""
    module = MagicMock()
    module.params = {
        'state': state,
        'typemap': typemap,
        'server': '1666',
        'user': 'admin',
        'password': 'pass',
        'charset': 'none',
    }
    module.check_mode = check_mode
    module._diff = diff
    module.exit_json = MagicMock(side_effect=exit_json_side_effect)
    module.fail_json = MagicMock(side_effect=fail_json_side_effect)
    return module


@pytest.fixture
def mock_p4():
    p4 = MagicMock()
    p4.connected.return_value = True
    return p4


def run(mock_module, mock_p4):
    """Execute run_module() with standard mocks and return the exc_info."""
    with patch('plugins.modules.helix_core_typemap.helix_core_connect', return_value=mock_p4):
        with patch('plugins.modules.helix_core_typemap.helix_core_disconnect'):
            with patch('plugins.modules.helix_core_typemap.AnsibleModule', return_value=mock_module):
                from plugins.modules.helix_core_typemap import run_module
                with pytest.raises((AnsibleExitJson, AnsibleFailJson)) as exc_info:
                    run_module()
    return exc_info


# ---------------------------------------------------------------------------
# state=present
# ---------------------------------------------------------------------------
class TestTypemapPresent:
    def test_set_typemap_on_empty_table(self, mock_p4):
        mock_p4.fetch_typemap.return_value = {}
        mod = make_module(typemap=[
            {'type': 'binary+l', 'path': '//depot/....exe'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True
        assert result['action'] == 'updated'
        assert len(result['changes']['added']) == 1
        assert result['changes']['added'][0]['type'] == 'binary+l'
        mock_p4.save_typemap.assert_called_once()

    def test_replace_existing_typemap(self, mock_p4):
        mock_p4.fetch_typemap.return_value = {
            'TypeMap': ['text //....txt']
        }
        mod = make_module(typemap=[
            {'type': 'binary+l', 'path': '//depot/....exe'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True
        added_types = [e['type'] for e in result['changes']['added']]
        removed_types = [e['type'] for e in result['changes']['removed']]
        assert 'binary+l' in added_types
        assert 'text' in removed_types

    def test_set_identical_typemap_is_idempotent(self, mock_p4):
        mock_p4.fetch_typemap.return_value = {
            'TypeMap': ['binary+l //depot/....exe', 'text+k //depot/....txt']
        }
        mod = make_module(typemap=[
            {'type': 'binary+l', 'path': '//depot/....exe'},
            {'type': 'text+k', 'path': '//depot/....txt'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is False
        assert result['action'] == 'unchanged'
        mock_p4.save_typemap.assert_not_called()

    def test_reordered_entries_detects_change(self, mock_p4):
        mock_p4.fetch_typemap.return_value = {
            'TypeMap': ['binary+l //depot/....exe', 'text+k //depot/....txt']
        }
        mod = make_module(typemap=[
            {'type': 'text+k', 'path': '//depot/....txt'},
            {'type': 'binary+l', 'path': '//depot/....exe'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True

    def test_changes_dict_accuracy(self, mock_p4):
        mock_p4.fetch_typemap.return_value = {
            'TypeMap': ['binary //....dll', 'text //....txt']
        }
        mod = make_module(typemap=[
            {'type': 'text', 'path': '//....txt'},
            {'type': 'binary+l', 'path': '//depot/....exe'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        added_paths = [e['path'] for e in result['changes']['added']]
        removed_paths = [e['path'] for e in result['changes']['removed']]
        assert '//depot/....exe' in added_paths
        assert '//....dll' in removed_paths
        # text //....txt is in both, so not in added or removed
        assert '//....txt' not in added_paths
        assert '//....txt' not in removed_paths

    def test_save_typemap_called_with_correct_format(self, mock_p4):
        mock_p4.fetch_typemap.return_value = {}
        mod = make_module(typemap=[
            {'type': 'binary+l', 'path': '//depot/....exe'},
            {'type': 'text+k', 'path': '//depot/....txt'},
        ])
        run(mod, mock_p4)

        saved_spec = mock_p4.save_typemap.call_args[0][0]
        assert saved_spec['TypeMap'] == ['binary+l //depot/....exe', 'text+k //depot/....txt']

    def test_result_typemap_matches_desired(self, mock_p4):
        mock_p4.fetch_typemap.return_value = {}
        mod = make_module(typemap=[
            {'type': 'binary+l', 'path': '//depot/....exe'},
            {'type': 'text+k', 'path': '//depot/....txt'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert len(result['typemap']) == 2
        types = [t['type'] for t in result['typemap']]
        assert types == ['binary+l', 'text+k']

    def test_set_multiple_entries(self, mock_p4):
        mock_p4.fetch_typemap.return_value = {}
        mod = make_module(typemap=[
            {'type': 'binary+l', 'path': '//depot/....exe'},
            {'type': 'binary+l', 'path': '//depot/....dll'},
            {'type': 'text+k', 'path': '//depot/....txt'},
            {'type': 'binary', 'path': '//depot/....zip'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True
        assert len(result['changes']['added']) == 4


# ---------------------------------------------------------------------------
# state=absent
# ---------------------------------------------------------------------------
class TestTypemapAbsent:
    def test_clear_existing_typemap(self, mock_p4):
        mock_p4.fetch_typemap.return_value = {
            'TypeMap': ['text //....txt', 'binary //....exe']
        }
        mod = make_module(state='absent')
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True
        assert result['action'] == 'cleared'
        assert len(result['changes']['removed']) == 2
        mock_p4.save_typemap.assert_called_once()

    def test_clear_already_empty_is_idempotent(self, mock_p4):
        mock_p4.fetch_typemap.return_value = {}
        mod = make_module(state='absent')
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is False
        assert result['action'] == 'unchanged'
        mock_p4.save_typemap.assert_not_called()

    def test_clear_sets_empty_typemap_list(self, mock_p4):
        mock_p4.fetch_typemap.return_value = {
            'TypeMap': ['text //....txt']
        }
        mod = make_module(state='absent')
        run(mod, mock_p4)

        saved_spec = mock_p4.save_typemap.call_args[0][0]
        assert saved_spec['TypeMap'] == []


# ---------------------------------------------------------------------------
# Check mode
# ---------------------------------------------------------------------------
class TestTypemapCheckMode:
    def test_check_mode_present(self, mock_p4):
        mock_p4.fetch_typemap.return_value = {}
        mod = make_module(check_mode=True, typemap=[
            {'type': 'binary+l', 'path': '//depot/....exe'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True
        mock_p4.save_typemap.assert_not_called()

    def test_check_mode_absent(self, mock_p4):
        mock_p4.fetch_typemap.return_value = {
            'TypeMap': ['text //....txt']
        }
        mod = make_module(state='absent', check_mode=True)
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True
        assert result['action'] == 'cleared'
        mock_p4.save_typemap.assert_not_called()


# ---------------------------------------------------------------------------
# Diff mode
# ---------------------------------------------------------------------------
class TestTypemapDiffMode:
    def test_diff_for_present_replace(self, mock_p4):
        mock_p4.fetch_typemap.return_value = {
            'TypeMap': ['text //....txt']
        }
        mod = make_module(diff=True, typemap=[
            {'type': 'binary+l', 'path': '//depot/....exe'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert 'diff' in result
        assert 'text' in result['diff']['before']
        assert 'binary+l' in result['diff']['after']

    def test_diff_for_absent_clear(self, mock_p4):
        mock_p4.fetch_typemap.return_value = {
            'TypeMap': ['text //....txt']
        }
        mod = make_module(state='absent', diff=True)
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert 'diff' in result
        assert 'text' in result['diff']['before']
        assert result['diff']['after'] == ''

    def test_no_diff_when_idempotent(self, mock_p4):
        mock_p4.fetch_typemap.return_value = {
            'TypeMap': ['binary+l //depot/....exe']
        }
        mod = make_module(diff=True, typemap=[
            {'type': 'binary+l', 'path': '//depot/....exe'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert 'diff' not in result


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------
class TestTypemapEdgeCases:
    def test_p4_error_propagation(self, mock_p4):
        mock_p4.fetch_typemap.return_value = {
            'TypeMap': ['text //....txt']
        }
        mock_p4.save_typemap.side_effect = Exception('Permission denied')
        mod = make_module(state='absent')
        exc = run(mod, mock_p4)

        assert isinstance(exc.value, AnsibleFailJson)
        result = exc.value.args[0]
        assert 'Permission denied' in result['msg']

    def test_fetch_error_propagation(self, mock_p4):
        mock_p4.fetch_typemap.side_effect = Exception('Connection refused')
        mod = make_module(typemap=[
            {'type': 'binary+l', 'path': '//depot/....exe'},
        ])
        exc = run(mod, mock_p4)

        assert isinstance(exc.value, AnsibleFailJson)
        result = exc.value.args[0]
        assert 'Connection refused' in result['msg']

    def test_none_typemap_key(self, mock_p4):
        """TypeMap key present but None should be treated as empty."""
        mock_p4.fetch_typemap.return_value = {'TypeMap': None}
        mod = make_module(typemap=[
            {'type': 'binary+l', 'path': '//depot/....exe'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True
