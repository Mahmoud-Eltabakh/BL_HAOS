# Phase 3: BlueZ D-Bus Bluetooth Controller - Research

**Phase:** 3 (BlueZ D-Bus Bluetooth Controller)
**Researched:** 2026-09-21
**Confidence:** HIGH

## Overview

Phase 3 builds the core Python Bluetooth management library (`bl_haos.bluetooth`).
Using `dbus-fast`, it interfaces with the BlueZ daemon running on the host system via `/var/run/dbus/system_bus_socket`.

## Key Architectural Patterns

1. **BlueZ ObjectManager Pattern**:
   - Call `GetManagedObjects` on `org.bluez` at `/` to discover all existing adapters and cached devices.
   - Attach listener to `org.freedesktop.DBus.ObjectManager.InterfacesAdded` to react in real-time when new adapters are plugged in or new devices are discovered during discovery scan.
   - Attach listener to `org.freedesktop.DBus.ObjectManager.InterfacesRemoved` to handle device unpairing or adapter removal.

2. **PropertiesChanged Signal Pattern**:
   - Listen to `org.freedesktop.DBus.Properties.PropertiesChanged` on device paths to capture live RSSI signal strength variations, connection state changes (`Connected = true/false`), and pairing states.

3. **D-Bus Pairing Agent (`org.bluez.Agent1`)**:
   - Register an agent on object path `/org/bl_haos/agent` with methods:
     - `RequestPinCode(device)`: Prompts or returns default/configured PIN.
     - `DisplayPinCode(device, pincode)`: Logs/emits PIN for display in UI.
     - `RequestPasskey(device)`: Returns passkey.
     - `DisplayPasskey(device, passkey, entered)`: Emits passkey update.
     - `RequestConfirmation(device, passkey)`: Confirms numeric comparison.
     - `RequestAuthorization(device)`: Authorizes connection.
     - `AuthorizeService(device, uuid)`: Authorizes A2DP / AVRCP profile connections.
     - `Cancel()`: Cancels pairing request.

4. **Audio Sink Filter**:
   - Major device class `0x0400` (Audio/Video).
   - Minor device classes: `0x0414` (Loudspeaker), `0x0418` (Headphones), `0x0404` (Wearable Headset), `0x041C` (HiFi Audio Device).
   - Service UUIDs: `0000110b-0000-1000-8000-00805f9b34fb` (A2DP Audio Sink).

---
*Research for Phase 3: BlueZ D-Bus Bluetooth Controller*
