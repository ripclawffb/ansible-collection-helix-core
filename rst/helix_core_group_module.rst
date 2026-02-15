.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.24.0

.. Anchors

.. _ansible_collections.ripclawffb.helix_core.helix_core_group_module:

.. Anchors: short name for ansible.builtin

.. Title

ripclawffb.helix_core.helix_core_group module -- Manage groups on Perforce Helix Core
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `ripclawffb.helix_core collection <https://galaxy.ansible.com/ui/repo/published/ripclawffb/helix_core/>`_ (version 1.0.7).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible\-galaxy collection install ripclawffb.helix\_core`.
    You need further requirements to be able to use this module,
    see :ref:`Requirements <ansible_collections.ripclawffb.helix_core.helix_core_group_module_requirements>` for details.

    To use it in a playbook, specify: :code:`ripclawffb.helix_core.helix_core_group`.

.. version_added

.. rst-class:: ansible-version-added

New in ripclawffb.helix\_core 1.0.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Add or delete users from a group, or set the maxresults, maxscanrows, maxlocktime, and timeout limits for the members of a group
- This module supports check mode.


.. Aliases


.. Requirements

.. _ansible_collections.ripclawffb.helix_core.helix_core_group_module_requirements:

Requirements
------------
The below requirements are needed on the host that executes this module.

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
        <div class="ansibleOptionAnchor" id="parameter-p4charset"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__parameter-charset:
      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__parameter-p4charset:

      .. rst-class:: ansible-option-title

      **charset**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-charset" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-aliases:`aliases: p4charset`

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Character set used for translation of unicode files

      Can also use 'P4CHARSET' environment variable


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"none"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldapconfig"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__parameter-ldapconfig:

      .. rst-class:: ansible-option-title

      **ldapconfig**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldapconfig" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The LDAP configuration to use when populating the group’s user list from an LDAP query


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldapsearchquery"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__parameter-ldapsearchquery:

      .. rst-class:: ansible-option-title

      **ldapsearchquery**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldapsearchquery" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The LDAP query used to identify the members of the group


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ldapuserattribute"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__parameter-ldapuserattribute:

      .. rst-class:: ansible-option-title

      **ldapuserattribute**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ldapuserattribute" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The LDAP attribute that represents the user’s username


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-maxlocktime"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__parameter-maxlocktime:

      .. rst-class:: ansible-option-title

      **maxlocktime**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-maxlocktime" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The maximum length of time (in milliseconds) that any one operation can lock any database table when scanning data


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"unset"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-maxopenfiles"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__parameter-maxopenfiles:

      .. rst-class:: ansible-option-title

      **maxopenfiles**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-maxopenfiles" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The maximum number of files that a member of a group can open using a single command


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"unset"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-maxresults"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__parameter-maxresults:

      .. rst-class:: ansible-option-title

      **maxresults**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-maxresults" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The maximum number of results that members of this group can access from the service from a single command


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"unset"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-maxscanrows"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__parameter-maxscanrows:

      .. rst-class:: ansible-option-title

      **maxscanrows**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-maxscanrows" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The maximum number of rows that members of this group can scan from the service from a single command


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"unset"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-name"></div>
        <div class="ansibleOptionAnchor" id="parameter-group"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__parameter-group:
      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__parameter-name:

      .. rst-class:: ansible-option-title

      **name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-name" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-aliases:`aliases: group`

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The name of the group that needs to be managed


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-owners"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__parameter-owners:

      .. rst-class:: ansible-option-title

      **owners**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-owners" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Names of other Helix server users


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-password"></div>
        <div class="ansibleOptionAnchor" id="parameter-p4passwd"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__parameter-p4passwd:
      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__parameter-password:

      .. rst-class:: ansible-option-title

      **password**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-password" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-aliases:`aliases: p4passwd`

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The login password

      Can also use 'P4PASSWD' environment variable


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-passwordtimeout"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__parameter-passwordtimeout:

      .. rst-class:: ansible-option-title

      **passwordtimeout**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-passwordtimeout" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The length of time (in seconds) for which passwords for users in this group remain valid


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"unset"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-server"></div>
        <div class="ansibleOptionAnchor" id="parameter-p4port"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__parameter-p4port:
      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__parameter-server:

      .. rst-class:: ansible-option-title

      **server**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-server" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-aliases:`aliases: p4port`

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The hostname/ip and port of the server (perforce:1666)

      Can also use 'P4PORT' environment variable


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-state"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__parameter-state:

      .. rst-class:: ansible-option-title

      **state**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-state" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Determines if the group is present or deleted


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"present"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"absent"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-subgroups"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__parameter-subgroups:

      .. rst-class:: ansible-option-title

      **subgroups**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-subgroups" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Names of other Helix server groups


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-timeout"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__parameter-timeout:

      .. rst-class:: ansible-option-title

      **timeout**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-timeout" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The duration (in seconds) of the validity of a session ticket created by p4 login


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"43200"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-user"></div>
        <div class="ansibleOptionAnchor" id="parameter-p4user"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__parameter-p4user:
      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__parameter-user:

      .. rst-class:: ansible-option-title

      **user**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-user" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-aliases:`aliases: p4user`

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A user with access to perform this operation

      Can also use 'P4USER' environment variable


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-users"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__parameter-users:

      .. rst-class:: ansible-option-title

      **users**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-users" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The Helix server usernames of the group members


      .. raw:: html

        </div>


.. Attributes


.. Notes


.. Seealso

See Also
--------

.. seealso::

   `Helix Core Group <https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_group.html>`_
       Add or delete users from a group, or set the maxresults, maxscanrows, maxlocktime, and timeout limits for the members of a group
   `P4Python Pip Module <https://pypi.org/project/p4python/>`_
       Python module to interact with Helix Core

.. Examples

Examples
--------

.. code-block:: yaml+jinja

    # Create a group
    - name: Create a new group
      helix_core_group:
        state: present
        name: group1
        users:
            - root
        server: '1666'
        user: bruno
        charset: none
        password: ''

    # Delete a group
    - name: Delete a group
      helix_core_group:
        state: absent
        name: new_user
        server: '1666'
        user: bruno
        charset: none
        password: ''



.. Facts


.. Return values

Return Values
-------------
Common return values are documented :ref:`here <common_return_values>`, the following are the fields unique to this module:

.. tabularcolumns:: \X{1}{3}\X{2}{3}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Key
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-changed"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__return-changed:

      .. rst-class:: ansible-option-title

      **changed**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-changed" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Whether any changes were made to the group.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`true`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-diff"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__return-diff:

      .. rst-class:: ansible-option-title

      **diff**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-diff" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A dictionary containing 'before' and 'after' state of the resource.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` when diff mode is enabled


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-diff/after"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__return-diff/after:

      .. rst-class:: ansible-option-title

      **after**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-diff/after" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The state of the resource after the action.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` success


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-diff/before"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.ripclawffb.helix_core.helix_core_group_module__return-diff/before:

      .. rst-class:: ansible-option-title

      **before**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-diff/before" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The state of the resource before the action.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` success


      .. raw:: html

        </div>




..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Asif Shaikh (@ripclawffb)


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
