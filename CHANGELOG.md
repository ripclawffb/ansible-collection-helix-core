# Ripclawffb\.Helix\_Core Release Notes

**Topics**

- <a href="#v1-0-7">v1\.0\.7</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#minor-changes">Minor Changes</a>
    - <a href="#bugfixes">Bugfixes</a>
- <a href="#v1-0-6">v1\.0\.6</a>
    - <a href="#release-summary-1">Release Summary</a>
    - <a href="#minor-changes-1">Minor Changes</a>
- <a href="#v1-0-5">v1\.0\.5</a>
    - <a href="#release-summary-2">Release Summary</a>
    - <a href="#minor-changes-2">Minor Changes</a>

<a id="v1-0-7"></a>
## v1\.0\.7

<a id="release-summary"></a>
### Release Summary

Added compatibility for Ubuntu 24\.04 and fixed P4Python installation issues\.

<a id="minor-changes"></a>
### Minor Changes

* Ubuntu 24\.04 support \- Added Molecule tests and Dockerfiles for Ubuntu 24\.04 with Perforce r23\.1\, r23\.2\, r24\.1\, and r24\.2\.

<a id="bugfixes"></a>
### Bugfixes

* Documentation generator \- Fixed <em class="title-reference">antsibull\-docs</em> configuration in GitHub Actions to support newer versions and correct path structure\.
* P4Python 3\.12 support \- Updated Molecule configuration to install <em class="title-reference">perforce\-p4python3\-python3\.12</em> on Ubuntu 24\.04 \(Noble Numbat\)\.

<a id="v1-0-6"></a>
## v1\.0\.6

<a id="release-summary-1"></a>
### Release Summary

Fix helix\_core\_client idempotency for 23\.1 or newer

<a id="minor-changes-1"></a>
### Minor Changes

* helix\_core\_client \- Check for noaltsync option when creating clients on Helix Core 23\.1 or newer

<a id="v1-0-5"></a>
## v1\.0\.5

<a id="release-summary-2"></a>
### Release Summary

Updated the collection metadata URLs and added docs

<a id="minor-changes-2"></a>
### Minor Changes

* docs \- Generated HTML documentation for modules
* urls \- Update URLs for the collection
