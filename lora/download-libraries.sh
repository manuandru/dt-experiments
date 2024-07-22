#!/bin/bash

set -e

git clone https://github.com/Xinyuan-LilyGO/LilyGo-LoRa-Series.git /tmp/LilyGo-LoRa-Series || true
cd /tmp/LilyGo-LoRa-Series
git checkout 99a724dc1a3cc9580fe8408b69ebe4286ea9380d
cd -

cp -r /tmp/LilyGo-LoRa-Series/lib libraries
