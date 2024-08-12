#!/bin/bash

set -e

THING_DIRECTORY=${THING_DIRECTORY:-http://thing-directory}
echo "Thing Directory docker name: $THING_DIRECTORY"

rm -rf thing-directory/root
cp -r thing-directory/root-template thing-directory/root

if ! command -v envsubst &> /dev/null; then
    echo "envsubst is not installed. Please install it using your package manager."
    exit 1
fi

for file in $(ls thing-directory/root/*.jsonld); do
    THING_DIRECTORY=$THING_DIRECTORY envsubst < $file > $file.tmp
    mv $file.tmp $file
done