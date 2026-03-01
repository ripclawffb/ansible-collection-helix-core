# Ripclawffb\.Helix\_Core Release Notes

**Topics**

- <a href="#v1-2-0">v1\.2\.0</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#minor-changes">Minor Changes</a>
- <a href="#v1-1-1">v1\.1\.1</a>
    - <a href="#release-summary-1">Release Summary</a>
    - <a href="#minor-changes-1">Minor Changes</a>
    - <a href="#bugfixes">Bugfixes</a>
- <a href="#v1-1-0">v1\.1\.0</a>
    - <a href="#release-summary-2">Release Summary</a>
    - <a href="#minor-changes-2">Minor Changes</a>
    - <a href="#bugfixes-1">Bugfixes</a>
- <a href="#v1-0-7">v1\.0\.7</a>
    - <a href="#release-summary-3">Release Summary</a>
    - <a href="#minor-changes-3">Minor Changes</a>
    - <a href="#bugfixes-2">Bugfixes</a>
- <a href="#v1-0-6">v1\.0\.6</a>
    - <a href="#release-summary-4">Release Summary</a>
    - <a href="#minor-changes-4">Minor Changes</a>
- <a href="#v1-0-5">v1\.0\.5</a>
    - <a href="#release-summary-5">Release Summary</a>
    - <a href="#minor-changes-5">Minor Changes</a>

<a id="v1-2-0"></a>
## v1\.2\.0

<a id="release-summary"></a>
### Release Summary

Added info modules for all resources\, Rocky Linux 8 support\, and Perforce 25\.x compatibility\.

<a id="minor-changes"></a>
### Minor Changes

* Perforce 25\.x support \- Added Molecule tests for Perforce r25\.1 and r25\.2 across all supported platforms\.
* README\.md \- Updated compatibility matrix and included modules table\.
* Rocky Linux 8 support \- Added Molecule tests and Dockerfiles for Rocky Linux 8 with Perforce r23\.1\, r23\.2\, r24\.1\, r24\.2\, r25\.1\, and r25\.2\.
* helix\_core\_client\_info \- New module to fetch client/workspace information\.
* helix\_core\_configurable\_info \- New module to fetch server configurable information\.
* helix\_core\_depot\_info \- New module to fetch depot information\.
* helix\_core\_group\_info \- New module to fetch group information\.
* helix\_core\_ldap\_info \- New module to fetch LDAP configuration information\.
* helix\_core\_server\_info \- New module to fetch server specification information\.
* helix\_core\_stream\_info \- New module to fetch stream information\.
* helix\_core\_trigger\_info \- New module to fetch triggers table information\.
* helix\_core\_typemap\_info \- New module to fetch typemap table information\.
* helix\_core\_user\_info \- New module to fetch user information\.

<a id="v1-1-1"></a>
## v1\.1\.1

<a id="release-summary-1"></a>
### Release Summary

Added position parameter to the protect module and fixed ordering issues\.

<a id="minor-changes-1"></a>
### Minor Changes

* helix\_core\_protect \- Add <code>position</code> parameter to control where new entries are inserted in the protections table \(beginning\, end\, or specific index\) when using <code>mode\=entry</code>\.

<a id="bugfixes"></a>
### Bugfixes

* helix\_core\_protect \- Fixed duplicate playbook entries being inserted multiple times into the protections table\.
* helix\_core\_protect \- Fixed protections table ordering\. The module now preserves entry order instead of using unordered sets\, which previously caused unpredictable entry placement\.

<a id="v1-1-0"></a>
## v1\.1\.0

<a id="release-summary-2"></a>
### Release Summary

Added new modules \(typemap\, triggers\, protect\, protect\_info\, ldap\) and added diff mode support to all modules\.

<a id="minor-changes-2"></a>
### Minor Changes

* diff mode \- Added diff mode support to all modules \(\#124\)
* helix\_core\_ldap \- Manage LDAP configurations \(\#114\)
* helix\_core\_protect \- Manage Perforce Helix Core protections table \(\#109\)
* helix\_core\_protect\_info \- Get protection table info \(\#111\)
* helix\_core\_trigger \- Manage Perforce Helix Core triggers table \(\#107\)
* helix\_core\_typemap \- Manage Perforce Helix Core typemap table \(\#105\)

<a id="bugfixes-1"></a>
### Bugfixes

* Documentation \- Fixed P4Python installation requirements in docs \(\#133\)
* README\.md \- Fixed documentation links \(\#100\)
* helix\_core\_protect\_info \- Fixed documentation issues \(\#112\, \#122\)

<a id="v1-0-7"></a>
## v1\.0\.7

<a id="release-summary-3"></a>
### Release Summary

Added compatibility for Ubuntu 24\.04 and fixed P4Python installation issues\.

<a id="minor-changes-3"></a>
### Minor Changes

* Ubuntu 24\.04 support \- Added Molecule tests and Dockerfiles for Ubuntu 24\.04 with Perforce r23\.1\, r23\.2\, r24\.1\, and r24\.2\.

<a id="bugfixes-2"></a>
### Bugfixes

* Documentation generator \- Fixed <em class="title-reference">antsibull\-docs</em> configuration in GitHub Actions to support newer versions and correct path structure\.
* P4Python 3\.12 support \- Updated Molecule configuration to install <em class="title-reference">perforce\-p4python3\-python3\.12</em> on Ubuntu 24\.04 \(Noble Numbat\)\.

<a id="v1-0-6"></a>
## v1\.0\.6

<a id="release-summary-4"></a>
### Release Summary

Fix helix\_core\_client idempotency for 23\.1 or newer

<a id="minor-changes-4"></a>
### Minor Changes

* helix\_core\_client \- Check for noaltsync option when creating clients on Helix Core 23\.1 or newer

<a id="v1-0-5"></a>
## v1\.0\.5

<a id="release-summary-5"></a>
### Release Summary

Updated the collection metadata URLs and added docs

<a id="minor-changes-5"></a>
### Minor Changes

* docs \- Generated HTML documentation for modules
* urls \- Update URLs for the collection
