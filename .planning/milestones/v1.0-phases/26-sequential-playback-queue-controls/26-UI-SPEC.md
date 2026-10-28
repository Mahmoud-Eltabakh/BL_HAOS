---
phase: "26"
slug: "sequential-playback-queue-controls"
status: draft
shadcn_initialized: false
preset: none
created: "2026-10-27"
---

# Phase 26 — UI Design Contract

> Visual and interaction contract for Sequential Playback & Queue Controls. Preserve the existing HA-authenticated Library panel and the ingress SpeakerCard. This contract covers PL-07, PL-08, PL-09, and PL-10 only. Local/mock evidence is not production acceptance.

---

## Design System

| Property | Value |
|----------|-------|
| Tool | none; retain the existing manually-authored Neumorphic styles |
| Preset | not applicable; no shadcn configuration or package |
| Component library | none; React with semantic HTML controls |
| Icon library | Existing `lucide-react`; use the installed version without upgrading |
| Font | Existing panel `ui-sans-serif, sans-serif` stack; no new font |

Keep the dark, restrained Neumorphic surface language in both existing frontends. In the HA panel, reuse `neu-page`, `neu-surface`, `neu-inset`, `neu-button`, and the existing focus-visible outline. In ingress, reuse the existing Neumorphic card, inset well, button, and status styles. Keep queue content within the existing surfaces; do not add a component library, decorative gradients, nested cards, or a separate browser playback subsystem.

Use Lucide icons for transport and mode controls. Icon-only controls must have a visible tooltip and an accessible name; use semantic buttons, a labelled native select for repeat mode, and a labelled toggle for shuffle. Status meaning must never rely on icon or color alone.

---

## Spacing Scale

Declared values (multiples of 4):

| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px | Icon and compact metadata gaps |
| sm | 8px | Control-group and row-action gaps |
| md | 16px | Queue surface padding and default control spacing |
| lg | 24px | Page padding on narrow screens and section separation |
| xl | 32px | Major layout gaps |
| 2xl | 48px | Empty-state separation |
| 3xl | 64px | Page-level separation only |

Exceptions: Every interactive target is at least 44px high/wide, including transport buttons, shuffle/repeat controls, target selection, dialog actions, and icon-only buttons. Keep the four transport controls in a stable row when they fit; allow them to wrap without overlap on narrow screens. Use 24px page padding at 375px.

---

## Typography

Use exactly four sizes and two weights, matching the existing panel contract.

| Role | Size | Weight | Line Height |
|------|------|--------|-------------|
| Status and metadata | 12px | 400 | 1.5 |
| Body, controls, and item title | 14px | 400 | 1.5 |
| Section heading and selected mode | 16px | 600 | 1.2 |
| Page heading | 24px | 600 | 1.2 |

---

## Color

| Role | Value | Usage |
|------|-------|-------|
| Dominant (60%) | `#151a23` | Page background and unframed space |
| Secondary (30%) | `#242d3b` | Existing Library and speaker surfaces |
| Accent (10%) | `#3b82f6` | Primary `Play playlist` action, selected target, and selected shuffle/repeat mode only |
| Destructive | Existing rose semantic (`#e11d48` family) | Playback failure/unavailable messaging and the explicit `Stop` action only |

Accent reserved for: the primary `Play playlist` action, the selected connected target, and selected mode states. Do not recolor every transport button blue. Reuse semantic emerald for connected/playing, amber for pending, rose for failed/disconnected, and cyan `#67e8f9` for the existing focus-visible outline. Pair every semantic color with visible text or an accessible label. Preserve audited text contrast on raised and inset surfaces.

---

## Playback and Queue Contract

### HA Library launch

