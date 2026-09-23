#!/bin/bash
set -e

HAOS_HOST=${HAOS_HOST:-"localhost"}
HAOS_PORT=${HAOS_SSH_PORT:-22222}
SSH_KEY=${SSH_KEY:-"$(dirname "$0")/../config_usb/haos_test_rsa"}
ADDON_DIR="$(dirname "$0")/../../../modules/bridge"

echo "Waiting for HAOS SSH to become available at $HAOS_HOST:$HAOS_PORT..."
until ssh -o StrictHostKeyChecking=no -i "$SSH_KEY" -p "$HAOS_PORT" root@"$HAOS_HOST" "echo 'SSH Ready'"; do
    sleep 5
done

echo "Copying BL-HAOS add-on to HAOS host..."
ssh -o StrictHostKeyChecking=no -i "$SSH_KEY" -p "$HAOS_PORT" root@"$HAOS_HOST" "mkdir -p /mnt/data/supervisor/addons/local/bl_haos"
scp -o StrictHostKeyChecking=no -i "$SSH_KEY" -P "$HAOS_PORT" -r $ADDON_DIR/* root@"$HAOS_HOST":/mnt/data/supervisor/addons/local/bl_haos/

echo "Installing add-on via Supervisor CLI..."
ssh -o StrictHostKeyChecking=no -i "$SSH_KEY" -p "$HAOS_PORT" root@"$HAOS_HOST" "ha addons reload"
ssh -o StrictHostKeyChecking=no -i "$SSH_KEY" -p "$HAOS_PORT" root@"$HAOS_HOST" "ha addons install local_bl_haos"
ssh -o StrictHostKeyChecking=no -i "$SSH_KEY" -p "$HAOS_PORT" root@"$HAOS_HOST" "ha addons start local_bl_haos"

echo "Add-on deployed successfully."
