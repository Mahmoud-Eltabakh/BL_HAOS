# Phase 23 - UI Visual & Experience Design Review

**Audited:** 2026-09-25  
**Audited target:** BL-HAOS Ingress Web Dashboard (`modules/bridge/web_ui/src`)  
**Assessment standard:** Six-pillar frontend design review, WCAG 2.1 AA expectations, and Home Assistant operator UI conventions  
**Evidence:** Static source review, existing UI tests, prior phase review artifacts, and the reported Playwright run. No fresh screenshots were captured during this audit.

## Verdict

**Overall: 18/24 - Strong foundation; visual refinement and runtime verification remain.**

The phase delivers a clear real-time discovery workflow: opening the dialog starts scanning, discovered devices are sorted by signal and recency, and the operator can filter, connect, disconnect, remove, or enter a MAC address manually. The main limitations are visual density in the discovery dialog, repeated blue/slate treatment for both action and metadata, compact typography, and the lack of fresh screenshot evidence at the target responsive widths.

## Pillar Scorecard

| Pillar | Score | Summary |
|---|---:|---|
| **1. Hierarchy & Layout** | **3/4** | The dashboard-to-discovery flow is easy to follow, but the discovery dialog contains several equally weighted control bands before the device list. |
| **2. Color & Theme** | **3/4** | The dark neumorphic system is consistent and status colors are meaningful, but blue is used for branding, actions, selected filters, identity, and signal metadata. |
| **3. Typography & Microcopy** | **3/4** | Labels and empty-state guidance are concrete, though primary interaction and device metadata rely heavily on small `text-xs` and technical Bluetooth terminology. |
| **4. Interaction & Feedback** | **3/4** | Auto-start scanning, loading labels, inline status banners, filtering, and focus handling are strong; scan failures and adapter failures remain less visible than successful paths. |
| **5. Component Polish** | **3/4** | Components are cohesive, responsive, and iconographically consistent, but nested raised/inset surfaces create a visually busy hierarchy in the modal and cards. |
| **6. Accessibility & Inclusive Experience** | **3/4** | Dialog semantics, focus return/trapping, keyboard dismissal, live regions, labels, and slider ARIA values are present; dense status text and lack of runtime accessibility capture leave residual risk. |

**Total: 18/24**

## Detailed Assessment

### 1. Hierarchy & Layout - 3/4

**Strengths**

- The primary operator journey is direct: the `Add Speaker` CTA opens the dialog and starts discovery automatically in `DiscoveryModal.tsx`.
- The discovery dialog has a stable structure: title, status, scan controls, search/filter controls, device list, and manual MAC entry.
- Device results sort strongest RSSI first and use recency as a tie-breaker, which supports quick selection while devices stream in.
- The dashboard remains responsive with one, two, and three-column speaker grids in `App.tsx`.

**Findings**

- The dialog header, scan bar, search/filter bar, device rows, and manual-entry footer are all framed as similarly weighted inset or raised surfaces. This makes the live result list compete with controls that are secondary once scanning is active.
- A row with a long device name plus three badges, MAC address, device type, RSSI, and action buttons can become crowded at narrow widths. The source has responsive wrapping, but this needs screenshot validation at 375px.

### 2. Color & Theme - 3/4

**Strengths**

- The dark surface variables in `index.css` give the neumorphic system a consistent foundation.
- Emerald, rose, amber, and blue communicate connected, error, disconnecting, and active states respectively.
- Focus-visible styling and reduced-motion handling are defined globally.

**Findings**

- Blue is doing too many jobs: primary action, Bluetooth identity, selected filter, signal icon, address emphasis, and some metadata. Reserve blue primarily for action/selection and reduce emphasis on device facts.
- The raised and inset shadows are visually distinctive but can reduce edge separation when many surfaces are adjacent. A flatter treatment for the result list would improve scanability and reduce visual noise.

### 3. Typography & Microcopy - 3/4

**Strengths**

- Copy is task-oriented: `Add Speaker`, `Start Scan`, `All Devices`, `Speakers`, `Connect`, and `Remove` are immediately understandable.
- Empty states explain what to do next, including pairing-mode guidance and manual MAC management.
- Connection failures include useful pairing-mode guidance rather than only exposing an operation failure.

**Findings**

- `text-xs` is used for many controls, status labels, metadata rows, and error messages. This keeps the compact dashboard dense but leaves little typographic separation between primary guidance and supporting details.
- Terms such as RSSI, dBm, adapter interface names, and MAC address are appropriate for diagnostics but should remain visually subordinate to the device name and connection action.
- The UI still uses the configured sans default rather than an intentional product typeface or documented type scale.

