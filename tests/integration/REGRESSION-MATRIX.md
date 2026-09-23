# BL-HAOS Release Regression Matrix

This matrix is the scenario-level companion to
[RELEASE-GATES.md](RELEASE-GATES.md). Every scenario has one exact command,
one blocking or environment-qualified outcome, and a required artifact. A
scenario cannot be marked passed from a successful command alone when its
evidence is missing.

## Runtime and Native HA Scenarios

| ID | Scenario | Exact command / gate | Expected result | Evidence | Outcome |
|---|---|---|---|---|---|
| `REL-01-START` | Add-on startup and health | `python -m pytest tests/ -q` / `SIL-CONTAINER` | Service starts, health is honest, no fatal supervisor failure | Test result and SIL reports | Blocking |
| `REL-01-CONNECT` | Adapter discovery and speaker connect | `python -m pytest tests/ -q` / `SIL-CONTAINER` | Valid adapter/device transition and connected state | JUnit and coverage | Blocking |
| `REL-01-DISCONNECT` | Speaker disconnect | `python -m pytest tests/ -q` / `SIL-CONTAINER` | Disconnect is observed without stale connected state | JUnit and coverage | Blocking |
| `REL-01-RECONNECT` | Reconnect exhaustion and recovery | `python -m pytest tests/ -q` / `SIL-CONTAINER` | Bounded retries reach degraded state, later recovery clears it | JUnit and redacted recovery evidence | Blocking |
| `REL-01-PLAYBACK` | Playback failure and recovery | `python -m pytest tests/ -q` / `SIL-CONTAINER` | Failure is surfaced and recovery action is deterministic | JUnit and coverage | Blocking |
| `REL-01-AUTH-OK` | Native HA authentication success | `python -m pytest tests/ -q` / `SIL-CONTRACT` | Valid credentials authorize the native boundary | Contract test result | Blocking |
| `REL-01-AUTH-FAIL` | Native HA authentication failure | `python -m pytest tests/ -q` / `SIL-CONTRACT` | Invalid/missing credentials are rejected without secret leakage | Contract result and redacted log | Blocking |
| `REL-01-DEGRADED` | Dependency/service degradation | `docker compose -f tests/integration/docker-compose.yml run --rm test-runner` / `SIL-CONTAINER` | Missing optional dependency or service is visible as non-passing, never silently skipped | Runner output and reports | Blocking |
| `REL-01-RECOVERY` | Recovery actions and diagnostics | `python -m pytest tests/ -q` / `REGRESSION` | Recovery guidance and diagnostics identify actionable state | Test result and redacted evidence | Blocking |

## Deterministic Demo Scenarios (OPS-03)

| ID | Scenario | Exact command / gate | Expected result | Evidence | Outcome |
|---|---|---|---|---|---|
| `OPS-03-SCAN` | Demo adapter/device scan | `python -m pytest modules/bridge/tests/test_demo_mode.py -q` / `DEMO-OFFLINE` | Same fixture input produces the same ordered devices | Demo JUnit/output | Blocking |
| `OPS-03-PAIR` | Demo pair/trust flow | same command / `DEMO-OFFLINE` | Pairing transition is deterministic without hardware | Demo JUnit/output | Blocking |
| `OPS-03-PLAY` | Demo playback/control flow | same command / `DEMO-OFFLINE` | Media controls and state transitions are deterministic | Demo JUnit/output | Blocking |
| `OPS-03-FAIL` | Demo failure/degraded flow | same command / `DEMO-OFFLINE` | Failure and recovery state are explicit and reproducible | Demo JUnit/output | Blocking |
| `OPS-03-OFFLINE` | Offline/no-BlueZ operation | same command / `DEMO-OFFLINE` | No hardware or network is required; demo cannot be confused with live validation | Demo JUnit/output | Blocking |

## Build, Security, and Support Scenarios

| ID | Scenario | Exact command / gate | Expected result | Evidence | Outcome |
|---|---|---|---|---|---|
| `REL-02-SIL` | Sequential bridge then integration SIL | `docker compose -f tests/integration/docker-compose.yml run --rm test-runner` / `SIL-CONTAINER` | Both suites run in order and aggregate status propagates | Two JUnit plus merged JUnit | Blocking |
| `REL-02-COVERAGE` | XML and HTML coverage | same command / `SIL-CONTAINER` | XML and HTML coverage are generated and non-missing | `coverage.xml`, `coverage-html/` | Blocking |
| `REL-02-REPORTS` | Complete SIL evidence set | same command / `SIL-CONTAINER` | Per-suite, merged JUnit, XML coverage, and HTML coverage all exist | `bridge-junit.xml`, `integration-junit.xml`, `sil-junit.xml`, `coverage.xml`, `coverage-html/` | Blocking |
| `REL-03-AUDIT` | Python/npm/container dependencies | pinned audit commands in `DEPENDENCY-AUDIT` | High/critical findings fail closed | Audit logs | Blocking |
| `REL-03-ARCH` | Architecture parity | workflow builder matrix and manifest assertions | `aarch64`, `amd64`, `armv7` all build | Build evidence per architecture | Blocking |
| `REL-03-COMPAT` | Stable/preview and native integration compatibility | `ARTIFACT-COMPAT` workflow assertions plus release review | Version contract and boundaries are documented | Release record | Blocking |
| `REL-04-REDACT` | Secret-safe evidence | release evidence review | No token, raw WebSocket frame, private URL, PIN, or full device address | Redacted artifact bundle | Blocking |
| `REL-04-HW` | Live hardware qualification | `python test_live_pi.py` and/or `python test_full_pi_workflow.py` / `LIVE-HARDWARE` | Capable environment proves live behavior | Redacted operator evidence | Environment-qualified; unavailable is not pass |
| `REL-04-DEEP` | HAOS/KVM qualification | documented `DEEP-HAOS` compose command | HAOS orchestration succeeds | Redacted logs and SIL reports | Environment-qualified; unavailable is not pass |

## Support and Compatibility Policy

Stable and preview releases follow the support, architecture, native
integration compatibility, upgrade, vulnerability disclosure, dependency
exception, and mandatory redaction rules in [RELEASE-GATES.md](RELEASE-GATES.md).
Stable targets Home Assistant Core 2024.x or later; Preview uses the same
compatibility and security gates before promotion.
The supported architecture set is explicitly `aarch64`, `amd64`, and `armv7`.
high and critical dependency findings are blocking and require a named security owner and expiry date for any documented exception. Retained evidence must be redacted.
Sendspin is an operational reference only; Music Assistant and Sendspin are not
runtime dependencies.
