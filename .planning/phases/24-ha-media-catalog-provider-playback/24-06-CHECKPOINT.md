---
phase: 24-ha-media-catalog-provider-playback
plan: "06"
status: blocked
gate: blocking-human
updated: "2026-10-24"
completion_scope: authorized-local-portions-only
commits: 0
---

# Plan 24-06 Local-Only Checkpoint

## Controlled Deployment and Test Window - Planning Only

The user selected "Plan a controlled deployment and test window" after local verification. This authorizes planning and read-only inventory, not publishing, backups, installs, service calls, restarts, session export or playback. No deployment window has been scheduled or executed.

Current autonomous re-entry read-only check: Core remains 2026.10.3; the shared HA browser shows one BL-HAOS media_player (`media_player.logitech_bt_adapter`) idle/not connected, and the attempted `media_source/browse_media` query is unavailable. This does not prove whether any provider is configured. A connected target and actual provider/playlist references remain external prerequisites.

### Observed Baseline and Candidate Identity

- Read-only Supervisor inventory: add-on c839f4a9_bl_haos is started at 0.2.67, latest advertised 0.2.67, update_available=false, boot=auto. The host previously reported amd64, Core 2026.10.3, HTTP port 80 and KVM virtualization. The listed add-on architectures are supported targets, not proof that all three builds exist.
- Installed integration manifest reports 0.2.19 and lacks the local candidate's HTTP dependency. Therefore its version alone does not identify the new source. Capture a file hash/archive before any replacement.
- Local bridge candidate is 0.2.69 and local integration candidate is 0.2.20, now distinct from live integration 0.2.19. The manifest and package-layout assertion were updated together; the focused assertion passed and the full package-layout suite passed 10 tests. This clears local identity only. Publication remains NO-GO pending separate release authorization, immutable bridge artifact comparison, rollback-source verification and maintenance-window inputs.
- Do not publish different integration contents as the already installed 0.2.19. Do not overwrite an existing bridge tag without comparing its immutable digest.
- The existing build-and-push.ps1 publishes both the version and latest tags, and defaults to three architectures. It was inspected, not executed. Publishing latest or additional architectures requires explicit release authorization; prefer a reviewed version-only amd64 candidate and recorded immutable digest for the first window.

### Before Booking the Window

1. Choose the release owner, rollback owner and a maintenance time. Allow a provisional 45-minute live window, with image builds, registry authentication, signing/publishing and test-fixture preparation completed beforehand. Build duration is unmeasured; do not include an unverified build in the outage budget.
2. Authorize release preparation/publication separately if desired. Agree exact bridge and unique integration versions, source revisions/archive hashes, amd64 image digest and install mechanism. No commit, push, tag or registry mutation is authorized by this plan.
3. Require a verified restore point: a Supervisor backup that includes add-on data and Home Assistant configuration, plus an independent archive/hash of the installed integration. Store snapshots and secrets outside the source checkout; retain only non-secret identifiers. Confirm that the operator can restore it without depending on the candidate.
4. Verify that the baseline 0.2.67 image/digest or a restorable backup is actually available. An old version number is not a rollback mechanism. Do not start if restore ownership or access is unknown.
5. Recheck Core 2026.10.3 and current bridge health. Confirm one named test speaker is powered, in range and not held by another source. The last observed Logitech link was disconnected; this is a separate unresolved prerequisite. No unpairing, radio reset or host reboot is included.
6. Select real provider and playlist opaque references and one explicit connected BL-HAOS entity. The operator approves audible playback and acceptable volume; do not invent a URL or substitute a different target if the chosen one fails.
7. Prepare two distinct external disposable browser-state fixtures under operator control: a valid test session and a separate formerly valid, already-expired fixture with owner attestation and read-only expiry consent. Do not extract or revoke the shared browser session, put secrets in chat, or save fixtures in any source checkout. The harness observes rejection; it cannot cryptographically prove why an owner-attested fixture is invalid.
8. Run the documented local/WSL gates and pure host validators on the finalized artifacts. The existing Windows POSIX-only skip is not a hardware pass. Confirm the harness has all required inputs and no debug/trace/video output that can retain secrets.

### Proposed Live Sequence and Go/No-Go Points

