#!/usr/bin/env bash

set -o pipefail

if [ -z ${PROJ_ROOT+x} ]; then echo "PROJ_ROOT is unset, please source the env script"; exit 1; else echo "PROJ_ROOT is set to '$PROJ_ROOT'"; fi

rm -rf $PROJ_ROOT/myCA
./play.sh "/ansible/day_-1/build-ca.yml"
