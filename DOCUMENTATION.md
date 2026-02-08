# Documentation

Documentation is generated using antsibull-docs and Sphinx by reading the contents of the documentation section in the Ansible modules.

## Initial Setup

This section tells you how to generate the sphinx config files for a new Ansible collection project that contains modules. This has already been done, so you can skip this section. The requirements required for antsibull-docs is already contained in the Pipfile.

The collection must be installed in the proper collection path available to Ansible.

Example: `~/.ansible/collections/ansible_collections/ripclawffb/helix_core`

To initialize the sphinx config files and build scripts by running the command below. This only needs to be done once.

```shell
antsibull-docs sphinx-init --use-current --dest-dir . ripclawffb.helix_core
```
Then run `./build.sh` to generate the documentation

## Updating Documentation

If you add or update the Helix Core modules, you'll need to run  `./build.sh` from the root of this project. This will update the html files in the `builds` folder.

Review the changes by opening the `builds/html/index.html` file and navigating through the various links.

If changes look good, copy the contents of the `builds/html` into the `docs` folder. Commit and push the changes up to Github.


## Generating Changelog

When releasing a new version of this collection, add the changes to the `changelogs/changelog.yml`. Docs can be found [here](https://github.com/ansible-community/antsibull-changelog/tree/main/docs).

Once the `changelog.yml` has been updated, run the following commands in the `pipenv` environment:

```
antsibull-changelog lint
antsibull-changelog generate
```

Commit and push changes up to Github.
