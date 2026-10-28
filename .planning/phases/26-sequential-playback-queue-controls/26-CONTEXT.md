# Phase 26: Sequential Playback & Queue Controls - Context

**Gathered:** 2026-10-27
**Status:** Ready for planning
**Mode:** Autonomous defaults selected because the user is unavailable; choices follow the existing HA authentication boundary and project queue ownership decision.

<domain>
## Phase Boundary

Play saved Phase 25 custom playlists and provider shortcuts on one explicitly selected BL-HAOS speaker. The Home Assistant integration remains the media-source resolver and authenticated command gateway; the bridge owns the per-speaker playback process queue. Show active item/playlist state and provide queue controls through the existing ingress dashboard and supported native Home Assistant media-player entity.

This phase covers PL-07, PL-08, PL-09, and PL-10 only. Playlist definitions remain owned by Phase 25. Do not persist queue state across restart, synchronize queues across speakers, add provider SDKs, or claim live provider/physical playback acceptance. Work is authorized for local/mock-only progression. PL-01/02/03 remain production-pending, T-24-15 remains OPEN/HIGH, T-24-16 remains OPEN/MEDIUM, and release/deployment are blocked. Do not access a live host or provider, deploy, restart, or perform physical playback.
</domain>

<decisions>
## Implementation Decisions

### Queue Ownership and Lifecycle
- **D-26-01:** The bridge owns process sequencing and one in-memory queue per speaker. The queue is not restored after Home Assistant/add-on restart and is never synchronized across speakers; a new queue replaces only the active queue for its selected speaker.
- **D-26-02:** Home Assistant resolves every saved reference through its authenticated media-source API before queue start. Resolve the full requested playlist before replacing/starting bridge playback; if any item fails resolution, do not start a partial queue and identify the failed item. Resolved URLs exist only in the authenticated transient command and bridge memory; never persist, publish, or log them.
- **D-26-03:** Starting a saved playlist is initiated from the existing HA-authenticated media panel with exactly one connected target. Keep provider resolution and access inside Home Assistant; the panel does not receive playable URLs.
- **D-26-04:** Treat an existing single-item `media_player.play_media` request as replacement playback: cancel and clear the active queue before playing the one item. Starting another saved playlist also replaces the queue on that speaker.
- **D-26-05:** A bridge queue generation/process identity owns each completion. Ignore completions from a replaced, stopped, disconnected, or otherwise stale generation. Stop and speaker loss cancel queued work and never advance.

### Completion, Failure, and Controls
- **D-26-06:** Automatic advancement occurs only when the current decoder/player pair completes naturally with the bridge's accepted success exit codes. A nonzero/abnormal exit stops advancement, keeps the failed item current, and exposes a bounded failure state; never silently skip.
- **D-26-07:** `Next` is an explicit user-requested skip. `Previous` restarts the current item when its position exceeds three seconds; otherwise it selects the prior item. Neither control hides a failure without the user taking that action.
- **D-26-08:** Shuffle changes the remaining order without changing the currently playing item. Repeat modes are `off`, `one`, and `all`; repeat-one restarts the current item after successful natural completion, and repeat-all wraps at the end. Defaults are shuffle off and repeat off.
- **D-26-09:** Expose truthful current playlist, item, position/duration where available, queue length/index, shuffle/repeat mode, and error/completion status. `Play` resumes a paused current item or explicitly retries the current failed item; `Pause` and `Stop` retain their standard meanings.

