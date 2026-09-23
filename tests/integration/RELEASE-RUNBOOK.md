# BL-HAOS Release Runbook

This runbook is the operator path for one release candidate. It is fail-closed:
an unavailable environment is recorded as a blocker, never as a skipped pass.
Retain only redacted evidence under `tests/integration/reports/release/`.

## Lanes and prerequisites

| Lane | Environment | Evidence status |
|---|---|---|
| Deterministic | Windows, Linux, or CI with Python and Docker as declared | Required for every candidate |
| Deep HAOS | Linux/KVM, Docker, HAOS image/config, network | Required release evidence; unavailable means `blocked` |
| Live hardware | Reachable HAOS, approved adapter/speaker/media item, `HA_URL`, `HA_WS`, `HA_TOKEN` in the process environment | Required for hardware claims; unavailable means `blocked` |
| Architecture build | Linux CI, Buildx/QEMU, registry credentials | Required for architecture claims; local Windows cannot substitute |

The native integration and add-on must refer to the same candidate version. Never
put a host, token, raw WebSocket frame, private media URL, PIN, or full device
address in retained evidence.

## 1. Deterministic gates

From the repository root, run in order and preserve each exit status:

```text
python -m pytest tests/integration/tests/test_release_contract.py tests/integration/tests/test_orchestration.py tests/integration/tests/test_release_evidence.py -q
python -m pytest modules/bridge/tests/test_demo_mode.py -q
python -m pytest tests/ -q
docker compose -f tests/integration/docker-compose.yml build test-runner
docker compose -f tests/integration/docker-compose.yml run --rm test-runner
```

Require the five reports under `tests/integration/reports/`: the two per-suite
JUnit files, `sil-junit.xml`, `coverage.xml`, and non-empty `coverage-html/`.
Run dependency/security audits exactly as specified by `RELEASE-GATES.md`; a
missing tool is a dependency or infrastructure blocker, not a pass.

## 2. HAOS read-only preflight

Set `HA_URL`, `HA_WS`, and `HA_TOKEN` only in the local process environment.
The first live command is read-only and resolves the add-on slug from
authenticated Supervisor metadata:

```text
python query_ha.py preflight
```

Capture only add-on slug/state, version, architecture/build identity, native
config-entry count, entity availability, and bounded health results. If this
fails, stop the live lane and record the owner plus this exact rerun command.

## 3. Candidate lifecycle and smoke checks

After preflight passes, every mutation requires the explicit guard:

```text
python query_ha.py addon-stop --apply
python query_ha.py addon-start --apply
python query_ha.py addon-restart --apply
python query_ha.py native-setup --apply
python query_ha.py play-media --apply --entity-id media_player.<approved_entity> --media-id <approved_media_id> --media-type <approved_media_type>
```

Observe bounded startup/health, connect, disconnect, reconnect, and playback
failure behavior. A live hardware lane additionally requires operator audible
confirmation. Demo/SIL scenarios remain hardware-free and deterministic.

## 4. Upgrade and rollback rehearsal

Before updating, record the current known-good add-on version, image/build
identity, options/config snapshot, native config-entry/entity presence, and the
approved rollback target or Supervisor backup identifier. Do not proceed without
a known-good target and a bounded recovery owner.

1. Run `preflight` and save the redacted baseline.
2. Preserve the config/backup and record candidate version, architecture, and
   image digest when Supervisor exposes it.
3. Install/update the candidate through the Supervisor UI or approved release
   mechanism. Do not invent an unguarded API mutation.
4. Verify add-on state, diagnostics/health, native config entry/entity, and the
   bounded playback acknowledgement.
5. Trigger rollback if startup health, native control, reconnect, or playback
   fails, or if recovery exceeds the bounded operator timeout.
6. Restore the known-good version/image or backup, then run the guarded start
   and `python query_ha.py preflight` again.
7. Confirm the restored version/identity, add-on health, native config/entity,
   and bounded playback acknowledgement. Record both observed versions and the
   rollback result.

Rollback is `HOLD` until the post-rollback native path is verified. A Windows
workstation cannot prove HAOS upgrade/rollback or Bluetooth behavior.

## 5. Evidence and decision

Create `tests/integration/reports/release/evidence.json` with the candidate
identity, timestamped command exit statuses, all required gate statuses, report
paths, and blocker records containing `gate`, `owner`, and `rerun_command`.
Then run:

```text
python tests/integration/scripts/validate-release-evidence.py --evidence-dir tests/integration/reports/release
```

The release owner signs `GO-LIVE-READOUT.md` only after inspecting redaction,
identity, upgrade/rollback, and every blocker. `GO` is prohibited for any
non-passing gate or unresolved environment-qualified blocker.