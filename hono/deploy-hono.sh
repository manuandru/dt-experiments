#!/bin/bash

helm repo add eclipse-iot https://eclipse.org/packages/charts

kubectl create namespace hono
kubectl config set-context --current --namespace=hono
helm install eclipse-hono eclipse-iot/hono -n hono --wait

kubectl wait --for=condition=Ready pods --all -n hono

./create-hono-env.sh playground/hono.env
