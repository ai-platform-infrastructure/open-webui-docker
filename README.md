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
