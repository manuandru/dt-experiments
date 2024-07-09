#!/bin/bash

helm repo add eclipse-iot https://eclipse.org/packages/charts

NS=cloud2edge
kubectl create namespace $NS

RELEASE=c2e
helm install -n $NS --wait --timeout 20m --set hono.useLoadBalancer=true \
 --set hono.kafka.externalAccess.broker.service.type=LoadBalancer \
 --set hono.kafka.externalAccess.controller.service.type=LoadBalancer \
 --set ditto.nginx.service.type=LoadBalancer $RELEASE eclipse-iot/cloud2edge
