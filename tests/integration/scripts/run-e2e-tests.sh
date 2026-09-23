#!/bin/bash
# ==============================================================================
# BL-HAOS: full-stack E2E simulation runner
# ------------------------------------------------------------------------------
# Launches the real bridge container (Docker) across every demo scenario and
# drives it over real HTTP/WebSocket, exercising:
#   - connect device      (adapters/devices visible)
#   - connect integration  (real in-process Home Assistant + real network)
#   - play music           (native play/pause/set_volume/play_media commands)
#   - edge cases            (bad token, bad payloads, disconnected speaker)
#   - recovery              (recovery contract + recovery actions)
#   - all implemented features (health, diagnostics, support bundle redaction)
#
# Usage:
#   ./tests/integration/scripts/run-e2e-tests.sh                 # all scenarios
#   ./tests/integration/scripts/run-e2e-tests.sh healthy         # one scenario
#
# Requires: Docker + Docker Compose v2 ("docker compose").
#
# When you add a feature, add its coverage here too -- see
# .github/skills/update-e2e-tests/SKILL.md.
# ==============================================================================

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_DIR="$SCRIPT_DIR/.."
COMPOSE_FILE="$COMPOSE_DIR/docker-compose.e2e.yml"
REPORTS_DIR="$COMPOSE_DIR/reports"
COMPOSE="docker compose -f $COMPOSE_FILE"

# Every scenario the demo runtime supports (modules/bridge/backend/bl_haos/demo.py).
ALL_SCENARIOS="healthy pairing_failure sink_missing reconnect_exhausted native_integration_unavailable restart_degraded"
SCENARIOS="${1:-$ALL_SCENARIOS}"

mkdir -p "$REPORTS_DIR"
overall_status=0
declare -A scenario_status

cleanup() {
    $COMPOSE down --remove-orphans >/dev/null 2>&1
}
trap cleanup EXIT

wait_for_bridge() {
    echo "==> Waiting for bridge health endpoint..."
    for _ in $(seq 1 60); do
        if $COMPOSE exec -T bridge curl -sf http://localhost:8099/api/health >/dev/null 2>&1; then
            return 0
        fi
        sleep 1
    done
    echo "ERROR: bridge never became healthy" >&2
    return 1
}

# pytest-homeassistant-custom-component blocks DNS resolution of non-literal
# hostnames in every test (even with the socket_enabled fixture), so the
# runner must talk to the bridge's raw container IP, not the "bridge" DNS name.
resolve_bridge_ip() {
    docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' bl_haos_e2e_bridge 2>/dev/null
}

for scenario in $SCENARIOS; do
    echo ""
    echo "=================================================================="
    echo "==> Scenario: $scenario"
    echo "=================================================================="

    export BLHAOS_DEMO_SCENARIO="$scenario"

    echo "==> Building and starting bridge for scenario '$scenario'"
    $COMPOSE up -d --build --force-recreate bridge
    if ! wait_for_bridge; then
        scenario_status[$scenario]=2
        overall_status=1
        $COMPOSE logs bridge
        continue
    fi

    echo "==> Running E2E scenario suite against the live bridge"
    bridge_ip=$(resolve_bridge_ip)
    if [ -z "$bridge_ip" ]; then
        echo "ERROR: could not resolve bridge container IP" >&2
        scenario_status[$scenario]=2
        overall_status=1
        continue
    fi
    $COMPOSE run --rm -e BRIDGE_URL="http://$bridge_ip:8099" -e BLHAOS_DEMO_SCENARIO="$scenario" e2e-runner
    result=$?
    scenario_status[$scenario]=$result
    if [ "$result" -ne 0 ]; then
        overall_status=1
        echo "==> Scenario '$scenario' FAILED (exit $result); dumping bridge logs"
        $COMPOSE logs bridge
    fi

    $COMPOSE stop bridge >/dev/null 2>&1
done

echo ""
echo "=================================================================="
echo "==> E2E summary"
echo "=================================================================="
for scenario in $SCENARIOS; do
    status="${scenario_status[$scenario]:-unknown}"
    if [ "$status" = "0" ]; then
        echo "  PASS  $scenario"
    else
        echo "  FAIL  $scenario (exit $status)"
    fi
done
echo "Reports written to: $REPORTS_DIR"
echo "Overall status: $overall_status"

exit "$overall_status"
