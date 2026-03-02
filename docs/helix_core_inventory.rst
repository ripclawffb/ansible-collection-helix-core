Dynamic Inventory Plugin
========================

The ``ripclawffb.helix_core.helix_core`` inventory plugin discovers your
Perforce server topology automatically by querying ``p4 servers`` on the
commit server.

Use Case
--------

In a Perforce **federated environment**, you have a commit server plus
edge and replica servers. Instead of maintaining a static inventory file,
this plugin queries the commit server and builds the inventory dynamically.
When you add a new edge server to your Perforce federation, it appears in
inventory automatically — no manual updates needed.

Configuration
-------------

Create an inventory file ending in ``.helix_core.yml`` or ``.helix_core.yaml``:

.. code-block:: yaml

   # inventory.helix_core.yml
   plugin: ripclawffb.helix_core.helix_core
   server: ssl:commit-server:1666
   user: admin
   password: "{{ vault_p4_password }}"

Options
~~~~~~~

+-------------------+----------+-----------+----------------------------------------------+
| Option            | Required | Default   | Description                                  |
+===================+==========+===========+==============================================+
| ``plugin``        | yes      |           | Must be ``ripclawffb.helix_core.helix_core`` |
+-------------------+----------+-----------+----------------------------------------------+
| ``server``        | yes      |           | P4PORT of the commit server                  |
+-------------------+----------+-----------+----------------------------------------------+
| ``user``          | yes      |           | Perforce user with ``p4 servers`` access      |
+-------------------+----------+-----------+----------------------------------------------+
| ``password``      | yes      |           | Perforce password                            |
+-------------------+----------+-----------+----------------------------------------------+
| ``charset``       | no       | ``none``  | P4CHARSET value                              |
+-------------------+----------+-----------+----------------------------------------------+
| ``server_types``  | no       | ``[]``    | Filter to specific types                     |
+-------------------+----------+-----------+----------------------------------------------+
| ``include_commit``| no       | ``true``  | Include the commit server                    |
+-------------------+----------+-----------+----------------------------------------------+

All connection options also support environment variable fallback
(``P4PORT``, ``P4USER``, ``P4PASSWD``, ``P4CHARSET``).

Example Output
--------------

Running ``ansible-inventory -i inventory.helix_core.yml --list``:

.. code-block:: json

   {
     "commit_server": {
       "hosts": ["master.1"]
     },
     "edge_server": {
       "hosts": ["edge-chicago", "edge-london"]
     },
     "replica": {
       "hosts": ["replica-backup"]
     },
     "_meta": {
       "hostvars": {
         "edge-chicago": {
           "ansible_host": "edge-chi.example.com",
           "server_id": "edge-chicago",
           "server_address": "ssl:edge-chi.example.com:1666",
           "server_type": "edge-server",
           "services": "edge-server",
           "description": "Chicago edge server",
           "p4port": "ssl:edge-chi.example.com:1666"
         }
       }
     }
   }

Practical Examples
------------------

**Target all edge servers:**

.. code-block:: yaml

   - hosts: edge_server
     tasks:
       - name: Set configurables on all edges
         ripclawffb.helix_core.helix_core_configurable:
           name: dm.keys.hide
           value: "2"

**Group by server type with custom prefix:**

.. code-block:: yaml

   # inventory.helix_core.yml
   plugin: ripclawffb.helix_core.helix_core
   server: ssl:commit-server:1666
   user: admin
   password: "{{ vault_p4_password }}"
   keyed_groups:
     - key: server_type
       prefix: p4
       separator: "_"

This creates groups like ``p4_edge_server``, ``p4_commit_server``, etc.

**Filter to edge servers only:**

.. code-block:: yaml

   # inventory.helix_core.yml
   plugin: ripclawffb.helix_core.helix_core
   server: ssl:commit-server:1666
   user: admin
   password: "{{ vault_p4_password }}"
   server_types:
     - edge-server

Host Variables
--------------

Each discovered server has the following host variables:

+---------------------+--------------------------------------------------+
| Variable            | Description                                      |
+=====================+==================================================+
| ``ansible_host``    | Hostname extracted from ``ServerAddress``         |
+---------------------+--------------------------------------------------+
| ``server_id``       | The Perforce ``ServerID``                        |
+---------------------+--------------------------------------------------+
| ``server_address``  | Full ``ServerAddress`` (e.g. ``ssl:host:1666``)  |
+---------------------+--------------------------------------------------+
| ``server_type``     | Server type (``edge-server``, ``replica``, etc.) |
+---------------------+--------------------------------------------------+
| ``services``        | Raw ``Services`` field                           |
+---------------------+--------------------------------------------------+
| ``description``     | Server description                               |
+---------------------+--------------------------------------------------+
| ``p4port``          | Same as ``server_address``, for convenience      |
+---------------------+--------------------------------------------------+
| ``p4_port_number``  | Port number extracted from address               |
+---------------------+--------------------------------------------------+
