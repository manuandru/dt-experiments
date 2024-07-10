#!/bin/bash

source hono.env
source variables.env

#### Create a tenant ####

echo "Creating tenant ${TENANT}"

curl -X POST ${CURL_OPTIONS} -H "content-type: application/json" --data-binary '{
  "ext": {
    "messaging-type": "kafka"
  }
}' ${BASE_PATH}/tenants/${TENANT}

echo
echo
##########################



#### Create a device ####

echo "Creating device ${DEVICE} in tenant ${TENANT}"

curl -X POST ${CURL_OPTIONS} ${BASE_PATH}/devices/${TENANT}/${DEVICE}

echo
echo
##########################



#### Set device credentials ####

echo "Set credentials for ${DEVICE} in tenant ${TENANT}"

curl -X PUT ${CURL_OPTIONS} -H "content-type: application/json" --data-binary '[{
  "type": "hashed-password",
  "auth-id": "'${DEVICE}'",
  "secrets": [{
      "pwd-plain": "'${DEVICE_PASSWORD}'"
  }]
}]' ${BASE_PATH}/credentials/${TENANT}/${DEVICE}

echo
echo
##########################
