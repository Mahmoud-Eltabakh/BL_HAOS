#!/bin/sh
# Runs inside the e2e-runner container (see docker-compose.e2e.yml). Waits for
# the live bridge container and executes the real-network E2E scenario suite
# for exactly one demo scenario (BLHAOS_DEMO_SCENARIO). Invoked once per
# scenario by run-e2e-tests.sh; not meant to be run standalone from a host shell.

set -u

REPORTS_DIR=${REPORTS_DIR:-/reports}
WORKSPACE=${WORKSPACE:-/workspace}
SCENARIO=${BLHAOS_DEMO_SCENARIO:-healthy}
E2E_SUITE=tests/integration/tests/test_e2e_live_bridge.py

export PYTHONPATH="$WORKSPACE/modules/bridge/backend:$WORKSPACE/modules/integration${PYTHONPATH:+:$PYTHONPATH}"

mkdir -p "$REPORTS_DIR"
cd "$WORKSPACE" || exit 1

echo "==> Preflighting E2E test dependencies"
if ! python -c 'import pytest, httpx, pytest_homeassistant_custom_component'; then
    echo "ERROR: required E2E test dependencies are unavailable (pytest, httpx, pytest-homeassistant-custom-component)" >&2
    exit 2
fi

echo "==> Running E2E scenario suite for scenario '$SCENARIO': $E2E_SUITE"
python -m pytest "$E2E_SUITE" \
    --junitxml="$REPORTS_DIR/e2e-${SCENARIO}-junit.xml" \
    -v
status=$?

echo "==> E2E scenario '$SCENARIO' status: $status"
exit "$status"
