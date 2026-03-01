"""
Helpers for comparing and updating Perforce spec dicts against Ansible module parameters.
"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


def build_after_spec(params, mapping):
    """
    Build a dict representing the desired 'after' state for diff output.

    Args:
        params: The module params dict.
        mapping: Dict mapping spec field names to param keys,
                 e.g. {'Description': 'description', 'Users': 'users'}.

    Returns:
        A dict containing only fields whose param value is not None.
    """
    after = {}
    for spec_field, param_key in mapping.items():
        value = params.get(param_key)
        if value is not None:
            after[spec_field] = value
    return after


def check_spec(spec, params, mapping, rstrip_fields=None):
    """
    Compare a Perforce spec dict against module params to detect changes.

    Args:
        spec: The current Perforce spec dict (from p4.fetch_*).
        params: The module params dict.
        mapping: Dict mapping spec field names to param keys.
        rstrip_fields: Optional list of spec field names whose values should
                       be .rstrip()'d before comparison (e.g. ['Description']).

    Returns:
        True if changes are detected (i.e. spec differs from params),
        False if no changes are needed.
    """
    if rstrip_fields is None:
        rstrip_fields = []

    for spec_field, param_key in mapping.items():
        param_value = params.get(param_key)

        if param_value is not None:
            # Param is provided — compare against spec
            spec_value = spec.get(spec_field)
            if spec_value is None:
                # Spec key doesn't exist but param is provided.
                # Perforce drops empty list fields from specs, so an empty
                # list param is equivalent to a missing spec key.
                if isinstance(param_value, list) and len(param_value) == 0:
                    continue
                return True

            # Apply rstrip if configured for this field
            if spec_field in rstrip_fields and isinstance(spec_value, str):
                spec_value = spec_value.rstrip()

            if spec_value != param_value:
                return True
        else:
            # Param is None (optional, not provided) — if spec key exists,
            # that means it should be removed
            if spec_field in spec:
                return True

    return False


def update_spec(spec, params, mapping):
    """
    Apply module param values to a Perforce spec dict in-place.

    For provided params (not None), the spec field is set.
    For None params, the spec field is deleted if it exists.

    Args:
        spec: The Perforce spec dict to update in-place.
        params: The module params dict.
        mapping: Dict mapping spec field names to param keys.
    """
    for spec_field, param_key in mapping.items():
        param_value = params.get(param_key)

        if param_value is not None:
            spec[spec_field] = param_value
        elif spec_field in spec:
            del spec[spec_field]


def changed_fields(spec, params, mapping, rstrip_fields=None):
    """
    Compare a Perforce spec dict against module params and return per-field diffs.

    Uses the same comparison logic as check_spec but collects all differences
    instead of returning a boolean on the first mismatch.

    Args:
        spec: The current Perforce spec dict (from p4.fetch_*).
        params: The module params dict.
        mapping: Dict mapping spec field names to param keys.
        rstrip_fields: Optional list of spec field names whose values should
                       be .rstrip()'d before comparison (e.g. ['Description']).

    Returns:
        A list of dicts, each with 'field', 'before', and 'after' keys.
        Empty list means no changes detected.
    """
    if rstrip_fields is None:
        rstrip_fields = []

    changes = []

    for spec_field, param_key in mapping.items():
        param_value = params.get(param_key)

        if param_value is not None:
            spec_value = spec.get(spec_field)
            if spec_value is None:
                if isinstance(param_value, list) and len(param_value) == 0:
                    continue
                changes.append({'field': spec_field, 'before': None, 'after': param_value})
                continue

            compare_value = spec_value
            if spec_field in rstrip_fields and isinstance(compare_value, str):
                compare_value = compare_value.rstrip()

            if compare_value != param_value:
                changes.append({'field': spec_field, 'before': spec_value, 'after': param_value})
        else:
            if spec_field in spec:
                changes.append({'field': spec_field, 'before': spec.get(spec_field), 'after': None})

    return changes
