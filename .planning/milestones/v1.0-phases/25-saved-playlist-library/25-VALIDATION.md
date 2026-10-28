---
phase: "25"
slug: "saved-playlist-library"
status: approved
nyquist_compliant: false
wave_0_complete: false
created: "2026-10-25"
---

# Phase 25 - Validation Strategy

> Local/mock-only execution is authorized. Production/live HA acceptance is not authorized; PL-01/02/03 remain pending, T-24-15 OPEN/HIGH and T-24-16 OPEN/MEDIUM remain open, and release/deployment remain blocked.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 9.0.3, Vitest 5.0.4, Playwright 1.63.0 |
| **Config files** | `modules/integration/pytest.ini`, `modules/integration/panel_ui/vitest.config.ts`, `modules/integration/panel_ui/playwright.mock.config.ts` |
| **Focused panel command** | `npm --prefix modules/integration/panel_ui test -- --run src/playlist-library.test.tsx` |
| **Mock browser command** | `npm --prefix modules/integration/panel_ui run test:mock-panel` |
| **Panel build command** | `npm --prefix modules/integration/panel_ui run build` |
| **Pure validator/migration unit command** | `wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/unit/test_playlist_library.py -q -p asyncio --asyncio-mode=auto --tb=short --show-capture=no` |
| **SIL runtime** | Ubuntu WSL, Core 2026.10.3, helper 0.13.374, aiohttp 3.14.5, pytest 9.0.3 |
| **SIL executable** | `/home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python` |
| **WSL checkout path** | `/mnt/f/Workspace/BL-HAOS/modules/integration` |

SIL commands below are invoked from the repository root with `wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest ...`. Pure unit tests use the existing `tests/unit` stubs in a separate pytest process; do not mix them with real-Core SIL collection. Native Windows collection skips are not SIL evidence. Panel Vitest and mock Playwright remain separate from Core SIL and production acceptance.

---

## Sampling Rate

- **After every task:** Run the narrowest relevant unit, SIL, Vitest, or mock-browser check from the map below.
- After each wave, run the panel Vitest suite and build; run the pinned Core SIL suite for all changed integration behavior.
- Before phase verification, run the focused SIL selectors for the library, the complete panel Vitest suite, the panel build, and mock Playwright suite.
- Do not run host Playwright, deployment, restart, real provider, or playback checks.

## Existing Worktree Baseline

Read-only status showed `modules/integration/panel_ui/` and `modules/integration/custom_components/bl_haos/panel_static/` as existing untracked local content, with nearby integration source already modified. Preserve those baseline files and make only scoped edits. **For this autonomous run, do not stage or commit any work:** task outputs overlap the untracked baseline, and path or hunk staging cannot establish a clean, independently valid commit without absorbing existing work. Record completed local work in summaries; require later user review and explicit scope approval before committing.

The UI design contract in `25-UI-SPEC.md` is approved (2026-10-25). This approval covers the design contract, not execution evidence or production acceptance.

---

## Per-Task Verification Map

Each task below records its exact plan, wave, requirements, threat reference, runnable command, and immediate observable failure condition. Command paths are repository-root-relative except the established WSL executable and checkout location.

