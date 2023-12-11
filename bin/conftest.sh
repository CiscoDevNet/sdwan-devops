#!/usr/bin/env bash

CONFTEST_VERSION=${CONFTEST_VERSION:-v0.47.0}

docker run --rm -v $PROJ_ROOT/config:/project openpolicyagent/conftest:${CONFTEST_VERSION} test config.yaml -d policy/data.yaml
