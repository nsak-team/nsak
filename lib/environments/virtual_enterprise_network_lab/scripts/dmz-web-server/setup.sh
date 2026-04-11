#!/bin/sh
set -e

SCRIPT_DIR="$(dirname "$0")"

echo "[dmz] starting DNS..."
sh "$SCRIPT_DIR/dns.sh"

echo "[dmz] starting web server..."
sh "$SCRIPT_DIR/web.sh"

echo "[dmz] setup complete"
