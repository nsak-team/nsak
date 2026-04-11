#!/bin/sh
set -e

SCRIPT_DIR="$(dirname "$0")"

echo "[ctrl-server] starting file server (Samba)..."
sh "$SCRIPT_DIR/server_smb.sh"

echo "[ctrl-server] starting SSH..."
ssh-keygen -A
/usr/sbin/sshd

echo "[ctrl-server] starting domain controller (LDAP)..."
sh "$SCRIPT_DIR/server_ldap.sh"

echo "[ctrl-server] setup complete"
