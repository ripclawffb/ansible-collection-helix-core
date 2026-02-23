"""
Unit tests for protect helpers.

These are pure-function tests — no Perforce connection required.
Run with: pytest test/unit/test_helix_core_protect.py -v
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from plugins.modules.helix_core_protect import (
    protections_to_list, list_to_protections, entry_to_tuple
)


class TestProtectionsToList:
    def test_basic_entries(self):
        spec = {'Protections': [
            'write user alice * //depot/...',
            'read group developers * //...',
        ]}
        result = protections_to_list(spec)
        assert result == [
            ('write', 'user', 'alice', '*', '//depot/...'),
            ('read', 'group', 'developers', '*', '//...'),
        ]

    def test_empty_protections(self):
        assert protections_to_list({'Protections': []}) == []

    def test_missing_protections_key(self):
        assert protections_to_list({}) == []

    def test_none_protections(self):
        assert protections_to_list({'Protections': None}) == []

    def test_entry_with_fewer_than_five_fields(self):
        """Entries with fewer than 5 fields should be skipped."""
        spec = {'Protections': ['write user alice']}
        result = protections_to_list(spec)
        assert result == []

    def test_host_with_ip(self):
        spec = {'Protections': ['super user admin 192.168.1.0/24 //...']}
        result = protections_to_list(spec)
        assert result == [('super', 'user', 'admin', '192.168.1.0/24', '//...')]


class TestListToProtections:
    def test_basic_conversion(self):
        entries = [
            ('write', 'user', 'alice', '*', '//depot/...'),
            ('read', 'group', 'developers', '*', '//...'),
        ]
        result = list_to_protections(entries)
        assert result == [
            'write user alice * //depot/...',
            'read group developers * //...',
        ]

    def test_empty_list(self):
        assert list_to_protections([]) == []

    def test_roundtrip(self):
        """list_to_protections output should be parseable by protections_to_list."""
        entries = [('super', 'user', 'admin', '*', '//...')]
        strings = list_to_protections(entries)
        parsed = protections_to_list({'Protections': strings})
        assert parsed == entries


class TestEntryToTuple:
    def test_basic_conversion(self):
        entry = {'access': 'write', 'type': 'user', 'name': 'alice', 'host': '*', 'path': '//depot/...'}
        result = entry_to_tuple(entry)
        assert result == ('write', 'user', 'alice', '*', '//depot/...')

    def test_tuple_equality(self):
        """Two dicts with same values should produce equal tuples."""
        entry1 = {'access': 'read', 'type': 'group', 'name': 'devs', 'host': '*', 'path': '//...'}
        entry2 = {'access': 'read', 'type': 'group', 'name': 'devs', 'host': '*', 'path': '//...'}
        assert entry_to_tuple(entry1) == entry_to_tuple(entry2)

    def test_tuple_inequality(self):
        entry1 = {'access': 'read', 'type': 'user', 'name': 'alice', 'host': '*', 'path': '//...'}
        entry2 = {'access': 'write', 'type': 'user', 'name': 'alice', 'host': '*', 'path': '//...'}
        assert entry_to_tuple(entry1) != entry_to_tuple(entry2)
