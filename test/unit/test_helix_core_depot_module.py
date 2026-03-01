"""
Unit tests for helix_core_depot run_module().

Mocks P4 and AnsibleModule to test all branching logic.
Run with: pytest test/unit/test_helix_core_depot_module.py -v
"""

import sys
import os
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


class AnsibleExitJson(Exception):
    """Exception to capture exit_json calls."""
    pass


class AnsibleFailJson(Exception):
    """Exception to capture fail_json calls."""
    pass


def exit_json_side_effect(**kwargs):
    raise AnsibleExitJson(kwargs)


def fail_json_side_effect(**kwargs):
    raise AnsibleFailJson(kwargs)


@pytest.fixture
def mock_module():
    """Create a mock AnsibleModule with default params for depot."""
    module = MagicMock()
    module.params = {
        'state': 'present',
        'name': 'test_depot',
        'description': 'Test depot',
        'type': 'local',
        'map': 'test_depot/...',
        'address': None,
        'specmap': None,
        'streamdepth': None,
        'suffix': None,
        'server': '1666',
        'user': 'admin',
        'password': 'pass',
        'charset': 'none',
    }
    module.check_mode = False
    module._diff = False
    module.exit_json = MagicMock(side_effect=exit_json_side_effect)
    module.fail_json = MagicMock(side_effect=fail_json_side_effect)
    return module


@pytest.fixture
def mock_p4():
    """Create a mock P4 connection."""
    p4 = MagicMock()
    p4.connected.return_value = True
    return p4


@pytest.fixture
def existing_depot_spec():
    """A depot spec representing an existing depot."""
    return {
        'Depot': 'test_depot',
        'Description': 'Test depot',
        'Type': 'local',
        'Map': 'test_depot/...',
    }


class TestDepotCreate:
    def test_create_new_depot(self, mock_module, mock_p4, existing_depot_spec):
        mock_p4.fetch_depot.return_value = existing_depot_spec
        mock_p4.run.return_value = []  # no existing depots

        with patch('plugins.modules.helix_core_depot.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_depot.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_depot.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_depot import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'created'
        assert result['depot_spec'] is not None
        mock_p4.save_depot.assert_called_once()

    def test_create_new_depot_check_mode(self, mock_module, mock_p4, existing_depot_spec):
        mock_module.check_mode = True
        mock_p4.fetch_depot.return_value = existing_depot_spec
        mock_p4.run.return_value = []

        with patch('plugins.modules.helix_core_depot.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_depot.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_depot.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_depot import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'created'
        mock_p4.save_depot.assert_not_called()


class TestDepotUpdate:
    def test_update_existing_no_changes(self, mock_module, mock_p4, existing_depot_spec):
        mock_p4.fetch_depot.return_value = existing_depot_spec
        mock_p4.run.return_value = [{'name': 'test_depot'}]

        with patch('plugins.modules.helix_core_depot.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_depot.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_depot.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_depot import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert result['action'] == 'unchanged'
        assert result['changes'] == []
        assert result['depot_spec'] == existing_depot_spec
        mock_p4.save_depot.assert_not_called()

    def test_update_existing_with_changes(self, mock_module, mock_p4, existing_depot_spec):
        mock_module.params['description'] = 'Updated description'
        mock_p4.fetch_depot.return_value = existing_depot_spec
        mock_p4.run.return_value = [{'name': 'test_depot'}]

        with patch('plugins.modules.helix_core_depot.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_depot.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_depot.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_depot import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'updated'
        assert len(result['changes']) > 0
        assert result['changes'][0]['field'] == 'Description'
        mock_p4.save_depot.assert_called_once()

    def test_update_with_changes_check_mode(self, mock_module, mock_p4, existing_depot_spec):
        mock_module.check_mode = True
        mock_module.params['description'] = 'Updated description'
        mock_p4.fetch_depot.return_value = existing_depot_spec
        mock_p4.run.return_value = [{'name': 'test_depot'}]

        with patch('plugins.modules.helix_core_depot.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_depot.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_depot.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_depot import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'updated'
        mock_p4.save_depot.assert_not_called()


class TestDepotDelete:
    def test_delete_existing_depot(self, mock_module, mock_p4, existing_depot_spec):
        mock_module.params['state'] = 'absent'
        mock_p4.fetch_depot.return_value = existing_depot_spec
        mock_p4.run.return_value = [{'name': 'test_depot'}]

        with patch('plugins.modules.helix_core_depot.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_depot.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_depot.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_depot import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'deleted'
        mock_p4.delete_depot.assert_called_once_with('-f', 'test_depot')

    def test_delete_nonexistent_depot(self, mock_module, mock_p4):
        mock_module.params['state'] = 'absent'
        mock_p4.run.return_value = []  # depot not found

        with patch('plugins.modules.helix_core_depot.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_depot.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_depot.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_depot import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is False
        assert result['action'] == 'unchanged'
        mock_p4.delete_depot.assert_not_called()

    def test_delete_check_mode(self, mock_module, mock_p4, existing_depot_spec):
        mock_module.params['state'] = 'absent'
        mock_module.check_mode = True
        mock_p4.fetch_depot.return_value = existing_depot_spec
        mock_p4.run.return_value = [{'name': 'test_depot'}]

        with patch('plugins.modules.helix_core_depot.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_depot.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_depot.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_depot import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert result['action'] == 'deleted'
        mock_p4.delete_depot.assert_not_called()


class TestDepotDiff:
    def test_create_with_diff(self, mock_module, mock_p4, existing_depot_spec):
        mock_module._diff = True
        mock_p4.fetch_depot.return_value = existing_depot_spec
        mock_p4.run.return_value = []

        with patch('plugins.modules.helix_core_depot.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_depot.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_depot.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_depot import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert result['changed'] is True
        assert 'diff' in result
        assert result['diff']['before'] == ''
        assert 'Description' in result['diff']['after']

    def test_update_with_diff(self, mock_module, mock_p4, existing_depot_spec):
        mock_module._diff = True
        mock_module.params['description'] = 'Updated'
        mock_p4.fetch_depot.return_value = existing_depot_spec
        mock_p4.run.return_value = [{'name': 'test_depot'}]

        with patch('plugins.modules.helix_core_depot.helix_core_connect', return_value=mock_p4):
            with patch('plugins.modules.helix_core_depot.helix_core_disconnect'):
                with patch('plugins.modules.helix_core_depot.AnsibleModule', return_value=mock_module):
                    from plugins.modules.helix_core_depot import run_module
                    with pytest.raises(AnsibleExitJson) as exc_info:
                        run_module()

        result = exc_info.value.args[0]
        assert 'diff' in result
        assert 'Test depot' in result['diff']['before']
        assert 'Updated' in result['diff']['after']
