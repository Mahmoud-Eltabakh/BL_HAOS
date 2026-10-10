# Phase 06 — Ingress Web Dashboard UI Review

**Audited:** 2026-09-22
**Baseline:** Abstract 6-Pillar Standards & Home Assistant Ingress Design Guidelines
**Screenshots:** Not captured (no dev server running; code-level static analysis performed)
**Audited Directory:** `modules/bridge/web_ui/src`

---

## Pillar Scores

| Pillar | Score | Key Finding |
|--------|-------|-------------|
| 1. Hierarchy & Layout | 3/4 | Clean card grid and header, but developer diagnostics push primary content down and discovery modal has 4 competing toolbars |
| 2. Color & Theme | 3/4 | Strong Home Assistant dark mode alignment, but modal suffers from badge color sprawl and small 10px low-contrast text |
| 3. Typography & Microcopy | 2/4 | Heavy Bluetooth jargon ("All MACs", "MAC Beacon", "Audio Sinks", "Aggressive Auto-Reconnect") clutters user experience |
| 4. Interaction & Feedback | 2/4 | Disruptive browser `alert()` and `confirm()` calls freeze HA webview; speaker volume slider is disconnected from backend |
| 5. Component Polish | 2/4 | Inconsistent card dividers, lack of modal backdrop click-to-close or transitions, un-debounced controls |
| 6. Accessibility & Experience Design | 1/4 | Almost zero ARIA attributes, no modal `role="dialog"`, no `Escape` key listeners, and no WebSocket auto-reconnect retry loop |

**Overall: 13/24**

---

## Top 3 Priority Fixes

