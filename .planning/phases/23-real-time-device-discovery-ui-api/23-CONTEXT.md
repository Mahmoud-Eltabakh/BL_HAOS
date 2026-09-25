# Phase 23 Context: Neumorphic Discovery UI

## Intent

Convert the BL-HAOS ingress web dashboard and real-time Bluetooth discovery flow from the current flat dark-slate treatment to restrained Neumorphism. The style should make surfaces and control states legible through depth, not through excessive borders, gradients, or decoration.

## Scope

- Dashboard shell, header actions, compact adapter/integration status, speaker cards, discovery modal, settings modal, form controls, sliders, badges, and inline feedback states.
- The standalone Diagnostics and Guided recovery panels are intentionally removed from the primary dashboard to keep the operator workflow focused; support/recovery remains an API concern for future dedicated tooling.
- Real-time device rows must remain easy to scan as devices arrive incrementally during an active scan.
- This is a visual-system change. Discovery API/WebSocket behavior and backend contracts are unchanged unless implementation reveals a direct styling integration issue.

## Visual Contract

### Surfaces and depth

- Define a small CSS token system in the UI stylesheet for the base surface, raised surface, inset surface, highlight shadow, deep shadow, and text roles.
- Use one coherent neutral base surface across the page and modal surfaces; avoid a separate card-colored slate hierarchy.
- Raised containers use paired soft light and dark shadows. Inputs, sliders, search fields, and recessed status areas use inset shadows.
- Interactive controls transition between raised and pressed/inset states on activation. Do not use border-heavy controls as the primary depth cue.
- Keep radii restrained and consistent with the existing layout; do not turn every text element into a pill.
- Do not introduce decorative gradients, floating blobs, or visual effects that reduce information density.

### Color and semantics

- Semantic accents remain stable and recognizable: connected/live uses emerald, pending/reconnecting uses amber, errors/offline use rose, and diagnostics/recovery uses cyan.
- Apply semantic colors to icons, labels, indicators, and focused action details rather than making every surface a saturated color block.
- Text and state indicators must retain WCAG AA contrast against the new neutral surface in both normal and disabled states.
- Focus-visible outlines remain explicit and must not rely on shadow changes alone.

### Components and states

- Header and primary actions: clear raised hierarchy with an obvious pressed/loading state.
- Adapter, integration, and speaker surfaces: raised at rest, with consistent depth and no competing border system.
- Discovery results: stable row dimensions, visible live-arrival state, readable RSSI/status metadata, and a clear selected/paired state.
- Text inputs and volume sliders: inset treatment with visible focus and sufficient thumb/track contrast.
- Modal backdrops remain functional and accessible; modal content uses the same surface tokens as the dashboard.
- Error, warning, empty, loading, offline, and reduced-motion states must remain understandable without relying on depth or color alone.

## Responsive and Accessibility Constraints

- Preserve the existing one/two/three-column responsive behavior and avoid shadow or padding changes that cause layout shift.
- Keep touch targets at least 44 CSS pixels where practical, including discovery and speaker actions.
- Preserve dialog semantics, focus restoration/trapping, keyboard dismissal, `aria-live` announcements, and slider value attributes.
- Verify contrast, focus visibility, reduced-motion behavior, and readable text at mobile and desktop breakpoints.

## Implementation Tasks

1. Establish shared Neumorphic CSS tokens and utility classes in `modules/bridge/web_ui/src/index.css` and the Tailwind configuration only where existing utilities cannot express the states cleanly.
2. Convert the page shell and shared panels first, then apply the same surface/state vocabulary to `AdapterStatus`, `DiagnosticsPanel`, `RecoveryPanel`, `SpeakerCard`, `DiscoveryModal`, and `SettingsModal`.
3. Replace border/color-only control states with raised, inset, hover, focus, pressed, disabled, loading, and error states while retaining semantic accents.
4. Add or update frontend tests for discovery-row rendering, modal/control states, and volume/discovery interactions without coupling tests to incidental shadow class names.
5. Run the frontend typecheck, unit tests, production build, and Playwright discovery flow at desktop and mobile viewport sizes.

## Acceptance Criteria

- The ingress dashboard visibly uses the shared Neumorphic surface system across the discovery workflow, rather than isolated one-off shadows.
- A user can distinguish raised, inset, focused, pressed, disabled, loading, connected, warning, and error states without relying on color alone.
- Newly discovered devices remain scannable and stable as real-time events append or update rows.
- Existing keyboard, screen-reader, reduced-motion, responsive, and semantic-status behavior remains intact.
- Frontend validation passes for typecheck, unit tests, production build, and the relevant discovery E2E flow.