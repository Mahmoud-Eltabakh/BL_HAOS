# Phase 28: Package Panel Bundle Parity - Pattern Map

**Mapped:** 2026-10-28  
**Files analyzed:** 2 implementation targets  
**Analogs found:** 2 / 2

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `modules/integration/tests/test_package_layout.py` | test | batch / transform verification | Same file, existing `test_panel_build_source_and_stable_bundle_contract` | exact |
| `modules/integration/custom_components/bl_haos/panel_static/bl-haos-media-panel.js` | generated package asset | transform | `modules/integration/panel_ui/vite.config.ts` | exact producer |

No new source component or dependency is indicated. The normal Vite build already creates the package asset; the implementation target is its intentional refresh after the reviewed TSX input is confirmed. A fresh temporary build is test output, not a checked-in file.

## Pattern Assignments

### `modules/integration/tests/test_package_layout.py` (test, batch / transform verification)

**Analog:** `modules/integration/tests/test_package_layout.py`, `test_panel_build_source_and_stable_bundle_contract` (lines 116-129; tracked).

This module deliberately checks package structure without requiring Home Assistant. Extend its existing panel contract rather than introducing a separate test module.

**Imports and path convention** (lines 1-9):

```python
"""Static package checks that do not require a Home Assistant runtime."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).parents[1]
COMPONENT = ROOT / "custom_components" / "bl_haos"
```

**Existing package/build assertion pattern** (lines 116-129):

```python
def test_panel_build_source_and_stable_bundle_contract():
    panel = ROOT / "panel_ui"
    assert (panel / "src" / "media-panel.tsx").is_file()
    package = json.loads((panel / "package.json").read_text(encoding="utf-8"))
    assert package["scripts"]["build"] == "tsc && vite build"
    assert all(not pin.startswith(("^", "~")) for pin in package["dependencies"].values())
    assert (panel / "package-lock.json").is_file()
    bundle = COMPONENT / "panel_static" / "bl-haos-media-panel.js"
    assert bundle.is_file()
    assert {path.name for path in bundle.parent.iterdir()} == {bundle.name}
    compiled = bundle.read_text(encoding="utf-8")
    assert "bl-haos-media-panel" in compiled
    assert "--neu-page" in compiled
```

For parity, preserve this static-contract style and add the proposed fresh-build comparison here. Use pytest's `tmp_path` for an isolated output directory, invoke the existing local Vite toolchain with `--outDir`, assert that output contains exactly the expected JS file, then compare its bytes with the tracked bundle. Do not first run the ordinary build: the Vite config sets `emptyOutDir: true` and writes directly into `panel_static`, which would replace the evidence being checked.

**Queue UI behavior analog** (source assertions are currently missing at this package boundary):

```python
for marker in ("Playback queue", "Play playlist"):
    assert marker in compiled
```

Use the panel's existing accessible behavior as the marker source: `modules/integration/panel_ui/src/media-panel.tsx` lines 1053-1092. Existing component tests in `modules/integration/panel_ui/src/media-panel.test.tsx` lines 83-190 verify explicit speaker selection, the saved-record launch WebSocket call, replacement confirmation, and queue snapshot rendering. Those are source-level behavior tests; do not treat them as package parity.

### `modules/integration/custom_components/bl_haos/panel_static/bl-haos-media-panel.js` (generated package asset, transform)

**Producer analog:** `modules/integration/panel_ui/vite.config.ts` (lines 1-15; tracked).

This is generated output, so there is no hand-authored code pattern to copy into the asset. Preserve the existing Vite producer contract and make only the intentional build-generated refresh after the panel source is reviewed.

**Build contract:**

```typescript
build: {
  outDir: '../custom_components/bl_haos/panel_static',
  emptyOutDir: true,
  lib: {
    entry: 'src/media-panel.tsx',
    formats: ['es'],
    fileName: () => 'bl-haos-media-panel.js',
  },
  rollupOptions: { output: { inlineDynamicImports: true } },
},
```

For the test, override only `outDir` to a new temporary directory. Keep the configured normal build output unchanged for the eventual reviewed artifact refresh. The existing `modules/integration/panel_ui/package.json` script is `"build": "tsc && vite build"`; no dependency or lockfile change is indicated by the research.

## Shared Patterns

### Separate generation from verification

**Sources:** `modules/integration/tests/test_package_layout.py` lines 116-129 and `modules/integration/panel_ui/vite.config.ts` lines 5-15.  
**Apply to:** package parity test and intentional artifact refresh.

The test should build to a fresh temporary directory and compare against the existing tracked output without mutating it. Run the normal package build only for the intentional artifact update, not as a precondition to the parity assertion.

### Keep package and serving boundaries distinct

**Source:** `modules/integration/tests/test_panel_registration.py` lines 77-116; tracked.  
**Apply to:** validation planning, not as a replacement for byte parity.

```python
async def assert_module_status(http, status):
    response = await http.get(PANEL_URL)
    assert response.status == status
    if status == 200:
        assert "bl-haos-media-panel" in await response.text()
```

The SIL test covers the Home Assistant static route and unload/reload lifecycle. Keep that serving check separate from the static package test: a successful route response does not prove that the served bundle matches current source.

## Planning Notes

- The integration subrepository confirms `panel_ui/src/media-panel.tsx` and `panel_ui/src/media-panel.test.tsx` have existing uncommitted changes. Preserve them; do not run the normal build until the phase owner confirms those changes are the reviewed build input.
- `custom_components/bl_haos/panel_static/bl-haos-media-panel.js` is currently clean/tracked. Do not overwrite it during test implementation; refresh it only as the intentional package update.
- Research leaves the Node/npm reproducibility choice open. Do not invent a runtime pin in `package.json`, CI, or testing documentation during the parity-test change. If the plan includes recording a supported runtime, first select it and identify its owning config/doc file.
- `modules/integration/tests/test_panel_registration.py` and the panel TSX tests are validation neighbors, not proposed edits for this package-parity scope.

## No Analog Found

None. The existing package-layout test is the direct test analog, and the Vite config is the direct producer for the generated bundle.

## Metadata

**Analog search scope:** `modules/integration/tests`, `modules/integration/panel_ui`, `modules/integration/custom_components/bl_haos`  
**Tracked-source verification:** All analog and target paths listed above were verified by `git -C modules/integration ls-files`.  
**Pattern extraction date:** 2026-10-28