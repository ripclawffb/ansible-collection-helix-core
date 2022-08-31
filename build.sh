#!/usr/bin/env bash
set -e
cd /root/github/ripclawffb/ansible_collections/ripclawffb/helix_core

# Create collection documentation into temporary directory
rm -rf temp-rst
mkdir -p temp-rst
antsibull-docs collection \
    --use-current \
    --no-use-html-blobs \
    --breadcrumbs \
    --indexes \
    --dest-dir temp-rst \
    ripclawffb.helix_core

# Copy collection documentation into source directory
rsync -cprv --delete-after temp-rst/collections/ rst/collections/

# Build Sphinx site
sphinx-build -M html rst build -c . -W --keep-going

