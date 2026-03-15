"""
Comprehensive unit tests for helix_core_protect run_module().

Covers entry mode (add/remove), replace mode, position logic,
check mode, diff mode, and edge cases.

Run with: pytest test/unit/test_helix_core_protect_module.py -v
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


def make_module(state='present', mode='entry', position='end', protections=None,
                check_mode=False, diff=False):
    """Build a mock AnsibleModule with the given params."""
    module = MagicMock()
    module.params = {
        'state': state,
        'mode': mode,
        'position': position,
        'protections': protections,
        'server': '1666',
        'user': 'admin',
        'password': 'pass',
        'charset': 'none',
    }
    module.check_mode = check_mode
    module._diff = diff
    module.exit_json = MagicMock(side_effect=exit_json_side_effect)
    module.fail_json = MagicMock(side_effect=fail_json_side_effect)
    module.warn = MagicMock()
    return module


@pytest.fixture
def mock_p4():
    p4 = MagicMock()
    p4.connected.return_value = True
    return p4


def run(mock_module, mock_p4):
    """Execute run_module() with standard mocks and return the result dict."""
    with patch('plugins.modules.helix_core_protect.helix_core_connect', return_value=mock_p4):
        with patch('plugins.modules.helix_core_protect.helix_core_disconnect'):
            with patch('plugins.modules.helix_core_protect.AnsibleModule', return_value=mock_module):
                from plugins.modules.helix_core_protect import run_module
                with pytest.raises((AnsibleExitJson, AnsibleFailJson)) as exc_info:
                    run_module()
    return exc_info


# ---------------------------------------------------------------------------
# state=present, mode=entry — adding entries
# ---------------------------------------------------------------------------
class TestProtectPresentEntryAdd:
    def test_add_single_new_entry(self, mock_p4):
        mock_p4.fetch_protect.return_value = {
            'Protections': ['read user bob * //...']
        }
        mod = make_module(protections=[
            {'access': 'write', 'type': 'group', 'name': 'devs', 'host': '*', 'path': '//depot/...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True
        assert result['action'] == 'updated'
        assert len(result['changes']['added']) == 1
        assert result['changes']['added'][0]['name'] == 'devs'
        assert result['changes']['removed'] == []
        mock_p4.save_protect.assert_called_once()

    def test_add_existing_entry_is_idempotent(self, mock_p4):
        mock_p4.fetch_protect.return_value = {
            'Protections': ['write user alice * //...']
        }
        mod = make_module(protections=[
            {'access': 'write', 'type': 'user', 'name': 'alice', 'host': '*', 'path': '//...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is False
        assert result['action'] == 'unchanged'
        mock_p4.save_protect.assert_not_called()

    def test_add_multiple_new_entries(self, mock_p4):
        mock_p4.fetch_protect.return_value = {'Protections': []}
        mod = make_module(protections=[
            {'access': 'write', 'type': 'user', 'name': 'alice', 'host': '*', 'path': '//...'},
            {'access': 'read', 'type': 'group', 'name': 'devs', 'host': '*', 'path': '//depot/...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True
        assert len(result['changes']['added']) == 2

    def test_add_mix_of_new_and_existing(self, mock_p4):
        """Only truly new entries should appear in changes.added."""
        mock_p4.fetch_protect.return_value = {
            'Protections': ['write user alice * //...']
        }
        mod = make_module(protections=[
            {'access': 'write', 'type': 'user', 'name': 'alice', 'host': '*', 'path': '//...'},
            {'access': 'read', 'type': 'group', 'name': 'devs', 'host': '*', 'path': '//depot/...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True
        assert len(result['changes']['added']) == 1
        assert result['changes']['added'][0]['name'] == 'devs'

    def test_save_protect_called_with_correct_format(self, mock_p4):
        mock_p4.fetch_protect.return_value = {'Protections': []}
        mod = make_module(protections=[
            {'access': 'super', 'type': 'user', 'name': 'admin', 'host': '*', 'path': '//...'},
        ])
        run(mod, mock_p4)

        saved_spec = mock_p4.save_protect.call_args[0][0]
        assert saved_spec['Protections'] == ['super user admin * //...']

    def test_result_protections_list_matches_updated_table(self, mock_p4):
        mock_p4.fetch_protect.return_value = {
            'Protections': ['read user bob * //...']
        }
        mod = make_module(protections=[
            {'access': 'write', 'type': 'group', 'name': 'devs', 'host': '*', 'path': '//depot/...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        # Should contain both original and new entry
        assert len(result['protections']) == 2
        names = [e['name'] for e in result['protections']]
        assert 'bob' in names
        assert 'devs' in names

    def test_duplicate_desired_entries_deduplicated(self, mock_p4):
        """If the user specifies the same entry twice, it should only be added once."""
        mock_p4.fetch_protect.return_value = {'Protections': []}
        mod = make_module(protections=[
            {'access': 'write', 'type': 'user', 'name': 'alice', 'host': '*', 'path': '//...'},
            {'access': 'write', 'type': 'user', 'name': 'alice', 'host': '*', 'path': '//...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert len(result['changes']['added']) == 1


# ---------------------------------------------------------------------------
# state=present, mode=entry — position logic
# ---------------------------------------------------------------------------
class TestProtectPresentEntryPosition:
    def test_position_beginning(self, mock_p4):
        mock_p4.fetch_protect.return_value = {
            'Protections': ['super user admin * //...']
        }
        mod = make_module(position='beginning', protections=[
            {'access': 'read', 'type': 'group', 'name': 'everyone', 'host': '*', 'path': '//...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        # New entry should be first in the result
        assert result['protections'][0]['name'] == 'everyone'
        assert result['protections'][1]['name'] == 'admin'

    def test_position_end_default(self, mock_p4):
        mock_p4.fetch_protect.return_value = {
            'Protections': ['super user admin * //...']
        }
        mod = make_module(position='end', protections=[
            {'access': 'read', 'type': 'group', 'name': 'everyone', 'host': '*', 'path': '//...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        # New entry should be last
        assert result['protections'][-1]['name'] == 'everyone'
        assert result['protections'][0]['name'] == 'admin'

    def test_position_numeric_index(self, mock_p4):
        mock_p4.fetch_protect.return_value = {
            'Protections': [
                'super user admin * //...',
                'write group devs * //depot/...',
            ]
        }
        mod = make_module(position='1', protections=[
            {'access': 'read', 'type': 'user', 'name': 'bob', 'host': '*', 'path': '//...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        # Inserted at index 1 (between admin and devs)
        assert result['protections'][0]['name'] == 'admin'
        assert result['protections'][1]['name'] == 'bob'
        assert result['protections'][2]['name'] == 'devs'

    def test_position_beyond_table_length_clamps_to_end(self, mock_p4):
        mock_p4.fetch_protect.return_value = {
            'Protections': ['read user bob * //...']
        }
        mod = make_module(position='999', protections=[
            {'access': 'write', 'type': 'user', 'name': 'alice', 'host': '*', 'path': '//...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        # Should be appended at end
        assert result['protections'][-1]['name'] == 'alice'

    def test_position_zero(self, mock_p4):
        mock_p4.fetch_protect.return_value = {
            'Protections': ['read user bob * //...']
        }
        mod = make_module(position='0', protections=[
            {'access': 'write', 'type': 'user', 'name': 'alice', 'host': '*', 'path': '//...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['protections'][0]['name'] == 'alice'

    def test_invalid_position_fails(self, mock_p4):
        mock_p4.fetch_protect.return_value = {'Protections': []}
        mod = make_module(position='middle', protections=[
            {'access': 'write', 'type': 'user', 'name': 'alice', 'host': '*', 'path': '//...'},
        ])
        exc = run(mod, mock_p4)

        assert isinstance(exc.value, AnsibleFailJson)
        result = exc.value.args[0]
        assert 'Invalid position' in result['msg']

    def test_position_ignored_for_existing_entry(self, mock_p4):
        """If the entry already exists, position should have no effect."""
        mock_p4.fetch_protect.return_value = {
            'Protections': [
                'super user admin * //...',
                'write user alice * //...',
            ]
        }
        mod = make_module(position='beginning', protections=[
            {'access': 'write', 'type': 'user', 'name': 'alice', 'host': '*', 'path': '//...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is False
        mock_p4.save_protect.assert_not_called()


# ---------------------------------------------------------------------------
# state=present, mode=replace
# ---------------------------------------------------------------------------
class TestProtectPresentReplace:
    def test_replace_entire_table(self, mock_p4):
        mock_p4.fetch_protect.return_value = {
            'Protections': ['read user bob * //...']
        }
        mod = make_module(mode='replace', protections=[
            {'access': 'super', 'type': 'user', 'name': 'admin', 'host': '*', 'path': '//...'},
            {'access': 'write', 'type': 'group', 'name': 'devs', 'host': '*', 'path': '//depot/...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True
        assert result['action'] == 'updated'
        assert len(result['changes']['added']) == 2
        assert len(result['changes']['removed']) == 1
        mock_p4.save_protect.assert_called_once()

    def test_replace_with_same_entries_is_idempotent(self, mock_p4):
        mock_p4.fetch_protect.return_value = {
            'Protections': [
                'super user admin * //...',
                'write group devs * //depot/...',
            ]
        }
        mod = make_module(mode='replace', protections=[
            {'access': 'super', 'type': 'user', 'name': 'admin', 'host': '*', 'path': '//...'},
            {'access': 'write', 'type': 'group', 'name': 'devs', 'host': '*', 'path': '//depot/...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is False
        assert result['action'] == 'unchanged'
        mock_p4.save_protect.assert_not_called()

    def test_replace_reordered_entries_detects_change(self, mock_p4):
        """Order matters in protection tables, so reordering is a change."""
        mock_p4.fetch_protect.return_value = {
            'Protections': [
                'super user admin * //...',
                'write group devs * //depot/...',
            ]
        }
        mod = make_module(mode='replace', protections=[
            {'access': 'write', 'type': 'group', 'name': 'devs', 'host': '*', 'path': '//depot/...'},
            {'access': 'super', 'type': 'user', 'name': 'admin', 'host': '*', 'path': '//...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True

    def test_replace_changes_dict_accuracy(self, mock_p4):
        mock_p4.fetch_protect.return_value = {
            'Protections': [
                'read user alice * //...',
                'write user bob * //...',
            ]
        }
        mod = make_module(mode='replace', protections=[
            {'access': 'write', 'type': 'user', 'name': 'bob', 'host': '*', 'path': '//...'},
            {'access': 'super', 'type': 'user', 'name': 'admin', 'host': '*', 'path': '//...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        added_names = [e['name'] for e in result['changes']['added']]
        removed_names = [e['name'] for e in result['changes']['removed']]
        assert 'admin' in added_names
        assert 'alice' in removed_names
        # bob is in both, so not in added/removed
        assert 'bob' not in added_names
        assert 'bob' not in removed_names

    def test_replace_result_protections_matches_desired(self, mock_p4):
        mock_p4.fetch_protect.return_value = {
            'Protections': ['read user old * //...']
        }
        desired = [
            {'access': 'super', 'type': 'user', 'name': 'admin', 'host': '*', 'path': '//...'},
        ]
        mod = make_module(mode='replace', protections=desired)
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert len(result['protections']) == 1
        assert result['protections'][0]['name'] == 'admin'


# ---------------------------------------------------------------------------
# state=absent, mode=entry
# ---------------------------------------------------------------------------
class TestProtectAbsentEntry:
    def test_remove_existing_entry(self, mock_p4):
        mock_p4.fetch_protect.return_value = {
            'Protections': [
                'write user alice * //...',
                'read user bob * //...',
            ]
        }
        mod = make_module(state='absent', protections=[
            {'access': 'write', 'type': 'user', 'name': 'alice', 'host': '*', 'path': '//...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True
        assert result['action'] == 'updated'
        assert len(result['changes']['removed']) == 1
        assert result['changes']['removed'][0]['name'] == 'alice'
        mock_p4.save_protect.assert_called_once()

    def test_remove_nonexistent_entry_is_idempotent(self, mock_p4):
        mock_p4.fetch_protect.return_value = {
            'Protections': ['read user bob * //...']
        }
        mod = make_module(state='absent', protections=[
            {'access': 'write', 'type': 'user', 'name': 'alice', 'host': '*', 'path': '//...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is False
        assert result['action'] == 'unchanged'
        mock_p4.save_protect.assert_not_called()

    def test_remove_multiple_entries(self, mock_p4):
        mock_p4.fetch_protect.return_value = {
            'Protections': [
                'write user alice * //...',
                'read user bob * //...',
                'super user admin * //...',
            ]
        }
        mod = make_module(state='absent', protections=[
            {'access': 'write', 'type': 'user', 'name': 'alice', 'host': '*', 'path': '//...'},
            {'access': 'read', 'type': 'user', 'name': 'bob', 'host': '*', 'path': '//...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True
        assert len(result['changes']['removed']) == 2
        # Only admin should remain
        assert len(result['protections']) == 1
        assert result['protections'][0]['name'] == 'admin'

    def test_remove_result_shows_remaining_table(self, mock_p4):
        mock_p4.fetch_protect.return_value = {
            'Protections': [
                'write user alice * //...',
                'read user bob * //...',
            ]
        }
        mod = make_module(state='absent', protections=[
            {'access': 'write', 'type': 'user', 'name': 'alice', 'host': '*', 'path': '//...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert len(result['protections']) == 1
        assert result['protections'][0]['name'] == 'bob'


# ---------------------------------------------------------------------------
# state=absent, mode=replace — blocked
# ---------------------------------------------------------------------------
class TestProtectAbsentReplaceDenied:
    def test_replace_absent_blocked(self, mock_p4):
        """state=absent + mode=replace should be blocked for security."""
        mod = make_module(state='absent', mode='replace')
        exc = run(mod, mock_p4)

        assert isinstance(exc.value, AnsibleFailJson)
        result = exc.value.args[0]
        assert 'not allowed for security reasons' in result['msg']


# ---------------------------------------------------------------------------
# Check mode
# ---------------------------------------------------------------------------
class TestProtectCheckMode:
    def test_check_mode_present_entry(self, mock_p4):
        mock_p4.fetch_protect.return_value = {'Protections': []}
        mod = make_module(check_mode=True, protections=[
            {'access': 'write', 'type': 'user', 'name': 'alice', 'host': '*', 'path': '//...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True
        mock_p4.save_protect.assert_not_called()

    def test_check_mode_present_replace(self, mock_p4):
        mock_p4.fetch_protect.return_value = {
            'Protections': ['read user old * //...']
        }
        mod = make_module(mode='replace', check_mode=True, protections=[
            {'access': 'super', 'type': 'user', 'name': 'admin', 'host': '*', 'path': '//...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True
        mock_p4.save_protect.assert_not_called()

    def test_check_mode_absent_entry(self, mock_p4):
        mock_p4.fetch_protect.return_value = {
            'Protections': ['write user alice * //...']
        }
        mod = make_module(state='absent', check_mode=True, protections=[
            {'access': 'write', 'type': 'user', 'name': 'alice', 'host': '*', 'path': '//...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True
        assert result['action'] == 'updated'
        mock_p4.save_protect.assert_not_called()


# ---------------------------------------------------------------------------
# Diff mode
# ---------------------------------------------------------------------------
class TestProtectDiffMode:
    def test_diff_for_entry_add(self, mock_p4):
        mock_p4.fetch_protect.return_value = {
            'Protections': ['read user bob * //...']
        }
        mod = make_module(diff=True, protections=[
            {'access': 'write', 'type': 'user', 'name': 'alice', 'host': '*', 'path': '//...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert 'diff' in result
        assert 'bob' in result['diff']['before']
        assert 'alice' in result['diff']['after']
        assert 'bob' in result['diff']['after']  # original entry preserved

    def test_diff_for_entry_remove(self, mock_p4):
        mock_p4.fetch_protect.return_value = {
            'Protections': [
                'write user alice * //...',
                'read user bob * //...',
            ]
        }
        mod = make_module(state='absent', diff=True, protections=[
            {'access': 'write', 'type': 'user', 'name': 'alice', 'host': '*', 'path': '//...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert 'diff' in result
        assert 'alice' in result['diff']['before']
        assert 'alice' not in result['diff']['after']
        assert 'bob' in result['diff']['after']

    def test_diff_for_replace(self, mock_p4):
        mock_p4.fetch_protect.return_value = {
            'Protections': ['read user old * //...']
        }
        mod = make_module(mode='replace', diff=True, protections=[
            {'access': 'super', 'type': 'user', 'name': 'admin', 'host': '*', 'path': '//...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert 'diff' in result
        assert 'old' in result['diff']['before']
        assert 'admin' in result['diff']['after']

    def test_no_diff_when_unchanged(self, mock_p4):
        mock_p4.fetch_protect.return_value = {
            'Protections': ['write user alice * //...']
        }
        mod = make_module(diff=True, protections=[
            {'access': 'write', 'type': 'user', 'name': 'alice', 'host': '*', 'path': '//...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert 'diff' not in result


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------
class TestProtectEdgeCases:
    def test_empty_protections_key(self, mock_p4):
        """Table with no Protections key should be treated as empty."""
        mock_p4.fetch_protect.return_value = {}
        mod = make_module(protections=[
            {'access': 'write', 'type': 'user', 'name': 'alice', 'host': '*', 'path': '//...'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True

    def test_p4_error_propagation(self, mock_p4):
        mock_p4.fetch_protect.return_value = {
            'Protections': ['write user alice * //...']
        }
        mock_p4.save_protect.side_effect = Exception('Permission denied')

        mod = make_module(state='absent', protections=[
            {'access': 'write', 'type': 'user', 'name': 'alice', 'host': '*', 'path': '//...'},
        ])
        exc = run(mod, mock_p4)

        assert isinstance(exc.value, AnsibleFailJson)
        result = exc.value.args[0]
        assert 'Permission denied' in result['msg']

    def test_position_warning_when_irrelevant(self, mock_p4):
        """Position set with state=absent should produce a warning."""
        mock_p4.fetch_protect.return_value = {'Protections': []}
        mod = make_module(state='absent', position='beginning', protections=[
            {'access': 'write', 'type': 'user', 'name': 'alice', 'host': '*', 'path': '//...'},
        ])
        run(mod, mock_p4)

        mod.warn.assert_called_once()
        assert 'position' in mod.warn.call_args[0][0].lower()

    def test_absent_entry_no_protections_fails(self, mock_p4):
        """state=absent, mode=entry with no protections should fail."""
        mod = make_module(state='absent', protections=None)
        exc = run(mod, mock_p4)

        assert isinstance(exc.value, AnsibleFailJson)

    def test_fetch_error_propagation(self, mock_p4):
        mock_p4.fetch_protect.side_effect = Exception('Connection refused')
        mod = make_module(protections=[
            {'access': 'write', 'type': 'user', 'name': 'alice', 'host': '*', 'path': '//...'},
        ])
        exc = run(mod, mock_p4)

        assert isinstance(exc.value, AnsibleFailJson)
        result = exc.value.args[0]
        assert 'Connection refused' in result['msg']
