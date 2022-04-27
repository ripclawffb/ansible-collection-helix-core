.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. role:: ansible-attribute-support-label
.. role:: ansible-attribute-support-property
.. role:: ansible-attribute-support-full
.. role:: ansible-attribute-support-partial
.. role:: ansible-attribute-support-none
.. role:: ansible-attribute-support-na
.. role:: ansible-option-type
.. role:: ansible-option-elements
.. role:: ansible-option-required
.. role:: ansible-option-versionadded
.. role:: ansible-option-aliases
.. role:: ansible-option-choices
.. role:: ansible-option-choices-entry
.. role:: ansible-option-default
.. role:: ansible-option-default-bold
.. role:: ansible-option-configuration
.. role:: ansible-option-returned-bold
.. role:: ansible-option-sample-bold

.. Anchors

.. _ansible_collections.ripclawffb.helix_core.helix_core_client_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

ripclawffb.helix_core.helix_core_client module -- This module will allow you to manage client/workspace on Perforce Helix Core
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `ripclawffb.helix_core collection <https://galaxy.ansible.com/ripclawffb/helix_core>`_ (version 1.0.4).

    You might already have this collection installed if you are using the ``ansible`` package.
    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install ripclawffb.helix_core`.

    To use it in a playbook, specify: :code:`ripclawffb.helix_core.helix_core_client`.

.. version_added


.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- A client/workspace specification defines the portion of the depot that can be accessed from that workspace and specifies where local copies of files in the depot are stored.
- This module supports check mode.


.. Aliases


.. Requirements

Requirements
------------
The below requirements are needed on the host that executes this module.

- P4Python pip module is required. Tested with 2018.2.1743033


.. Options

Parameters
----------

.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Comments

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-altroots"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_client_module__parameter-altroots:

      .. rst-class:: ansible-option-title

      **altroots**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-altroots" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Up to two optional alternate client workspace roots


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"None"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-charset"></div>
        <div class="ansibleOptionAnchor" id="parameter-p4charset"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_client_module__parameter-charset:
      .. _ansible_collections.ripclawffb.helix_core.helix_core_client_module__parameter-p4charset:

      .. rst-class:: ansible-option-title

      **charset**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-charset" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-aliases:`aliases: p4charset`

      .. rst-class:: ansible-option-type-line

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
        <div class="ansibleOptionAnchor" id="parameter-description"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_client_module__parameter-description:

      .. rst-class:: ansible-option-title

      **description**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-description" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A textual description of the workspace


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"Created by user."`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-host"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_client_module__parameter-host:

      .. rst-class:: ansible-option-title

      **host**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-host" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The name of the workstation on which this workspace resides


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"hostname"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-lineend"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_client_module__parameter-lineend:

      .. rst-class:: ansible-option-title

      **lineend**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-lineend" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Configure carriage-return/linefeed (CR/LF) conversion


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-default-bold:`local` :ansible-option-default:`← (default)`
      - :ansible-option-choices-entry:`unix`
      - :ansible-option-choices-entry:`mac`
      - :ansible-option-choices-entry:`win`
      - :ansible-option-choices-entry:`share`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-name"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_client_module__parameter-name:

      .. rst-class:: ansible-option-title

      **name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-name" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The name of the client that needs to be managed


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-options"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_client_module__parameter-options:

      .. rst-class:: ansible-option-title

      **options**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-options" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A set of switches that control particular workspace options


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"noallwrite noclobber nocompress unlocked nomodtime normdir"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-password"></div>
        <div class="ansibleOptionAnchor" id="parameter-p4passwd"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_client_module__parameter-password:
      .. _ansible_collections.ripclawffb.helix_core.helix_core_client_module__parameter-p4passwd:

      .. rst-class:: ansible-option-title

      **password**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-password" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-aliases:`aliases: p4passwd`

      .. rst-class:: ansible-option-type-line

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
        <div class="ansibleOptionAnchor" id="parameter-root"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_client_module__parameter-root:

      .. rst-class:: ansible-option-title

      **root**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-root" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The directory (on the local host) relative to which all the files in the View are specified


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-server"></div>
        <div class="ansibleOptionAnchor" id="parameter-p4port"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_client_module__parameter-server:
      .. _ansible_collections.ripclawffb.helix_core.helix_core_client_module__parameter-p4port:

      .. rst-class:: ansible-option-title

      **server**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-server" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-aliases:`aliases: p4port`

      .. rst-class:: ansible-option-type-line

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

      .. _ansible_collections.ripclawffb.helix_core.helix_core_client_module__parameter-state:

      .. rst-class:: ansible-option-title

      **state**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-state" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Determines if the client is present or deleted


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-default-bold:`present` :ansible-option-default:`← (default)`
      - :ansible-option-choices-entry:`absent`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-submitoptions"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_client_module__parameter-submitoptions:

      .. rst-class:: ansible-option-title

      **submitoptions**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-submitoptions" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Options to govern the default behavior of p4 submit


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"submitunchanged"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-user"></div>
        <div class="ansibleOptionAnchor" id="parameter-p4user"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_client_module__parameter-user:
      .. _ansible_collections.ripclawffb.helix_core.helix_core_client_module__parameter-p4user:

      .. rst-class:: ansible-option-title

      **user**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-user" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-aliases:`aliases: p4user`

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A user with access to create clients/workspaces

      Can also use 'P4USER' environment variable


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-view"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_client_module__parameter-view:

      .. rst-class:: ansible-option-title

      **view**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-view" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Specifies the mappings between files in the depot and files in the workspace


      .. raw:: html

        </div>


.. Attributes


.. Notes


.. Seealso

See Also
--------

.. seealso::

   `Helix Core Client <https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_client.html>`_
       Create or edit a client workspace specification and its view
   `P4Python Pip Module <https://pypi.org/project/p4python/>`_
       Python module to interact with Helix Core

.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
    # Create a client
    - name: Create a new client
      helix_core_client:
        state: present
        name: bruno_new_client
        description: 'New client for Bruno'
        host: workstation01
        root: /tmp/bruno_new_client
        view:
          - //depot/... //bruno_new_client/depot/...
        server: '1666'
        user: bruno
        charset: none
        password: ''
    # Delete a client
    - name: Delete a client
      helix_core_client:
        state: absent
        name: bruno_new_client
        server: '1666'
        user: bruno
        charset: none
        password: ''




.. Facts


.. Return values


..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Asif Shaikh (@ripclawffb)



.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. raw:: html

  <p class="ansible-links">
    <a href="https://github.com/ripclawffb/ansible-collection-helix-core" aria-role="button" target="_blank" rel="noopener external">Issue Tracker</a>
    <a href="https://github.com/ripclawffb/ansible-collection-helix-core" aria-role="button" target="_blank" rel="noopener external">Repository (Sources)</a>
  </p>

.. Parsing errors

