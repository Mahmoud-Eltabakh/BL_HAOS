---
phase: "02"
plan: "02"
status: complete
completed_at: "2026-09-21"
---

# Plan 02-02 Summary: WirePlumber Bluetooth Codec Ranking, Low-Latency Tuning & AVRCP Volume Sync

## What was built:
1. WirePlumber SPA Bluetooth policy configuration in `rootfs/etc/wireplumber/wireplumber.conf.d/50-bluez.conf` configuring:
   - Audiophile codec ranking: `ldac`, `aptx_hd`, `aptx`, `aac`, `sbc_xq`, `sbc`
   - `bluez5.enable-sbc-xq = true`
   - Bidirectional AVRCP hardware volume sync: `bluez5.enable-volume-sync = true`, `bluez5.enable-hw-volume = true`
   - Auto-connection rules for `a2dp_sink` nodes
2. Automated pytest test suite `tests/test_pipewire_config.py` verifying clock parameters, codec ranking order, and volume sync rules.
