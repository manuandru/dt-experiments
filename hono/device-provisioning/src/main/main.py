import argparse, getpass, os
import hono_client_api
import yaml

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

def load_config_from_yaml(args):
    print(f"Loading configuration from {args.from_yaml}")
    if args.from_yaml is None or not os.path.exists(args.from_yaml):
        print("File does not exist")
        return
    with open(args.from_yaml, 'r') as file:
        config = yaml.load(file, Loader=yaml.CLoader)
        if 'tenants' not in config:
            print("Missing tenants in configuration")
            return
        for tenant in config['tenants']:
            if 'tenant-id' not in tenant:
                print("Missing tenant_id in tenant configuration")
                continue
            tenant_id = tenant['tenant-id']
            _, response = hono_client_api.add_tenant(tenant_id)
            print(tenant_id, response, sep=": ")
            if 'devices' not in tenant:
                print("No devices in tenant")
                continue
            for device in tenant['devices']:
                if 'device-id' not in device:
                    print("Missing device_id in device configuration")
                    continue
                device_id = device['device-id']
                _, response = hono_client_api.add_device(device_id, tenant_id)
                print(f"\t{device_id}", response, sep=": ")
                if 'password' in device:
                    password = device['password']
                    _, response = hono_client_api.set_credentials(tenant_id, device_id, password)
                    print(f"\tCredentials set for {device_id}: {response}")

def delete_config_from_yaml(args):
    print(f"Delete configuration from {args.from_yaml}")
    if args.from_yaml is None or not os.path.exists(args.from_yaml):
        print("File does not exist")
        return
    with open(args.from_yaml, 'r') as file:
        config = yaml.load(file, Loader=yaml.CLoader)
        if 'tenants' not in config:
            print("Missing tenants in configuration")
            return
        for tenant in config['tenants']:
            if 'tenant-id' not in tenant:
                print("Missing tenant_id in tenant configuration")
                continue
            tenant_id = tenant['tenant-id']
            if 'devices' in tenant:
                for device in tenant['devices']:
                    if 'device-id' not in device:
                        print("Missing device_id in device configuration")
                        continue
                    device_id = device['device-id']
                    _, response = hono_client_api.delete_device(device_id, tenant_id)
                    print(f"\tDeleted device {device_id}: {response}")

            _, response = hono_client_api.delete_tenant(tenant_id)
            print(f"Deleted tenant {tenant_id} {response}")

def main():
    parser = argparse.ArgumentParser(description="Command line parser for hono device management")
    subparsers = parser.add_subparsers(help="Commands")

    # add
    parser_add = subparsers.add_parser('add', help='Add operations')
    subparsers_add = parser_add.add_subparsers(help="Add an entity to the system")

    # add --from-yaml
    parser_add.add_argument('--from-yaml', type=str, help='YAML file to load configuration from')
    parser_add.set_defaults(func=load_config_from_yaml)

    # add tenant
    parser_add_tenant_cmd = subparsers_add.add_parser('tenant', help='Add a new tenant')
    parser_add_tenant_cmd.add_argument('tenant_id', type=str, help='Tenant ID')
    parser_add_tenant_cmd.set_defaults(func=add_tenant)

    # add device
    parser_add_device_cmd = subparsers_add.add_parser('device', help='Add a new device')
    parser_add_device_cmd.add_argument('device_id', type=str, help='Device ID')
    parser_add_device_cmd.add_argument('--tenant-id', dest='tenant_id', type=str, required=True, help='Tenant ID')
    parser_add_device_cmd.set_defaults(func=add_device)

    # delete
    parser_delete = subparsers.add_parser('delete', help='Delete operations')

    # delete --from-yaml
    parser_delete.add_argument('--from-yaml', type=str, help='YAML file to load configuration from')
    parser_delete.set_defaults(func=delete_config_from_yaml)

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
