---
phase: 11-migration-live-verification
reviewed: 2026-09-23T00:00:00Z
depth: standard
files_reviewed: 2
files_reviewed_list:
  - modules/bridge/backend/bl_haos/api/routes.py
  - modules/integration/custom_components/bl_haos/client.py
findings:
  critical: 1
  warning: 1
  info: 0
  total: 2
status: issues_found
---

# Phase 11: Code Review Report

**Reviewed:** 2026-09-23T00:00:00Z  
**Depth:** standard  
**Files Reviewed:** 2 source files; root submodule pointer changes inspected separately  
**Status:** issues_found

## Summary

The native bridge and integration changes were reviewed against the Phase 11 migration requirements, nearby tests, startup/network configuration, and the bridge execution path. The focused test suites pass, but the native control plane is not authenticated despite being described as authenticated, and the integration cache never removes speakers that disappear from an authoritative snapshot. Root changes are gitlink updates only; no additional root-level implementation was present to review.

## Critical Issues

### CR-01: Native control endpoints have no authentication

**File:** `modules/bridge/backend/bl_haos/api/routes.py:121-149`

**Issue:** The command endpoint accepts play, stop, volume, and arbitrary HTTP(S) media playback without validating a token, session, or caller identity. The native client also sends an empty header set, and `/ws/native` accepts connections without authentication. The daemon binds to `0.0.0.0:8099`; therefore any process that can reach the add-on's private network can control trusted speakers and inject playback, contrary to the route's “authenticated command” contract and the Phase 11 threat model. The unrestricted CORS policy in `modules/bridge/backend/bl_haos/main.py` further makes browser-originated requests possible wherever the endpoint is reachable.

**Fix:** Generate/provision a bridge credential during add-on startup, require it on every native REST and WebSocket request, send it from `BLHAOSClient`, and reject missing or invalid credentials before resolving devices or executing commands. Restrict CORS to the expected Home Assistant origins and add tests for unauthorized REST, WebSocket, and cross-origin command attempts.

## Warnings

### WR-01: Snapshot refresh never evicts removed speakers

**File:** `modules/integration/custom_components/bl_haos/client.py:53-59`

**Issue:** `_async_refresh_snapshot()` only calls `_async_process_speaker()` for entries returned by the bridge and never removes addresses already present in `self.speakers`. If a speaker is deleted, becomes non-trusted, or is no longer returned by the authoritative `/speakers` snapshot, its stale cached record remains indefinitely. `media_player.async_setup_entry()` creates an entity for every cached address, and subsequent commands can still target that stale device until an unrelated update changes it. This violates the snapshot/source-of-truth behavior and leaves stale entities available in Home Assistant.

**Fix:** Build a normalized snapshot in a temporary mapping, replace or reconcile `self.speakers` after a successful 200 response, and notify listeners for both added/changed and removed addresses. The entity layer should mark removed speakers unavailable or remove them according to the integration lifecycle policy. Add a test that refreshes from a non-empty snapshot to an empty/different snapshot and asserts stale addresses are evicted and listeners are notified.

---

_Reviewed: 2026-09-23T00:00:00Z_  
_Reviewer: the agent (gsd-code-reviewer)  
_Depth: standard_
