---
phase: 20-release-quality-gates-go-live
reviewed: 2026-09-24T00:00:00Z
depth: standard
files_reviewed: 3
files_reviewed_list:
  - modules/integration/custom_components/bl_haos/client.py
  - modules/integration/custom_components/bl_haos/media_player.py
  - modules/integration/tests/test_ha_integration_sil.py
findings:
  critical: 0
  warning: 3
  info: 0
  total: 3
status: issues_found
---

# Phase 20: Code Review Report

**Reviewed:** 2026-09-24T00:00:00Z  
**Depth:** standard  
**Files Reviewed:** 3  
**Status:** issues_found

## Summary

The scoped Home Assistant client, media-player entity, and SIL tests were reviewed against the bridge native REST/WebSocket contract and the checked-in speaker fixtures. No critical security vulnerability or immediate data-loss defect was found in the supported HTTP config-flow path. Three robustness and contract warnings remain, and command-path coverage is incomplete because the SIL fake session rejects every POST request.

## Warnings

### WR-01: WebSocket transport does not preserve a secure endpoint scheme

**File:** `modules/integration/custom_components/bl_haos/client.py:126-128`

**Issue:** `_async_listen()` always constructs the native WebSocket URL with the `ws` scheme, even when `self.endpoint` is `https`. A client created from an HTTPS config entry or an imported/migrated entry will therefore fail to connect securely, and a proxy or deployment that accepts both schemes could expose the bearer token over plaintext WebSocket transport. The current config flow normalizes user input to HTTP, but the client itself does not enforce or preserve that contract.

**Fix:** Derive `wss` for an `https` endpoint and `ws` for `http`, or reject unsupported endpoint schemes before starting the client. Add a focused test asserting both conversions and ensuring the Authorization header is sent only over the matching secure transport.

### WR-02: Malformed native WebSocket messages terminate the listener task

**File:** `modules/integration/custom_components/bl_haos/client.py:137-141`

**Issue:** `message.json()` can produce a non-dict JSON value such as a list. The following `payload.get(...)` then raises `AttributeError`, which is not caught by `_async_listen()`; the background task exits permanently instead of reconnecting. The same failure mode exists for a malformed top-level snapshot in `_async_refresh_snapshot()` when `payload.get("speakers")` is evaluated. This can leave cached entities with stale state and prevent future availability updates after a malformed or incompatible bridge response.

**Fix:** Validate decoded payload types before accessing mapping methods, ignore or log malformed event frames, and include the relevant protocol/type errors in the reconnect boundary. Add tests for a list/scalar WebSocket frame and an invalid snapshot response, asserting the listener remains alive or retries and transport state is updated truthfully.

### WR-03: Snapshot reconciliation counts rejected speakers as present

**File:** `modules/integration/custom_components/bl_haos/client.py:64-70`

**Issue:** `_async_refresh_snapshot()` adds every valid-address record to `snapshot_addresses` before `_async_process_speaker()` applies the `is_audio_sink` and trusted/paired/connected filters. If a speaker already cached as an audio sink is later returned with a valid address but `is_audio_sink` false or no valid-sink status, it is rejected for replacement but still considered present, so the old cached record and entity are retained. The bridge currently filters its normal `/native/speakers` response, but this client-side reconciliation still fails closed against malformed, version-skewed, or future bridge payloads.

**Fix:** Build the accepted snapshot from the same predicate used to process records, then evict cached addresses absent from that accepted set; alternatively make `_async_process_speaker()` return whether it accepted the record and use that result for reconciliation. Add a regression fixture where a cached speaker becomes a non-audio or untrusted record and assert it is evicted.

## Validation Gaps

- `python -m pytest modules/integration/tests/test_ha_integration_sil.py -q` could not collect in the current environment: `pytest_homeassistant_custom_component.common` is unavailable. The suite therefore provides no executable pass/fail evidence here.
- `FakeSession.post()` in the adjacent integration test fixture always raises `AssertionError`, so the scoped SIL tests do not exercise the client command payloads or response handling for play, pause, stop, volume, or media playback.
- Existing tests cover snapshot creation, normal eviction, unload, diagnostics, and a WebSocket connection failure, but not secure WebSocket URL derivation, malformed frames/snapshots, rejected-record eviction, or native command request/response contracts.
- Bridge-side tests cover native URL validation and WebSocket authentication, but they do not substitute for the integration-side command and reconnection tests above.

---

_Reviewed: 2026-09-24T00:00:00Z_  
_Reviewer: the agent (gsd-code-reviewer)  
_Depth: standard_
