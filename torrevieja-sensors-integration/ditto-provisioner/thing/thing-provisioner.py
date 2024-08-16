#!/usr/bin/env python3

import os, json, requests
from base64 import b64encode

THING_DESCRIPTION_CONFIG_FILE = os.environ.get('THING_DESCRIPTION_CONFIG_FILE', 'thing-description.json')
DITTO_GATEWAY = os.environ.get('DITTO_GATEWAY', 'http://nginx')
DITTO_USERNAME = os.environ.get('DITTO_USERNAME', 'ditto')
DITTO_PASSWORD = os.environ.get('DITTO_PASSWORD', 'ditto')

THING_NAMESPACE = os.environ.get('THING_NAMESPACE', 'torrevieja')
THING_ENDPOINT = f'{DITTO_GATEWAY}/api/2/things'

def get_thing_from_url(url) -> dict:
    response = requests.get(url, verify=False)
    response.raise_for_status()
    return response.json()

def get_thing_safe_id(location_id) -> str:
    return b64encode(location_id.encode()).decode()

def main():
    with open(THING_DESCRIPTION_CONFIG_FILE) as f:
        config = json.load(f)

    already_provisioned = set()

    for thing_config in config:
        response = get_thing_from_url(thing_config['endpoint'])
        if 'data' not in response:
            raise Exception('No data in response')
        
        for thing in response['data']:

            ditto_request_headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            ditto_request_payload = {
                'definition': thing_config['thingDescription'],
                'attributes': {
                    'location_id': thing['location_id'],
                    'name': thing['name'],
                    'coordinates': {
                        'latitude': thing['lat'],
                        'longitude': thing['lon'],
                        'altitude': thing['alt']
                    }
                }
            }

            thing_id = get_thing_safe_id(thing['location_id'])
            if thing_id in already_provisioned:
                continue
            already_provisioned.add(thing_id)

            print(thing)

            response = requests.put(
                url=f"{THING_ENDPOINT}/{THING_NAMESPACE}:{thing_id}",
                headers=ditto_request_headers,
                auth=(DITTO_USERNAME, DITTO_PASSWORD),
                json=ditto_request_payload
            )
            response.raise_for_status()

if __name__ == '__main__':
    main()