### 4. Interaction & Feedback - 3/4

**Strengths**

- Discovery starts automatically once per modal open, matching the real-time discovery goal.
- Scan state is visible, scan controls can be toggled, and devices update through the existing event-driven data path.
- Connect, disconnect, and remove actions disable while pending and communicate progress with labels such as `Connecting...`.
- Success and failure results are presented inline without blocking browser dialogs.

**Findings**

- Auto-start scan errors are shown as a status message, but the initial failure path is not paired with a stronger recovery affordance beyond manually trying `Start Scan`.
- The adapter power action reports failures inline, but the compact adapter strip gives limited context about whether a failure affects discovery. A disabled or unavailable scan state should be visibly connected to adapter health.
- The existing reported Playwright run had 3 passing tests and 1 failing recovery/support-export test because the expected `Export support bundle` control was absent. That test appears outside the current discovery surface, but it means the full UI suite is not green evidence for this audit.

### 5. Component Polish - 3/4

**Strengths**

- `lucide-react` icons provide a consistent visual vocabulary.
- Modal max-height and scrollable device results prevent the dialog from growing beyond the viewport.
- Buttons maintain stable icon-plus-label patterns, and responsive action rows stack on narrow screens.
- Existing cards and modals use consistent corner radii, spacing utilities, and state badges.

**Findings**

- The repeated `neu-surface`, `neu-surface-subtle`, and `neu-inset` nesting in a single modal creates several competing elevations. The result rows would benefit from one restrained list treatment and clearer separation only on hover/selection.
- The manual MAC footer is useful but visually equal to the live-discovery path. It should read as an advanced fallback rather than a second primary workflow.
- No new motion or transition treatment specifically communicates incremental device arrival beyond the scanning indicator; a restrained row insertion state could help without adding noise.

### 6. Accessibility & Inclusive Experience - 3/4

**Strengths**

- Both modals expose `role="dialog"`, `aria-modal`, and an associated visible heading.
- Escape handling, focus trapping, and focus restoration are implemented for the modal workflows.
- Icon-only controls have accessible labels, and the volume controls expose explicit ARIA values.
- Live status regions announce adapter and integration state changes.
- Reduced-motion preferences are respected globally.

**Findings**

- The audit did not include a fresh browser accessibility tree or keyboard walkthrough at mobile and desktop widths. Source-level semantics are positive evidence, but not a substitute for runtime verification.
- Device rows are generic `div` containers rather than list semantics, and newly discovered devices do not have a dedicated live announcement. The visible scan status is helpful, but assistive technology users may not learn that a new result arrived without moving focus.
- Dense badge groups and low-emphasis metadata should be checked for contrast against the inset surfaces in a rendered browser.

## Priority Recommendations

1. Capture and review screenshots at 375px, 768px, and 1440px with zero, one, and several discovered devices; include long names, scan errors, and the manual MAC path.
2. Reduce elevation nesting in `DiscoveryModal.tsx`: keep the controls grouped, flatten result rows, and visually subordinate the manual MAC fallback.
3. Reserve blue for primary actions and selected filters; use neutral text for MAC/device metadata and reserve semantic colors for actual state.
4. Promote scan failure and adapter-unavailable states into a single actionable discovery status with retry guidance.
5. Add a focused runtime accessibility pass covering dialog focus order, result announcements, contrast, and keyboard operation.

## Verification Evidence

- Existing source-level frontend asset and component contract tests cover relative ingress paths, required components, diagnostics wiring, and hook ordering.
- The reported Playwright run completed 3 tests and failed 1 recovery/support-export test because `Export support bundle` was not found.
- No fresh screenshots or runtime accessibility tree were available for this audit.

## Files Audited

- `modules/bridge/web_ui/src/App.tsx`
- `modules/bridge/web_ui/src/index.css`
- `modules/bridge/web_ui/src/components/AdapterStatus.tsx`
- `modules/bridge/web_ui/src/components/DiscoveryModal.tsx`
- `modules/bridge/web_ui/src/components/SpeakerCard.tsx`
- `modules/bridge/web_ui/src/components/SettingsModal.tsx`
- `modules/bridge/web_ui/src/hooks/useBluetoothEvents.ts`
- `modules/bridge/web_ui/src/api/client.ts`
- `modules/bridge/web_ui/package.json`
- `modules/bridge/tests/test_frontend_assets.py`
- `.planning/STATE.md`
- `.planning/phases/20-release-quality-gates-go-live/20-UI-REVIEW.md`
