# Docker setup for open WebUI

https://docs.openwebui.com/

## Install

Use the task file to install it.

```shell
task clone
task install
```

### Task install

Installs open-webui from this fork of [open-webui](https://github.com/itk-dev/open-webui).

### Storage

Log into minio and create the bucket "openwebui" before uploading files.

## Usage

```shell
task open
```

## OIDC

An (incomplete) OIDC dev setup with a mock server is included. Currently, this fails with

```text
Unhandled exception. System.IO.FileLoadException: Could not load file or assembly 'OpenIdConnectServerMock, Version=0.10.1.0, Culture=neutral, PublicKeyToken=null'.
```

## Configuring connections and models and stuff

The `litellm_config.yaml` file should have the proper api keys. If these were not set from the get-go, you should
restart the container with the new values.

Go to `/admin/settings/connections` and configure the connections, OpenAI API should have the Api Base Url
`http://litellm:4000/v1` and api key `sk-1234` (see `docker.compose.yml`). Then the models will appear in the models
tab: `/admin/settings/models`.

## Patching

This project requires us to make changes requested by the project owner to align with the organization. The upstream
project may not appreciate some of these changes, so we need to be able to keep this project in sync with upstream and
at the same time track local changes/patches to the codebase.

### Branches

* merged/dev (merge of the patching branches)
* merged/main (merge of upstream and local dev branch for next patched release)

All branches will be kept up to date with upstream branches (dev and main). Please use rebase if

### Rules

So the following rules should help with this goal.

1. Prefix all commits with a ticket number, and each feature should have its own ticket, this is to be able to remove a
   single change or isolate a change for easier merge conflict handling.
2. Always first try to make at pull request back
   to [https://github.com/open-webui/open-webui/](https://github.com/open-webui/open-webui/), if the request is
   declined,
   make a new pull request to the patche branch above base on what you changes are.
3. Then update the [change log](https://github.com/itk-dev/open-webui-docker/blob/main/CHANGELOG.md) in this repository,
   so we can track changes between releases.