| Stage | Proposed Action After Separate Approval | Advance Only If | Stop / Roll Back If |
|-------|-----------------------------------------|-----------------|---------------------|
| 0: preflight and backup | Capture bounded current health/versions and create the approved restore point; verify its completion and recoverability | Restore point, owner and candidate identities are confirmed | Backup/restore access, expected Core version or baseline health is uncertain |
| 1: bridge candidate | Install the approved amd64 bridge image through Supervisor using the agreed version/digest; let that update restart only the add-on | Within a provisional 5-minute observation budget, add-on remains started, D-Bus/adapter/PipeWire are available, native authentication works, and one selected trusted speaker inventory is preserved | Startup/health loops, missing adapter/trusted inventory, native-auth failure or new reconnect storm |
| 2: integration candidate | Install the uniquely versioned integration artifact with the fixed panel bundle, then run Core configuration validation; use one planned Core restart if the chosen install path requires it | Within a provisional 5-minute startup budget, Core is reachable, the expected entry/native entities load, and the fixed module/panel is served without setup errors | Configuration validation fails, Core/native entries fail to load or static/panel setup is unavailable |
| 3: read-only catalog | Open the actual HA-owned panel; verify explicit empty target selection, provider hierarchy, opaque playlist metadata, native Browse Media and ingress navigation | No copied credentials, raw resolved URL, provider fallback or bridge catalog proxy is involved | Unexpected endpoint/storage access, leaked URL material, wrong provider metadata or stale-session behavior |
| 4: approved playback | Select only the approved connected speaker and submit one provider item/playlist reference under explicit playback consent; stop it afterward | One service submission/target, bounded success state and operator audible confirmation agree | Duplicate submissions, target substitution, unexplained restart, invalid reference fallback or audible instability |
| 5: failure/session tests | Run unavailable/denied/unresolvable cases and the separate owner-attested expired fixture, never the shared session | Errors stay bounded, no automatic replay/skip or credential leak; fixture rejection is recorded with its attestation limitation | Shared session is touched, an unapproved target plays, requests leak secrets or an accepting session is called expired |
| 6: visual review | Capture actual HA-shell screenshots at 375/768/1440; review long names, 44px targets, overflow, keyboard/focus, labels/live region, contrast and reduced motion | Automated assertions and the human backstop pass | Layout/accessibility defects or missing evidence; do not substitute offline fixtures |
| 7: soak and release decision | Observe an agreed initial 10-15 minute stability period and inspect sanitized logs; schedule a longer reconnect soak separately if required | Owner signs the observed evidence with no unresolved gate | Any privacy/auth fault, repeated reconnect failure or rollback trigger |

These budgets are proposed operator stop points, not measured deployment timing or performance guarantees. If they expire, stop rather than extend the outage indefinitely.

### Restart and Rollback Budget to Approve Before Execution

- Proposed normal rollout: one update-induced add-on restart and at most one Core restart. The earlier disposable-probe restart approval is exhausted and cannot cover these actions.
- Reserve explicit rollback authorization before starting: restoring the integration may require one additional Core restart, and restoring the add-on may restart it again. If that reserve is not approved, do not begin a rollout that cannot be recovered within the authorized actions.
- Rollback uses the verified backup/baseline image and integration archive, not an improvised Docker command, raw configuration edit or assumed downgrading flag. Preserve Bluetooth bonds, add-on options and integration entries; do not remove/re-add the integration to hide a failed upgrade.
- After restore, confirm observed baseline identities/hashes, Core/native entry/entity availability, bridge health and the previously approved bounded control test. Treat rollback as HOLD until the operator validates restored native control; version display alone is insufficient.
- No OS reboot, Bluetooth controller reset, re-pairing, global latest-tag publication, shared-session revocation or extra retries is included. Each would require a new explicit decision.

### Evidence and Final Exit

Use the current TESTING.md and the separate panel host harness, not the older release runbook's retired Docker-Compose acceptance commands. Keep fixtures, raw logs and screenshots in approved ignored/external locations. Publish only sanitized versions/digests, command exit statuses, bounded health results, scenario labels and pass/fail decisions; do not attach credentials, session contents or resolved URLs.

Phase 24 stays human_needed until its mandatory host scenarios and human backstop pass and the owner accepts them. Phase 27 still needs its own real reconnect soak before claiming the original live fault fixed. Phases 25-26 and milestone completion remain gated. **This plan is not deployment approval.**

## Current Task

**24-06-01 remains blocked:** production panel not deployed, last known speaker
disconnected, no provider metadata/references or external disposable session
files supplied. Harness preparation is local work, not satisfaction of this
mandatory task. No complete SUMMARY is created; global STATE, ROADMAP,
REQUIREMENTS and state.json remain parent-owned and untouched by this run.

## Completed Local Work

| Task | Local Result | Commit |
|---|---|---|
| 24-06-01 preparation only | Separate real-host config/spec, sanitized reporter, pure input validators; host execution blocked | None, prohibited |
| 24-06-02 | Five docs and content-sensitive tests updated with local/deployment/Phase 25/26 boundaries | None, prohibited |
| 24-06-03 | Bridge constants/config/top changelog synchronized at 0.2.69, undeployed; 0.2.68 reconnect work preserved | None, prohibited |

Integration manifest candidate version is 0.2.20; live version remains 0.2.19. Only @playwright/test
1.63.0 was added as a direct test dependency after registry verification;
three package entries were added, no other direct pins upgraded.

