---
phase: 25-saved-playlist-library
plan: 04
subsystem: storage
tags: [home-assistant, websocket, provider-shortcuts, playlist-library, sil]
requires:
  - phase: 25-01
    provides: Authenticated HA-owned Store and create/list path
  - phase: 25-02
    provides: Shared bounds, mutation locking, revision checks, and fail-closed persistence
provides:
  - Idempotent exact-reference provider shortcuts with local rename/remove
  - Authenticated custom update/reorder/delete with stable IDs and revision protection
  - Core 2026.10.3 SIL coverage for provider bounds, redaction, and custom record isolation
affects: [25-03, 25-05, 26]
actuals:
  tokens: 9800 # Approximate chars/4 for this run's additions; the pre-existing source file was untracked at start.
  tasks: 3
  commits: 0
tech-stack:
  added: []
  patterns: [strict provider record allowlist, fixed-message rejection for extra provider fields, update-only custom command]
key-files:
  created: []
  modified:
    - modules/integration/custom_components/bl_haos/playlist_library.py
    - modules/integration/tests/test_playlist_library_sil.py
key-decisions:
  - "Provider retries are keyed by exact media-source ID and return the original record unchanged, including its local name and display snapshot."
  - "Custom edits use update_custom and require an existing custom record; save_custom retains stable-ID create/retry behavior."
  - "No staging, commits, or planning-state updates were made, per the canonical Phase 25 context."
patterns-established:
  - "All playlist record kinds share the same document validator, serialized mutation lock, Store commit, and read-back verification."
  - "Provider shortcuts persist one opaque reference and allowlisted display fields only; local rename/remove never invokes provider APIs."
requirements-completed: [PL-04, PL-05, PL-11]
coverage:
  - id: D1
    description: "Exact provider media-source IDs map to one stable shortcut across retries; retries preserve local labels and metadata."
    requirement: PL-05
    verification:
      - kind: integration
        ref: "tests/test_playlist_library_sil.py::test_playlist_library_provider_shortcut_retry_and_local_rename_remove"
        status: pass
    human_judgment: false
  - id: D2
    description: "Provider shortcuts reject URL/credential references and obey shared field, record-count, and aggregate-size bounds without copying tracks."
    requirement: PL-11
    verification:
      - kind: integration
        ref: "tests/test_playlist_library_sil.py provider selector on Core 2026.10.3"
        status: pass
    human_judgment: false
  - id: D3
    description: "Authenticated custom update/reorder/delete preserve stable identity and exact duplicate entry order, reject stale revisions, and isolate provider records."
    requirement: PL-04
    verification:
      - kind: integration
        ref: "tests/test_playlist_library_sil.py custom_update/custom_delete selector on Core 2026.10.3"
        status: pass
    human_judgment: false
duration: unknown
completed: 2026-10-27
status: complete
---

# Phase 25 Plan 04 Summary

**Idempotent HA provider playlist shortcuts and revision-protected custom update/reorder/delete through the authenticated integration WebSocket API**

## Performance

- **Duration:** Not measured
- **Started:** 2026-10-27
- **Completed:** 2026-10-27
- **Tasks:** 3/3
- **Implementation/test files modified:** 2
- **Task commits:** None; staging and commits were prohibited for this run.

## Accomplishments

- Added exact-ID provider shortcut deduplication under the shared mutation lock. Retries preserve the stable local ID, label, and original allowlisted metadata.
- Added provider-local rename/remove commands. Provider shortcuts store one reference and bounded display metadata; extra track/error fields are rejected, with no browse, resolve, expansion, or playback call.
- Added shared shape/byte/record/document-bound enforcement for provider records and fixed-message rejection for unexpected provider fields.
- Added update-only custom mutation with stable record IDs, exact submitted entry ordering including duplicates, stale-revision conflicts, and bounded not-found behavior. Custom deletion cannot remove a provider shortcut.
- Preserved authenticated HA WebSocket access, common Store serialization, and canonical read-back persistence behavior.

## Verification

All commands ran in Ubuntu WSL using Core 2026.10.3, helper 0.13.374, aiohttp 3.14.5, and pytest 9.0.3. No native Windows skip was counted as a pass.

