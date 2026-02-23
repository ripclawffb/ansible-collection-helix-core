"""
Unit tests for LDAP sync_options helper.

These are pure-function tests — no Perforce connection required.
Run with: pytest test/unit/test_helix_core_ldap.py -v
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from plugins.modules.helix_core_ldap import sync_options


class TestSyncOptions:
    def test_none_desired_returns_existing(self):
        result = sync_options("nodowncase nogetattrs", None)
        assert result == "nodowncase nogetattrs"

    def test_empty_existing_uses_defaults(self):
        result = sync_options("", ['downcase'])
        # Empty string triggers default "nodowncase nogetattrs norealminusername"
        # Then 'downcase' replaces 'nodowncase'
        opts = set(result.split())
        assert 'downcase' in opts
        assert 'nodowncase' not in opts
        assert 'nogetattrs' in opts
        assert 'norealminusername' in opts

    def test_set_downcase_removes_nodowncase(self):
        result = sync_options("nodowncase nogetattrs norealminusername", ['downcase'])
        opts = set(result.split())
        assert 'downcase' in opts
        assert 'nodowncase' not in opts

    def test_set_nodowncase_removes_downcase(self):
        result = sync_options("downcase nogetattrs norealminusername", ['nodowncase'])
        opts = set(result.split())
        assert 'nodowncase' in opts
        assert 'downcase' not in opts

    def test_set_getattrs_removes_nogetattrs(self):
        result = sync_options("nodowncase nogetattrs norealminusername", ['getattrs'])
        opts = set(result.split())
        assert 'getattrs' in opts
        assert 'nogetattrs' not in opts

    def test_set_realminusername_removes_norealminusername(self):
        result = sync_options("nodowncase nogetattrs norealminusername", ['realminusername'])
        opts = set(result.split())
        assert 'realminusername' in opts
        assert 'norealminusername' not in opts

    def test_multiple_options(self):
        result = sync_options("nodowncase nogetattrs norealminusername", ['downcase', 'getattrs'])
        opts = set(result.split())
        assert 'downcase' in opts
        assert 'getattrs' in opts
        assert 'nodowncase' not in opts
        assert 'nogetattrs' not in opts
        assert 'norealminusername' in opts

    def test_result_is_sorted(self):
        result = sync_options("nodowncase nogetattrs norealminusername", ['downcase'])
        words = result.split()
        assert words == sorted(words)

    def test_idempotent_same_option(self):
        """Setting an option that's already set should not change anything."""
        existing = "nodowncase nogetattrs norealminusername"
        result = sync_options(existing, ['nodowncase'])
        opts = set(result.split())
        expected = set(existing.split())
        assert opts == expected
