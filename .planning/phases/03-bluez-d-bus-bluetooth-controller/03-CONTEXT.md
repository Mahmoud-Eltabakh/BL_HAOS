# Phase 3: BlueZ D-Bus Bluetooth Controller - Context

**Gathered:** 2026-09-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 3 delivers the asynchronous Python Bluetooth subsystem controller using `dbus-fast`:
- Asynchronous connection to BlueZ `org.bluez` over system D-Bus.
- AdapterManager discovering and monitoring all available host Bluetooth controllers (`hci0`, `hci1`, etc.) with independent state management (Power, Discoverable, Pairable, Alias).
- DiscoveryScanner managing discovery sessions per adapter with live RSSI signal telemetry, device filtering (A2DP audio sinks/sources via UUID `0000110b-...` / `0000110a-...` and Class of Device audio bits), and manufacturer data parsing.
- PairingAgent implementing BlueZ `org.bluez.Agent1` D-Bus interface for PIN entry, Passkey display, and SSP (Secure Simple Pairing) numeric confirmation.
- DeviceController managing device lifecycle: pairing, trusting, connecting A2DP audio profiles, disconnecting, and removing devices.
- Mockable architecture and comprehensive test suite for continuous integration in non-hardware environments.

</domain>

<decisions>
## Implementation Decisions

### D-Bus Library & Async Architecture
- **D-01:** Standardize on pure-async `dbus-fast` with `asyncio`. Connect to `BusType.SYSTEM` using `MessageBus(bus_type=BusType.SYSTEM)`. BlueZ events will be tracked via `org.freedesktop.DBus.ObjectManager.InterfacesAdded` and `PropertiesChanged` signal callbacks. — **Reversibility:** costly — core transport for all Bluetooth interactions.

### Bluetooth Audio Device Filtering
- **D-02:** Filter scanned devices to prioritize Audio sinks (speakers/headphones) by checking:
  1. Service UUIDs: `0000110b-0000-1000-8000-00805f9b34fb` (Audio Sink / A2DP Sink), `0000110c-...` (AVRCP Target), `0000110e-...` (AVRCP).
  2. Bluetooth Class of Device (CoD): Major Device Class = Audio/Video (`0x040000` / bitmask `0x1F00 == 0x0400`).
  Allow toggling "Show all devices" in UI/API for edge-case speakers. — **Reversibility:** reversible.

### Pairing Agent Implementation
- **D-03:** Implement a dedicated D-Bus Agent (`/org/bl_haos/agent`) registered via `org.bluez.AgentManager1.RegisterAgent` with capability `DisplayYesNo` or `KeyboardDisplay`. Support dynamic PIN callbacks and auto-confirmation for trusted devices. — **Reversibility:** reversible.

### Multi-Adapter Management
- **D-04:** Each adapter (`/org/bluez/hci0`, `/org/bluez/hci1`) is represented by a first-class `BluetoothAdapter` object, allowing simultaneous or independent discovery scans and device connections. — **Reversibility:** reversible.

### Module Structure
- **D-05:** Structure Python package under `backend/bl_haos/bluetooth/`:
  - `manager.py`: `BluetoothManager` orchestrating adapters and agents.
  - `adapter.py`: `BluetoothAdapter` managing power, scanning, and HCI properties.
  - `device.py`: `BluetoothDevice` representing remote speakers with connection/pairing methods.
  - `agent.py`: `BlueZAgent` implementing `org.bluez.Agent1`.
  - `models.py`: Pydantic dataclasses for Adapter, Device, RSSI, and Pairing state.
  - `constants.py`: BlueZ interface names, UUIDs, and D-Bus paths. — **Reversibility:** reversible.

</decisions>

<canonical_refs>
## Canonical References

### BlueZ D-Bus API Specifications
- `https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/adapter-api.txt` — `org.bluez.Adapter1`
- `https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/device-api.txt` — `org.bluez.Device1`
- `https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/agent-api.txt` — `org.bluez.Agent1` and `org.bluez.AgentManager1`

### Python & D-Bus Libraries
- `dbus-fast` (https://github.com/Bluetooth-Devices/dbus-fast) — High performance async D-Bus library for Python.

### Project Context
- `.planning/PROJECT.md` — BL-HAOS core architecture.
- `.planning/REQUIREMENTS.md` — Requirements `BT-01`, `BT-02`, `BT-03`, `BT-04`.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `rootfs/usr/bin/bl-haos-probe` contains preliminary D-Bus socket checks.
- `Dockerfile` installs `python3-dbus-fast`, `bluez`, `bluez-tools`.

### Integration Points
- Backend services in Phase 4 (Auto-Reconnect) and Phase 5 (FastAPI / Ingress UI) will consume `BluetoothManager`.
</code_context>
