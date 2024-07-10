#!/bin/bash

source hono.env
source variables.env

#### Delete tenant ####

echo "Deleting tenant ${TENANT}"

curl -X DELETE ${CURL_OPTIONS} ${BASE_PATH}/tenants/${TENANT}

echo
##########################



#### Delete device ####

echo "Deleting device ${DEVICE} in tenant ${TENANT}"

curl -X DELETE ${CURL_OPTIONS} ${BASE_PATH}/devices/${TENANT}/${DEVICE}

echo
##########################