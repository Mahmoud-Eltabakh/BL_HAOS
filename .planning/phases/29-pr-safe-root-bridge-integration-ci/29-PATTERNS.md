# Phase 29: PR-Safe Root, Bridge & Integration CI - Pattern Map

**Mapped:** 2026-10-28  
**Files analyzed:** 2 target files  
**Analogs found:** 2 / 2

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `.github/workflows/tests.yml` | config / CI orchestration | batch | Existing `integration-unit` and `frontend` jobs in the same workflow | exact |
| `modules/integration/tests/test_package_layout.py` | test | transform/build validation | `test_panel_bundle_matches_fresh_build` and `test_test_strategy_artifacts_are_checked_in` in the same file; workflow-contract style in bridge `test_addon_config.py` | role-match |

## Pattern Assignments

### `.github/workflows/tests.yml` (config, batch)

**Analog:** Existing jobs in `.github/workflows/tests.yml`.

**Workflow policy pattern** (lines 3-12):

```yaml
on:
  push:
    branches:
      - main
  pull_request:
  workflow_dispatch:

permissions:
  contents: read
```

**Python job setup pattern** (integration L1, lines 66-84):

```yaml
  integration-unit:
    name: Integration client unit (L1)
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: modules/integration
    steps:
      - uses: actions/checkout@v5
        with:
          submodules: recursive
      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"
```

**Existing Node 22 setup pattern** (frontend job, lines 108-125):

```yaml
  frontend:
    name: Frontend unit + build + E2E (L3)
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: modules/bridge/web_ui
    steps:
      - uses: actions/checkout@v5
        with:
          submodules: recursive
      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"
      - uses: actions/setup-node@v5
        with:
          node-version: "22"
```

**Minimal change recommendation:** Add setup-node v5 with Node 22 and a lockfile install using `npm ci --prefix panel_ui --ignore-scripts` to `integration-unit`, whose working directory is `modules/integration`. Add the Node/npm/Vite/TypeScript preflight before running the existing `tests/unit tests/test_package_layout.py` command. Preserve Python 3.12 for this job and Python 3.14 in `integration-sil`; do not add release permissions, artifact publication, or an edge to the bridge publisher.

### `modules/integration/tests/test_package_layout.py` (test, build validation)

**Analog:** Existing package parity test and workflow-artifact check in this file.

**Workflow artifact convention** (lines 101-110):

```python
def test_test_strategy_artifacts_are_checked_in():
    """The layered test strategy (TESTING.md) must stay checked in and current."""
    repo = ROOT.parents[1]
    assert (repo / "TESTING.md").is_file()
    assert (repo / "scripts" / "run-tests.ps1").is_file()
    assert (repo / "scripts" / "run-tests.sh").is_file()
    assert (repo / ".github" / "workflows" / "tests.yml").is_file()
```

**Skip guard** (lines 141-150):

```python
def test_panel_bundle_matches_fresh_build(tmp_path):
    panel = ROOT / "panel_ui"
    bundle = COMPONENT / "panel_static" / "bl-haos-media-panel.js"
    node = shutil.which("node.exe") or shutil.which("node")
    npm = shutil.which("npm.cmd") or shutil.which("npm")
    vite_package = panel / "node_modules" / "vite" / "package.json"
    typescript_package = panel / "node_modules" / "typescript" / "package.json"
    if node is None or npm is None or not vite_package.is_file() or not typescript_package.is_file():
        pytest.skip("Node.js, npm, Vite, and TypeScript are required for the local bundle parity check")
```

**Core parity pattern** (lines 152-171):

```python
    build_dir = tmp_path / "panel-build"
    subprocess.run(
        [
            npm,
            "--prefix",
            str(panel),
            "run",
            "build",
            "--",
            "--outDir",
            str(build_dir),
        ],
        cwd=ROOT,
        check=True,
    )
    assert {path.name for path in build_dir.iterdir()} == {bundle.name}
    fresh_bundle = build_dir / bundle.name
    assert filecmp.cmp(fresh_bundle, bundle, shallow=False), "tracked panel bundle differs from a fresh Vite build"
```

**Minimal change recommendation:** Keep the existing skip guard for local developer environments; make CI's missing-tool preflight fail before pytest can interpret missing prerequisites as a skip. The existing parity build writes under `tmp_path`, so retain it unchanged and do not run a regular build into the tracked `panel_static` directory. If adding a static PR-safety assertion, this file is the closest root-workflow test surface: it already resolves the root workflow path. Assert only the required workflow contract (ordinary `pull_request`, read-only permissions, and no publication invocation/permission), not implementation details of the separate publisher.

### Static workflow-contract test analog (reference only)

**Tracked analog:** `modules/bridge/tests/test_addon_config.py`, `test_dependency_and_release_policy_is_explicit` (lines 166-173).

```python
def test_dependency_and_release_policy_is_explicit():
    dockerfile = Path("Dockerfile").read_text(encoding="utf-8")
    workflow = Path(".github/workflows/builder.yaml").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "npm --prefix web_ui audit --audit-level=high" in workflow
    assert "pip_audit" in workflow
    assert "severity: HIGH,CRITICAL" in workflow
```

This demonstrates the repository's existing lightweight static-contract style: read workflow text and assert required policy fragments. Treat it as a style reference only. Do not edit that test, inspect or invoke the nested publisher, or change nested release scripts. Prefer putting a root workflow assertion beside the integration workflow-artifact check if the plan requires an automated contract check.

## Shared Patterns

### Runtime setup
**Source:** `.github/workflows/tests.yml`  
**Apply to:** `integration-unit` only for the panel parity toolchain.  
Use `actions/setup-node@v5` with `node-version: "22"`, matching the existing frontend job. Keep existing Python runtime assignments: 3.12 for client/unit and 3.14 for pinned Home Assistant SIL.

### Reproducible, non-executing dependency installation
**Source:** Phase 29 research and the tracked panel lockfile.  
The nine existing `SUS: too-new` entries were reviewed in `29-RESEARCH.md`: locked versions match registry versions, sources are canonical, adoption is high, and no relevant direct install lifecycle scripts were found. Use `npm ci --prefix panel_ui --ignore-scripts` with the existing lock; do not upgrade, remove, regenerate, or otherwise change the entries. No dependency installation was performed during pattern mapping.

### Non-publishing boundary
**Source:** Root `.github/workflows/tests.yml` event and permission contract.  
Keep root PR validation read-only and test/build-only. Do not add a publisher invocation, `packages: write`, registry login, push, deployment, or release-artifact upload. No nested bridge publisher or script was modified or called.

## No Analog Found

None. The workflow runtime pattern is already present in the root workflow, the package parity behavior is implemented, and the repository has a static workflow-text assertion pattern.

## Metadata

**Analog search scope:** Root `.github/workflows`, `modules/integration/tests`, and `modules/bridge/tests`.  
**Files scanned:** Root workflow; integration package-layout tests; bridge static workflow-contract test.  
**Tracking check:** Root workflow verified with root `git ls-files`; test analogs verified with `git -C` inside their owning nested repositories.  
**Pattern extraction date:** 2026-10-28
