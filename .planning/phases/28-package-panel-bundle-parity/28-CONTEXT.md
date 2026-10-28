# Phase 28: Package Panel Bundle Parity - Context

**Gathered:** 2026-10-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Prove that the integration's packaged Home Assistant panel is generated from the reviewed panel source, contains the saved-playlist launch and queue summary, and is served through the existing static-route lifecycle. This is a local packaging and verification phase; it does not add UI behavior or authorize deployment or publication.

</domain>

<decisions>
## Implementation Decisions

### Claude's Discretion
- This is an infrastructure phase with an existing checker-approved plan; implementation details remain within that plan and the existing Vite/package-test patterns.
- Preserve the current panel behavior: saved-playlist launch and queue summary remain in the panel, while transport controls remain owned by the native media-player entity.
- Review and test the existing dirty panel source/test changes before using them as build input. Do not edit or revert those changes.
- Build parity checks only into a fresh temporary directory. Refresh `panel_static` only as a distinct, intentional local build after source review and passing focused tests.
- Keep static package assertions runnable without Node. The fresh-build test may skip only when Node/npm or panel build dependencies are unavailable; Phase 29 owns provision of the chosen toolchain in CI.
- Do not stage or commit; do not deploy, publish, change a host, restart Home Assistant, perform playback/provider/session operations, or run hardware tests.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `modules/integration/tests/test_package_layout.py` owns static package assertions without a Home Assistant runtime.
- `modules/integration/panel_ui/vite.config.ts` is the existing Vite producer for the packaged panel bundle.
- `modules/integration/tests/test_panel_registration.py` owns Home Assistant static-route and unload/reload SIL coverage.

### Established Patterns
- Build generated output to a unique `tmp_path`, assert the expected output set, and compare bytes without first overwriting the tracked artifact.
- Keep package-content assertions separate from Home Assistant serving and lifecycle assertions.
- Use the pinned local TypeScript/Vite toolchain; do not add dependencies or select CI runtime pins in this phase.

### Integration Points
- Source: `modules/integration/panel_ui/src/media-panel.tsx`.
- Packaged bundle: `modules/integration/custom_components/bl_haos/panel_static/bl-haos-media-panel.js`.
- Served module URL: `/api/bl_haos/catalog/bl-haos-media-panel.js`.

</code_context>

<specifics>
## Specific Ideas

No new user-facing design requirements. Retain the existing package and serving boundaries.

</specifics>

<deferred>
## Deferred Ideas

- CI Node/npm runtime selection and dependency installation belong to Phase 29.
- Live Home Assistant/provider/playback acceptance belongs to Phase 31; HA-shell accessibility to Phase 32; hardware soak to Phase 33.

</deferred>