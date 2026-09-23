# Phase 19 - UI Review

**Audited:** 2026-09-23  
**Baseline:** Abstract 6-pillar standards; no `UI-SPEC.md` was present  
**Screenshots:** Not captured; no dev server was available on ports 3000, 5173, or 8080

## Verdict

**Overall: 14/24 - Needs revision before release.**

The UI is structurally complete and the current Vite build passes. The phase contract test also passes when run from its expected `modules/bridge` working directory. However, the implementation has release-relevant interaction and feedback weaknesses: several runtime failures are swallowed or exposed as raw error text, modal focus behavior is incomplete, adapter actions have no visible failure state, and the visual system is mostly ad hoc Tailwind utility styling with no shared tokens or focus/reduced-motion foundation. Phase 20 remains on HOLD, so this audit does not recommend treating the UI as production-ready.

## Pillar Scores

| Pillar | Score | Key Finding |
|---|---:|---|
| 1. Copywriting | 3/4 | Domain-specific labels and useful empty/error copy are present, but recovery actions render raw operation IDs and some failure copy is generic or leaks backend detail. |
| 2. Visuals | 2/4 | Clear dashboard grouping exists, but diagnostics and recovery are stacked as dense panels with limited hierarchy and no screenshot evidence of responsive composition. |
| 3. Color | 2/4 | Status colors are semantically recognizable, but blue/cyan accents and slate surfaces are repeated throughout without a documented 60/30/10 system or shared tokens. |
| 4. Typography | 2/4 | The scale is compact and readable in principle, but the UI uses the browser/system sans default and four weight families with no typographic contract. |
| 5. Spacing | 3/4 | Spacing is consistently utility-based and no arbitrary pixel/rem values were found, but dense nested panels and repeated rounded containers reduce scanability. |
| 6. Experience Design | 2/4 | Loading, empty, disabled, success, and modal error states exist, but adapter failures, initial Bluetooth failures, focus management, and recovery error propagation are incomplete. |

## Top 3 Priority Fixes

1. **Make failure states truthful and actionable** - `useBluetoothEvents` logs initial adapter/device failures to the console only, while `AdapterStatus` does not expose power-toggle failures and recovery converts all failures into a fabricated empty diagnostics object. Add shared error state, visible retry guidance, and bounded user-facing messages in `modules/bridge/web_ui/src/hooks/useBluetoothEvents.ts`, `modules/bridge/web_ui/src/components/AdapterStatus.tsx`, and `modules/bridge/web_ui/src/components/RecoveryPanel.tsx`.
2. **Complete keyboard and focus behavior for modals** - Both dialogs close on Escape and backdrop click but do not trap focus, return focus to the trigger, or associate visible headings with the dialog. Add a focus trap, initial focus, focus return, and `aria-labelledby` in `modules/bridge/web_ui/src/components/DiscoveryModal.tsx` and `modules/bridge/web_ui/src/components/SettingsModal.tsx`.
3. **Establish a small visual system and responsive hierarchy** - Replace repeated slate/blue values and one-off rounded surfaces with shared CSS/Tailwind tokens, add explicit responsive panel ordering and density rules, and provide focus-visible/reduced-motion styles in `modules/bridge/web_ui/src/index.css` and the component classes. Validate at 375px, 768px, and 1440px with Playwright screenshots before release.

## Strengths

- The primary workflow is recognizable: adapter status, diagnostics, guided recovery, integration status, and speaker management are presented in a sensible top-to-bottom order in `modules/bridge/web_ui/src/App.tsx`.
- Domain copy is generally concrete: `Add Speaker`, `Speakers`, `Diagnostics`, `Guided recovery`, `No speakers added yet`, and `No Bluetooth devices detected yet` are better than generic dashboard labels.
- The implementation includes explicit loading, empty, disabled, success, failure, demo, and unavailable paths across the panels and modals.
- The Ingress asset contract is preserved with a relative Vite base and dynamic REST/WebSocket URLs in `modules/bridge/web_ui/vite.config.ts` and `modules/bridge/web_ui/src/api/client.ts`.
- Current evidence supports build integrity: `npm --prefix modules/bridge/web_ui run build` passed, and `modules/bridge/tests/test_frontend_assets.py` passed 5 tests when run from `modules/bridge`.

## Detailed Findings

### Pillar 1: Copywriting (3/4)

**WARNING** `modules/bridge/web_ui/src/components/RecoveryPanel.tsx:36` renders `action.replace(/_/g, ' ')`, producing implementation-oriented labels such as `retry reconnect` rather than concise operator language such as `Retry connection`. The guidance diagnosis and expected outcome are useful, but each allowlisted action should have a presentation label separate from its API ID.

