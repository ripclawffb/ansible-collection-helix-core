"""
Unit tests for trigger helpers.

These are pure-function tests — no Perforce connection required.
Run with: pytest test/unit/test_helix_core_trigger.py -v
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from plugins.modules.helix_core_trigger import triggers_to_list, list_to_triggers


class TestTriggersToList:
    def test_basic_entries(self):
        spec = {'Triggers': [
            'check_submit change-submit //depot/... /scripts/validate.sh',
            'notify_commit change-commit //depot/... /scripts/notify.sh',
        ]}
        result = triggers_to_list(spec)
        assert result == [
            ('check_submit', 'change-submit', '//depot/...', '/scripts/validate.sh'),
            ('notify_commit', 'change-commit', '//depot/...', '/scripts/notify.sh'),
        ]

    def test_command_with_spaces(self):
        spec = {'Triggers': [
            'check_submit change-submit //depot/... /scripts/validate.sh %changelist% %user%',
        ]}
        result = triggers_to_list(spec)
        assert result == [
            ('check_submit', 'change-submit', '//depot/...', '/scripts/validate.sh %changelist% %user%'),
        ]

    def test_quoted_command(self):
        """Quoted commands should have quotes stripped."""
        spec = {'Triggers': [
            'check_submit change-submit //depot/... "/scripts/validate.sh %changelist%"',
        ]}
        result = triggers_to_list(spec)
        assert result == [
            ('check_submit', 'change-submit', '//depot/...', '/scripts/validate.sh %changelist%'),
        ]

    def test_empty_triggers(self):
        assert triggers_to_list({'Triggers': []}) == []

    def test_missing_triggers_key(self):
        assert triggers_to_list({}) == []

    def test_none_triggers(self):
        assert triggers_to_list({'Triggers': None}) == []

    def test_three_field_entry(self):
        """Entries with only 3 fields should get empty command."""
        spec = {'Triggers': ['name type path']}
        result = triggers_to_list(spec)
        assert result == [('name', 'type', 'path', '')]


class TestListToTriggers:
    def test_basic_conversion(self):
        entries = [
            {'name': 'check', 'type': 'change-submit', 'path': '//depot/...', 'command': '/scripts/run.sh'},
        ]
        result = list_to_triggers(entries)
        assert result == ['check change-submit //depot/... /scripts/run.sh']

    def test_command_with_spaces_gets_quoted(self):
        entries = [
            {'name': 'check', 'type': 'change-submit', 'path': '//depot/...', 'command': '/scripts/run.sh %changelist%'},
        ]
        result = list_to_triggers(entries)
        assert result == ['check change-submit //depot/... "/scripts/run.sh %changelist%"']

    def test_already_quoted_command_not_double_quoted(self):
        entries = [
            {'name': 'check', 'type': 'change-submit', 'path': '//depot/...', 'command': '"/scripts/run.sh %changelist%"'},
        ]
        result = list_to_triggers(entries)
        # Should NOT double-quote
        assert result == ['check change-submit //depot/... "/scripts/run.sh %changelist%"']

    def test_empty_list(self):
        assert list_to_triggers([]) == []

    def test_simple_command_no_quotes(self):
        entries = [
            {'name': 'check', 'type': 'change-submit', 'path': '//depot/...', 'command': '/scripts/run.sh'},
        ]
        result = list_to_triggers(entries)
        # No spaces in command, should NOT be quoted
        assert '"' not in result[0]
