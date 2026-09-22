---
phase: "02"
plan: "01"
status: complete
completed_at: "2026-09-21"
---

# Plan 02-01 Summary: PipeWire Audio Server Core Config & S6 Longrun Supervision

## What was built:
1. Core PipeWire clock and quantum configuration in `rootfs/etc/pipewire/pipewire.conf.d/10-clock.conf` defining `default.clock.rate = 48000`, `default.clock.quantum = 1024`, `min-quantum = 512`, `max-quantum = 2048`.
2. S6-rc v3 longrun service `10-pipewire` depending on `00-init-environment` and bundled into `user/contents.d/`.
3. S6-rc v3 longrun service `20-wireplumber` depending on `10-pipewire` and bundled into `user/contents.d/`.
4. Automated pytest test suite `tests/test_pipewire_s6.py` verifying the S6 services, dependency chain, and runtime exports.
