import argparse
import getpass
import hono_client_api

def add_tenant(args):
    _, response = hono_client_api.add_tenant(args.tenant_id)
    print(response)

def add_device(args):
    _, response = hono_client_api.add_device(args.device_id, args.tenant_id)
    print(response)

def set_credentials(args):
    password = getpass.getpass("Enter device password: ")
    code, response = hono_client_api.set_credentials(args.tenant_id, args.device_id, password)
    print(f"{code} {response}")

def list_tenants(args):
    tenants, _ = hono_client_api.get_tenants()
    print("Tenants ID:")
    for tenant in tenants:
        print(tenant)

def list_devices(args):
    devices, _ = hono_client_api.get_devices()
    print("TenantID:DeviceID")
    for device in devices:
        print(device[0], ":", device[1], sep="")

def main():
    parser = argparse.ArgumentParser(description="Command line parser for hono device management")
    subparsers = parser.add_subparsers(help="Commands")

    # add
    parser_add_tenant = subparsers.add_parser('add', help='Add operations')
    subparsers_add = parser_add_tenant.add_subparsers(help="Add an entity to the system")

    # add tenant
    parser_add_tenant_cmd = subparsers_add.add_parser('tenant', help='Add a new tenant')
    parser_add_tenant_cmd.add_argument('tenant_id', type=str, help='Tenant ID')
    parser_add_tenant_cmd.set_defaults(func=add_tenant)

    # add device
    parser_add_device_cmd = subparsers_add.add_parser('device', help='Add a new device')
    parser_add_device_cmd.add_argument('device_id', type=str, help='Device ID')
    parser_add_device_cmd.add_argument('--tenant-id', dest='tenant_id', type=str, required=True, help='Tenant ID')
    parser_add_device_cmd.set_defaults(func=add_device)

    # set-credentials
    parser_set_credentials = subparsers.add_parser('set-credentials', help='Set credentials for a device')
    parser_set_credentials.add_argument('--tenant-id', type=str, required=True, help='Tenant ID')
    parser_set_credentials.add_argument('--device-id', type=str, required=True, help='Device ID')
    parser_set_credentials.set_defaults(func=set_credentials)

    # list
    parser_list_tenants = subparsers.add_parser('list', help='List operations')
    subparsers_list = parser_list_tenants.add_subparsers(help="List commands")

    # list tenant
    parser_list_tenant = subparsers_list.add_parser('tenant', help='List all tenants')
    parser_list_tenant.set_defaults(func=list_tenants)

    # list device
    parser_list_device = subparsers_list.add_parser('device', help='List all devices')
    parser_list_device.set_defaults(func=list_devices)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