- Add an explicit `Play on` connected-target selector to the existing Library view. Start with no target selected; never silently choose the first speaker or switch targets. List only currently connected BL-HAOS `media_player` entities. If none are connected, show the unavailable state and disable launch actions.
- Show a `Play playlist` action on each saved custom playlist and provider shortcut. The selected speaker is visible beside the action. Recheck that exact target is connected at submit time; do not fall back to another speaker.
- Launch sends only the saved record identity and selected entity identity through the existing authenticated HA panel connection. Home Assistant resolves every saved reference and submits the queue to the bridge. The panel must not receive, store, render, or log resolved playback URLs. Do not expose the native bearer or provider credentials to browser code.
- A custom playlist starts in its saved order. A provider shortcut remains one opaque, atomic HA-owned media item; Home Assistant resolves/streams its provider-owned contents. Do not expand provider tracks or imply that queue Next/Previous addresses the provider's internal track list.
- When the target already has an active queue, require a native `<dialog>` confirmation before replacement. Name the playlist and target, explain that the current queue on that target will stop, provide `Keep current queue` and `Replace queue`, and focus `Keep current queue` by default. Escape cancels. Restore focus to the invoking `Play playlist` button. If resolution or target validation fails after confirmation, retain the old queue and report the bounded error.
- Keep queue state transient. Do not persist it in browser storage, local storage, URL/query state, or the playlist library. Reopening the panel renders the latest bridge snapshot only; it does not reconstruct a queue from browser state.

### Shared bridge snapshot and display

- Render one bridge-owned, per-speaker queue snapshot in both the Library panel and the matching ingress `SpeakerCard`. The ingress card is already the explicit speaker target. Both surfaces send commands to the existing protected path for their context and render the same authoritative queue result/event; neither computes order, advances tracks, nor owns a second queue.
- The URL-free display snapshot contains only allowlisted display fields: playlist label, current item title and optional artist, position and duration when available, one-based current index and total count, shuffle state, repeat mode (`off`, `one`, `all`), player/queue status, and bounded error text. Do not include playback URLs, signed query values, media-source IDs, provider credentials, raw exception text, or the native bearer. Do not log request/response bodies containing transient resolved URLs.
- Show the current playlist and item title as primary information, with `Item {index} of {count}`, optional artist, and an accessible timeline. Show time as `mm:ss` when known; show `Time unavailable` when position/duration is unknown instead of inventing a value. The timeline is read-only and must not imply seek support. Announce snapshot changes through one polite, atomic status region; expose actionable failures with an alert.
- Keep the ordinary HA media-player state projection (`playing`, `paused`, `idle`, or `off`) separate from the queue lifecycle status. Native HA queue controls appear only when the bridge queue capability is available; they operate on the same queue and use Home Assistant's standard media-player control surface.

### Controls and per-context semantics

- Group ingress controls as `Previous`, `Play` or `Pause`, `Next`, and `Stop`; use Lucide icons with accessible names and tooltips. `Play` resumes a paused item or explicitly retries the current failed item. `Pause` pauses without changing the queue. `Stop` cancels and clears queued work on this speaker; it does not require an extra confirmation.
- `Next` is always an explicit user skip, including when the current item failed; it never occurs automatically on failure. With repeat off at the final item, disable `Next`. With repeat all, `Next` wraps to the first item. The queue's automatic advancement is only shown after successful natural completion.
- `Previous` restarts the current item when position is greater than three seconds. At or below three seconds, it selects the prior item. At the first item, restart that item; do not wrap backward. Disable `Previous` only when there is no current item.
- Shuffle is a two-state toggle, default off. Enabling it never moves the current item; it changes only the remaining order. Repeat is a labelled three-option control (`Off`, `One`, `All`), default Off. Repeat One restarts the current item after successful natural completion; Repeat All wraps after the final item. Failure never auto-retries or auto-skips in any mode.
- Disable duplicate playback commands while an action is pending and show the pending label. Keep the last confirmed snapshot visible; do not optimistically change the current item, index, mode, or queue order. Reconcile from the next bridge snapshot/event. Queue start, Next, and Previous are single user actions; a transport error must not trigger an automatic retry.
- When a queue is replaced, the old queue remains visible until the bridge accepts the replacement. On successful acceptance, render the new bridge snapshot. On rejection, keep the old snapshot. A stop, replacement, or speaker loss invalidates the old queue; late process completion must not appear as a new item in either UI.

---

## Copywriting Contract

