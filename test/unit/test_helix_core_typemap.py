"""
Unit tests for typemap helpers.

These are pure-function tests — no Perforce connection required.
Run with: pytest test/unit/test_helix_core_typemap.py -v
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from plugins.modules.helix_core_typemap import typemap_to_list, list_to_typemap


class TestTypemapToList:
    def test_basic_entries(self):
        spec = {'TypeMap': ['binary+l //depot/....exe', 'text+k //depot/....txt']}
        result = typemap_to_list(spec)
        assert result == [('binary+l', '//depot/....exe'), ('text+k', '//depot/....txt')]

    def test_empty_typemap(self):
        spec = {'TypeMap': []}
        assert typemap_to_list(spec) == []

    def test_missing_typemap_key(self):
        assert typemap_to_list({}) == []

    def test_none_typemap(self):
        assert typemap_to_list({'TypeMap': None}) == []

    def test_path_with_spaces(self):
        """Paths shouldn't have spaces normally, but split(None, 1) handles it."""
        spec = {'TypeMap': ['binary //depot/path with spaces/...']}
        result = typemap_to_list(spec)
        assert result == [('binary', '//depot/path with spaces/...')]

    def test_malformed_entry_skipped(self):
        """Single-word entries with no path should be skipped."""
        spec = {'TypeMap': ['binary+l']}
        result = typemap_to_list(spec)
        assert result == []


class TestListToTypemap:
    def test_basic_conversion(self):
        entries = [{'type': 'binary+l', 'path': '//depot/....exe'},
                   {'type': 'text+k', 'path': '//depot/....txt'}]
        result = list_to_typemap(entries)
        assert result == ['binary+l //depot/....exe', 'text+k //depot/....txt']

    def test_empty_list(self):
        assert list_to_typemap([]) == []

    def test_roundtrip(self):
        """list_to_typemap output should be parseable by typemap_to_list."""
        entries = [{'type': 'binary+l', 'path': '//depot/....exe'}]
        strings = list_to_typemap(entries)
        parsed = typemap_to_list({'TypeMap': strings})
        assert parsed == [('binary+l', '//depot/....exe')]