**WARNING** `modules/bridge/web_ui/src/App.tsx:37` and `modules/bridge/web_ui/src/components/RecoveryPanel.tsx:24` use generic `Diagnostics are unavailable` and `Recovery unavailable` messages without telling the operator what to do next. Add a retry or refresh action and a short cause-neutral instruction.

**WARNING** `modules/bridge/web_ui/src/components/DiscoveryModal.tsx:60-64` can display a backend-derived error fragment after `Connection failed for ...`. The backend contract says raw exceptions should not reach the UI; normalize the client error into bounded, user-safe copy.

**Strength:** Empty and primary-action copy is specific to the Bluetooth task in `App.tsx:179-183` and `DiscoveryModal.tsx:242-250`.

### Pillar 2: Visuals (2/4)

**WARNING** `modules/bridge/web_ui/src/App.tsx:103-111` places diagnostics and recovery before the main speaker grid, making operational panels dominate the first viewport even for healthy users. Use a compact health summary with expandable detail, or visually subordinate recovery until an actionable failure exists.

**WARNING** The UI uses repeated bordered, rounded panels in `App.tsx:103`, `App.tsx:113`, `App.tsx:124`, `DiagnosticsPanel.tsx:11`, and `RecoveryPanel.tsx:29`. This creates a stack of similarly weighted containers rather than one clear focal area. Distinguish primary speaker management from support tooling through spacing, hierarchy, and progressive disclosure.

**WARNING** No browser screenshots could be captured because no local server was running. Responsive visual behavior therefore remains unverified; the source has mobile utility classes, but that is not evidence that the combined modal and panel layout remains usable.

**Strength:** Consistent iconography from `lucide-react` and explicit status badges give the main dashboard a recognizable operational language.

### Pillar 3: Color (2/4)

**WARNING** `index.html:7`, `App.tsx:54`, and nearly every component use the same slate surface family with blue/cyan action accents. The palette communicates state, but there are no CSS variables or documented semantic tokens for surface, action, success, warning, and danger roles. This makes contrast and future theme adjustments difficult.

**WARNING** Blue is used for branding, primary actions, selected discovery filters, device identity, and status-adjacent labels (`App.tsx:61-68`, `DiscoveryModal.tsx:286-300`, `SpeakerCard.tsx:49-60`). Reserve the accent for actions and selection; use neutral/semantic colors for device metadata to improve hierarchy.

**WARNING** `index.css` only declares `color-scheme: dark` and provides no focus-visible, form-control, reduced-motion, or semantic color foundation. The visual language is therefore dependent on scattered utility classes.

**Strength:** Success, warning, danger, live/offline, and demo states are visually differentiated in `App.tsx:68-76`, `SpeakerCard.tsx:49-60`, and `DiagnosticsPanel.tsx:18`.

### Pillar 4: Typography (2/4)

**WARNING** `index.html:7` relies on `font-sans`, which resolves to the configured/default system sans stack. There is no intentional typeface or typography contract for an operator-facing product.

**WARNING** The audit found five text-size classes and four font-weight families across the source. Compact `text-xs` usage is widespread (`App.tsx:68`, `DiagnosticsPanel.tsx:18`, `DiscoveryModal.tsx:286-300`), including primary status and action content, which risks low legibility and weak hierarchy at mobile widths.

**WARNING** The code mixes text sizes and weights at component level without shared heading/body/caption primitives. Establish a small scale and reserve the smallest size for metadata only.

**Strength:** Speaker names and modal headings have stronger emphasis than metadata, for example `SpeakerCard.tsx:43-47` and `DiscoveryModal.tsx:129-133`.

### Pillar 5: Spacing (3/4)

**WARNING** No arbitrary pixel/rem spacing classes were found, which is good consistency evidence. However, the layout repeatedly nests `p-4`/`p-5`/`p-6` sections inside bordered containers (`DiscoveryModal.tsx:145-216`, `SettingsModal.tsx:96-160`) and uses many rounded surfaces, increasing visual density without a documented spacing scale.

**WARNING** `App.tsx:50` applies `p-6 md:p-10` to the entire shell while the header, diagnostics, recovery, integration accordion, and speaker grid each add their own vertical margins. At 375px this likely leaves less room for the core speaker workflow; screenshot validation is required.

**Strength:** The source uses standard Tailwind spacing utilities and responsive grid changes (`App.tsx:171`, `App.tsx:199`, `DiscoveryModal.tsx:206-211`) rather than arbitrary values.

### Pillar 6: Experience Design (2/4)

**BLOCKER** `modules/bridge/web_ui/src/hooks/useBluetoothEvents.ts:14-23` catches initial adapter/device load failures and only calls `console.error`, leaving the interface with empty lists and no visible degraded state. An operator can interpret a backend failure as “no adapters” or “no speakers.” Surface an unavailable state with retry.

