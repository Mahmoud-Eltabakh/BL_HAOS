# Requirements

**Project:** BL-HAOS (Bluetooth Audio Adapter for Home Assistant OS)
**Defined:** 2026-09-22

## Native Media Player Bridge Requirements

### Native Integration (NMP)

- [x] **NMP-01**: Bundle and install a Home Assistant custom integration without overwriting user-managed Home Assistant configuration.
- [x] **NMP-02**: Register exactly one configurable BL-HAOS integration entry after Home Assistant loads the bundled component.
- [x] **NMP-03**: Create a native `media_player` entity for each trusted Bluetooth audio sink with a stable unique ID and speaker device record.
- [x] **NMP-04**: Use the add-on REST API plus WebSocket events as the primary entity control and state transport; no MQTT broker is required for the core entity path.
- [ ] **NMP-05**: Map play, pause, stop, play-media, and volume commands to the add-on and reflect acknowledgements and connection availability in Home Assistant.
- [ ] **NMP-06**: Resolve Home Assistant media-source and TTS URLs so the add-on can play them on the selected Bluetooth speaker.
- [ ] **NMP-07**: Recreate entities and state correctly after Home Assistant or add-on restart, speaker disconnect, and auto-reconnect.

### Migration & Validation (MIG)

- [ ] **MIG-01**: Deprecate MQTT `media_player` discovery while retaining MQTT only as an optional interoperability transport.
- [ ] **MIG-02**: Surface native-integration installation and connection status in the Ingress UI and add-on diagnostics.
- [ ] **MIG-03**: Verify the Logitech Bluetooth adapter appears as a native media player and can receive a real Home Assistant media command on the live Raspberry Pi.

## Out of Scope

- **HFP/HSP Microphone Input for Voice Satellite**: V1 strictly targets high-quality A2DP stereo playback sinks; two-way microphone communication degrades codec quality to 8kHz/16kHz mono and is excluded.
- **Custom Hardware Firmware Flashing**: BL-HAOS runs on standard HAOS Linux Bluetooth adapters without requiring custom hardware modifications.

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| NMP-01 | Phase 9 | Complete |
| NMP-02 | Phase 9 | Complete |
| NMP-03 | Phase 9 | Complete |
| NMP-04 | Phase 9 | Complete |
| NMP-05 | Phase 10 | Planned |
| NMP-06 | Phase 10 | Planned |
| NMP-07 | Phase 10 | Planned |
| MIG-01 | Phase 11 | Planned |
| MIG-02 | Phase 11 | Planned |
| MIG-03 | Phase 11 | Planned |

---
*Requirements defined: 2026-09-22*
