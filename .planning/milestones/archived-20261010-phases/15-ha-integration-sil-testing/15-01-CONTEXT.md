# Phase 15 Context

## Scope

Build isolated Home Assistant core SIL coverage for the bundled `bl_haos` custom integration. The suite must load the integration, feed deterministic bridge `/api/native/speakers` snapshots, exercise config-entry setup and unload, and verify native `media_player` entity lifecycle behavior.

## Decisions

- **D-01:** Use the Home Assistant custom-component pytest harness in-process; do not require a running HAOS VM, live bridge, Bluetooth hardware, D-Bus, or network service for Phase 15 tests.
- **D-02:** Represent authoritative bridge state with checked-in static JSON snapshots, including an initial multi-speaker snapshot and a later snapshot with one speaker absent.
- **D-03:** Treat stale-speaker removal as a platform lifecycle contract: a speaker absent from a refreshed snapshot must be removed from the active Home Assistant entity set, not merely deleted from the client's cache. The SIL test must fail against the current behavior if eviction is not wired through `media_player` setup.
- **D-04:** Keep Phase 15 limited to integration SIL tests and the minimal production lifecycle wiring required for those tests; leave test-runner orchestration and unified reporting to Phase 16.

## Verification Boundary

Focused verification runs from the repository root with the shared pytest configuration. The focused integration SIL module must pass before the full repository test suite is run. The existing bridge SIL suite remains a regression dependency but is not modified by this phase.

## Package Legitimacy Audit

| Package | Registry | Purpose | Status |
|---|---|---|---|
| `pytest-homeassistant-custom-component` | https://pypi.org/project/pytest-homeassistant-custom-component/ | Home Assistant core fixtures and custom-component loading | VERIFIED |

No production runtime dependency is introduced. The package is test-only and belongs in `tests/integration/requirements-test.txt`, which is consumed by the Phase 13/16 test runner image.