```xml
<task id="25-01-01" plan="25-01" wave="1" requirements="PL-04 PL-06 PL-11" threat="T-25-01">
	<automated>wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_playlist_library_sil.py -q -p asyncio --asyncio-mode=auto -k "playlist_library_create"</automated>
	<fails_when>The SIL skips, the authenticated create/list path fails, a repeated ID creates a duplicate, or the response contains fields outside the record contract.</fails_when>
	<automated>npm --prefix modules/integration/panel_ui test -- --run src/playlist-library.test.tsx</automated>
	<fails_when>Library create success precedes HA acknowledgment, the injected hass boundary is bypassed, or a browser/add-on persistence or playback action appears.</fails_when>
</task>
<task id="25-01-02" plan="25-01" wave="1" requirements="PL-06 PL-11" threat="T-25-01">
	<automated>wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_playlist_library_sil.py -q -p asyncio --asyncio-mode=auto -k "playlist_library and (reload or restart or persistence)"</automated>
	<fails_when>The SIL skips, entry reload clears data or duplicates global WebSocket registration, fresh Store reconstruction changes IDs/order, or bridge-session replacement mutates HA storage.</fails_when>
</task>
<task id="25-02-01" plan="25-02" wave="2" requirements="PL-04 PL-06 PL-11" threat="T-25-02 T-25-03">
	<automated>wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_playlist_library_sil.py -q -p asyncio --asyncio-mode=auto -k "playlist_library and (validation or migration or corruption or concurrent or revision or redaction)"</automated>
	<fails_when>The SIL skips, bounds or complete-reference rejection are wrong, Store.path cases are misclassified, migration overwrites unsupported data, or concurrent/stale writes lose saved state.</fails_when>
</task>
<task id="25-02-02" plan="25-02" wave="2" requirements="PL-06 PL-11" threat="T-25-01 T-25-02">
	<automated>wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_playlist_library_sil.py -q -p asyncio --asyncio-mode=auto -k "playlist_library and (authenticated or storage_failure or schema)"</automated>
	<fails_when>The SIL skips, authenticated users do not share the library, anonymous access succeeds, a storage failure enables mutation or reports success, or malformed schema payloads are accepted or mutate storage.</fails_when>
</task>
<task id="25-02-03" plan="25-02" wave="2" requirements="PL-04 PL-06 PL-11" threat="T-25-02 T-25-03">
	<automated>wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/unit/test_playlist_library.py -q -p asyncio --asyncio-mode=auto --tb=short --show-capture=no</automated>
	<fails_when>The focused unit file is missing or skipped, any configured boundary or raw/encoded credential-reference case is accepted, accepted IDs/order change, or migration rewrites unsupported data.</fails_when>
</task>
<task id="25-04-03" plan="25-04" wave="3" requirements="PL-04" threat="T-25-02">
	<automated>wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_playlist_library_sil.py -q -p asyncio --asyncio-mode=auto -k "playlist_library and (custom_update or custom_delete or revision_conflict)"</automated>
	<fails_when>The SIL skips, custom update/reorder/delete is missing, stale revisions overwrite newer data, or unknown/custom IDs mutate another record.</fails_when>
</task>
<task id="25-03-01" plan="25-03" wave="4" requirements="PL-04" threat="T-25-04">
	<automated>npm --prefix modules/integration/panel_ui test -- --run src/playlist-library.test.tsx</automated>
	<fails_when>Any editor, duplicate/empty draft, order, focus, draft-retention, conflict, or exact-reference assertion fails.</fails_when>
	<automated>npm --prefix modules/integration/panel_ui run build</automated>
	<fails_when>The panel bundle or TypeScript build fails.</fails_when>
</task>
<task id="25-03-02" plan="25-03" wave="4" requirements="PL-04" threat="T-25-04">
	<automated>npm --prefix modules/integration/panel_ui test -- --run src/playlist-library.test.tsx</automated>
	<fails_when>Confirmation copy/focus, dirty-draft protection, failure retention, Escape behavior, or focus restoration fails.</fails_when>
</task>
<task id="25-04-01" plan="25-04" wave="3" requirements="PL-05 PL-11" threat="T-25-05">
	<automated>wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_playlist_library_sil.py -q -p asyncio --asyncio-mode=auto -k "playlist_library_provider"</automated>
	<fails_when>The SIL skips, exact-ID retries duplicate or rename a shortcut, distinct references collapse, a prohibited complete reference is stored, or provider tracks are copied.</fails_when>
</task>
<task id="25-04-02" plan="25-04" wave="3" requirements="PL-05 PL-11" threat="T-25-05">
	<automated>wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_playlist_library_sil.py -q -p asyncio --asyncio-mode=auto -k "playlist_library_provider and (limit or allowlist or redaction)"</automated>
	<fails_when>The SIL skips, provider records bypass common limits, complete-reference URL/credential cases are accepted, or URL/credential/provider-error sentinels appear in saved data, responses, or logs.</fails_when>
</task>
<task id="25-05-01" plan="25-05" wave="5" requirements="PL-05" threat="T-25-06">
	<automated>npm --prefix modules/integration/panel_ui test -- --run src/playlist-library.test.tsx</automated>
	<fails_when>Save does not submit the exact HA-browse reference, retry changes the local label, or server acknowledgment does not control success.</fails_when>
</task>
<task id="25-05-02" plan="25-05" wave="5" requirements="PL-05" threat="T-25-06">
	<automated>npm --prefix modules/integration/panel_ui test -- --run src/playlist-library.test.tsx</automated>
	<fails_when>Removal is unconfirmed or targets provider content, a failed request hides the row/dialog, or empty/error/focus assertions fail.</fails_when>
	<automated>npm --prefix modules/integration/panel_ui run build</automated>
	<fails_when>The typed panel build fails.</fails_when>
</task>
<task id="25-06-01" plan="25-06" wave="6" requirements="PL-06 PL-11" threat="T-25-07">
	<automated>wsl.exe -d Ubuntu --cd /mnt/f/Workspace/BL-HAOS/modules/integration env BLHAOS_RUN_SIL=1 PYTHONDONTWRITEBYTECODE=1 /home/mse/.venvs/bl-haos-sil-2026.10.3/bin/python -m pytest tests/test_playlist_library_sil.py -q -p asyncio --asyncio-mode=auto -k "playlist_library_availability"</automated>
	<fails_when>The SIL skips, browse success is inferred from playability, an error changes stored bytes/order, or media resolution is invoked.</fails_when>
</task>
<task id="25-06-02" plan="25-06" wave="6" requirements="PL-06 PL-11" threat="T-25-07">
	<automated>npm --prefix modules/integration/panel_ui test -- --run src/playlist-library.test.tsx</automated>
	<fails_when>A check runs without user action, an accepted ID changes, failures alter saved data, statuses persist across reload, or status/accessibility assertions fail.</fails_when>
	<automated>npm --prefix modules/integration/panel_ui run build</automated>
	<fails_when>The typed panel build fails or adds a resolver/playback path to availability checks.</fails_when>
</task>
<task id="25-07-01" plan="25-07" wave="7" requirements="PL-04 PL-05 PL-06 PL-11" threat="T-25-08">
	<automated>npm --prefix modules/integration/panel_ui test -- --run</automated>
	<fails_when>The focused panel suite exits non-zero or reports no matching tests.</fails_when>
	<automated>npm --prefix modules/integration/panel_ui run test:mock-panel</automated>
	<fails_when>A mock workflow fails, a request escapes to a live host, IDs/order or data are lost, or playback/queue behavior appears.</fails_when>
</task>
<task id="25-07-02" plan="25-07" wave="7" requirements="PL-04 PL-05 PL-06 PL-11" threat="T-25-08">
	<automated>npm --prefix modules/integration/panel_ui test -- --run</automated>
	<fails_when>Component accessibility, keyboard, semantic status, or focus assertions fail.</fails_when>
	<automated>npm --prefix modules/integration/panel_ui run test:mock-panel</automated>
	<fails_when>Any of the ten backstops lacks a local assertion, a viewport overlaps/overflows, or a visible target is below 44px.</fails_when>
</task>
<task id="25-07-03" plan="25-07" wave="7" requirements="PL-04 PL-05 PL-06 PL-11" threat="T-25-08">
	<automated>python -m pytest modules/integration/tests/test_phase25_docs.py -q</automated>
	<fails_when>The test exits non-zero or reports stale Phase 25 deferral or false production-acceptance wording.</fails_when>
	<automated>Push-Location modules/bridge; python -m pytest tests/test_phase25_docs.py -q; $code = $LASTEXITCODE; Pop-Location; exit $code</automated>
	<fails_when>The test exits non-zero or reports a stale playlist phase-boundary claim in bridge documentation.</fails_when>
</task>
```

