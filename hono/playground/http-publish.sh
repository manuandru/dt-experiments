#!/bin/bash

source hono.env
source variables.env

curl -i -u ${DEVICE}@${TENANT}:${DEVICE_PASSWORD} ${CURL_OPTIONS} -H 'Content-Type: application/json' --data-binary '{"temp": 5}' https://${HTTP_ADAPTER_IP}:8443/telemetry
