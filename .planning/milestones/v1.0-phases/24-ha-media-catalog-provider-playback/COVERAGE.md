# Phase 24 API Capability Coverage

The deterministic detector returned `detected: true` for the roadmap Phase 24 section plus generated plan bodies. This matrix applies full coverage first, then explicitly subtracts only user-locked exclusions and actions assigned to Phases 25/26.

| capability | decision | reason |
|---|---|---|
| Core custom panel module registration | INTEGRATE | Register one integration-owned custom element through panel_custom.async_register_panel. |
| Core integration static module serving | INTEGRATE | Serve one deterministic packaged bundle through hass.http.async_register_static_paths. |
| Injected Home Assistant session access | INTEGRATE | Use only the current Core-supplied hass object and fail closed when access expires or is denied. |
| Home Assistant media source root browse | INTEGRATE | Browse supported source roots through authenticated hass.callWS. |
| Home Assistant media source child browse | INTEGRATE | Preserve and navigate provider hierarchy through authenticated hass.callWS. |
| Home Assistant advertised media search | INTEGRATE | Expose search only when the current HA source advertises can_search. |
| BrowseMedia metadata and capabilities | INTEGRATE | Preserve titles, thumbnails, opaque IDs, media type/class, can_play, can_expand, and can_search. |
| Connected BL-HAOS entity discovery | INTEGRATE | Derive available targets from current HA entity state for explicit selection. |
| Native media player play_media service | INTEGRATE | Submit the original opaque ID and type through hass.callService. |
| Exactly one explicit service target | INTEGRATE | Target one user-selected connected BL-HAOS media_player entity. |
| Entity-side media source resolution | INTEGRATE | Resolve the opaque reference inside the selected native entity through Home Assistant. |
| Denied and expired session handling | INTEGRATE | Surface bounded reconnect or permission errors with no alternate authentication path. |
| Unavailable and unresolvable media handling | INTEGRATE | Preserve the selected reference and report failure without fallback, skip, or automatic retry. |
| Target Core panel lifecycle validation | INTEGRATE | Validate registration, serving, injected calls, unload, and partial failure on user-approved Core 2026.10.3. Local 24-test SIL passed; Task 24-01-02 host gate remains pending. |
| Browser-side media source resolution | OPT-OUT | Exposes resolved URLs to browser state and violates the HA-owned late-resolution boundary. |
| Browser or add-on HA token storage | OPT-OUT | The current injected HA session is the only approved authentication authority. |
| Bridge media catalog or provider endpoints | OPT-OUT | The bridge is not a catalog proxy and must not receive HA or provider credentials. |
| Direct provider API or SDK operations | OPT-OUT | Home Assistant owns provider authentication, catalog behavior, and reference resolution. |
| Raw provider URL playback fallback | OPT-OUT | Phase 24 preserves opaque HA references and fails closed when HA cannot resolve them. |
| Implicit or multi-speaker targeting | OPT-OUT | Phase 24 requires exactly one explicitly selected connected entity. |
| Saved playlist create read update delete | OPT-OUT | Saved playlist management is explicitly assigned to Phase 25. |
| Save provider playlist reference | OPT-OUT | Persisted provider references and playlist library behavior are assigned to Phase 25. |
| Queue inspection and transport controls | OPT-OUT | Previous, next, shuffle, repeat, queue state, and advancement are assigned to Phase 26. |
| Automatic retry skip or next-item action | OPT-OUT | Phase 24 preserves visible failure and never advances or substitutes media automatically. |