| Element | Copy |
|---------|------|
| Primary CTA | `Play playlist` |
| Target selector | Label: `Play on`; empty option: `Select a connected speaker` |
| Empty queue heading | `No active queue` |
| Empty queue body | `Choose a saved playlist in Library and select a connected speaker to start playback.` |
| No connected target | `No connected speakers are available. Connect a speaker, then select it to play a playlist.` |
| Pending launch | `Preparing “{playlist name}” for {speaker name}…` |
| Pending control | `Sending {action}…` |
| Empty playlist | `This playlist has no items to play.` |
| Resolution error | `Couldn't prepare “{playlist name}”. “{item title}” could not be resolved. The current queue was not changed. Check Home Assistant access and try again.` |
| Playback error | `Playback failed for “{item title}”. Nothing was skipped. Select Play to retry or Next to skip this item.` |
| Completed | `Playlist complete` |
| Disconnected | `Speaker disconnected. The queue was stopped. Select a connected speaker to start a playlist.` |
| Replacement confirmation | `Replace queue: Stop the current queue on {speaker name} and play “{playlist name}”?` Actions: `Keep current queue` / `Replace queue`. Default focus: `Keep current queue`. |
| Replacement error | `Couldn't start “{playlist name}” on {speaker name}. The current queue is unchanged. Check the speaker connection and Home Assistant access, then try again.` |
| Error recovery | Retry only through the explicit `Play` action for the failed current item, or an explicit new `Play playlist` action. Never show a generic retry that may duplicate a queue command. |

Use bounded, user-safe errors only. Do not interpolate raw bridge/provider exceptions, media URLs, URL query values, or credential data into visible or assistive text.

---

## UI Considerations

Applicable state considerations resolved: 19 covered, 7 backstop, 0 unresolved. Apply held-out/mock rendering assertions at 375px, 768px, and 1440px for each backstop; these are local UI evidence only.

| Category | Element(s) | Status | Resolution / Reason |
|----------|------------|--------|---------------------|
| empty | Library playlist launcher | ✅ covered | Preserve the Phase 25 empty-library copy and show no playable action for a zero-item playlist. |
| loading | Library playlist launcher | ✅ covered | Show `Preparing “{playlist name}”…`; disable duplicate launch and keep the last confirmed queue visible. |
| error | Library playlist launcher | ✅ covered | Show the bounded resolution/replacement error and state explicitly that the existing queue was not changed. |
| populated | Library playlist launcher | ✅ covered | Keep the Phase 25 scannable playlist rows and attach `Play playlist` to each saved record. |
| partial | Library playlist launcher | ✅ covered | Identify an unavailable reference without hiding other library rows; a launch that cannot fully resolve fails before queue replacement. |
| overflow | Library playlist launcher | 🧪 backstop | Allow vertical scrolling and wrap row labels/actions without horizontal page overflow at all required widths. |
| zero-one-many | Library playlist launcher | ✅ covered | Keep row geometry stable; zero uses the empty copy, one is a normal row, and many remain a scannable list. |
| long-text | Playlist and target labels | 🧪 backstop | Wrap long names in rows and selectors; retain complete accessible names and do not clip the launch action. |
| empty | Connected-target selector | ✅ covered | Show `Select a connected speaker`; with no connected targets, disable launch and show the no-target copy. |
| error | Connected-target selector | ✅ covered | If the chosen entity disconnects, mark it unavailable, disable controls, and never substitute another target. |
| empty | Queue summary | ✅ covered | Show `No active queue` and the Library next step; do not imply queue state is persisted or resumable. |
| loading | Queue summary | ✅ covered | Keep the last confirmed snapshot and expose pending status while HA resolves or a bridge command is in flight. |
| error | Queue summary | ✅ covered | Keep the failed item current with bounded error copy; announce it as an alert and offer only explicit user recovery. |
| populated | Queue summary | ✅ covered | Show playlist, current title, timeline when known, item index/count, shuffle/repeat modes, and status from the bridge snapshot. |
| partial | Queue summary | ✅ covered | Missing artist or timing is omitted or labelled unavailable; do not fabricate metadata or clear valid queue fields. |
| overflow | Queue summary | 🧪 backstop | Keep summary and controls reachable in a vertically scrollable surface; prevent fixed-width timeline or title overflow. |
| zero-one-many | Queue summary | ✅ covered | One-item queues show `Item 1 of 1`; multi-item counts remain stable; empty uses the dedicated no-queue state. |
| long-text | Current title and playlist label | 🧪 backstop | Wrap or safely reflow long titles and labels without obscuring timeline, status, or controls. |
| loading | Playback controls | ✅ covered | Prevent duplicate commands, expose `Sending {action}…`, and retain the authoritative snapshot until confirmation. |
| error | Playback controls | ✅ covered | Keep command failure distinct from item failure; never report success or advance optimistically. |
| long-text | Control names and status | 🧪 backstop | Keep visible labels concise; full action names remain available to assistive technology and tooltips. |
| loading | Queue replacement dialog | ✅ covered | Disable duplicate confirmation while the replacement is pending and preserve the existing queue until bridge acceptance. |
| error | Queue replacement dialog | ✅ covered | Keep the dialog context and old queue on failure; show the bounded recovery path without raw errors. |
| overflow | Queue replacement dialog | 🧪 backstop | Constrain long confirmation content to a scrollable native dialog while both actions remain reachable. |
| long-text | Queue replacement dialog | 🧪 backstop | Wrap long playlist and speaker names without clipping the target identity or confirmation actions. |
| error | Disconnected speaker state | ✅ covered | Show `Speaker disconnected. The queue was stopped.`; disable transport and mode controls and require a new explicit target selection. |

