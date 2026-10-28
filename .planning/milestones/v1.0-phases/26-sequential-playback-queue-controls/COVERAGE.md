# API Coverage - Playback Queue

> Full queue/control coverage by default. Local-only exclusions are explicit; this matrix is not production acceptance.

| capability | decision | reason | local evidence / boundary |
|---|---|---|---|
| HA-owned library lookup for custom records | INTEGRATE | Required to load the authoritative ordered references before queue start. | Pinned SIL `test_custom_playlist_start_resolves_every_reference_before_one_queue_command`; authenticated handler loads `PlaylistLibrary.async_list()`. |
| HA media-source resolution for each custom reference | INTEGRATE | Home Assistant remains the authentication and provider-resolution boundary. | Pinned SIL ordered-resolution, target-loss, resolver-failure tests in `test_playlist_library_sil.py`. |
| HA media-source resolution for a provider shortcut | INTEGRATE | Resolve its one opaque reference as one atomic queue item; provider-internal tracks are not expanded. | Pinned SIL `test_provider_shortcut_starts_as_one_atomic_queue_item`; mock queue acceptance checks one item. |
| All-or-nothing queue start after complete resolution | INTEGRATE | Resolution failure must not partially replace an existing queue. | Pinned SIL failure/payload-bound tests; panel Vitest and mock Playwright confirm prior snapshot retention. |
| Bridge per-speaker queue start and process ownership | INTEGRATE | The bridge owns decoder/player processes and sequencing. | Bridge `test_media_player.py -k queue`; per-address process/session ownership and fencing. |
| Natural-success automatic advancement | INTEGRATE | Advance only after both current item processes complete with the explicit success contract. | Bridge `test_media_player.py -k queue`; local mock browser advances only on explicit successful completion. |
| Queue state snapshot and native speaker publication | INTEGRATE | HA entities need active item, timeline, queue index/count, mode, and bounded status. | Bridge `test_api.py` and `test_native_transport.py -k queue`; integration snapshot mapping SIL. |
| Ingress playback update event and queue controls | INTEGRATE | Ingress displays and controls the same bridge-owned queue. | Ingress client/event/SpeakerCard Vitest queue selectors; local mock snapshot/failure/disconnect scenarios. |
| Native Home Assistant play, pause, stop, next, previous | INTEGRATE | Required native controls map to the same per-speaker queue session. | Pinned SIL `test_native_queue_controls_are_capability_gated_and_use_shared_snapshot`. |
| Shuffle and repeat off/one/all | INTEGRATE | Required user controls with deterministic queue semantics. | Pinned SIL native controls plus ingress queue API and SpeakerCard Vitest. |
| Failure, cancellation, stale-generation, and disconnect outcomes | INTEGRATE | Required to prevent silent skips or stale advancement. | Bridge queue lifecycle tests; pinned resolver/disconnect SIL; panel and mock failure/disconnect tests. |
| Automatic retry or silent skip after a failed item | OPT-OUT | Explicitly prohibited; recovery must be user initiated. | Explicit assertions: queue start/next/previous are one attempt; failed-item tests require a user command to skip/retry. |
| Provider-specific SDK/API clients or credential storage | OPT-OUT | Home Assistant owns provider authentication and resolution. | Playlist-library and panel tests use HA media-source references only; no provider SDK or credentials are added. |
| Browser-owned queue sequencing or resolved URL state | OPT-OUT | Queue lifecycle belongs to the bridge; URLs never enter browser state. | Panel identity-only callWS tests, ingress snapshot sanitizer tests, and mock URL-free snapshot checks. |
| Queue restore after restart (PL-12) | OPT-OUT | Explicitly deferred; queue/process state remains in memory. | Bridge queue-session lifecycle tests; docs state queues do not resume after restart. |
| Multi-speaker synchronized queues (PL-13) | OPT-OUT | Explicitly out of scope for this selected-speaker phase. | No synchronization implementation or test; every start/control is scoped to one explicit speaker. |
| Live provider, physical speaker, deployment, release acceptance | OPT-OUT | Current authorization is local/mock-only; production acceptance remains a separate gate. | No live host/provider, deployment, restart, or physical playback was performed; see Phase 26 verification residuals. |
