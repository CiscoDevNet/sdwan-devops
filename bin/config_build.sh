#!/usr/bin/env bash

CONFTEST_VERSION=${CONFTEST_VERSION:-v0.48.0}

set -o pipefail

# Uncomment the line below if you want to enforce the OPA rules in `config/policy/config.rego` that check the AWS instance types for given SD-WAN versions.
# See config/policy/README for further explanation.
#set -e

echo "[i] Running conftest on config.yaml ..."
docker run --rm -v $PROJ_ROOT/config:/project openpolicyagent/conftest:${CONFTEST_VERSION} test config.yaml -d policy/data.yaml
echo ""

echo "[i] Rendering config.yaml to Ansible configuration ..."
echo ""
./play.sh -c render -u
