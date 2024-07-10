#!/bin/bash

HONO_ENV_FILE=$1

REGISTRY_IP=$(kubectl get service eclipse-hono-service-device-registry-ext --output="jsonpath={.status.loadBalancer.ingress[0]['hostname','ip']}" -n hono)
echo "export REGISTRY_IP=${REGISTRY_IP}" > ${HONO_ENV_FILE}

HTTP_ADAPTER_IP=$(kubectl get service eclipse-hono-adapter-http --output="jsonpath={.status.loadBalancer.ingress[0]['hostname','ip']}" -n hono)
echo "export HTTP_ADAPTER_IP=${HTTP_ADAPTER_IP}" >> ${HONO_ENV_FILE}

MQTT_ADAPTER_IP=$(kubectl get service eclipse-hono-adapter-mqtt --output="jsonpath={.status.loadBalancer.ingress[0]['hostname','ip']}" -n hono)
echo "export MQTT_ADAPTER_IP=${MQTT_ADAPTER_IP}" >> ${HONO_ENV_FILE}

TRUSTSTORE_PATH=/tmp/truststore.pem
echo "export TRUSTSTORE_PATH=${TRUSTSTORE_PATH}" >> ${HONO_ENV_FILE}
kubectl get configmaps eclipse-hono-example-trust-store --template="{{index .data \"ca.crt\"}}" -n hono > ${TRUSTSTORE_PATH}

KAFKA_IP=$(kubectl get service eclipse-hono-kafka-controller-0-external --output="jsonpath={.status.loadBalancer.ingress[0]['hostname','ip']}" -n hono)
echo "export KAFKA_IP=${KAFKA_IP}" >> ${HONO_ENV_FILE}
echo "export APP_OPTIONS='-H ${KAFKA_IP} -P 9094 -u hono -p hono-secret --ca-file ${TRUSTSTORE_PATH} --disable-hostname-verification'" >> ${HONO_ENV_FILE}

echo "export CURL_OPTIONS='--insecure'" >> ${HONO_ENV_FILE}
echo "export MOSQUITTO_OPTIONS='--cafile ${TRUSTSTORE_PATH} --insecure'" >> ${HONO_ENV_FILE}
