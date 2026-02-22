"""
Unit tests for _helix_core_spec helpers.

These are pure-function tests — no Perforce connection required.
Run with: pytest test/unit/test_helix_core_spec.py -v
"""

import sys
import os
import pytest

# Add the collection root to sys.path so we can import the helpers directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from plugins.module_utils._helix_core_spec import (
    build_after_spec,
    check_spec,
    update_spec,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def simple_mapping():
    """A mapping with required and optional fields."""
    return {
        'Description': 'description',
        'Type': 'type',
        'Address': 'address',       # optional
        'Users': 'users',           # optional list
    }


# ---------------------------------------------------------------------------
# check_spec tests
# ---------------------------------------------------------------------------

class TestCheckSpec:
    def test_no_changes(self, simple_mapping):
        spec = {'Description': 'my depot', 'Type': 'local'}
        params = {'description': 'my depot', 'type': 'local', 'address': None, 'users': None}
        assert check_spec(spec, params, simple_mapping) is False

    def test_required_field_mismatch(self, simple_mapping):
        spec = {'Description': 'old', 'Type': 'local'}
        params = {'description': 'new', 'type': 'local', 'address': None, 'users': None}
        assert check_spec(spec, params, simple_mapping) is True

    def test_rstrip(self, simple_mapping):
        spec = {'Description': 'my depot   \n', 'Type': 'local'}
        params = {'description': 'my depot', 'type': 'local', 'address': None, 'users': None}
        # Without rstrip_fields, this should detect a change
        assert check_spec(spec, params, simple_mapping) is True
        # With rstrip_fields, trailing whitespace is stripped before comparison
        assert check_spec(spec, params, simple_mapping, rstrip_fields=['Description']) is False

    def test_optional_both_absent(self, simple_mapping):
        spec = {'Description': 'x', 'Type': 'local'}
        params = {'description': 'x', 'type': 'local', 'address': None, 'users': None}
        assert check_spec(spec, params, simple_mapping) is False

    def test_optional_param_none_spec_exists(self, simple_mapping):
        spec = {'Description': 'x', 'Type': 'local', 'Address': '1.2.3.4'}
        params = {'description': 'x', 'type': 'local', 'address': None, 'users': None}
        assert check_spec(spec, params, simple_mapping) is True

    def test_optional_param_set_spec_missing(self, simple_mapping):
        spec = {'Description': 'x', 'Type': 'local'}
        params = {'description': 'x', 'type': 'local', 'address': '1.2.3.4', 'users': None}
        assert check_spec(spec, params, simple_mapping) is True

    def test_optional_param_matches(self, simple_mapping):
        spec = {'Description': 'x', 'Type': 'local', 'Address': '1.2.3.4'}
        params = {'description': 'x', 'type': 'local', 'address': '1.2.3.4', 'users': None}
        assert check_spec(spec, params, simple_mapping) is False

    def test_list_field(self, simple_mapping):
        spec = {'Description': 'x', 'Type': 'local', 'Users': ['alice', 'bob']}
        params = {'description': 'x', 'type': 'local', 'address': None, 'users': ['alice', 'bob']}
        assert check_spec(spec, params, simple_mapping) is False

        params_changed = {'description': 'x', 'type': 'local', 'address': None, 'users': ['alice']}
        assert check_spec(spec, params_changed, simple_mapping) is True

    def test_empty_list_equals_absent(self, simple_mapping):
        """Perforce drops empty list fields from specs, so [] == key absent."""
        spec = {'Description': 'x', 'Type': 'local'}
        params = {'description': 'x', 'type': 'local', 'address': None, 'users': []}
        assert check_spec(spec, params, simple_mapping) is False


# ---------------------------------------------------------------------------
# update_spec tests
# ---------------------------------------------------------------------------

class TestUpdateSpec:
    def test_sets_required(self, simple_mapping):
        spec = {'Description': 'old', 'Type': 'local'}
        params = {'description': 'new', 'type': 'remote', 'address': None, 'users': None}
        update_spec(spec, params, simple_mapping)
        assert spec['Description'] == 'new'
        assert spec['Type'] == 'remote'

    def test_adds_optional(self, simple_mapping):
        spec = {'Description': 'x', 'Type': 'local'}
        params = {'description': 'x', 'type': 'local', 'address': '1.2.3.4', 'users': None}
        update_spec(spec, params, simple_mapping)
        assert spec['Address'] == '1.2.3.4'

    def test_deletes_optional(self, simple_mapping):
        spec = {'Description': 'x', 'Type': 'local', 'Address': '1.2.3.4'}
        params = {'description': 'x', 'type': 'local', 'address': None, 'users': None}
        update_spec(spec, params, simple_mapping)
        assert 'Address' not in spec

    def test_no_delete_if_key_absent(self, simple_mapping):
        spec = {'Description': 'x', 'Type': 'local'}
        params = {'description': 'x', 'type': 'local', 'address': None, 'users': None}
        # Should not raise KeyError
        update_spec(spec, params, simple_mapping)
        assert 'Address' not in spec


# ---------------------------------------------------------------------------
# build_after_spec tests
# ---------------------------------------------------------------------------

class TestBuildAfterSpec:
    def test_includes_required(self, simple_mapping):
        params = {'description': 'x', 'type': 'local', 'address': '1.2.3.4', 'users': None}
        result = build_after_spec(params, simple_mapping)
        assert result == {'Description': 'x', 'Type': 'local', 'Address': '1.2.3.4'}

    def test_skips_none(self, simple_mapping):
        params = {'description': 'x', 'type': 'local', 'address': None, 'users': None}
        result = build_after_spec(params, simple_mapping)
        assert result == {'Description': 'x', 'Type': 'local'}
        assert 'Address' not in result
        assert 'Users' not in result
