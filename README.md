# BL-HAOS

BL-HAOS is the umbrella project for Bluetooth audio playback on Home Assistant OS. It is split into two independently versioned modules.

## Modules

| Module | Repository | Responsibility |
|---|---|---|
| Bridge | [BL-HAOS-Bridge](https://github.com/Mahmoud-Eltabakh/BL-HAOS-Bridge) | Privileged Home Assistant OS add-on: BlueZ, PipeWire, WirePlumber, Snapcast, playback, and authenticated REST/WebSocket bridge. |
| Integration | [BL-HAOS-Integration](https://github.com/Mahmoud-Eltabakh/BL-HAOS-Integration) | HACS custom integration: native `media_player` entities and Home Assistant config flow. |

The modules are included here as Git submodules under `modules/bridge` and `modules/integration`.

## Install

1. Add `https://github.com/Mahmoud-Eltabakh/BL-HAOS-Bridge` to the Home Assistant Add-on Store.
2. Install and start **BL-HAOS**.
3. Add `https://github.com/Mahmoud-Eltabakh/BL-HAOS-Integration` as a custom HACS Integration repository.
4. Install the integration and restart Home Assistant Core. It connects to the Bridge automatically via Supervisor discovery; only fall back to entering the Bridge endpoint and token manually if discovery doesn't complete the setup prompt.

## Development

```powershell
git clone --recurse-submodules https://github.com/Mahmoud-Eltabakh/BL_HAOS.git
```

Develop and release the Bridge and Integration from their own repositories. This repository retains project coordination and planning artifacts.

## Testing & Verification

Use the [canonical smoke matrix](tests/integration/SMOKE-MATRIX.md) to select
the deterministic, deep HAOS, or live Bluetooth validation lane. The
[CI gate contract](tests/integration/CI-GATES.md) defines blocking behavior,
required JUnit and coverage artifacts, and environment-qualified exceptions.

The fast local checks are:

```powershell
pytest tests/integration/tests/test_orchestration.py -q
pytest tests/ -q
```

The authoritative SIL evidence path requires Docker and is documented in the
matrix; live credentials and Bluetooth hardware are not required for SIL.
