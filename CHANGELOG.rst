====================================
Ripclawffb.Helix\_Core Release Notes
====================================

.. contents:: Topics

v1.1.0
======

Release Summary
---------------

Added new modules (typemap, triggers, protect, protect_info, ldap) and added diff mode support to all modules.

Minor Changes
-------------

- diff mode - Added diff mode support to all modules (#124)
- helix_core_ldap - Manage LDAP configurations (#114)
- helix_core_protect - Manage Perforce Helix Core protections table (#109)
- helix_core_protect_info - Get protection table info (#111)
- helix_core_trigger - Manage Perforce Helix Core triggers table (#107)
- helix_core_typemap - Manage Perforce Helix Core typemap table (#105)

Bugfixes
--------

- Documentation - Fixed P4Python installation requirements in docs (#133)
- README.md - Fixed documentation links (#100)
- helix_core_protect_info - Fixed documentation issues (#112, #122)

v1.0.7
======

Release Summary
---------------

Added compatibility for Ubuntu 24.04 and fixed P4Python installation issues.

Minor Changes
-------------

- Ubuntu 24.04 support - Added Molecule tests and Dockerfiles for Ubuntu 24.04 with Perforce r23.1, r23.2, r24.1, and r24.2.

Bugfixes
--------

- Documentation generator - Fixed `antsibull-docs` configuration in GitHub Actions to support newer versions and correct path structure.
- P4Python 3.12 support - Updated Molecule configuration to install `perforce-p4python3-python3.12` on Ubuntu 24.04 (Noble Numbat).

v1.0.6
======

Release Summary
---------------

Fix helix_core_client idempotency for 23.1 or newer

Minor Changes
-------------

- helix_core_client - Check for noaltsync option when creating clients on Helix Core 23.1 or newer

v1.0.5
======

Release Summary
---------------

Updated the collection metadata URLs and added docs

Minor Changes
-------------

- docs - Generated HTML documentation for modules
- urls - Update URLs for the collection
