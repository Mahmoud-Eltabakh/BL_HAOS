#!/bin/bash
set -e

USB_DIR="$(dirname "$0")/../config_usb"
mkdir -p "$USB_DIR"

if [ ! -f "$USB_DIR/haos_test_rsa" ]; then
    echo "Generating SSH keypair..."
    ssh-keygen -t rsa -b 4096 -f "$USB_DIR/haos_test_rsa" -q -N ""
fi

echo "Creating FAT32 CONFIG image..."
# Create a 10MB blank image
dd if=/dev/zero of="$USB_DIR/config.img" bs=1M count=10
# Format it as FAT32
mkfs.vfat -n "CONFIG" "$USB_DIR/config.img"

echo "Copying authorized_keys..."
# We use mcopy from mtools to copy the public key to the FAT32 image without needing root/sudo to mount
mcopy -i "$USB_DIR/config.img" "$USB_DIR/haos_test_rsa.pub" ::/authorized_keys

echo "SSH configuration USB drive generated at $USB_DIR/config.img"