Accessibility contract: use semantic buttons and labelled controls, logical tab order, keyboard activation, visible `:focus-visible` outlines, and a polite atomic live region for pending/current-item/mode changes. Use an alert for resolution and playback failures. Use native dialog semantics with a labelled heading, described consequence, Escape cancellation, initial focus on `Keep current queue`, focus containment, and focus restoration. Do not add global keyboard shortcuts. Keep every target at least 44px and honor `prefers-reduced-motion` using the existing style behavior.

Responsive contract: at 375px, stack the target selector, queue metadata, timeline, and mode controls without horizontal scrolling; keep transport controls at 44px minimum and wrap only when needed. At 768px, preserve a compact single-column queue surface with readable metadata. At 1440px, constrain content to the existing page width and keep the Library launcher and queue summary scannable. Do not scale font sizes with viewport width.

---

## Registry Safety

| Registry | Blocks Used | Safety Gate |
|----------|-------------|-------------|
| none | none | not applicable; no shadcn or third-party registry is used |

---

## Phase Boundary and Verification

- This contract covers only local/mock UI behavior for PL-07 through PL-10 in the existing authenticated HA Library panel, ingress `SpeakerCard`, and supported native Home Assistant media-player controls.
- The bridge owns one transient queue per speaker and publishes the authoritative URL-free queue snapshot. The browser never owns the queue order or advancement, persists queue state, or receives resolved playback URLs. HA remains the resolver/authentication boundary; provider credentials and the native bearer never enter browser code.
- Use deterministic mock HA/API/WebSocket evidence only. Test URL non-disclosure with sentinel URL/query values; assert that no resolved URL, credential, or raw exception appears in rendered text, panel/client state exposed to UI, browser storage, or queue events. Validate launch, replacement, resolution failure, item failure, completion, disconnect, repeat/shuffle, and control semantics at 375px, 768px, and 1440px.
- Phase 25 verification passed 69/69 must-haves for its authorized local/mock scope and did not verify Phase 26 sequential playback. Phase 25 queue-metadata-only verification is not production acceptance. Mock evidence does not establish a live HA/provider session, actual session expiry, HA-shell behavior, physical audio, or release readiness.
- T-24-15 remains OPEN/HIGH and T-24-16 remains OPEN/MEDIUM. The temporary `security_block_on: critical` threshold is local-only, is not risk acceptance, and must be restored to `high` before live verification, publication, or deployment. Release and deployment remain blocked.
- Do not access live Home Assistant or provider services, deploy, restart, perform physical playback, change context/state/roadmap, stage files, or create commits as part of this phase UI contract.

---

## Checker Sign-Off

- [x] Dimension 1 Copywriting: PASS
- [x] Dimension 2 Visuals: PASS
- [x] Dimension 3 Color: PASS
- [x] Dimension 4 Typography: PASS
- [x] Dimension 5 Spacing: PASS
- [x] Dimension 6 Registry Safety: PASS
- [x] Dimension 7 Inventory Provenance: PASS (not applicable: Tool is none)

**Approval:** approved 2026-10-27 (GSD UI checker)
