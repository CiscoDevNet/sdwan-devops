#!/usr/bin/env bash

set -o pipefail

if [[ -n "$VPN_GW" && -n "$VPN_USER" && -n "$VPN_PASS" ]]; then
    echo "$VPN_PASS" | sudo openconnect --background --passwd-on-stdin --user=$VPN_USER $VPN_GW
    if [ -n "$VPN_HOST" ]; then
        ping -c 3 $VPN_HOST
    fi
else
    echo "OpenConnect VPN configuration required! Set VPN_GW, VPN_USER, VPN_PASS and VPN_HOST environment variables"
    exit 1
fi
