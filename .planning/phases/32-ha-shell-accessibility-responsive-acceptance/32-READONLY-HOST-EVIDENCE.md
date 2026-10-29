# Read-only HA-shell evidence

Captured on 2026-10-28 on the authorized host 192.168.1.18
(individual run timestamps are in the JSON reports),
Core 2026.10.4. Deployed baseline: bridge 0.2.71, integration 0.2.22.

## Scope and method

The user explicitly approved read-only native-panel inspection using an active
Playwright session stored outside Git. A local Chromium browser opened the real
`/bl-haos-media` panel and navigated Library, Browse media and Speakers. No
playback, scan, pairing, settings save or session revocation was requested.
The browser was closed after capture; the active fixture was not overwritten.
Input fields were masked in screenshots.

These are partial supporting observations, not execution or completion of
dependent Phase 32, acceptance of Phase 30, or release approval.

## Measurements

| View | Widths (height 900 px) | HA connected | Horizontal panel fit | Visible controls without detected names | Broken images |
|---|---|---|---|---|---|
| Library | 375, 768, 1440 | Yes | Yes | 0 | 0 |
| Browse media | 375, 768, 1440 | Yes | Yes | 0 | 8 at each width |
| Speakers | 375, 768, 1440 | Yes | Yes | 0 | 0 |

No document-level horizontal overflow or overflowing non-scrollable
section/div/main container was detected by the bounded DOM checks. These checks
do not establish full responsive or accessibility conformance.
The approved target `media_player.logitech_bt_adapter` existed and reported
`idle`; no audible playback was attempted.

The bounded visible-text credential-pattern check matched nothing. It did not
inspect authenticated network payloads or establish provider-session leakage
closure.

## Observed gap

Browse media renders eight failed images (`complete` with `naturalWidth === 0`)
at each viewport width. Broken thumbnails are visible in the screenshots.
Subsequent inspection identified same-origin `/api/brands/` requests returning
403: the deployed panel used plain image requests, whereas HA requires
authentication for these assets. Do not treat the deployed image rendering or
the complete UI acceptance gate as passed.

## Evidence

- [Machine-readable measurements](evidence/ha-shell-readonly.json)
- Library: [375](evidence/ha-shell-library-375.png),
  [768](evidence/ha-shell-library-768.png),
  [1440](evidence/ha-shell-library-1440.png)
- Browse media: [375](evidence/ha-shell-browse-media-375.png),
  [768](evidence/ha-shell-browse-media-768.png),
  [1440](evidence/ha-shell-browse-media-1440.png)
- Speakers: [375](evidence/ha-shell-speakers-375.png),
  [768](evidence/ha-shell-speakers-768.png),
  [1440](evidence/ha-shell-speakers-1440.png)

## Thumbnail remediation: local candidate verified in the real HA shell

The user requested investigation and repair of the failed artwork. The panel
now uses injected `hass.fetchWithAuth` for validated same-origin paths, rejects
redirects and non-image/error responses, and renders temporary blob URLs.
Requests are aborted and blob URLs revoked when their owner/session changes
or the component unmounts. Failures are explicitly labelled **Artwork
unavailable**; no unauthenticated retry or external-provider fallback is made.

Verification:

- Panel Vitest: 83 passed, including authenticated loading, HTTP denial,
  network/invalid-image failures, image decode failure, cleanup, stale-session
  isolation, missing-helper behavior and existing unsafe-path rejection.
- TypeScript and production panel build passed.
- Package-layout suite including fresh source-to-bundle parity: 12 passed.
- On the real Core 2026.10.4 shell, a local Playwright route override supplied
  the rebuilt module to this browser only. One candidate-module request was
  intercepted. No server files or configuration were changed.
- All eight catalog thumbnails decoded at each of 375, 768 and 1440 px:
  eight blob-backed images, zero broken images, zero unavailable-artwork
  indicators. Recorded image/brands responses were all 200.
- Lazy-loaded images were scrolled into view to verify decoding, then the
  catalog was returned to the top for screenshots.

Candidate evidence (not deployed-host acceptance):

- [Measurements](evidence/thumbnail-candidate/ha-shell-readonly.json)
- Browse media [375](evidence/thumbnail-candidate/ha-shell-browse-media-375.png),
  [768](evidence/thumbnail-candidate/ha-shell-browse-media-768.png),
  [1440](evidence/thumbnail-candidate/ha-shell-browse-media-1440.png)

This candidate validation preceded the approved 0.2.23 deployment below.

