---
phase: 15-ha-integration-sil-testing
plan: 01
subsystem: home-assistant-integration
status: complete
tags: [home-assistant, integration, sil, media-player]
requires: [SIL-02, SIL-04]
provides: [ha-integration-sil-suite, snapshot-fixtures, stale-entity-eviction]
affects: [modules/integration/custom_components/bl_haos/media_player.py]
tech-stack:
  added: [pytest-homeassistant-custom-component]
  patterns: [in-process Home Assistant harness, deterministic fake aiohttp transport]
key-files:
  created:
    - modules/integration/tests/conftest.py
    - modules/integration/tests/fixtures/speakers_initial.json
    - modules/integration/tests/fixtures/speakers_after_eviction.json
    - modules/integration/tests/test_ha_integration_sil.py
  modified:
    - modules/integration/custom_components/bl_haos/media_player.py
    - tests/integration/requirements-test.txt
decisions:
  - Keep bridge HTTP and websocket transport entirely in-process with checked-in JSON snapshots.
  - Remove stale media-player entities from the platform when the client cache reports an absent address.
  - Do not alter Phase 16 orchestration or reporting.
metrics:
  duration: "approximately 35 minutes"
  completed: 2026-09-23
  commits: 0
  plan_head_before: c7035f01c7f090b76364b7e3b04adc792bd8882e
actuals:
  tokens: 5600
  tasks: 3
  commits: 0
---

# Phase 15 Plan 01: Home Assistant Integration SIL Testing Summary

Implemented deterministic Home Assistant core SIL coverage for bridge snapshot loading, native media-player creation, strict stale-speaker eviction, config-flow validation, and config-entry unload cleanup. The production change is limited to scheduling `async_remove()` for an entity whose address is no longer present in `client.speakers`.

## Completed Work

- Added the verified test-only `pytest-homeassistant-custom-component` dependency.
- Added fake aiohttp-compatible identity, snapshot, and offline websocket transport fixtures.
- Added initial and reduced authoritative speaker snapshots, including invalid/non-sink records.
- Added four Home Assistant SIL tests covering creation, WR-01 eviction, config-flow outcomes, and unload cleanup.
- Preserved stable normalized unique IDs and retained-speaker state updates during eviction.

## Validation

- `python -m compileall -q modules/integration/custom_components/bl_haos modules/integration/tests/conftest.py modules/integration/tests/test_ha_integration_sil.py`: passed.
- `python -m pytest modules/integration/tests/test_ha_integration_sil.py -q -k snapshot_creation`: blocked during collection because `pytest_homeassistant_custom_component` is unavailable in the active Python 3.14 environment.
- `python -m pytest modules/integration/tests/test_ha_integration_sil.py -q -k eviction`: blocked by the same missing test harness dependency.
- `python -m pytest tests/ -q`: blocked during collection because `playwright` is unavailable in the active environment.

## Deviations from Plan

### Environment validation blocker

The plan's focused and full pytest commands could not execute after repeated attempts to install the verified test harness because the workspace Python installation has a locked `pytest.exe` and incomplete package state. No source workaround or unverified package substitution was made.

## Known Stubs

None. The fake transport is intentional SIL infrastructure and all snapshot data is checked in.

## Unrun Verification

Runtime Home Assistant SIL assertions remain unrun until the test runner environment has `pytest-homeassistant-custom-component` and the full shared requirements installed in the same active interpreter. Phase 16 owns orchestration and unified reporting.
