# Docker setup for open WebUI

https://docs.openwebui.com/

## Install

Use the taks file to install it.

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

An (incomplete) OIDC dev setup with mock server is included. Currently this fails with
```text
Unhandled exception. System.IO.FileLoadException: Could not load file or assembly 'OpenIdConnectServerMock, Version=0.10.1.0, Culture=neutral, PublicKeyToken=null'.
```

## Configuring connections and models and stuff

The `litellm_config.yaml` file should have the proper api keys. If these were not set from the get go, you should restart the container with the new values.

Go to `/admin/settings/connections` and configure the connections, OpenAI API should have the Api Base Url `http://litellm:4000/v1` and api key `sk-1234` (see `docker.compose.yml`). Then the models will appear in the models tab: `/admin/settings/models`.
