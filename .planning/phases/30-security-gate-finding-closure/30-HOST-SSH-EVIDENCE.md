# Phase 30 Host-Side (SSH) Evidence

**Date:** 2026-10-28  **Host:** 192.168.1.18 (HAOS, Core 2026.10.4)  **Authorization:** user ("no limits", SSH)
**Deployed:** add-on `c839f4a9_bl_haos` 0.2.70, integration 0.2.21. Read-only checks only; no tokens recorded.

## Results

| Check | Result |
|---|---|
| `/api/native/{identity,speakers,settings}` without token | 401 (pass) |
| `/api/native/speakers`, `POST /api/native/scan/start` with invalid bearer | 401 (pass) |
| Bearer/native_token/Authorization values in add-on, Core, Supervisor logs | 0 matches in each (pass) |
| Core log `bl_haos` errors after redeploy | 0 |
| Add-on log error lines | 6, all PipeWire RTKit `ServiceUnknown` noise; not auth related |
| Add-on port 8099 from LAN (host IP, workstation) | unreachable (not host-published; `host_network: false`); reachable only on the internal Supervisor network |

## Finding (new, medium)

Legacy UI routes are **unauthenticated** on the internal network: `GET /api/devices` and `GET /api/settings` return 200 without a token (`/api/health` is intentionally open). They are not LAN-exposed but any add-on on the Supervisor network can read them. Phase 38 (retire ingress UI and UI-only routes) closes this once deployed; until then, the exposure stands. Verify after deploying Phase 38 that both return 401/404.

## Still open (needs a human or live provider)

- T-24-15: real provider-session leakage observation and attested-fixture rejection. SSH log-leakage grep is clean but not sufficient.
- T-24-16: three HA-shell screenshots, audible playback, accessibility acceptance, production-provider evidence.
- Phase 39 go/no-go.

Neither finding is closed.

## Post-Phase-38 re-check (add-on 0.2.71, integration 0.2.22 deployed)

- Legacy /api/devices, /api/settings, /api/adapters now 404 (finding closed); ingress: false; /api/native/speakers still 401 without token; /api/health 200.
- Core log bl_haos errors: 0. GHCR pull needed three attempts (IPv6 connection resets) but succeeded.
