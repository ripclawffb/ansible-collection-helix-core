.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.24.0

.. Anchors

.. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module:

.. Anchors: short name for ansible.builtin

.. Title

ripclawffb.helix_core.helix_core_ldap module -- Manage LDAP configurations on Perforce Helix Core
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `ripclawffb.helix_core collection <https://galaxy.ansible.com/ui/repo/published/ripclawffb/helix_core/>`_ (version 1.0.7).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible\-galaxy collection install ripclawffb.helix\_core`.
    You need further requirements to be able to use this module,
    see :ref:`Requirements <ansible_collections.ripclawffb.helix_core.helix_core_ldap_module_requirements>` for details.

    To use it in a playbook, specify: :code:`ripclawffb.helix_core.helix_core_ldap`.

.. version_added


.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- This module allows you to create, modify, or delete LDAP configurations on Perforce Helix Core.
- Supports various bind methods (simple, search, sasl) and encryption types.


.. Aliases


.. Requirements

.. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module_requirements:

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
        <div class="ansibleOptionAnchor" id="parameter-attribute_email"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__parameter-attribute_email:

      .. rst-class:: ansible-option-title

      **attribute_email**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-attribute_email" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The attribute used for the user's email address.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-attribute_name"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__parameter-attribute_name:

      .. rst-class:: ansible-option-title

      **attribute_name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-attribute_name" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The attribute used for the user's full name.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-attribute_uid"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__parameter-attribute_uid:

      .. rst-class:: ansible-option-title

      **attribute_uid**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-attribute_uid" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The attribute used for the user ID.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-bind_method"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__parameter-bind_method:

      .. rst-class:: ansible-option-title

      **bind_method**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-bind_method" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The method used to bind to the LDAP server.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"simple"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"search"`
      - :ansible-option-choices-entry:`"sasl"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-charset"></div>
        <div class="ansibleOptionAnchor" id="parameter-p4charset"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__parameter-charset:
      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__parameter-p4charset:

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
        <div class="ansibleOptionAnchor" id="parameter-encryption"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__parameter-encryption:

      .. rst-class:: ansible-option-title

      **encryption**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-encryption" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The encryption method used to connect to the LDAP server.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"none"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"ssl"`
      - :ansible-option-choices-entry:`"tls"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-group_base_dn"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__parameter-group_base_dn:

      .. rst-class:: ansible-option-title

      **group_base_dn**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-group_base_dn" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The base DN for searching groups.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-group_search_filter"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__parameter-group_search_filter:

      .. rst-class:: ansible-option-title

      **group_search_filter**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-group_search_filter" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The filter used to search for groups.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-host"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__parameter-host:

      .. rst-class:: ansible-option-title

      **host**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-host" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The LDAP server hostname or IP address.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-name"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__parameter-name:

      .. rst-class:: ansible-option-title

      **name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-name" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The name of the LDAP configuration.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-options"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__parameter-options:

      .. rst-class:: ansible-option-title

      **options**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-options" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      specific options for the LDAP configuration.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"downcase"`
      - :ansible-option-choices-entry:`"nodowncase"`
      - :ansible-option-choices-entry:`"getattrs"`
      - :ansible-option-choices-entry:`"nogetattrs"`
      - :ansible-option-choices-entry:`"realminusername"`
      - :ansible-option-choices-entry:`"norealminusername"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-password"></div>
        <div class="ansibleOptionAnchor" id="parameter-p4passwd"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__parameter-p4passwd:
      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__parameter-password:

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

      The super user password

      Can also use 'P4PASSWD' environment variable


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-port"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__parameter-port:

      .. rst-class:: ansible-option-title

      **port**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-port" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The LDAP server port.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-search_base_dn"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__parameter-search_base_dn:

      .. rst-class:: ansible-option-title

      **search_base_dn**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-search_base_dn" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The base DN for searching users.

      Required if bind\_method is 'search'.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-search_bind_dn"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__parameter-search_bind_dn:

      .. rst-class:: ansible-option-title

      **search_bind_dn**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-search_bind_dn" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The DN used to bind to the LDAP server for searching.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-search_filter"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__parameter-search_filter:

      .. rst-class:: ansible-option-title

      **search_filter**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-search_filter" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The search filter used to find users (e.g., (uid=%user%)).

      Required if bind\_method is 'search'.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-search_passwd"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__parameter-search_passwd:

      .. rst-class:: ansible-option-title

      **search_passwd**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-search_passwd" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The password used to bind to the LDAP server for searching.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-server"></div>
        <div class="ansibleOptionAnchor" id="parameter-p4port"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__parameter-p4port:
      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__parameter-server:

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
        <div class="ansibleOptionAnchor" id="parameter-simple_pattern"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__parameter-simple_pattern:

      .. rst-class:: ansible-option-title

      **simple_pattern**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-simple_pattern" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The pattern used for simple binding (e.g., uid=%user%,ou=users,dc=example,dc=com).

      Required if bind\_method is 'simple'.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-state"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__parameter-state:

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

      Whether the LDAP configuration should exist or not.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"present"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"absent"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-user"></div>
        <div class="ansibleOptionAnchor" id="parameter-p4user"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__parameter-p4user:
      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__parameter-user:

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

      A user with super user access

      Can also use 'P4USER' environment variable


      .. raw:: html

        </div>


.. Attributes


.. Notes


.. Seealso

See Also
--------

.. seealso::

   `Helix Core LDAP <https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_ldap.html>`_
       Manage LDAP configurations
   `P4Python Pip Module <https://pypi.org/project/p4python/>`_
       Python module to interact with Helix Core

.. Examples

Examples
--------

.. code-block:: yaml+jinja

    - name: Create LDAP configuration with simple bind
      ripclawffb.helix_core.helix_core_ldap:
        name: simple_ldap
        host: ldap.example.com
        port: 389
        encryption: none
        bind_method: simple
        simple_pattern: "uid=%user%,ou=users,dc=example,dc=com"
        options:
          - nodowncase
          - getattrs
        server: '1666'
        user: bruno
        password: ''

    - name: Create LDAP configuration with search bind
      ripclawffb.helix_core.helix_core_ldap:
        name: search_ldap
        host: ldap.example.com
        port: 636
        encryption: ssl
        bind_method: search
        search_base_dn: "ou=users,dc=example,dc=com"
        search_filter: "(uid=%user%)"
        search_bind_dn: "cn=admin,dc=example,dc=com"
        search_passwd: "secret_password"
        options:
          - downcase
          - getattrs
        server: '1666'
        user: bruno
        password: ''

    - name: Remove LDAP configuration
      ripclawffb.helix_core.helix_core_ldap:
        name: simple_ldap
        state: absent
        host: ldap.example.com
        port: 389
        server: '1666'
        user: bruno
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

      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__return-changed:

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

      Whether any changes were made to the LDAP configuration.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`true`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-ldap_spec"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_ldap_module__return-ldap_spec:

      .. rst-class:: ansible-option-title

      **ldap_spec**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-ldap_spec" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The LDAP configuration specification.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`{"BindMethod": "simple", "Encryption": "none", "Host": "ldap.example.com", "Name": "simple\_ldap", "Port": 389}`


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
