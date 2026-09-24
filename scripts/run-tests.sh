#!/usr/bin/env bash
# One-command local test runner for BL-HAOS layers (Linux/macOS/WSL2).
set -euo pipefail

LAYER="${1:-all}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BRIDGE="$REPO_ROOT/modules/bridge"
INTEGRATION="$REPO_ROOT/modules/integration"
WEBUI="$BRIDGE/web_ui"
PYTHON="${PYTHON:-python}"

export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1

run_bridge() {
  (cd "$BRIDGE" && "$PYTHON" -m pytest tests -q)
}

run_integration_unit() {
  (cd "$INTEGRATION" && "$PYTHON" -m pytest tests/unit tests/test_package_layout.py -q -p asyncio --asyncio-mode=auto)
}

run_sil() {
  (cd "$INTEGRATION" && BLHAOS_RUN_SIL=1 "$PYTHON" -m pytest tests/test_ha_integration_sil.py -q -p asyncio --asyncio-mode=auto)
}

run_frontend_unit() {
  (cd "$WEBUI" && npm test)
}

run_frontend_build() {
  (cd "$WEBUI" && npm run build)
}

run_frontend_e2e() {
  (cd "$WEBUI" && npm run test:e2e)
}

case "$LAYER" in
  L0) run_frontend_build ;;
  L1)
    run_bridge
    run_integration_unit
    run_frontend_unit
    ;;
  L2) run_sil ;;
  L3)
    run_frontend_unit
    run_frontend_e2e
    ;;
  all)
    run_bridge
    run_integration_unit
    run_sil
    run_frontend_unit
    run_frontend_build
    ;;
  *)
    echo "Usage: $0 [L0|L1|L2|L3|all]" >&2
    exit 1
    ;;
esac

echo "==> Layer '$LAYER' completed successfully"
