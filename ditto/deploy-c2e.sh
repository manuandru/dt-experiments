#!/bin/bash

ENV_FILE=c2e.env

helm repo add eclipse-iot https://eclipse.org/packages/charts

NS=cloud2edge
echo "export NS=$NS" > $ENV_FILE
kubectl create namespace $NS
kubectl config set-context --current --namespace $NS

RELEASE=c2e
echo "export RELEASE=$RELEASE" >> $ENV_FILE
helm install -n $NS --wait --timeout 20m --set hono.useLoadBalancer=true \
 --set hono.kafka.externalAccess.broker.service.type=LoadBalancer \
 --set hono.kafka.externalAccess.controller.service.type=LoadBalancer \
 --set ditto.nginx.service.type=LoadBalancer $RELEASE eclipse-iot/cloud2edge

TRUSTSTORE_PATH=/tmp/c2e_hono_truststore.pem
echo "export TRUSTSTORE_PATH=$TRUSTSTORE_PATH" >> $ENV_FILE
openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out $TRUSTSTORE_PATH

curl https://www.eclipse.org/packages/packages/cloud2edge/scripts/setCloud2EdgeEnv.sh --output setCloud2EdgeEnv.sh
chmod u+x setCloud2EdgeEnv.sh

./setCloud2EdgeEnv.sh $RELEASE $NS $TRUSTSTORE_PATH >> $ENV_FILE