**BLOCKER** `modules/bridge/web_ui/src/components/AdapterStatus.tsx:11-14` does not catch or render errors from `setAdapterPower`. A failed privileged action can appear to do nothing, with no pending state, disabled state, or result feedback.

**BLOCKER** `modules/bridge/web_ui/src/components/RecoveryPanel.tsx:20-25` catches execution errors but creates a `RecoveryResult` with `diagnostics: {} as RecoveryResult['diagnostics']`, then `App.tsx:115` replaces the valid diagnostics snapshot with that empty object. This can erase the operator view after a failed recovery and violates truthful degraded-state presentation.

**WARNING** Dialogs implement Escape and backdrop dismissal (`DiscoveryModal.tsx:96-103`, `SettingsModal.tsx:54-61`) but do not trap focus, set `aria-labelledby`, or restore focus to the opening control. This is a keyboard accessibility regression for the main pairing/settings workflows.

**WARNING** Several icon controls rely on `title` rather than an explicit accessible name, including refresh/power/settings/remove controls (`App.tsx:85`, `AdapterStatus.tsx:34`, `SpeakerCard.tsx:157`, `DiscoveryModal.tsx:344`). Add `aria-label` consistently and verify accessible names with an automated accessibility pass.

**WARNING** `modules/bridge/web_ui/src/api/client.ts:99-108` forwards `payload.detail` directly into thrown errors, and multiple components render `err.message` (`DiscoveryModal.tsx:64`, `SettingsModal.tsx:64`, `SpeakerCard.tsx:30`, `SpeakerCard.tsx:44`). Even if the backend is intended to redact, the client should normalize server errors before display.

**Strength:** The UI has meaningful baseline state coverage: loading/error/empty paths in `App.tsx`, `DiagnosticsPanel.tsx`, `DiscoveryModal.tsx`, `RecoveryPanel.tsx`, `SettingsModal.tsx`, and `SpeakerCard.tsx`, plus disabled controls during active mutations.

## Available Verification Evidence

- `npm --prefix modules/bridge/web_ui run build`: passed with Vite 7.3.6.
- `python -m pytest tests/test_frontend_assets.py -q` from `modules/bridge`: 5 passed.
- Phase 19 summary reports 100 bridge tests passed and deterministic demo scenarios, but this audit did not rerun the full backend suite.
- No screenshots were captured because ports 3000, 5173, and 8080 were unavailable.
- No `UI-SPEC.md` was present; this review uses the abstract 6-pillar standards.
- Registry audit was skipped because no `components.json` or third-party registry contract was identified.

## Recommended Follow-Up

1. Fix the three experience blockers before release: visible initial-load failure state, adapter action feedback, and recovery failure preservation.
2. Add keyboard focus management and consistent accessible names, then run an automated accessibility check at desktop and mobile viewports.
3. Add a small semantic token layer in `index.css`/Tailwind and reduce nested panel weight around diagnostics and recovery.
4. Start the Vite dev server and capture 375px, 768px, and 1440px screenshots, checking modal overflow, long device names, error banners, and the empty speaker state.
5. Re-run the UI contract test from `modules/bridge` and the full bridge suite after the UI fixes; retain phase-20 release evidence as a separate go-live gate.

## Files Audited

- `modules/bridge/web_ui/src/App.tsx`
- `modules/bridge/web_ui/src/index.css`
- `modules/bridge/web_ui/src/main.tsx`
- `modules/bridge/web_ui/src/api/client.ts`
- `modules/bridge/web_ui/src/hooks/useBluetoothEvents.ts`
- `modules/bridge/web_ui/src/components/AdapterStatus.tsx`
- `modules/bridge/web_ui/src/components/DiagnosticsPanel.tsx`
- `modules/bridge/web_ui/src/components/DiscoveryModal.tsx`
- `modules/bridge/web_ui/src/components/RecoveryPanel.tsx`
- `modules/bridge/web_ui/src/components/SettingsModal.tsx`
- `modules/bridge/web_ui/src/components/SpeakerCard.tsx`
- `modules/bridge/web_ui/package.json`
- `modules/bridge/web_ui/vite.config.ts`
- `modules/bridge/web_ui/tailwind.config.js`
- `modules/bridge/web_ui/tsconfig.json`
- `modules/bridge/web_ui/index.html`
- `modules/bridge/DOCS.md`
- `.planning/STATE.md`
- `.planning/phases/19-diagnostics-supportability-observability/19-01-PLAN.md`
- `.planning/phases/19-diagnostics-supportability-observability/19-01-SUMMARY.md`
- `.planning/phases/19-diagnostics-supportability-observability/19-02-PLAN.md`
- `.planning/phases/19-diagnostics-supportability-observability/19-02-SUMMARY.md`
