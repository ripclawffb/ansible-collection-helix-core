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

.. _ansible_collections.ripclawffb.helix_core.helix_core_user_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

ripclawffb.helix_core.helix_core_user module -- This module will allow you to manage users on Perforce Helix Core
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `ripclawffb.helix_core collection <https://galaxy.ansible.com/ripclawffb/helix_core>`_ (version 1.0.4).

    You might already have this collection installed if you are using the ``ansible`` package.
    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install ripclawffb.helix_core`.

    To use it in a playbook, specify: :code:`ripclawffb.helix_core.helix_core_user`.

.. version_added


.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Create or edit Helix server user specifications and preferences
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
        <div class="ansibleOptionAnchor" id="parameter-authmethod"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_user_module__parameter-authmethod:

      .. rst-class:: ansible-option-title

      **authmethod**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-authmethod" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      One of the following, perforce or ldap


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-default-bold:`perforce` :ansible-option-default:`← (default)`
      - :ansible-option-choices-entry:`ldap`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-charset"></div>
        <div class="ansibleOptionAnchor" id="parameter-p4charset"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_user_module__parameter-charset:
      .. _ansible_collections.ripclawffb.helix_core.helix_core_user_module__parameter-p4charset:

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
        <div class="ansibleOptionAnchor" id="parameter-email"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_user_module__parameter-email:

      .. rst-class:: ansible-option-title

      **email**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-email" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The user’s email address


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"user@hostname"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-fullname"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_user_module__parameter-fullname:

      .. rst-class:: ansible-option-title

      **fullname**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-fullname" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The user’s full name


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"name"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-name"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_user_module__parameter-name:

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

      The name of the user that needs to be managed


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-password"></div>
        <div class="ansibleOptionAnchor" id="parameter-p4passwd"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_user_module__parameter-password:
      .. _ansible_collections.ripclawffb.helix_core.helix_core_user_module__parameter-p4passwd:

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
        <div class="ansibleOptionAnchor" id="parameter-server"></div>
        <div class="ansibleOptionAnchor" id="parameter-p4port"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_user_module__parameter-server:
      .. _ansible_collections.ripclawffb.helix_core.helix_core_user_module__parameter-p4port:

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

      .. _ansible_collections.ripclawffb.helix_core.helix_core_user_module__parameter-state:

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

      Determines if the user is present or deleted


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-default-bold:`present` :ansible-option-default:`← (default)`
      - :ansible-option-choices-entry:`absent`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-user"></div>
        <div class="ansibleOptionAnchor" id="parameter-p4user"></div>

      .. _ansible_collections.ripclawffb.helix_core.helix_core_user_module__parameter-user:
      .. _ansible_collections.ripclawffb.helix_core.helix_core_user_module__parameter-p4user:

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

      A user with access to create users

      Can also use 'P4USER' environment variable


      .. raw:: html

        </div>


.. Attributes


.. Notes


.. Seealso

See Also
--------

.. seealso::

   `Helix Core User <https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_user.html>`_
       Create, edit, or delete Helix server user specifications and preferences
   `P4Python Pip Module <https://pypi.org/project/p4python/>`_
       Python module to interact with Helix Core

.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
    # Create a user
    - name: Create a new user
      helix_core_user:
        state: present
        name: new_user
        email: new_user@perforce.com
        server: '1666'
        user: bruno
        charset: none
        password: ''
    # Delete a user
    - name: Delete a user
      helix_core_user:
        state: absent
        name: new_user
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

