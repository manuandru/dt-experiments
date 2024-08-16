#!/bin/bash

set -e

# Replace namespace for thing-provisioner deployment in connection/javascript-mapper.js
THING_NAMESPACE=${THING_NAMESPACE:-"torrevieja"}
file=${1:-connection/javascript-mapper.js}
THING_NAMESPACE=$THING_NAMESPACE envsubst < $file.template > $file

# Replace all endpoint for thing-directory deployment in thing/thing-description.json
THING_DIRECTORY=${THING_DIRECTORY:-http://thing-directory}
file=${2:-thing/thing-description.json}
THING_DIRECTORY=$THING_DIRECTORY envsubst < $file.template > $file
