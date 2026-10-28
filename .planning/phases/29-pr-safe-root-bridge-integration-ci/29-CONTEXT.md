# Phase 29: PR-Safe Root, Bridge & Integration CI - Context

**Gathered:** 2026-10-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Make root, bridge, and integration pull-request validation pass on declared runtimes, including the Phase 28 panel-bundle parity check, without publishing add-on images, packages, or release artifacts. This phase changes CI validation only; release workflows and publication remain separately gated.

</domain>

<decisions>
## Implementation Decisions

### Claude's Discretion
- This is an infrastructure phase; implementation choices should reuse existing workflow conventions and avoid application-code changes unless a CI blocker requires them.
- Use the repository's existing Node 22 CI convention for the panel validation job, and install the panel's locked dependencies so the Phase 28 parity test runs rather than skips.
- Keep pull-request validation separate from release/image-publishing workflows. Do not trigger or run a publishing workflow, push, deploy, or publish artifacts.
- Preserve the declared Python runtime split: Python 3.12 for client/unit gates and Python 3.14 for the pinned Home Assistant SIL gate.
- Do not stage or commit; do not make host, Core, playback, provider/session, or hardware changes.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `.github/workflows/tests.yml` already has repository hygiene, bridge L1, integration L1, integration SIL, and bridge frontend jobs.
- `modules/integration/panel_ui/package.json` and `package-lock.json` provide the locked Vite/TypeScript build toolchain.
- `modules/bridge/scripts/build-and-push.ps1` and other release scripts are publication surfaces and must remain outside PR validation.

### Established Patterns
- GitHub Actions uses `actions/setup-python@v6` and `actions/setup-node@v5` with explicit major runtimes.
- The bridge frontend job uses Node 22 and `npm ci --ignore-scripts`; integration Python CI installs only declared client-test dependencies.
- Pull-request jobs should run tests/builds without image or release publishing steps.

### Integration Points
- Root CI: `.github/workflows/tests.yml`.
- Bridge package/release workflow surfaces: `modules/bridge` workflows and scripts.
- Integration unit/package checks: `.github/workflows/tests.yml`, `modules/integration/tests/test_package_layout.py`, and `modules/integration/panel_ui`.
- Integration SIL remains a separate Python 3.14 gate.

</code_context>

<specifics>
## Specific Ideas

Make CI run the bundle parity test unconditionally by providing Node 22 and installing the panel lockfile. Preserve pull-request/push test workflows as non-publishing gates.

</specifics>

<deferred>
## Deferred Ideas

- Add-on/image/package publication, deployment, release-artifact upload, and go/no-go remain out of scope.
- Live Home Assistant/provider/playback, HA-shell accessibility, and reconnect hardware testing remain assigned to later authorized phases.

</deferred>