- Task 25-04-01: `wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_playlist_library_sil.py -q -p asyncio --asyncio-mode=auto -k "playlist_library_provider"` - **8 passed, 33 deselected** on the final focused run.
- Task 25-04-02: `wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_playlist_library_sil.py -q -p asyncio --asyncio-mode=auto -k "playlist_library_provider and (limit or allowlist or redaction)"` - **7 passed, 34 deselected** on the final focused run.
- Task 25-04-03: `wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_playlist_library_sil.py -q -p asyncio --asyncio-mode=auto -k "playlist_library and (custom_update or custom_delete or revision_conflict)"` - **3 passed, 37 deselected**.
- Complete playlist SIL regression: `wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_playlist_library_sil.py -q -p asyncio --asyncio-mode=auto` - **41 passed, no skips**.
- Editor diagnostics: no errors in either modified Python file.

## Files Created/Modified

- `modules/integration/custom_components/bl_haos/playlist_library.py` - Provider record validation and commands; strict custom update/not-found handling.
- `modules/integration/tests/test_playlist_library_sil.py` - Provider idempotency, local-only operations, bounds/redaction, and custom update/delete SIL cases.
- `.planning/phases/25-saved-playlist-library/25-04-SUMMARY.md` - This execution record.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Prevented provider schema errors from echoing extra-field values**
- **Found during:** Task 25-04-02
- **Issue:** Core's default WebSocket schema rejection included the unexpected `provider_error` value in its error response/log.
- **Fix:** Used Core's supported `probatio.All` schema with extra fields retained for dispatch, then rejected unexpected keys in the provider handler with a fixed bounded message.
- **Files modified:** `modules/integration/custom_components/bl_haos/playlist_library.py`, `modules/integration/tests/test_playlist_library_sil.py`
- **Verification:** Provider allowlist/redaction selector and complete SIL passed.
- **Committed in:** None; commits prohibited by the Phase 25 context.

**2. [Rule 2 - Missing Critical] Prevented custom delete from targeting provider records**
- **Found during:** Task 25-04-01 / Task 25-04-03 boundary verification
- **Issue:** The existing ID-only custom delete path could otherwise match and remove any record kind.
- **Fix:** Added typed not-found handling for absent or non-custom IDs; added provider deletion through a separate local-only command.
- **Files modified:** `modules/integration/custom_components/bl_haos/playlist_library.py`, `modules/integration/tests/test_playlist_library_sil.py`
- **Verification:** Custom delete isolation/not-found selector passed.
- **Committed in:** None; commits prohibited by the Phase 25 context.

**Total deviations:** 2 auto-fixed (Rule 2: 2). No out-of-scope work was added.

## Issues Encountered

- A first aggregate-bound fixture did not account for the per-entry payload needed to reach the document cap; the fixture was corrected and then verified at exactly `MAX_LIBRARY_BYTES - 1` before the provider mutation rejection.
- Core's WebSocket API requires a `probatio.All` schema for an open mapping; a prebuilt `vol.Schema` is not accepted by `websocket_command`. The implementation was adjusted to the pinned Core contract.

## Review Risks

- Home Assistant Core's WebSocket connection logger records inbound message contents at DEBUG in the SIL harness. The integration does not log media IDs, and application rejection responses are bounded/redacted, but framework-level debug logging can still expose submitted opaque references if DEBUG is enabled. No global Core logging policy was changed in this scoped plan.
- The server can enforce HA media-source ID shape and credential-key rejection, but cannot independently prove that an authenticated client sourced a submitted opaque ID from the HA Browse UI. Do not claim arbitrary third-party references are universally credential-free.
- Evidence is local Core SIL only. No live HA/provider, deployment, restart, playback, release, or production acceptance was performed; Phase 24 production/security blockers remain unchanged.

## Next Phase Readiness

The backend CRUD contract required before UI Plan 25-03 is implemented and covered in pinned SIL. Continue only with the approved local/mock Phase 25 scope; live host operations and release remain unauthorized.

## Self-Check: PASSED

- Summary and both declared implementation/test files exist; diagnostics are clean.
- Final Core 2026.10.3 SIL result is 41 passed with no skips.
- Task and metadata commits were intentionally omitted under the user-approved no-commit constraint.
- No STATE.md or ROADMAP.md update commands were run. Existing working-tree changes were preserved.

---
*Phase: 25-saved-playlist-library*
*Completed: 2026-10-27*