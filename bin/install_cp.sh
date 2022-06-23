#!/usr/bin/env bash

set -o pipefail

./play.sh /ansible/day_0/build-control-plane.yml
./play.sh /ansible/day_0/config-sdwan.yml
./play.sh /ansible/day_1/config-sdwan.yml
