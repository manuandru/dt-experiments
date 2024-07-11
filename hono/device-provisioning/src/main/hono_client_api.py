from typing import List, Tuple
from venv import logger
import requests, os

base_url = os.getenv("REGISTRY_ENDPOINT") or "https://localhost:28443/v1"

Response = Tuple[int, str]

def add_tenant(tenant_id: str = "", messaging_type: str = "kafka") -> Response:
    """
    Add a tenant to the system
    :param tenant_id: The tenant ID to add.
    """
    url = f"{base_url}/tenants/{tenant_id}"
    response = requests.post(url, verify=False, headers={"Content-Type": "application/json"}, json={
        "ext": {
            "messaging-type": f"{messaging_type}"
        }
    })
    return (response.status_code, response.text)

def add_device(device_id: str, tenant_id: str) -> Response:
    """
    Add a device to the system
    :param device_id: The device ID to add.
    :param tenant_id: The tenant ID to add the device to.
    """
    url = f"{base_url}/devices/{tenant_id}/{device_id}"
    response = requests.post(url, verify=False, headers={"Content-Type": "application/json"})
    return (response.status_code, response.text)

def set_credentials(tenant_id: str, device_id: str, password: str) -> Response:
    """
    Set the credentials for a device
    :param tenant_id: The tenant ID of the device.
    :param device_id: The device ID to set the credentials for. Used both as the device ID and auth ID.
    :param password: The password to set for the device.
    """
    url = f"{base_url}/credentials/{tenant_id}/{device_id}"
    response = requests.put(url, verify=False, headers={"Content-Type": "application/json"}, json=[{
        "type": "hashed-password",
        "auth-id": f"{device_id}",
        "secrets": [{
            "pwd-plain": f"{password}"
        }]
    }])
    return (response.status_code, response.text)

# TODO: Refactor types. E.g List[str] -> List[TenantId]
def get_tenants() -> Tuple[List[str], Response]:
    """
    Get a list of all tenants
    """
    url = f"{base_url}/tenants"
    response = requests.get(url, verify=False, headers={"Content-Type": "application/json"})
    json_response = response.json()
    
    tenants = []
    if "result" in json_response:
        tenants = json_response["result"]
    tenants = [tenant["id"] for tenant in tenants]

    return (tenants, (response.status_code, response.text))

def get_devices() -> Tuple[List[Tuple[str, str]], Response]:
    """
    Get a list of all devices with associated tenant IDs.
    :return: A list of tuples containing (tenant_id, device_id)
    """
    tenants, _ = get_tenants()
    devices = []
    for tenant in tenants:
        url = f"{base_url}/devices/{tenant}"
        response = requests.get(url, verify=False, headers={"Content-Type": "application/json"})
        json_response = response.json()

        if "result" in json_response:
            devices += [(tenant, device["id"]) for device in json_response["result"]]
        
    return (devices, (response.status_code, response.text))