1. **Eliminate native browser `alert()` and `confirm()` dialogs and wire the volume slider to backend APIs**
   - *User Impact*: Browser alerts freeze the JavaScript execution thread and render broken or unstyled dialogs inside Home Assistant Companion Apps and Ingress iframes. The speaker volume slider is purely local state (`useState(70)`) and does not change audio levels or sync with PipeWire.
   - *Concrete Fix*: Replace `alert()` and `confirm()` with inline toast/banner alerts and a lightweight modal confirm dialog in [SpeakerCard.tsx](modules/bridge/web_ui/src/components/SpeakerCard.tsx#L25) and [SettingsModal.tsx](modules/bridge/web_ui/src/components/SettingsModal.tsx#L43). Wire `SpeakerCard` volume to the audio endpoint with debounce.

2. **Simplify microcopy, eliminate low-level Bluetooth jargon, and tuck developer diagnostics away**
   - *User Impact*: Non-technical smart home users are confronted with technical Bluetooth terms ("All MACs", "MAC Beacon", "Audio Sinks") and prominent D-Bus diagnostics ("Bridge: ready", "Credential: configured") on the main landing view.
   - *Concrete Fix*: In [DiscoveryModal.tsx](modules/bridge/web_ui/src/components/DiscoveryModal.tsx#L206) and [App.tsx](modules/bridge/web_ui/src/App.tsx#L89), rename filters to "All Devices" and "Speakers", replace "MAC Beacon" with "Unnamed Device", and move the "Native integration" diagnostics into a collapsible details disclosure or settings drawer.

3. **Implement complete ARIA accessibility attributes, modal keyboard traps, and WebSocket reconnection logic**
   - *User Impact*: Users cannot close modals with the `Escape` key, screen readers lack context for icon buttons and sliders, and any transient network drop leaves the UI permanently in "Offline" state until manual browser reload.
   - *Concrete Fix*: Add `role="dialog"`, `aria-modal="true"`, `aria-label`, and `Escape` key handlers to [DiscoveryModal.tsx](modules/bridge/web_ui/src/components/DiscoveryModal.tsx) and [SettingsModal.tsx](modules/bridge/web_ui/src/components/SettingsModal.tsx). In [useBluetoothEvents.ts](modules/bridge/web_ui/src/hooks/useBluetoothEvents.ts#L33), implement an exponential backoff auto-reconnect timer in `ws.onclose`.

---

## Detailed Findings

### Pillar 1: Hierarchy & Layout (3/4)
- **Strengths:**
  - Clear, distinct header in [App.tsx](modules/bridge/web_ui/src/App.tsx#L33-L79) with live connection badge, primary "Add Speaker" CTA, and quick refresh button.
  - Responsive speaker grid (1 col mobile, 2 col tablet, 3 col desktop) in [App.tsx](modules/bridge/web_ui/src/App.tsx#L131) with clear empty state illustration.
- **Weaknesses:**
  - The "Native integration" diagnostics box ([App.tsx](modules/bridge/web_ui/src/App.tsx#L89-L105)) occupies prominent vertical real estate between the adapter status bar and the speakers list. This draws user focus away from speaker playback and management.
  - In [DiscoveryModal.tsx](modules/bridge/web_ui/src/components/DiscoveryModal.tsx#L143-L370), there are four stacked control rows (header -> scan status & PIN bar -> search & filter bar -> device list -> manual MAC footer), creating visual clutter and nested scrolling issues on mobile viewports.

### Pillar 2: Color & Theme (3/4)
- **Strengths:**
  - Cohesive dark palette using Tailwind `slate-900` background, `slate-800` cards, and Home Assistant primary `blue-600` / `blue-500` accents.
  - Semantic status indicators for `Live` / `Offline` and `Connected` / `Disconnected` states using emerald, amber, and rose tones.
- **Weaknesses:**
  - In [DiscoveryModal.tsx](modules/bridge/web_ui/src/components/DiscoveryModal.tsx#L269-L286), single device rows exhibit "badge salad" with up to four distinct pill badges simultaneously (`Named` in green, `MAC Beacon` in slate, `Speaker` in blue, `Connected` in dark emerald).
  - Use of `text-[10px]` with translucent backgrounds (e.g. `bg-emerald-900/40 text-emerald-400`) creates borderline WCAG AA contrast on lower-brightness mobile screens.

### Pillar 3: Typography & Microcopy (2/4)
- **Strengths:**
  - Clean font sizing across main headings (`text-2xl`, `text-lg`, `text-sm`) with clear information hierarchy.
- **Weaknesses:**
  - Overly technical Bluetooth jargon throughout the user flow:
    - `"All MACs"` in filter tabs ([DiscoveryModal.tsx](modules/bridge/web_ui/src/components/DiscoveryModal.tsx#L217)) should be `"All Devices"`.
    - `"Audio Sinks"` in filter tabs ([DiscoveryModal.tsx](modules/bridge/web_ui/src/components/DiscoveryModal.tsx#L228)) should be `"Speakers"`.
    - `"MAC Beacon"` badge ([DiscoveryModal.tsx](modules/bridge/web_ui/src/components/DiscoveryModal.tsx#L273)) should be `"Unnamed Device"`.
    - `"Aggressive Auto-Reconnect"` ([SettingsModal.tsx](modules/bridge/web_ui/src/components/SettingsModal.tsx#L110)) should be `"Auto-Reconnect on Startup / Wake"`.
    - `"Connect by Bluetooth MAC Address:"` in manual pairing footer should be simplified into an "Advanced Manual Pair" dropdown.
  - Diagnostics terminology (`"Bridge: ready"`, `"Credential: configured"`) exposed on the main dashboard without contextual explanation for end users.

### Pillar 4: Interaction & Feedback (2/4)
- **Strengths:**
  - Clear loading indicator on connect buttons (`"Connecting..."` / `"Disconnecting..."`) and spinning scan icon during Bluetooth discovery.
- **Weaknesses:**
  - **Disruptive Browser Alerts**: [SpeakerCard.tsx](modules/bridge/web_ui/src/components/SpeakerCard.tsx#L25) and [SettingsModal.tsx](modules/bridge/web_ui/src/components/SettingsModal.tsx#L43-L47) invoke `alert()` and `confirm()`. These browser-native blocking alerts degrade the Home Assistant Ingress iframe experience and cause app freezes in the HA iOS/Android companion webviews.
  - **Unconnected Volume Slider**: The volume slider in [SpeakerCard.tsx](modules/bridge/web_ui/src/components/SpeakerCard.tsx#L70-L80) updates internal React state `const [volume, setVolume] = useState(70)` only and does not communicate with any backend API or PipeWire audio node.
  - **No WebSocket Reconnection Retry**: In [useBluetoothEvents.ts](modules/bridge/web_ui/src/hooks/useBluetoothEvents.ts#L33-L35), `ws.onclose` simply sets `wsConnected = false` without attempting to reconnect. A temporary HA ingress proxy timeout leaves the UI disconnected indefinitely until a hard page reload.

### Pillar 5: Component Polish (2/4)
- **Strengths:**
  - Smooth rounded corners (`rounded-xl`, `rounded-2xl`), subtle borders (`border-slate-700`), and dark frosted backdrop filters (`backdrop-blur-sm`).
- **Weaknesses:**
  - Modals do not close when clicking the backdrop overlay outside the modal container in [DiscoveryModal.tsx](modules/bridge/web_ui/src/components/DiscoveryModal.tsx#L104) and [SettingsModal.tsx](modules/bridge/web_ui/src/components/SettingsModal.tsx#L52).
  - Inconsistent divider styling between components (`border-slate-700/60` vs `border-slate-700` vs `border-slate-800`).
  - No transition animations for modal enter/exit or status banner dismissals.

### Pillar 6: Accessibility & Experience Design (1/4)
- **Strengths:**
  - Semantic HTML tags (`<header>`, `<main>`, `<section>`, `<h1>`, `<h2>`, `<button>`) used in [App.tsx](modules/bridge/web_ui/src/App.tsx).
  - `aria-live="polite"` applied to the diagnostics section in [App.tsx](modules/bridge/web_ui/src/App.tsx#L89).
- **Weaknesses:**
  - Modals lack standard ARIA attributes (`role="dialog"`, `aria-modal="true"`, `aria-labelledby`) in both [DiscoveryModal.tsx](modules/bridge/web_ui/src/components/DiscoveryModal.tsx) and [SettingsModal.tsx](modules/bridge/web_ui/src/components/SettingsModal.tsx).
  - Keyboard navigation is missing: pressing `Escape` does not dismiss open modals, and tab navigation is not trapped within active dialogs.
  - Icon buttons lack `aria-label`s (e.g. Refresh buttons in [App.tsx](modules/bridge/web_ui/src/App.tsx#L68), Adapter Power toggle in [AdapterStatus.tsx](modules/bridge/web_ui/src/components/AdapterStatus.tsx#L32), Modal Close buttons in [DiscoveryModal.tsx](modules/bridge/web_ui/src/components/DiscoveryModal.tsx#L118)).
  - Volume sliders lack `aria-label="Speaker Volume"`, `aria-valuemin="0"`, `aria-valuemax="100"`, and `aria-valuenow`.

---

## Files Audited
- [modules/bridge/web_ui/src/App.tsx](modules/bridge/web_ui/src/App.tsx)
- [modules/bridge/web_ui/src/components/SpeakerCard.tsx](modules/bridge/web_ui/src/components/SpeakerCard.tsx)
- [modules/bridge/web_ui/src/components/DiscoveryModal.tsx](modules/bridge/web_ui/src/components/DiscoveryModal.tsx)
- [modules/bridge/web_ui/src/components/AdapterStatus.tsx](modules/bridge/web_ui/src/components/AdapterStatus.tsx)
- [modules/bridge/web_ui/src/components/SettingsModal.tsx](modules/bridge/web_ui/src/components/SettingsModal.tsx)
- [modules/bridge/web_ui/src/hooks/useBluetoothEvents.ts](modules/bridge/web_ui/src/hooks/useBluetoothEvents.ts)
- [modules/bridge/web_ui/src/api/client.ts](modules/bridge/web_ui/src/api/client.ts)
- [modules/bridge/web_ui/src/index.css](modules/bridge/web_ui/src/index.css)
- [modules/bridge/web_ui/index.html](modules/bridge/web_ui/index.html)
- [modules/bridge/web_ui/tailwind.config.js](modules/bridge/web_ui/tailwind.config.js)
