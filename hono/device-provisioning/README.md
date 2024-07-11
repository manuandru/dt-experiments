# Device provisioning

This module allows to provision devices in the Hono system. It provides a command line interface to create, list and manage entities in the Hono system.

## Installation

Install requirements (virtual environment recommended):

```bash
pip install -r requirements.txt
```

## Usage

```bash
python src/main/main.py -h
```

### Environment variables

- `REGISTRY_ENDPOINT`: base URL of the Hono system (default: `https://localhost:28443/v1`)

### Examples

> Note: The `PYTHONWARNINGS` environment variable is used to suppress warnings about unverified HTTPS requests.

```bash
PYTHONWARNINGS="ignore:Unverified HTTPS request" python src/main/main.py ...
```

#### Tenant creation

The following command creates a new tenant, named `my-tenant`, in the Hono system:

```bash
python src/main/main.py add tenant my-tenant
```

#### Device query

The following command query all devices in the Hono system:

```bash
python src/main/main.py list device
```

#### Set device credentials

The following command sets the credentials for a device, named `my-device`in  `my-tenant` tenant, in the Hono system (the script will prompt for the credentials):

```bash
python src/main/main.py set-credentials --tenant-id my-tenant --device-id my-device
```
