#!/bin/sh

set -u

REPORTS_DIR=${REPORTS_DIR:-/reports}
WORKSPACE=${WORKSPACE:-/workspace}
BRIDGE_SUITE=modules/bridge/tests/test_bridge_sil.py
INTEGRATION_SUITE=modules/integration/tests/test_ha_integration_sil.py
BRIDGE_SOURCE=modules/bridge/backend
INTEGRATION_SOURCE=modules/integration/custom_components/bl_haos

export PYTHONPATH="$WORKSPACE/modules/bridge/backend:$WORKSPACE/modules/integration${PYTHONPATH:+:$PYTHONPATH}"

mkdir -p "$REPORTS_DIR"
cd "$WORKSPACE" || exit 1

echo "==> Preflighting SIL test dependencies"
if ! python -c 'import pytest, pytest_cov, pytest_homeassistant_custom_component'; then
    echo "ERROR: required SIL test dependencies are unavailable (pytest, pytest-cov, pytest-homeassistant-custom-component)" >&2
    exit 2
fi
if ! command -v pytest >/dev/null 2>&1; then
    echo "ERROR: pytest executable is unavailable" >&2
    exit 2
fi
if ! python -m pytest --version >/dev/null 2>&1; then
    echo "ERROR: pytest is unavailable for the configured Python interpreter" >&2
    exit 2
fi
if ! command -v coverage >/dev/null 2>&1; then
    echo "ERROR: coverage executable is unavailable; install pytest-cov" >&2
    exit 2
fi

coverage erase
rm -f "$REPORTS_DIR/bridge-junit.xml" "$REPORTS_DIR/integration-junit.xml" "$REPORTS_DIR/sil-junit.xml" "$REPORTS_DIR/coverage.xml"
rm -rf "$REPORTS_DIR/coverage-html"

bridge_status=0
integration_status=0

echo "==> Running bridge SIL suite: $BRIDGE_SUITE"
python -m pytest "$BRIDGE_SUITE" \
    --cov="$BRIDGE_SOURCE" \
    --cov="$INTEGRATION_SOURCE" \
    --cov-append \
    --junitxml="$REPORTS_DIR/bridge-junit.xml" || bridge_status=$?

echo "==> Running Home Assistant integration SIL suite: $INTEGRATION_SUITE"
python -m pytest "$INTEGRATION_SUITE" \
    --cov="$BRIDGE_SOURCE" \
    --cov="$INTEGRATION_SOURCE" \
    --cov-append \
    --junitxml="$REPORTS_DIR/integration-junit.xml" || integration_status=$?

echo "==> Merging per-suite JUnit reports"
python - "$REPORTS_DIR/bridge-junit.xml" "$REPORTS_DIR/integration-junit.xml" "$REPORTS_DIR/sil-junit.xml" <<'PY'
import sys
import xml.etree.ElementTree as ET

output = ET.Element("testsuites")
for report_path in sys.argv[1:3]:
    try:
        root = ET.parse(report_path).getroot()
    except (ET.ParseError, OSError) as error:
        print(f"WARNING: unable to merge {report_path}: {error}", file=sys.stderr)
        continue
    if root.tag == "testsuite":
        output.append(root)
    else:
        output.extend(root.findall("testsuite"))

ET.ElementTree(output).write(sys.argv[3], encoding="utf-8", xml_declaration=True)
PY
merge_status=$?

echo "==> Writing combined coverage reports"
coverage report -m
coverage_status=$?
coverage xml -o "$REPORTS_DIR/coverage.xml"
xml_status=$?
coverage html -d "$REPORTS_DIR/coverage-html"
html_status=$?

status=0
for result in "$bridge_status" "$integration_status" "$merge_status" "$coverage_status" "$xml_status" "$html_status"; do
    if [ "$result" -ne 0 ]; then
        status=1
    fi
done

echo "==> SIL runner status: $status (bridge=$bridge_status integration=$integration_status)"
exit "$status"