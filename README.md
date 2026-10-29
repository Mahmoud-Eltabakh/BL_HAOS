# BL-HAOS

## Phase 24 Media Catalog (Local, Undeployed)

The Phase 24 integrated bridge 0.2.69 catalog candidate is historical and
undeployed.
Local Core 2026.10.3 tests do not prove actual provider layout, session expiry
or physical audio. Deployment requires separate authorization; the temporary
contract probe was removed after its one permitted restart.

The Phase 38.1 local integration 0.2.24 candidate replaces the sidebar panel
with the full-feature `custom:bl-haos-media-card`. It is not published or
deployed. After separately authorized installation, add the card from the
Lovelace **Add card** picker, or use `initial_view: browse`; placement on a
dashboard is always a user action. The card shares the catalog, playlists,
queue controls, pairing, speaker management, and settings UI. **Native Browse
Media** remains available on a speaker.

The integration loads its versioned frontend module automatically; YAML
dashboards normally need no `resources:` entry. It does not create resources or
modify dashboards. The old `/bl-haos-media` panel and bookmarks are not
redirected; after the authorized upgrade, point saved links (including the old
**Open Media Catalog** destination) at the dashboard view containing the card.
In **Play on**, select exactly one connected BL-HAOS speaker, browse the audio
provider hierarchy and press **Play** on an item or playlist. The original
opaque reference reaches native `media_player.play_media` unchanged; HA owns
provider authentication and reference resolution. A provider playlist stays
one reference, not a local queue. Submission does not prove audible playback.

The dashboard card does not store browser/add-on HA/provider credentials, proxy a bridge
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

## Phase 38 historical candidate and migration

The local bridge 0.2.71 and integration 0.2.22 candidates retire the add-on
Ingress UI; the Home Assistant-native media and Speakers panels remain. Update
the integration first, back up existing configuration/data, then update the bridge
and check HA Repairs. Pairing, settings, and adapter controls use the integration
Speakers view, services, or options flow. The supported candidate pair is 0.2.71
/ 0.2.22; the integration minimum add-on version is 0.2.70. These versions are
not published or deployed. See module migration instructions; Phase 39 separately
gates publication, installation, deployment and live acceptance.

## Phase 38.1 dashboard card candidate

The integration 0.2.24 candidate retires the separate BL-HAOS Media sidebar
panel and loads `custom:bl-haos-media-card` through Home Assistant's
`frontend.add_extra_js_url` lifecycle. No Lovelace resource or dashboard write
is performed by the integration. The Add card picker and YAML configuration are
supported; YAML dashboards need no `resources:` entry unless a custom frontend
configuration disables extra-module loading, in which case use the documented
versioned manual resource fallback. The candidate is local only. Deployment,
host changes, dashboard edits, and placement still require their separate
authorization and exact target confirmation.

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
and integration installed; validate pairing, playback, recovery, and native
`media_player` control against the live VM. The add-on Ingress UI is retired.

## Security

The Bridge add-on runs as **root with `full_access` and host D-Bus access**, because
host Bluetooth and audio are the point of the product — treat it as host-root software
and only deploy it where you are willing to grant that authority. Threat analysis for
the add-on, the integration and the native transport is kept as an untracked review
artifact (`THREAT-MODEL.md` in a working copy) rather than in source control.

Report a vulnerability through GitHub's private vulnerability reporting on the module
repositories (**Security → Report a vulnerability**) rather than in a public issue.
