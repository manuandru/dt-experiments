#/bin/bash

DITTO_GATEWAY=${DITTO_GATEWAY:-"http://nginx:8080"}
DITTO_ENDPOINT="${DITTO_GATEWAY}/api/2/connections"
DITTO_DEVOPS_USERNAME=${DITTO_DEVOPS_USERNAME:-"devops"}
DITTO_DEVOPS_PASSWORD=${DITTO_DEVOPS_PASSWORD:-"foobar"}
MQTT_BROKER=${MQTT_BROKER:-"tcp://mqtt-broker:1883"}

curl \
    -X POST $DITTO_ENDPOINT \
    -u $DITTO_DEVOPS_USERNAME:$DITTO_DEVOPS_PASSWORD \
    -H 'Content-Type: application/json' \
    -d '{
    "name": "MQTT Connection",
    "connectionType": "mqtt",
    "connectionStatus": "open",
    "failoverEnabled": true,
    "uri": "'$MQTT_BROKER'",
    "sources": [{
        "addresses": ["sensors/#"],
        "authorizationContext": ["nginx:ditto"],
        "qos": 1
    }]
}'
