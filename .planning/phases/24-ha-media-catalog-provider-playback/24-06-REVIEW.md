---
phase: 24-ha-media-catalog-provider-playback
plan: "06"
reviewed: 2026-10-24T16:51:36Z
resolution_audited: 2026-10-24
depth: standard
files_reviewed: 13
files_reviewed_list:
  - modules/integration/panel_ui/e2e/playwright.config.ts
  - modules/integration/panel_ui/e2e/catalog.spec.ts
  - modules/integration/panel_ui/e2e/expiry-evidence.mjs
  - modules/integration/panel_ui/e2e/host-env.mjs
  - modules/integration/panel_ui/e2e/host-env.test.mjs
  - modules/integration/panel_ui/e2e/safe-reporter.mjs
  - modules/integration/panel_ui/package.json
  - modules/integration/tests/test_package_layout.py
  - modules/bridge/tests/test_addon_config.py
  - README.md
  - TESTING.md
  - modules/bridge/CHANGELOG.md
  - modules/bridge/config.yaml
findings:
  critical: 0
  warning: 0
  info: 1
  total: 1
status: clean
review_scope: bounded-WR-02-resolution-local-only
---

# Phase 24-06: Code Review Report (authorized local portions only)

**Reviewed:** 2026-10-24T16:51:36Z
**Depth:** standard
**Scope:** local harness, docs and version contract. No host, network or
external-state file was touched. The 32-test pure suite, host typecheck and
package-layout guard passed. No browser/host test, external fixture contents or
missing-environment negative-exit check was run.

## Summary

Final bounded resolution audit on 2026-10-24 supersedes the open WR-02 verdict
below. The current classifier checks HTTP 401/403/token rejection inside the
live-connection branch and returns `denied`, including when no probe error code
exists. The independent final pure suite passed all 33 tests, including the new
live-response regression; host-harness typecheck passed. No source/test edit or
host execution was performed by this audit. The original review is retained as
history, not an open finding. Clean means no unresolved actionable finding in
this bounded local review; IN-02 remains informational and is not risk acceptance
or security/host sign-off.

WR-01 is resolved: the reporter now emits only fixed allowlisted scenario IDs
and normalized statuses. WR-02's original impossible predicate is replaced by
attested evidence classification, but a live-connection denial edge remains
misclassified; see WR-02. No false expiry pass was observed. The real-filesystem
test and manifest assertion also supersede prior IN-01 and IN-03.

Verified:

- **Target and refs.** `BLHAOS_HA_TARGET` must match `media_player.<id>`. Provider and playlist must be distinct `media-source://` refs. Real-play consent is a literal string. The spec asserts `Play on` is empty after each fresh load and that Play is disabled until the target is selected. It then asserts exactly one `media_player.play_media` call, with exactly two data keys and one target key, and zero `resolve` calls.
- **Auth-state paths.** Absolute path, `realpath` canonicalization, case-folded containment, and rejection when any parent holds `.git`. The shared and expiry fixtures are rejected on equal path or equal `dev:ino`. Contents are never read by the validator. Error text never reflects input.
- **Origin.** A bare http(s) origin only, with no credentials, path, query or fragment, and exact origin round-trip.
- **Leak surface.**
  - trace, video and screenshot are `off`, and retries are 0.
  - The reporter maps exact static test titles to fixed scenario IDs, maps
    unknown titles to `unlisted`, and normalizes statuses; it prints no title,
    error, URL or response data.
  - `onStdOut`, `onStdErr` and `onError` are muted.
  - `DEBUG` and `PWDEBUG` hard-fail.
  - The output dir is under the git-ignored `panel_ui/test-results/`.
  - The spec never logs requests, storage, HAR or `page.route`.
- **Shared session.** The spec never logs out, mutates or re-saves state. Expiry uses a separate context and fixture.
- **Expiry evidence.** A distinct external fixture plus explicit owner attestation
  is required. Only the exact HA login path or observed auth rejection can
  qualify, accepted calls and live successful probes defeat expiry, and numeric
  disconnects / permission denials are not expiry. This observes HA rejection;
  it does not cryptographically prove the fixture was formerly valid and has
  expired. The owner must attest that fact.
- **No skip.** A missing environment throws at config load, so there is no skip path. The spec has no `test.skip` or `test.fixme`.
- **Real hass check.** `openPanel` requires `hass.connection.connected`, `hass.user.id`, `hass.config.version === '2026.10.3'` and a non-empty shadow root. The target state, adapter and Bluetooth-address attributes are checked against the panel's `isConnectedTarget`. The audit wrapper forwards the real call and replaces no result.
- **Versions.** `VERSION`, `config.yaml` and the top CHANGELOG entry agree at 0.2.69. The integration manifest is 0.2.19 and is asserted by the package-layout test. Actual provider layout, actual expiry and physical audio remain pending host evidence; no claim is made that they were proven locally.
- **Scope.** The only new dependency is the exactly pinned `@playwright/test` 1.63.0.

## Warnings

### WR-02: Live HTTP auth denials are classified as acceptance (Resolved)

**Current disposition:** resolved by the narrow classifier change and the
`live HTTP auth rejection is denial without a probe error code` regression.
The historical reproduction below describes the pre-fix implementation.

**File:** `modules/integration/panel_ui/e2e/expiry-evidence.mjs:8`
**Issue:** The original self-contradictory predicate has been replaced, but when
`hass.connected === true`, the classifier returns `accepted` unless
`probe.code === 'unauthorized'`. It does not first honor captured
`responses.forbidden` or `responses.unauthorized`.
Pure probes confirmed that both a live 403 and a live HTTP 401 with no probe
code return `accepted`. The current tests cover a live `callWS` unauthorized
code and a 403 with no live connection, but not these response-counter/live-
connection combinations. The host poll therefore waits/fails instead of
reporting denial; this is fail-closed and cannot establish expiry.

**Fix:** after accepted-call/success checks, classify captured 401/403
responses and unauthorized probe codes as `denied` before the live-connection
fallback. Keep successful calls and successful live probes classified as
`accepted`, never `expired`.

## Info

### IN-02: Plain HTTP origins are accepted

**File:** `modules/integration/panel_ui/e2e/host-env.mjs:41-43`
**Issue:** `http:` is allowed for any host. The browser-state tokens could then be sent in clear text to a non-loopback origin. The docs state "HTTP(S)", so this matches the contract, but it is a risk.
**Fix:** Optionally restrict `http:` to loopback or RFC1918 hosts, or document the risk in TESTING.md.

## Verdict

WR-01 and WR-02 are resolved. The bounded local code-review verdict is **clean**,
with IN-02 retained as informational. The host gate remains unresolved: actual
fixture expiry, public provider layout and physical audio still require
authorized host evidence and human review. The attestation is an owner assertion,
not cryptographic proof. No source or test files were changed in this audit;
the final verification report records the independent classifier control matrix.

---

_Reviewed: 2026-10-24T16:51:36Z_
_Reviewer: the agent (gsd-code-reviewer)_
_Depth: standard_
