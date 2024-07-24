#!/bin/bash

set -e

if [ ! -d "libraries" ]; then
    ./download-libraries.sh
fi

rm -rf libraries/common 
cp -r common libraries/common
