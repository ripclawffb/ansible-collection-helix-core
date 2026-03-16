.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.24.0

.. Anchors

.. _ansible_collections.ripclawffb.helix_core.helix_core_remote_module:

.. Anchors: short name for ansible.builtin

.. Title

ripclawffb.helix_core.helix_core_remote module -- Manage remote specs on Perforce Helix Core
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `ripclawffb.helix_core collection <https://galaxy.ansible.com/ui/repo/published/ripclawffb/helix_core/>`_ (version 1.3.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible\-galaxy collection install ripclawffb.helix\_core`.
    You need further requirements to be able to use this module,
    see :ref:`Requirements <ansible_collections.ripclawffb.helix_core.helix_core_remote_module_requirements>` for details.

    To use it in a playbook, specify: :code:`ripclawffb.helix_core.helix_core_remote`.

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

- A remote specification describes the shared server that your server cooperates with.
- Uses the :literal:`p4 remote` command to create, modify, or delete a remote specification.
- This module supports check mode.


.. Aliases


.. Requirements

.. _ansible_collections.ripclawffb.helix_core.helix_core_remote_module_requirements:

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

      .. _ansible_collections.ripclawffb.helix_core.helix_core_remote_module__parameter-address:

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

      The P4PORT for the shared server.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-archivelimits"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_remote_module__parameter-archivelimits:

      .. rst-class:: ansible-option-title

      **archivelimits**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-archivelimits" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      One or more entries specifying how many revisions of file archives to store locally when the files are fetched.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-charset"></div>
        <div class="ansibleOptionAnchor" id="parameter-p4charset"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_remote_module__parameter-charset:
      .. _ansible_collections.ripclawffb.helix_core.helix_core_remote_module__parameter-p4charset:

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
        <div class="ansibleOptionAnchor" id="parameter-depotmap"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_remote_module__parameter-depotmap:

      .. rst-class:: ansible-option-title

      **depotmap**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-depotmap" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A list of one or more lines describing the mapping from the shared server's files to your personal server's files.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-description"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_remote_module__parameter-description:

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

      A description of the remote spec.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"Created by user."`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-options"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_remote_module__parameter-options:

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

      Flags to change the remote spec behavior.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"unlocked nocompress copyrcs"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-owner"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_remote_module__parameter-owner:

      .. rst-class:: ansible-option-title

      **owner**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-owner" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The name of the user who owns the remote spec. By default, this is the user who creates it.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-password"></div>
        <div class="ansibleOptionAnchor" id="parameter-p4passwd"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_remote_module__parameter-p4passwd:
      .. _ansible_collections.ripclawffb.helix_core.helix_core_remote_module__parameter-password:

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
        <div class="ansibleOptionAnchor" id="parameter-remoteid"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_remote_module__parameter-remoteid:

      .. rst-class:: ansible-option-title

      **remoteid**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-remoteid" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The name of the remote spec to manage.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-remoteuser"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_remote_module__parameter-remoteuser:

      .. rst-class:: ansible-option-title

      **remoteuser**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-remoteuser" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Specifies the identity (user) P4 Server uses to authenticate against this remote server when pushing and fetching.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-server"></div>
        <div class="ansibleOptionAnchor" id="parameter-p4port"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_remote_module__parameter-p4port:
      .. _ansible_collections.ripclawffb.helix_core.helix_core_remote_module__parameter-server:

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

      .. _ansible_collections.ripclawffb.helix_core.helix_core_remote_module__parameter-state:

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

      Determines if the remote spec is present or deleted.


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

      .. _ansible_collections.ripclawffb.helix_core.helix_core_remote_module__parameter-p4user:
      .. _ansible_collections.ripclawffb.helix_core.helix_core_remote_module__parameter-user:

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


.. Attributes


.. Notes


.. Seealso

See Also
--------

.. seealso::

   `Helix Core Remote <https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_remote.html>`_
       Create or edit a remote spec
   `P4Python Pip Module <https://pypi.org/project/p4python/>`_
       Python module to interact with Helix Core

.. Examples

Examples
--------

.. code-block:: yaml+jinja

    # Create a new remote spec
    - name: Create remote spec
      ripclawffb.helix_core.helix_core_remote:
        state: present
        remoteid: central-repo
        description: "Central repository shared server"
        address: "ssl:central-perforce:1666"
        depotmap:
          - "//depot/... //depot/..."
        server: '1666'
        user: bruno
        charset: auto
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
        <div class="ansibleOptionAnchor" id="return-action"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_remote_module__return-action:

      .. rst-class:: ansible-option-title

      **action**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-action" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The action performed.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always

      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Can only return:`

      - :ansible-option-choices-entry:`"created"`
      - :ansible-option-choices-entry:`"updated"`
      - :ansible-option-choices-entry:`"deleted"`
      - :ansible-option-choices-entry:`"unchanged"`


      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"created"`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-changed"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_remote_module__return-changed:

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

      Whether any changes were made to the remote spec.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`true`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-changes"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_remote_module__return-changes:

      .. rst-class:: ansible-option-title

      **changes**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-changes" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      List of fields that were changed.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`[{"after": "New description", "before": "Old description", "field": "Description"}]`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-diff"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_remote_module__return-diff:

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

      .. _ansible_collections.ripclawffb.helix_core.helix_core_remote_module__return-diff/after:

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

      .. _ansible_collections.ripclawffb.helix_core.helix_core_remote_module__return-diff/before:

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



  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-remote_spec"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_remote_module__return-remote_spec:

      .. rst-class:: ansible-option-title

      **remote_spec**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-remote_spec" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The remote specification after the operation.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`{"Address": "ssl:central\-perforce:1666", "Description": "Central repository shared server", "RemoteID": "central\-repo"}`


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