Threat register entries are scoped to Phase 25; T-24-15 remains OPEN/HIGH and T-24-16 remains OPEN/MEDIUM throughout this local/mock-only plan set.

---

## Wave 0 Requirements

Task 25-02-03 creates `modules/integration/tests/unit/test_playlist_library.py` for pure bounded validator and migration coverage using the existing `tests/unit` stubs; Store, WebSocket, media-source, and lifecycle semantics remain in pinned WSL SIL. Task 25-01-01 begins with RED assertions for the cross-layer create/list tracer before implementation. Each later behavior task adds its focused test first, observes the intended failure, then implements the behavior. `wave_0_complete` remains false until execution records RED/GREEN evidence; this document does not claim tests have run.

---

## UI Consideration Coverage

All 26 unmarked UI Considerations rows are lifted as exact must-have truth strings across plans 25-01, 25-03, and 25-06. All 10 rows explicitly marked `verification: backstop` are flat `{statement, verification: backstop}` entries in plan 25-07 and receive local rendered-panel assertions only. Backstops are not production HA-shell evidence.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| PL-01/02/03 real provider/authentication, production panel, physical playback | Pending | Phase 24 production acceptance is not authorized in this work. | Keep production requirements pending; local mock and SIL tests are not host evidence. |
| T-24-15 credential/session acceptance | OPEN/HIGH | Real-session acceptance is outside this authorized scope. | Remains a release blocker; no Phase 25 local test closes it. |
| T-24-16 production host/accessibility evidence | OPEN/MEDIUM | HA-shell/host acceptance is outside this authorized scope. | Remains a release blocker; mock screenshots do not satisfy it. |
| Release, deployment, live host operations, real provider/physical playback | Blocked / not authorized | Explicit user constraint. | No such task or command appears in this phase plan set. |

---

## Validation Sign-Off

- [ ] All 17 plan tasks pass their focused automated command(s) in the specified environment.
- [ ] Full panel Vitest, panel build, mock Playwright, and applicable Core 2026.10.3 SIL checks pass.
- [ ] Mock tests assert all 10 UI backstops and report only local/mock evidence.
- [ ] T-24-15 remains OPEN/HIGH; T-24-16 remains OPEN/MEDIUM; release/deployment remain blocked.
- [ ] `nyquist_compliant: true` set only after required local/SIL validation is complete.

**Validation strategy:** approved 2026-10-25. **Execution evidence:** not run.