## Integration 0.2.23 deployment and live verification

The user explicitly approved committing, pushing and deploying the fix.
Integration commit `1d3ef97` was pushed to main.

The initial deployment precondition found 0.2.19 on disk and a missing bundle,
instead of the previously observed 0.2.22. No cause was established. Deployment
stopped before extraction or restart; the user then explicitly instructed
"do not back up deploy only". No new backup was created.

The committed package was deployed from a tracked-file Git archive. HA Core
configuration validation and restart both succeeded. The installed manifest
then reported 0.2.23; bridge 0.2.71 remained started.

Archive/deployed bundle SHA256:
`913395cc6db01df450b9c592a634ec6c9a2dd03f8c12dc1933c1c777b680403b`.
The archive applied CRLF conversion; its JavaScript was verified identical to
the committed bundle after line-ending normalization.

At 2026-10-28T23:19:22.849Z the browser repeated the actual-shell checks with
**no module interception or candidate override**. All eight thumbnails decoded
at each required width (375, 768, 1440), all eight used blob image URLs, and
there were zero broken images or unavailable-artwork indicators. The recorded
image/brands responses were all 200. Nine fresh screenshots cover Library,
Browse media and Speakers. Playback and settings were not exercised.

- [Deployed measurements](evidence/thumbnail-deployed-0.2.23/ha-shell-readonly.json)
- Deployed browse media:
  [375](evidence/thumbnail-deployed-0.2.23/ha-shell-browse-media-375.png),
  [768](evidence/thumbnail-deployed-0.2.23/ha-shell-browse-media-768.png),
  [1440](evidence/thumbnail-deployed-0.2.23/ha-shell-browse-media-1440.png)

The thumbnail gap is resolved on the deployed host. This does not close
T-24-15/T-24-16 or establish full accessibility/release acceptance. Live
screenshots and detailed reports are retained locally rather than published
with the code change.

## Read-only keyboard and accessibility follow-up

The user explicitly requested further read-only checks of deployed 0.2.23.
The [accessibility measurements](evidence/accessibility-0.2.23/accessibility-readonly.json)
record the latest run timestamp and full observations.

| Sample | Widths | Result |
|---|---|---|
| Accessible-name DOM checks | 375, 768, 1440 | Zero unnamed sampled controls in Library, Browse media and Speakers |
| Effective target geometry | 375, 768, 1440 | Zero targets below 44 by 44 px when native associated labels are included |
| Text contrast | 375, 768, 1440 | Zero measured failures; 15 Library, 24 Browse and 63 Speakers text samples per width, zero unmeasured samples in this run |
| Reduced-motion preference | 375, 768, 1440 | Preference active; zero remaining nonzero-duration transitions or animations in sampled visible DOM |
| Tab traversal and focus outline | 375, 768, 1440 | Library 7/7, Browse 13/13, Speakers 33/33 controls reached at every width; zero missing visible outlines, off-viewport focused controls or unreachable sampled controls |

Contrast checks used 4.5:1 for normal text and 3:1 for qualifying large text,
compositing solid background colors through the HA/shadow-DOM ancestors.
The checker excludes opacity/gradient layers rather than treating them as
passes; none of the final samples were excluded.

Three checkbox inputs measured 13 by 44 px, but their native associated labels
provided targets at least 44 by 44 px (50 px high in the desktop sample).
These narrow input boxes are not recorded as target-size failures.

Only Tab navigation and computed focus outlines were checked. No playback,
scan, pairing, form editing, settings save or session mutation was performed.
Real screen-reader output, live error announcements, physical mobile-device
behavior, activation of state-changing controls, provider-content layouts
and full human accessibility acceptance remain unverified.

## Still required

- A separate genuine disposable expired-session fixture and read-only rejection
  evidence; none was supplied.
- Distinct real provider and playable-playlist references and their authorized
  positive/negative cases; the supplied local MP3 is not provider acceptance.
- Provider/playlist audible playback and active-queue shuffle/repeat and
  no-queue acceptance. Separately authorized local MP3 output was confirmed
  audible by the user; see
  [the Phase 31 local playback report](../31-authorized-ha-provider-playback-acceptance/31-LOCAL-PLAYBACK-EVIDENCE.md).
- Physical mobile-device behavior, real screen-reader announcements, dynamic error
  states and full human accessibility acceptance beyond the bounded checks
  above.
- Scoped reconnect/hardware soak, rollback rehearsal and reviewed go/no-go.

T-24-15 and T-24-16 remain open. No milestone is complete.
