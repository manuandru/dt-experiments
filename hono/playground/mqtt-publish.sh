#!/bin/bash

source hono.env
source variables.env

mosquitto_pub -h ${MQTT_ADAPTER_IP} -p 8883 -u ${DEVICE}@${TENANT} -P ${DEVICE_PASSWORD} ${MOSQUITTO_OPTIONS} -t telemetry -m '{"temp-from-mqtt": 5}'