### UI and Authentication Boundaries
- **D-26-10:** The HA-authenticated Library panel starts a saved playlist on the explicitly selected speaker and displays its current queue. The add-on ingress SpeakerCard mirrors active queue state and controls; both it and native HA media-player controls call the same bridge-owned queue. Do not add a second queue implementation in the browser.
- **D-26-11:** Extend only supported existing APIs and WebSocket/event paths. Ingress uses its existing protected add-on API path; the HA integration uses its existing bearer-authenticated native bridge client. Never pass the native bearer to browser code or expose resolved URLs in queue snapshots/events.
- **D-26-12:** Advertise native `NEXT_TRACK`, `PREVIOUS_TRACK`, `SHUFFLE_SET`, and `REPEAT_SET` features only when the bridge queue contract is available, alongside current play/pause/stop controls. All controls operate on the same queue session as ingress.
- **D-26-13:** Queue and player errors use bounded status copy. Resolution failure occurs before queue replacement; process failure retains the failed item; no automatic retry, auto-skip, or alternate speaker occurs.
- **D-26-14:** A saved provider shortcut remains one atomic queue item. Home Assistant resolves the exact opaque provider playlist reference as one media-source item; provider-internal tracks are HA-owned and are not expanded into BL-HAOS queue entries. Queue index/next/previous operate on custom playlist references and the saved-library item sequence, not a provider's internal list. Custom playlist entries use their already saved order.
- **D-26-15:** Keep normalized speaker address as the primary queue key, but promote the per-speaker playback value from one active process pair to a generation-fenced playback session that owns the current item, remaining queue, modes, and completion reason. The decoder/player pair remains one child owned by the session, not the queue identity itself.

### Claude's Discretion
- Select the exact bridge request/response fields, queue-state version, and native event representation after inspecting current API compatibility and test patterns.
- Choose concise queue labels, empty/completed state copy, and accessible control grouping consistent with the existing Neumorphic ingress and HA panel.
- Use deterministic fake process and mock-HA seams; do not install dependencies unless an existing requirement proves insufficient.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `modules/integration/custom_components/bl_haos/media_player.py` already resolves HA `media-source://` IDs through `async_resolve_media`, submits one playable item to the selected speaker, and exposes play/pause/stop/volume/browse features.
- `modules/integration/custom_components/bl_haos/client.py` owns the authenticated native REST command and WebSocket speaker cache/update listener.
- `modules/integration/custom_components/bl_haos/playlist_library.py` owns the installation-wide HA Store with ordered custom entries and provider shortcut records.
- `modules/bridge/backend/bl_haos/ha/player.py` owns one process pair per speaker, serializes player commands per address, reports timelines, and watches decoder/player process exits.
- `modules/bridge/backend/bl_haos/api/routes.py` validates authenticated native commands and returns the post-command speaker record; `main.py` publishes playback updates to ingress and native clients.
- `modules/bridge/web_ui/src/components/SpeakerCard.tsx`, `web_ui/src/api/client.ts`, and `web_ui/src/hooks/useBluetoothEvents.ts` provide the existing ingress device display, protected API calls, and live playback updates.

### Established Patterns
- Home Assistant owns provider authentication/resolution; the bridge accepts only bounded playable URLs from the native integration and does not receive playlist credentials.
- Bridge process identity is checked before cleanup/completion, and stale process watchers must not mutate replacement playback.
- Native API command payloads are versioned, bounded, authenticated, and redacted. Ingress REST/API results and WebSocket events must remain bounded and omit stream URLs.
- Phase 25 stored records are durable, but queue execution state is explicitly transient; add-on/Core restarts do not resume playback.

### Integration Points
- Saved-playlist start: existing `BLHAOSMediaPlayer.async_play_media` / HA media-panel action, library Store lookup, `async_resolve_media`, then one authenticated queue-start command to the bridge.
- Sequential process lifecycle: `MediaPlayerBridge.execute` / `play_url` / `_watch_processes` and its playback state callback.
- Queue controls: versioned native command route plus ingress API commands; native entity methods map HA media-player controls to the same bridge operations.
- State display: `playback_envelope`, `native_speaker_record`, `BLHAOSClient._async_listen`, and the ingress playback-updated event.
</code_context>

<specifics>
## Specific Ideas

- Keep exact library order and local display labels; show which item is current and which item failed.
- Do not persist queue URLs or active process state. Restart ends the queue with a truthful stopped/unavailable state rather than attempting resume.
- Use the existing speaker entity/control surfaces, not a synchronized multi-room queue or a parallel browser-only transport.
</specifics>

<deferred>
## Deferred Ideas

- Queue restoration across restart (PL-12) and synchronized multi-speaker queues (PL-13).
- Live Home Assistant/provider acceptance, deployment, actual audible playback, and release approval; these remain separately gated.
- New provider integrations, raw URL imports, automatic skip/retry, and queue persistence.

</deferred>

---

*Phase: 26-sequential-playback-queue-controls*
*Context gathered: 2026-10-27*
