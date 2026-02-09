.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.24.0

.. Anchors

.. _ansible_collections.ripclawffb.helix_core.helix_core_server_module:

.. Anchors: short name for ansible.builtin

.. Title

ripclawffb.helix_core.helix_core_server module -- This module will allow you to manage server spec on Perforce Helix Core
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `ripclawffb.helix_core collection <https://galaxy.ansible.com/ui/repo/published/ripclawffb/helix_core/>`_ (version 1.0.7).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible\-galaxy collection install ripclawffb.helix\_core`.
    You need further requirements to be able to use this module,
    see :ref:`Requirements <ansible_collections.ripclawffb.helix_core.helix_core_server_module_requirements>` for details.

    To use it in a playbook, specify: :code:`ripclawffb.helix_core.helix_core_server`.

.. version_added


.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- A server specification describes the high\-level configuration and intended usage of a Helix Server. For installations with only one Helix Server, the server specification is optional.
- This module supports check mode.


.. Aliases


.. Requirements

.. _ansible_collections.ripclawffb.helix_core.helix_core_server_module_requirements:

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
        <div class="ansibleOptionAnchor" id="parameter-address"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_server_module__parameter-address:

      .. rst-class:: ansible-option-title

      **address**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-address" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The P4PORT used by this server


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-allowedaddresses"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_server_module__parameter-allowedaddresses:

      .. rst-class:: ansible-option-title

      **allowedaddresses**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-allowedaddresses" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A list of addresses that are valid this server


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-archivedatafilter"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_server_module__parameter-archivedatafilter:

      .. rst-class:: ansible-option-title

      **archivedatafilter**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-archivedatafilter" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      For a replica server, this optional field can contain one or more patterns describing the policy for automatically scheduling the replication of file content. If this field is present, only those files described by the pattern are automatically transferred to the replica; other files are not transferred until they are referenced by a replica command that needs the file content.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-charset"></div>
        <div class="ansibleOptionAnchor" id="parameter-p4charset"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_server_module__parameter-charset:
      .. _ansible_collections.ripclawffb.helix_core.helix_core_server_module__parameter-p4charset:

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
        <div class="ansibleOptionAnchor" id="parameter-clientdatafilter"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_server_module__parameter-clientdatafilter:

      .. rst-class:: ansible-option-title

      **clientdatafilter**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-clientdatafilter" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      For a replica server, this optional field can contain one or more patterns describing how active client workspace metadata is to be filtered. Active client workspace data includes have lists, working records, and pending resolves.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-description"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_server_module__parameter-description:

      .. rst-class:: ansible-option-title

      **description**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-description" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A textual description of the server


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"Created by user."`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-distributedconfig"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_server_module__parameter-distributedconfig:

      .. rst-class:: ansible-option-title

      **distributedconfig**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-distributedconfig" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      For all server types, this field shows a line for each configurable that is set to a non\-default value. In this field, the admin can edit certain values, add a new line to set certain configurables to a non\-default value, or delete a line to reset certain configurables to their default value.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-externaladdress"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_server_module__parameter-externaladdress:

      .. rst-class:: ansible-option-title

      **externaladdress**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-externaladdress" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      This field contains the external address the commit server requires for connection to the edge server


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-name"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_server_module__parameter-name:

      .. rst-class:: ansible-option-title

      **name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-name" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The P4NAME associated with this server. You can leave this blank or you can set it to the same value as the serverid.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-options"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_server_module__parameter-options:

      .. rst-class:: ansible-option-title

      **options**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-options" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Controls how metadata is replicated to replicas


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"nomandatory"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-password"></div>
        <div class="ansibleOptionAnchor" id="parameter-p4passwd"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_server_module__parameter-p4passwd:
      .. _ansible_collections.ripclawffb.helix_core.helix_core_server_module__parameter-password:

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

      The user password

      Can also use 'P4PASSWD' environment variable


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-replicatingfrom"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_server_module__parameter-replicatingfrom:

      .. rst-class:: ansible-option-title

      **replicatingfrom**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-replicatingfrom" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Server ID of the server from which this server is replicating or journalcopy'ing


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-revisiondatafilter"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_server_module__parameter-revisiondatafilter:

      .. rst-class:: ansible-option-title

      **revisiondatafilter**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-revisiondatafilter" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      For a replica server, this optional field can contain one or more patterns describing how submitted revision metadata is to be filtered. Submitted revision data includes revision records, integration records, label contents, and the files listed in submitted changelists.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-server"></div>
        <div class="ansibleOptionAnchor" id="parameter-p4port"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_server_module__parameter-p4port:
      .. _ansible_collections.ripclawffb.helix_core.helix_core_server_module__parameter-server:

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
        <div class="ansibleOptionAnchor" id="parameter-serverid"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_server_module__parameter-serverid:

      .. rst-class:: ansible-option-title

      **serverid**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-serverid" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A unique identifier for this server


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-services"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_server_module__parameter-services:

      .. rst-class:: ansible-option-title

      **services**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-services" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The server type server provides


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"standard"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-serviceuser"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_server_module__parameter-serviceuser:

      .. rst-class:: ansible-option-title

      **serviceuser**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-serviceuser" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The service user name used by the server (this is the user field in server spec)


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-state"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_server_module__parameter-state:

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

      Determines if the server spec is present or deleted


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"present"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"absent"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-type"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_server_module__parameter-type:

      .. rst-class:: ansible-option-title

      **type**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-type" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Server executable type


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"server"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-updatedcachedrepos"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_server_module__parameter-updatedcachedrepos:

      .. rst-class:: ansible-option-title

      **updatedcachedrepos**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-updatedcachedrepos" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Beginning in 2019.2, this optional field can contain a list of repos to be updated, with each repo name on a separate line


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-user"></div>
        <div class="ansibleOptionAnchor" id="parameter-p4user"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_server_module__parameter-p4user:
      .. _ansible_collections.ripclawffb.helix_core.helix_core_server_module__parameter-user:

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

      A user with access to create clients/workspaces

      Can also use 'P4USER' environment variable


      .. raw:: html

        </div>


.. Attributes


.. Notes


.. Seealso

See Also
--------

.. seealso::

   `Helix Core Server <https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_server.html>`_
       Create, modify, or delete a Helix server specification
   `P4Python Pip Module <https://pypi.org/project/p4python/>`_
       Python module to interact with Helix Core

.. Examples

Examples
--------

.. code-block:: yaml+jinja

    # Create a server spec
    - name: Create a new server spec
      helix_core_server:
        state: present
        serverid: commit
        description: 'Commit server'
        services: standard
        server: '1666'
        user: bruno
        charset: none
        password: ''

    # Create a filtered edge server spec
    - name: Create filtered edge server
      helix_core_server:
        state: present
        serverid: edge_replica
        description: 'Created by root.'
        archivedatafilter:
          - //depot1/...
          - -//depot2/...
        clientdatafilter:
          - -//workstation1/...
        revisiondatafilter:
          - //depot1/...
          - -//depot2/...
        services: edge-server
        server: '1666'
        user: bruno
        charset: auto
        password: ''

    # Delete a server spec
    - name: Delete a server spec
      helix_core_server:
        state: absent
        serverid: commit
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

      .. _ansible_collections.ripclawffb.helix_core.helix_core_server_module__return-changed:

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

      Whether any changes were made to the server spec.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`true`


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