## Latest Gates

- WSL real Core: **127 passed**, no skips (123 baseline + 4).
- Separate WSL units: **58 passed**, no skips.
- Windows full bridge: **323 passed, 1 existing POSIX skip, 1 existing Starlette warning** (319 baseline + 4).
- Panel/bridge Vitest: **41 / 26 passed**; both typed builds passed.
- Actual root L1: passed, bridge **323 + 1 skip**, integration **68**, frontend **26**.
- Pure host-config tests: **21 passed**, no skips; host typecheck passed.
- Pre-full version/static gate: integration **10**, bridge config/assets **16**, passed.
- Missing-env Playwright: **expected exit 1**, exact missing-URL precondition, zero host scenarios, not a host pass.
- Scoped editor diagnostics and module/root whitespace checks passed; existing root CRLF advisories only.

Exact commands, RED/GREEN, timings and limitations are in 24-VALIDATION.md.

## This Run's Inventory

Six new files (relative to this run, not all pre-existing untracked work):

- modules/integration/panel_ui/e2e/playwright.config.ts
- modules/integration/panel_ui/e2e/catalog.spec.ts
- modules/integration/panel_ui/e2e/host-env.mjs
- modules/integration/panel_ui/e2e/host-env.test.mjs
- modules/integration/panel_ui/e2e/safe-reporter.mjs
- .planning/phases/24-ha-media-catalog-provider-playback/24-06-CHECKPOINT.md

Fifteen existing files modified/regenerated:

- README.md
- TESTING.md
- modules/integration/README.md
- modules/integration/tests/test_package_layout.py
- modules/integration/panel_ui/.gitignore
- modules/integration/panel_ui/package.json
- modules/integration/panel_ui/package-lock.json
- modules/integration/custom_components/bl_haos/panel_static/bl-haos-media-panel.js (generated only)
- modules/bridge/README.md
- modules/bridge/DOCS.md
- modules/bridge/CHANGELOG.md
- modules/bridge/config.yaml
- modules/bridge/backend/bl_haos/constants.py
- modules/bridge/tests/test_addon_config.py
- .planning/phases/24-ha-media-catalog-provider-playback/24-VALIDATION.md

Generated bridge dist, installed node_modules and test-results are ignored.
The obsolete temporary reporter .ts was removed. No auth state or screenshot
fixture was created as host proof. Panel output is 232397 bytes, SHA256
7ddaaad48e28683d0bdf2767b247ec1091acc1f481efb9f4a570d259df76cec6.

## Awaiting Separately Authorized Host Acceptance

Provide Core 2026.10.3 URL, authorization/deployed production integration,
explicit connected BL-HAOS target, actual opaque provider/playlist references,
external workspace-disposable authenticated state and real-play consent.
Also provide a different externally stored, separately authorized naturally
expiring test session and expiry-observation consent. See TESTING.md for exact
BLHAOS_HA_* variables and command. Never extract the current/shared session,
revoke it, mutate its tokens, guess providers or substitute raw URLs.

The expiry scenario is fail-closed: actual auth rejection after initial fixture
authentication is required. Its real-host observability is unverified; a
disconnect, timeout or invalid sentinel is not actual expiry proof. Public
provider layout/root discovery is also unverified. Long-name HA shell layout,
375/768/1440 screenshots, unavailable/denied/unresolvable behavior, accessibility
and physical audio need real evidence plus the specified human backstop.

No live access, production deployment, physical playback, additional restart,
pairing or radio operation is authorized/performed. The earlier accepted
temporary probe used its one Core restart and was removed. No second restart
is authorized. No commits, staging, branches, phase 27 source edits, new phases
or Phase 25/26 execution occurred. **Do not mark 24-06 or PL-01/02/03 complete.**

## 24-06-REVIEW WR-01/WR-02 Remediation (Local Only) - 2026-10-24

Supersedes the expiry paragraph above. WR-01: the reporter prints an
allowlisted static scenario id (`catalog-dispatch`, `unauthenticated-denial`,
`attested-expiry`, else `unlisted`) plus a known status only. WR-02: the
expiry scenario now needs a separate external fixture whose owner attests it
already expired (`BLHAOS_HA_EXPIRY_ATTESTATION`, read-only, hard-fail if
missing). It passes only for the HA login page or HA HTTP auth rejection with
no accepted call. Numeric disconnect, 403 and live-connection `unauthorized`
never count. IN-01 real temp-dir coverage and IN-03 manifest 0.2.19 assert
added; IN-02 unchanged. New file: e2e/expiry-evidence.mjs. Pure suite 32
passed, host typecheck passed, missing-env expected exit 1. Actual expiry,
provider layout, screenshots and audio remain **unverified**. Details are in
24-VALIDATION.md. No commits.