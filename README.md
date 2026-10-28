# BL-HAOS

## Phase 24 Media Catalog (Local, Undeployed)

The integrated bridge release 0.2.69 and production panel are undeployed.
Local Core 2026.10.3 tests do not prove actual provider layout, session expiry
or physical audio. Deployment requires separate authorization; the temporary
contract probe was removed after its one permitted restart.

After authorized installation, use **Native Browse Media** on a speaker or
**Open Media Catalog** beside Home Assistant Native integration in Ingress.
The link opens HA's **BL-HAOS Media** panel at `/bl-haos-media`. In **Play on**,
select exactly one connected BL-HAOS speaker, browse the audio provider hierarchy
and press **Play** on an item or playlist. The original opaque reference reaches
native `media_player.play_media` unchanged;
HA owns provider authentication and reference resolution. A provider playlist
stays one reference, not a local queue. Submission does not prove audible playback.

The panel does not store browser/add-on HA/provider credentials, proxy a bridge
catalog, call providers directly, or accept raw playback URLs. Existing native
direct-URL support is not a catalog fallback. The local Phase 25 candidate uses
the authenticated panel and HA-owned storage for custom playlists of ordered
Home Assistant media references and one-reference provider shortcuts; provider
tracks are not copied. Explicit availability checks browse the exact HA media
reference only; they do not resolve or play media and never rewrite saved IDs.
This remains local/mock behavior: Phase 24 production requirements are pending,
T-24-15 remains OPEN/HIGH, and T-24-16 remains OPEN/MEDIUM. Phase 26 owns
playback and queue controls. Release and deployment are not approved. See
[TESTING.md](TESTING.md) for local versus separately authorized host checks.
Retired Docker E2E and demo fixtures are not host proof.

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
4. Install the integration and restart Home Assistant Core. It connects to the Bridge automatically via Supervisor discovery and refreshes its credential if the add-on rotates it; only fall back to entering the Bridge endpoint and token manually if discovery doesn't complete the setup prompt.

## Development

```powershell
git clone --recurse-submodules https://github.com/Mahmoud-Eltabakh/BL_HAOS.git
```

Develop and release the Bridge and Integration from their own repositories. This repository retains project coordination and planning artifacts.

## Testing & Verification

Run the module-local unit and system-level tests with `pytest tests/ -q`.
For HAOS behavior, use a Home Assistant OS virtual machine with the add-on
and integration installed; validate pairing, playback, ingress, recovery,
and native `media_player` control against the live VM.

## Security

The Bridge add-on runs as **root with `full_access` and host D-Bus access**, because
host Bluetooth and audio are the point of the product — treat it as host-root software
and only deploy it where you are willing to grant that authority. Threat analysis for
the add-on, the integration and the native transport is kept as an untracked review
artifact (`THREAT-MODEL.md` in a working copy) rather than in source control.

Report a vulnerability through GitHub's private vulnerability reporting on the module
repositories (**Security → Report a vulnerability**) rather than in a public issue.
