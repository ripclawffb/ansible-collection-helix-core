.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.24.0

.. Anchors

.. _ansible_collections.ripclawffb.helix_core.helix_core_inventory:

.. Anchors: short name for ansible.builtin

.. Title

ripclawffb.helix_core.helix_core inventory -- Perforce Helix Core dynamic inventory plugin
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This inventory plugin is part of the `ripclawffb.helix_core collection <https://galaxy.ansible.com/ui/repo/published/ripclawffb/helix_core/>`_ (version 1.3.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible\-galaxy collection install ripclawffb.helix\_core`.
    You need further requirements to be able to use this inventory plugin,
    see :ref:`Requirements <ansible_collections.ripclawffb.helix_core.helix_core_inventory_requirements>` for details.

    To use it in a playbook, specify: :code:`ripclawffb.helix_core.helix_core`.

.. version_added

.. rst-class:: ansible-version-added

New in ripclawffb.helix\_core 1.3.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Discovers Perforce server topology by querying :literal:`p4 servers`.
- Each registered server becomes an Ansible host, keyed by its :literal:`ServerID`.
- Hosts are automatically grouped by server type (commit, edge, replica, etc.).
- Supports Constructable features like :literal:`compose`\ , :literal:`keyed\_groups`\ , and :literal:`groups`.
- Ideal for federated Perforce environments with commit + edge/replica servers.


.. Aliases


.. Requirements

.. _ansible_collections.ripclawffb.helix_core.helix_core_inventory_requirements:

Requirements
------------
The below requirements are needed on the local controller node that executes this inventory.

- P4Python pip module is required






.. Options

Parameters
----------

.. tabularcolumns:: \X{1}{3}\X{2}{3}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Parameter
    - Comments

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-charset"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_inventory__parameter-charset:

      .. rst-class:: ansible-option-title

      **charset**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-charset" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Character set used for translation of unicode files.

      Can also use :literal:`P4CHARSET` environment variable.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"none"`

      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - Environment variable: :envvar:`P4CHARSET`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-compose"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_inventory__parameter-compose:

      .. rst-class:: ansible-option-title

      **compose**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-compose" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Create vars from jinja2 expressions.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`{}`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-groups"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_inventory__parameter-groups:

      .. rst-class:: ansible-option-title

      **groups**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-groups" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Add hosts to group based on Jinja2 conditionals.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`{}`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-include_commit"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_inventory__parameter-include_commit:

      .. rst-class:: ansible-option-title

      **include_commit**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-include_commit" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Whether to include the commit server itself in the inventory.

      Only relevant when the commit server has a registered server spec.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-keyed_groups"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_inventory__parameter-keyed_groups:

      .. rst-class:: ansible-option-title

      **keyed_groups**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-keyed_groups" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Add hosts to group based on the values of a variable.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`[]`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-keyed_groups/default_value"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.ripclawffb.helix_core.helix_core_inventory__parameter-keyed_groups/default_value:

      .. rst-class:: ansible-option-title

      **default_value**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-keyed_groups/default_value" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in ansible-core 2.12`





      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The default value when the host variable's value is an empty string.

      This option is mutually exclusive with :ansopt:`ripclawffb.helix\_core.helix\_core#inventory:keyed\_groups[].trailing\_separator`.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-keyed_groups/key"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.ripclawffb.helix_core.helix_core_inventory__parameter-keyed_groups/key:

      .. rst-class:: ansible-option-title

      **key**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-keyed_groups/key" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The key from input dictionary used to generate groups


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-keyed_groups/parent_group"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.ripclawffb.helix_core.helix_core_inventory__parameter-keyed_groups/parent_group:

      .. rst-class:: ansible-option-title

      **parent_group**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-keyed_groups/parent_group" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      parent group for keyed group


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-keyed_groups/prefix"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.ripclawffb.helix_core.helix_core_inventory__parameter-keyed_groups/prefix:

      .. rst-class:: ansible-option-title

      **prefix**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-keyed_groups/prefix" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      A keyed group name will start with this prefix


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-keyed_groups/separator"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.ripclawffb.helix_core.helix_core_inventory__parameter-keyed_groups/separator:

      .. rst-class:: ansible-option-title

      **separator**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-keyed_groups/separator" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      separator used to build the keyed group name


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"\_"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-keyed_groups/trailing_separator"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.ripclawffb.helix_core.helix_core_inventory__parameter-keyed_groups/trailing_separator:

      .. rst-class:: ansible-option-title

      **trailing_separator**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-keyed_groups/trailing_separator" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in ansible-core 2.12`





      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Set this option to :ansval:`False` to omit the :ansopt:`ripclawffb.helix\_core.helix\_core#inventory:keyed\_groups[].separator` after the host variable when the value is an empty string.

      This option is mutually exclusive with :ansopt:`ripclawffb.helix\_core.helix\_core#inventory:keyed\_groups[].default\_value`.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-leading_separator"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_inventory__parameter-leading_separator:

      .. rst-class:: ansible-option-title

      **leading_separator**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-leading_separator" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in ansible-core 2.11`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Use in conjunction with keyed\_groups.

      By default, a keyed group that does not have a prefix or a separator provided will have a name that starts with an underscore.

      This is because the default prefix is "" and the default separator is "\_".

      Set this option to False to omit the leading underscore (or other separator) if no prefix is given.

      If the group name is derived from a mapping the separator is still used to concatenate the items.

      To not use a separator in the group name at all, set the separator for the keyed group to an empty string instead.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-password"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_inventory__parameter-password:

      .. rst-class:: ansible-option-title

      **password**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-password" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The login password for the Perforce user.

      Can also use :literal:`P4PASSWD` environment variable.


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - Environment variable: :envvar:`P4PASSWD`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-plugin"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_inventory__parameter-plugin:

      .. rst-class:: ansible-option-title

      **plugin**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-plugin" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Token to ensure this is an inventory plugin file.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"ripclawffb.helix\_core.helix\_core"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-server"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_inventory__parameter-server:

      .. rst-class:: ansible-option-title

      **server**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-server" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The hostname/ip and port of the Perforce server (e.g. :literal:`ssl:perforce:1666`\ ).

      Can also use :literal:`P4PORT` environment variable.


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - Environment variable: :envvar:`P4PORT`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-server_types"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_inventory__parameter-server_types:

      .. rst-class:: ansible-option-title

      **server_types**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-server_types" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Optional list of server types to include in the inventory.

      Valid types include :literal:`commit\-server`\ , :literal:`edge\-server`\ , :literal:`replica`\ , :literal:`forwarding\-replica`\ , :literal:`build\-server`\ , :literal:`depot\-master`\ , etc.

      If omitted, all server types are included.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`[]`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-strict"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_inventory__parameter-strict:

      .. rst-class:: ansible-option-title

      **strict**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-strict" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      If :ansval:`yes` make invalid entries a fatal error, otherwise skip and continue.

      Since it is possible to use facts in the expressions they might not always be available and we ignore those errors by default.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-use_extra_vars"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_inventory__parameter-use_extra_vars:

      .. rst-class:: ansible-option-title

      **use_extra_vars**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-use_extra_vars" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in ansible-core 2.11`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Merge extra vars into the available variables for composition (highest precedence).


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entry:

        .. code-block:: ini

          [inventory_plugins]
          use_extra_vars = false


      - Environment variable: :envvar:`ANSIBLE\_INVENTORY\_USE\_EXTRA\_VARS`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-user"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_inventory__parameter-user:

      .. rst-class:: ansible-option-title

      **user**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-user" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A Perforce user with permission to run :literal:`p4 servers`.

      Can also use :literal:`P4USER` environment variable.


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - Environment variable: :envvar:`P4USER`


      .. raw:: html

        </div>


.. note::

    Configuration entries listed above for each entry type (Ansible variable, environment variable, and so on) have a low to high priority order.
    For example, a variable that is lower in the list will override a variable that is higher up.
    The entry types are also ordered by precedence from low to high priority order.
    For example, an ansible.cfg entry (further up in the list) is overwritten by an Ansible variable (further down in the list).

.. Attributes


.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    # Minimal inventory file — discover all servers
    # inventory.helix_core.yml
    plugin: ripclawffb.helix_core.helix_core
    server: ssl:commit-server:1666
    user: admin
    password: "{{ vault_p4_password }}"

    # Filter to only edge servers and group by type
    plugin: ripclawffb.helix_core.helix_core
    server: ssl:commit-server:1666
    user: admin
    password: "{{ vault_p4_password }}"
    server_types:
      - edge-server
      - commit-server
    keyed_groups:
      - key: server_type
        prefix: p4
        separator: "_"

    # Use compose to set ansible_host from the server address
    plugin: ripclawffb.helix_core.helix_core
    server: ssl:commit-server:1666
    user: admin
    password: "{{ vault_p4_password }}"
    compose:
      ansible_port: 22



.. Facts


.. Return values


..  Status (Presently only deprecated)


.. Authors


.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. ansible-links::

  - title: "Issue Tracker"
    url: "https://github.com/ripclawffb/ansible-collection-helix-core/issues"
    external: true
  - title: "Homepage"
    url: "https://galaxy.ansible.com/ui/repo/published/ripclawffb/helix_core/"
    external: true
  - title: "Repository (Sources)"
    url: "https://github.com/ripclawffb/ansible-collection-helix-core"
    external: true


.. Parsing errors
