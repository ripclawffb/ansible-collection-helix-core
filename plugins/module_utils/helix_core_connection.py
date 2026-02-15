"""
This module is used to make connections to Perforce Helix
"""

from __future__ import (absolute_import, division, print_function)
import traceback
__metaclass__ = type

try:
    from P4 import P4
    HAS_P4 = True
except ImportError:
    P4_IMP_ERR = traceback.format_exc()
    HAS_P4 = False

from ansible.module_utils.basic import missing_required_lib, env_fallback


def helix_core_connection_argspec():
    """
    Returns the common connection arguments used by all Helix Core modules.
    This avoids duplicating these argument definitions across all modules.
    """
    return dict(
        server=dict(type='str', required=True, aliases=['p4port'], fallback=(env_fallback, ['P4PORT'])),
        user=dict(type='str', required=True, aliases=['p4user'], fallback=(env_fallback, ['P4USER'])),
        password=dict(type='str', required=True, aliases=['p4passwd'], fallback=(env_fallback, ['P4PASSWD']), no_log=True),
        charset=dict(type='str', default='none', aliases=['p4charset'], fallback=(env_fallback, ['P4CHARSET'])),
    )


def helix_core_connect(module, script_name):
    """
    Pass this function a user, p4port, password to connect to a Helix Core server
    """

    if not HAS_P4:
        module.fail_json(msg=missing_required_lib('p4python', url='https://pypi.org/project/p4python/'), exception=P4_IMP_ERR)

    try:
        p4 = P4()
        p4.prog = script_name
        p4.port = module.params['server']
        p4.user = module.params['user']
        p4.password = module.params['password']
        p4.charset = module.params['charset']
        p4.connect()
        p4.run_login()
        if p4.connected() is not True:
            module.fail_json(msg="Unable to connect to Helix")
        return p4
    except Exception as e:
        module.fail_json(msg="There was a problem connecting to Helix: {0}".format(e))


def helix_core_disconnect(module, connection):
    """
    Pass this function a connection object to disconnect the Helix Core
    session
    """

    try:
        connection.disconnect()
    except Exception as e:
        module.fail_json(msg="There was a problem disconnecting from Helix: {0}".format(e))


def spec_to_string(spec, fields):
    """
    Convert a Perforce spec dict to a readable string for diff output.
    Only includes the specified fields. List values are joined with newlines.
    """
    lines = []
    for field in fields:
        val = spec.get(field, '')
        if isinstance(val, list):
            val = ', '.join(val)
        if isinstance(val, str):
            val = val.rstrip()
        lines.append('{0}: {1}'.format(field, val))
    return '\n'.join(lines) + '\n'
