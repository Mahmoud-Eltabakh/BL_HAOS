# Pitfalls Research

**Domain:** Home Assistant OS Bluetooth Audio Adapter & Multi-Room Add-on
**Researched:** 2026-09-21
**Confidence:** HIGH

## Critical Pitfalls

### Pitfall 1: Docker Container D-Bus Isolation & Permission Blocking

**What goes wrong:**
The add-on container fails to discover or interact with Bluetooth adapters, throwing `DBusException: AccessDenied` or failing to see adapter interfaces.

**Why it happens:**
Home Assistant OS runs BlueZ on the host system. Add-on containers need explicit access to the system D-Bus socket (`/var/run/dbus/system_bus_socket`), `host_dbus: true`, and privileged hardware capabilities in `config.yaml` (`full_access: true`, `udev: true`, `devices: ["/dev/bus/usb"]`).

**How to avoid:**
Properly declare all required permissions in the Home Assistant add-on `config.yaml` and verify D-Bus communication during container bootstrap before launching PipeWire or the daemon.

**Warning signs:**
`bluetoothctl` or Python D-Bus fails to list any adapters under `org.bluez`.

**Phase to address:**
Phase 1 (Core Add-on Scaffolding & Container Permissions).

---

### Pitfall 2: BlueZ / PipeWire Audio Profile Locking & Audio Glitches

**What goes wrong:**
Bluetooth audio connects initially, but after a few seconds drops or suffers severe buffer underruns, popping, or silence.

**Why it happens:**
Multiple audio services (e.g., leftover PulseAudio, PipeWire SPA Bluetooth, or direct ALSA handles) competing for the same BlueZ Media endpoint (`org.bluez.MediaEndpoint1`).

**How to avoid:**
Run only PipeWire with its native SPA Bluetooth module; ensure no conflicting audio daemons attempt to register endpoints on BlueZ. Tune PipeWire buffer quantum (`default.clock.quantum = 1024` or `2048` for Bluetooth A2DP) to prevent buffer underruns over 2.4GHz RF.

**Warning signs:**
Logs show `spa.bluez5: connection error` or `Endpoint unregistered`.

**Phase to address:**
Phase 2 (PipeWire Audio Stack & Codec Tuning).

---

### Pitfall 3: Reconnection Storms & Deadlocks on Speaker Power-Down

**What goes wrong:**
When a speaker is powered off or goes to sleep, reconnect attempts flood the BlueZ D-Bus daemon, causing the Bluetooth adapter to hang or crash host Bluetooth services.

**Why it happens:**
Tight reconnection loops without exponential backoff or failing to detect that the adapter is already busy in a connection handshake.

**How to avoid:**
Implement an exponential backoff state machine with jitter, circuit breaker limits, and explicit lock acquisition per adapter before invoking `org.bluez.Device1.Connect`.

**Warning signs:**
HCI timeout errors (`HCI Request timed out`), adapter resetting unexpectedly (`hci0: Resetting...`).

**Phase to address:**
Phase 3 (Bluetooth Manager & Auto-Reconnect Engine).

---

### Pitfall 4: Home Assistant Ingress CSP / WebSocket Proxy Issues

**What goes wrong:**
The web UI dashboard loads blank or WebSocket disconnects immediately when opened via Home Assistant Ingress.

**Why it happens:**
HA Ingress proxies web apps under a dynamically generated path prefix (e.g. `/api/hassio_ingress/{token}/`). Hardcoded root paths (`/api`, `/ws`, `/static/bundle.js`) break routing.

**How to avoid:**
Use relative base paths in Vite (`base: './'`) and derive WebSocket URLs dynamically from `window.location`.

**Warning signs:**
404 errors for JavaScript/CSS assets or WebSocket handshake errors in browser console.

**Phase to address:**
Phase 4 (Ingress Web UI & REST/WS APIs).

---

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Parsing raw `bluetoothctl` CLI stdout string output | Fast initial prototype | Highly fragile across BlueZ versions and internationalized systems | Never — use structured D-Bus async calls (`dbus-fast`) |
| Hardcoding single adapter `hci0` | Simpler codebase | Breaks immediately on systems with multiple dongles or disabled onboard BT | Never — enumerate adapters dynamically |
| Static sleep timers (`time.sleep(2)`) during pairing handshakes | Easy synchronization | Blocks event loop, causes dropped D-Bus signals and UI freezes | Never — use async event listeners for property changes |

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Home Assistant MQTT Discovery | Publishing retained state messages that persist after speaker is deleted | Clean up retained MQTT discovery topics upon speaker unpairing |
| PipeWire WirePlumber | Manually killing and restarting WirePlumber on every disconnect | Let WirePlumber automatically track dynamic SPA Bluetooth node additions/removals |
| Snapcast Server | Opening high-rate raw PCM pipes without flow control | Use named pipes with proper buffer sizing and format descriptors (48000:16:2) |

---
*Pitfalls research for: Home Assistant OS Bluetooth Audio Adapter*
*Researched: 2026-09-21*
