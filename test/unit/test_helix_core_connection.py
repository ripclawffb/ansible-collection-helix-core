"""
Unit tests for spec_to_string helper in _helix_core_connection.

These are pure-function tests — no Perforce connection required.
Run with: pytest test/unit/test_helix_core_connection.py -v
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from plugins.module_utils._helix_core_connection import spec_to_string


class TestSpecToString:
    def test_basic_fields(self):
        spec = {'Description': 'My depot', 'Type': 'local'}
        result = spec_to_string(spec, ['Description', 'Type'])
        assert result == 'Description: My depot\nType: local\n'

    def test_missing_field_uses_empty_string(self):
        spec = {'Description': 'My depot'}
        result = spec_to_string(spec, ['Description', 'Type'])
        assert result == 'Description: My depot\nType: \n'

    def test_list_field_joined_with_newline_tab(self):
        spec = {'Users': ['alice', 'bob', 'charlie']}
        result = spec_to_string(spec, ['Users'])
        assert result == 'Users: alice\n\tbob\n\tcharlie\n'

    def test_empty_list_field(self):
        spec = {'Users': []}
        result = spec_to_string(spec, ['Users'])
        assert result == 'Users: \n'

    def test_rstrip_on_string_values(self):
        spec = {'Description': 'My depot   \n'}
        result = spec_to_string(spec, ['Description'])
        assert result == 'Description: My depot\n'

    def test_field_order_matches_fields_list(self):
        spec = {'Type': 'local', 'Description': 'My depot', 'Name': 'test'}
        result = spec_to_string(spec, ['Name', 'Description', 'Type'])
        lines = result.strip().split('\n')
        assert lines[0].startswith('Name:')
        assert lines[1].startswith('Description:')
        assert lines[2].startswith('Type:')

    def test_integer_value(self):
        """Non-string, non-list values should be included as-is."""
        spec = {'Timeout': 43200}
        result = spec_to_string(spec, ['Timeout'])
        assert result == 'Timeout: 43200\n'
