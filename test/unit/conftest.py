"""
Shared pytest configuration for unit tests.

Mocks ansible and ansible_collections dependencies so that module-level
imports in plugins/modules/*.py don't fail when ansible is not installed.
"""

import sys
import os
from unittest.mock import MagicMock

# Add the collection root to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Mock ansible core modules
ansible_mock = MagicMock()
ansible_mock.module_utils.basic.env_fallback = MagicMock()

sys.modules['ansible'] = ansible_mock
sys.modules['ansible.module_utils'] = ansible_mock.module_utils
sys.modules['ansible.module_utils.basic'] = ansible_mock.module_utils.basic

# Mock P4 module (used by _helix_core_connection)
sys.modules['P4'] = MagicMock()

# Import real module_utils so they're available under the ansible_collections path
from plugins.module_utils import _helix_core_connection  # noqa: E402

# Mock the ansible_collections import chain, pointing to our real modules
ac_mock = MagicMock()
ac_mock.ripclawffb.helix_core.plugins.module_utils._helix_core_connection = _helix_core_connection

sys.modules['ansible_collections'] = ac_mock
sys.modules['ansible_collections.ripclawffb'] = ac_mock.ripclawffb
sys.modules['ansible_collections.ripclawffb.helix_core'] = ac_mock.ripclawffb.helix_core
sys.modules['ansible_collections.ripclawffb.helix_core.plugins'] = ac_mock.ripclawffb.helix_core.plugins
sys.modules['ansible_collections.ripclawffb.helix_core.plugins.module_utils'] = ac_mock.ripclawffb.helix_core.plugins.module_utils
sys.modules['ansible_collections.ripclawffb.helix_core.plugins.module_utils._helix_core_connection'] = _helix_core_connection
