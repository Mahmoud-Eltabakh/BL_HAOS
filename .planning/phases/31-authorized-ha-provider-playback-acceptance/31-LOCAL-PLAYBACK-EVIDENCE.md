# Authorized local MP3 playback

## Scope and approval

The user explicitly selected playback of their supplied local MP3 on
`media_player.logitech_bt_adapter` and agreed to confirm audible output.
This is a separately scoped local-media observation, not acceptance of the
provider/expiry/playlist requirements or completion of dependent Phase 31.

Host baseline: Core 2026.10.4, bridge 0.2.71, integration 0.2.23.
The existing authorized active browser fixture was used without copying
credentials to the repository.

## Result

- One `media_player.play_media` request was sent using the original reference
  `media-source://media_source/local/5cc9f578195e0.mp3`, type `audio/mpeg`,
  to the exact approved entity. No retries or alternate targets.
- Request accepted at 2026-10-28T23:29:30.743Z; HA reported `playing` at
  2026-10-28T23:29:31.796Z, with duration 182 seconds.
- Volume remained 0.3 (30%); no volume/settings/pairing changes were made.
- The user explicitly confirmed: "I hear the expected audio clearly".
- Playback was not automatically stopped after the observation.

[Machine-readable evidence](evidence/local-mp3-playback-0.2.23.json)

## Remaining gates

This verifies the supplied local media's service/state path plus human-audible
output on one speaker. It does not establish real provider-playlist behavior,
saved custom queue controls, denied/unavailable/expired-session handling,
leakage under those cases, hardware soak, rollback rehearsal or release
go/no-go. T-24-15/T-24-16 and the milestone remain open.

## Follow-up media prerequisites on integration0.2.24

After the user requested continuation, a bounded read-only metadata browse ran
on the new Audio dashboard at2026-10-29T01:28:51.965Z. Root sources included
My media and Radio Browser alongside image/camera/TTS sources. Only local
media folders and Radio Browser metadata were inspected; camera/image sources
were not traversed.

Five nodes were browsed (depth bound2, node bound12, at most40 summarized
children each). The sampled local media folders contained playable items but
no playable playlist metadata. Radio Browser's root had more than40 children
and its summary was truncated; no exhaustive playlist absence is asserted.
Zero playable playlists were found in this bounded sample.

No reference was resolved, no playback was started and no library, settings
or session was changed. A custom local playlist could support queue testing
after explicit create/play/delete approval, but would not substitute for
genuine provider-playlist or expired-session acceptance.

[Bounded metadata report](evidence/media-prerequisites-0.2.24.json)

## Authorized custom queue check blocked by HTTP playlist creation

The user explicitly authorized a temporary two-entry custom playlist using the
previously approved local MP3 twice, on `media_player.logitech_bt_adapter`,
including shuffle/repeat/next/previous, stop and targeted deletion. No volume
change was authorized.

The dashboard's Create playlist action failed before opening its editor. A
follow-up browser check confirmed `window.isSecureContext` was false,
`crypto.randomUUID` was unavailable, and `crypto.getRandomValues` was available.
Clicking the enabled action emitted a TypeError identifying the missing
randomUUID function. This reproduces the previously reported inability to
create playlists, rather than a queue service failure.

Neither attempted run saved a playlist or started playback; the observed
speaker volume was unchanged. No cleanup mutation was necessary. The local
queue report remains a failed acceptance result, not a pass.

A local fix now uses cryptographically secure random bytes to construct UUIDv4
record IDs when randomUUID is unavailable. Verification: 35 targeted
playlist/card unit tests, one browser regression creating two distinct
playlists with randomUUID absent, 12 package/documentation/parity checks,
TypeScript/Vite build and whitespace checks passed. The local candidate has
not been deployed, and the actual queue controls remain untested here.

## Integration0.2.25 deployed and local custom queue controls verified

The user explicitly approved release, commit, push, deployment, one Core
restart without backup, and the previously scoped temporary Logitech test.
Integration commit `fde38f0` was pushed and installed over0.2.24. Core check and
one restart succeeded. Deployed and local bundle SHA256 matched. The bridge
remains0.2.71; no dashboard configuration changes were made.

Live dashboard playlist creation now succeeds over HTTP. The first post-fix
helper run incorrectly waited for a Replace queue dialog even though no active
queue existed. It timed out, stopped playback and removed its temporary
playlist. This harness timeout is not reported as a product launch failure.

After correcting that assumption to match the card's existing launch flow,
the final scoped test at2026-10-29T01:44:23Z passed:

- Created and saved one temporary custom playlist through the real dashboard
  with two entries referencing the approved local MP3.
- Launched that playlist through the card and observed a playing two-item queue.
- Native shuffle_set accepted on/off; entity and queue snapshots matched.
- Native repeat_set accepted all/one/off; entity and queue snapshots matched.
- Next reached item2 and Previous returned to item1, both playing without a
  reported queue error.
- Cleanup stopped playback (idle), deleted only the test playlist, and verified
  all other saved records matched the baseline.
- Volume remained0.08 throughout; no volume change was requested.

This proves local custom queue state/control behavior, not distinct-track
audibility, natural completion/repeat wraparound, genuine provider-playlist
behavior, session expiry, no-queue semantics or hardware reliability.

Validation before deployment: 35 targeted unit tests, one actual-browser
regression, 23 package/compatibility/documentation tests and TypeScript/Vite
build passed. An initial release-check invocation duplicated pytest's plugin
registration; rerunning with the repository's existing plugin setup passed.
No hosted workflow result was returned for the release commit.

[Final queue report](evidence/local-queue-0.2.25-controls.json)

## Authorized idle/no-queue shuffle/repeat gating

The user separately approved shuffle/repeat checks on the idle Logitech entity
without playback. The integration intentionally advertises shuffle/repeat only
when a queue exists. The first helper assumed these requests would succeed;
the second expected a backend No active queue reason. Both assumptions were
incorrect for native HA service validation. Inspection of the existing
supported_features implementation established the intended feature gate.

The corrected negative check verified all five requests (shuffle true/false,
repeat all/one/off) were rejected by native HA with
`service_validation_error` and an unsupported-action reason. None produced
the generic Native playback command failed error. This is expected rejection,
not successful mode setting while idle. The speaker stayed idle, without a
queue or playback, and volume stayed unchanged.

No product changes or deployment were required for this check. It does not
establish backend race-path rejection, provider/expiry behavior or no-queue
UI visibility; only native service gating and unchanged idle state were
observed.

[No-queue feature-gating report](evidence/noqueue-rejection-0.2.25.json)
