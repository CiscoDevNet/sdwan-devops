#!/usr/bin/env bash
#This can call python to write all vars to the vault
#Logon to the vault and pass the ssh-token to the build container. The build container will use the API of vault to write the vars to vault.
chmod a+x vault.py
python3 vault.py