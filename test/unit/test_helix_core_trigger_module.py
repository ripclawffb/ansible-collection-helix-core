"""
Comprehensive unit tests for helix_core_trigger run_module().

Covers state=present (set/replace/idempotent), state=absent (clear),
check mode, diff mode, and edge cases.

Run with: pytest test/unit/test_helix_core_trigger_module.py -v
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


def make_module(state='present', triggers=None, check_mode=False, diff=False):
    """Build a mock AnsibleModule with the given params."""
    module = MagicMock()
    module.params = {
        'state': state,
        'triggers': triggers,
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
    with patch('plugins.modules.helix_core_trigger.helix_core_connect', return_value=mock_p4):
        with patch('plugins.modules.helix_core_trigger.helix_core_disconnect'):
            with patch('plugins.modules.helix_core_trigger.AnsibleModule', return_value=mock_module):
                from plugins.modules.helix_core_trigger import run_module
                with pytest.raises((AnsibleExitJson, AnsibleFailJson)) as exc_info:
                    run_module()
    return exc_info


# ---------------------------------------------------------------------------
# state=present
# ---------------------------------------------------------------------------
class TestTriggerPresent:
    def test_set_triggers_on_empty_table(self, mock_p4):
        mock_p4.fetch_triggers.return_value = {}
        mod = make_module(triggers=[
            {'name': 'check_submit', 'type': 'change-submit', 'path': '//depot/...', 'command': '/scripts/validate.sh'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True
        assert result['action'] == 'updated'
        assert len(result['changes']['added']) == 1
        assert result['changes']['added'][0]['name'] == 'check_submit'
        mock_p4.save_triggers.assert_called_once()

    def test_replace_existing_triggers(self, mock_p4):
        mock_p4.fetch_triggers.return_value = {
            'Triggers': ['old_trigger change-submit //... /old/script.sh']
        }
        mod = make_module(triggers=[
            {'name': 'new_trigger', 'type': 'change-commit', 'path': '//depot/...', 'command': '/new/script.sh'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True
        added_names = [e['name'] for e in result['changes']['added']]
        removed_names = [e['name'] for e in result['changes']['removed']]
        assert 'new_trigger' in added_names
        assert 'old_trigger' in removed_names

    def test_set_identical_triggers_is_idempotent(self, mock_p4):
        mock_p4.fetch_triggers.return_value = {
            'Triggers': ['check_submit change-submit //depot/... /scripts/validate.sh']
        }
        mod = make_module(triggers=[
            {'name': 'check_submit', 'type': 'change-submit', 'path': '//depot/...', 'command': '/scripts/validate.sh'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is False
        assert result['action'] == 'unchanged'
        mock_p4.save_triggers.assert_not_called()

    def test_reordered_triggers_detects_change(self, mock_p4):
        mock_p4.fetch_triggers.return_value = {
            'Triggers': [
                'trigger_a change-submit //... /script_a.sh',
                'trigger_b change-commit //... /script_b.sh',
            ]
        }
        mod = make_module(triggers=[
            {'name': 'trigger_b', 'type': 'change-commit', 'path': '//...', 'command': '/script_b.sh'},
            {'name': 'trigger_a', 'type': 'change-submit', 'path': '//...', 'command': '/script_a.sh'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True

    def test_save_triggers_quotes_commands_with_spaces(self, mock_p4):
        mock_p4.fetch_triggers.return_value = {}
        mod = make_module(triggers=[
            {'name': 'check', 'type': 'change-submit', 'path': '//depot/...', 'command': '/scripts/run.sh %changelist%'},
        ])
        run(mod, mock_p4)

        saved_spec = mock_p4.save_triggers.call_args[0][0]
        assert saved_spec['Triggers'] == ['check change-submit //depot/... "/scripts/run.sh %changelist%"']

    def test_result_triggers_matches_desired(self, mock_p4):
        mock_p4.fetch_triggers.return_value = {}
        mod = make_module(triggers=[
            {'name': 'trig1', 'type': 'change-submit', 'path': '//...', 'command': '/run.sh'},
            {'name': 'trig2', 'type': 'change-commit', 'path': '//depot/...', 'command': '/notify.sh'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert len(result['triggers']) == 2
        names = [t['name'] for t in result['triggers']]
        assert names == ['trig1', 'trig2']

    def test_set_multiple_triggers(self, mock_p4):
        mock_p4.fetch_triggers.return_value = {}
        mod = make_module(triggers=[
            {'name': 'trig1', 'type': 'change-submit', 'path': '//...', 'command': '/run.sh'},
            {'name': 'trig2', 'type': 'change-commit', 'path': '//depot/...', 'command': '/notify.sh'},
            {'name': 'trig3', 'type': 'form-save', 'path': 'client', 'command': '/validate_client.sh'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True
        assert len(result['changes']['added']) == 3


# ---------------------------------------------------------------------------
# state=absent
# ---------------------------------------------------------------------------
class TestTriggerAbsent:
    def test_clear_existing_triggers(self, mock_p4):
        mock_p4.fetch_triggers.return_value = {
            'Triggers': ['my_trigger change-submit //... "/usr/bin/script"']
        }
        mod = make_module(state='absent')
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True
        assert result['action'] == 'cleared'
        assert len(result['changes']['removed']) == 1
        mock_p4.save_triggers.assert_called_once()

    def test_clear_already_empty_is_idempotent(self, mock_p4):
        mock_p4.fetch_triggers.return_value = {}
        mod = make_module(state='absent')
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is False
        assert result['action'] == 'unchanged'
        mock_p4.save_triggers.assert_not_called()

    def test_clear_multiple_entries(self, mock_p4):
        mock_p4.fetch_triggers.return_value = {
            'Triggers': [
                'trig1 change-submit //... /script1.sh',
                'trig2 change-commit //... /script2.sh',
            ]
        }
        mod = make_module(state='absent')
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True
        assert len(result['changes']['removed']) == 2

    def test_clear_sets_empty_triggers_list(self, mock_p4):
        mock_p4.fetch_triggers.return_value = {
            'Triggers': ['trig1 change-submit //... /script.sh']
        }
        mod = make_module(state='absent')
        run(mod, mock_p4)

        saved_spec = mock_p4.save_triggers.call_args[0][0]
        assert saved_spec['Triggers'] == []


# ---------------------------------------------------------------------------
# Check mode
# ---------------------------------------------------------------------------
class TestTriggerCheckMode:
    def test_check_mode_present(self, mock_p4):
        mock_p4.fetch_triggers.return_value = {}
        mod = make_module(check_mode=True, triggers=[
            {'name': 'check', 'type': 'change-submit', 'path': '//...', 'command': '/run.sh'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True
        mock_p4.save_triggers.assert_not_called()

    def test_check_mode_absent(self, mock_p4):
        mock_p4.fetch_triggers.return_value = {
            'Triggers': ['my_trigger change-submit //... /script.sh']
        }
        mod = make_module(state='absent', check_mode=True)
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['changed'] is True
        assert result['action'] == 'cleared'
        mock_p4.save_triggers.assert_not_called()


# ---------------------------------------------------------------------------
# Diff mode
# ---------------------------------------------------------------------------
class TestTriggerDiffMode:
    def test_diff_for_present_replace(self, mock_p4):
        mock_p4.fetch_triggers.return_value = {
            'Triggers': ['old_trig change-submit //... /old.sh']
        }
        mod = make_module(diff=True, triggers=[
            {'name': 'new_trig', 'type': 'change-commit', 'path': '//depot/...', 'command': '/new.sh'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert 'diff' in result
        assert 'old_trig' in result['diff']['before']
        assert 'new_trig' in result['diff']['after']

    def test_diff_for_absent_clear(self, mock_p4):
        mock_p4.fetch_triggers.return_value = {
            'Triggers': ['my_trig change-submit //... /script.sh']
        }
        mod = make_module(state='absent', diff=True)
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert 'diff' in result
        assert 'my_trig' in result['diff']['before']
        assert result['diff']['after'] == ''

    def test_no_diff_when_idempotent(self, mock_p4):
        mock_p4.fetch_triggers.return_value = {
            'Triggers': ['check change-submit //depot/... /run.sh']
        }
        mod = make_module(diff=True, triggers=[
            {'name': 'check', 'type': 'change-submit', 'path': '//depot/...', 'command': '/run.sh'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert 'diff' not in result


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------
class TestTriggerEdgeCases:
    def test_p4_error_propagation(self, mock_p4):
        mock_p4.fetch_triggers.return_value = {
            'Triggers': ['my_trig change-submit //... /script.sh']
        }
        mock_p4.save_triggers.side_effect = Exception('Permission denied')
        mod = make_module(state='absent')
        exc = run(mod, mock_p4)

        assert isinstance(exc.value, AnsibleFailJson)
        result = exc.value.args[0]
        assert 'Permission denied' in result['msg']

    def test_fetch_error_propagation(self, mock_p4):
        mock_p4.fetch_triggers.side_effect = Exception('Connection refused')
        mod = make_module(triggers=[
            {'name': 'check', 'type': 'change-submit', 'path': '//...', 'command': '/run.sh'},
        ])
        exc = run(mod, mock_p4)

        assert isinstance(exc.value, AnsibleFailJson)
        result = exc.value.args[0]
        assert 'Connection refused' in result['msg']

    def test_command_with_spaces_roundtrip(self, mock_p4):
        """Verify a trigger with spaces in command is handled from present through result."""
        mock_p4.fetch_triggers.return_value = {}
        mod = make_module(triggers=[
            {'name': 'check', 'type': 'change-submit', 'path': '//depot/...', 'command': '/scripts/run.sh %changelist% %user%'},
        ])
        exc = run(mod, mock_p4)
        result = exc.value.args[0]

        assert result['triggers'][0]['command'] == '/scripts/run.sh %changelist% %user%'
