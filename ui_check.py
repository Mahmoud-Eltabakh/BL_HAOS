"""End-to-end UI check for the BL-HAOS Ingress dashboard and HA media player.

Prints a pass/fail report for the surfaces an operator sees:

  * the Ingress page and the bundle it actually serves
  * the bridge HTTP API the UI depends on
  * the Home Assistant `media_player` attributes the Lovelace card renders

Usage:
    set HATOK=<long-lived-token>
    python ui_check.py [--host homeassistant.local:8123] [--entity media_player.speaker]

Host, token, ingress session/URL, TTS entity, and the probe media URL come from
arguments or environment variables; see the *_ENV_VAR constants below. When
--entity is omitted the native BL-HAOS media_player is discovered from its
published attributes, so no installation-specific entity id is baked into this
file.

Sections that the current environment cannot evaluate are reported as SKIP, not
FAIL: the media-playback section when no probe URL is set, and both playback and
text-to-speech when the speaker is not connected (media_player state "off"),
which is a hardware state rather than a regression.

The script only reads state plus one short playback so the card can be
inspected; it leaves nothing playing.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from http import HTTPStatus
from typing import Any

import aiohttp

TIMEOUT = 30
# Home Assistant and Supervisor protocol vocabulary used by the checks below.
HA_WEBSOCKET_PATH = "/api/websocket"
HA_SERVICE_PATH = "/api/services"
HA_STATES_PATH = "/api/states"
SUPERVISOR_INGRESS_SESSION_ENDPOINT = "/ingress/session"
SUPERVISOR_ADDON_INFO_ENDPOINT = "/addons/c839f4a9_bl_haos/info"
SUPERVISOR_API_COMMAND = "supervisor/api"
AUTHORIZATION_HEADER = "Authorization"
COOKIE_HEADER = "Cookie"
CONTENT_TYPE_HEADER = "Content-Type"
INGRESS_SESSION_COOKIE = "ingress_session"
BEARER_PREFIX = "Bearer "
JSON_CONTENT_TYPE = "application/json"
SERVICE_CALL_TIMEOUT_SECONDS = 120
MEDIA_PROBE_SETTLE_SECONDS = 6
PAUSE_SETTLE_SECONDS = 2
BRIDGE_STATUS_OK = "ok"
BRIDGE_STATUS_HEALTHY = "healthy"
HA_STATE_IDLE = "idle"
HA_STATE_PLAYING = "playing"
HA_STATE_PAUSED = "paused"
# Bridge-side label for Home Assistant text-to-speech streams.
TTS_STREAM_TITLE = "Text to speech"
TTS_PROBE_MESSAGE = "UI check."
TTS_PROBE_TIMEOUT_SECONDS = 8
TTS_POLL_INTERVAL_SECONDS = 0.4
HA_DEFAULT_PORT = 8123
# Environment variables that override every installation-specific value, so no
# host, entity, or probe URL has to be edited into this file.
TOKEN_ENV_VAR = "HATOK"
HOST_ENV_VAR = "BLHAOS_HOST"
ENTITY_ENV_VAR = "BLHAOS_ENTITY"
TTS_ENTITY_ENV_VAR = "BLHAOS_TTS"
INGRESS_SESSION_ENV_VAR = "BLHAOS_INGRESS_SESSION"
INGRESS_URL_ENV_VAR = "BLHAOS_INGRESS_URL"
MEDIA_URL_ENV_VAR = "BLHAOS_UI_CHECK_MEDIA"
DEFAULT_HOST = os.environ.get(HOST_ENV_VAR, f"homeassistant.local:{HA_DEFAULT_PORT}")
# Empty means "discover the native entity from its published attributes"; the
# deployed entity id is derived from the speaker name, so any hardcoded default
# would only ever be right for one installation.
DEFAULT_ENTITY = os.environ.get(ENTITY_ENV_VAR, "")
DEFAULT_TTS_ENTITY = os.environ.get(TTS_ENTITY_ENV_VAR, "tts.google_translate_en_com")
# The native BL-HAOS media_player publishes these attributes (bridge
# native_speaker_record -> integration extra_state_attributes). Their presence
# is what identifies it, so the check never has to be told an entity id.
NATIVE_ENTITY_ATTRIBUTES = ("bluetooth_address", "adapter")
ENTITY_PREFIX = "media_player."
HA_STATE_OFF = "off"
# Strings that must have disappeared with the operator panels (bridge 0.2.50).
REMOVED_FROM_UI = (
    "Export support bundle",
    "Guided recovery",
    "executeRecovery",
    "support/bundle",
)
# Strings the simplified dashboard must still offer.
PRESENT_IN_UI = (
    "Add Speaker",
    "Home Assistant Native integration",
    "Speakers",
    "Adapters",
)
# path -> expected status code
API_SURFACE = (
    ("/api/health", HTTPStatus.OK),
    ("/api/adapters", HTTPStatus.OK),
    ("/api/devices?audio_only=false", HTTPStatus.OK),
    ("/api/recovery", HTTPStatus.NOT_FOUND),
    ("/api/support/bundle", HTTPStatus.NOT_FOUND),
    ("/api/diagnostics", HTTPStatus.NOT_FOUND),
)

_failures: list[str] = []
_skipped: list[str] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    """Record and print one assertion outcome."""
    print(f"  {'OK  ' if ok else 'FAIL'}  {label}{(' -> ' + detail) if detail else ''}")
    if not ok:
        _failures.append(label)


def skip(label: str, reason: str) -> None:
    """Record a check the current environment cannot evaluate.

    A skip is deliberately not a failure: an offline speaker or an unset probe
    URL must not make a healthy installation look broken, but it must also stay
    visible so nobody mistakes a skip for a pass.
    """
    print(f"  SKIP  {label} ({reason})")
    _skipped.append(f"{label}: {reason}")


def opener(session: str) -> urllib.request.OpenerDirector:
    build = urllib.request.build_opener()
    build.addheaders = [(COOKIE_HEADER, f"{INGRESS_SESSION_COOKIE}={session}")]
    return build


def fetch(op: urllib.request.OpenerDirector, url: str) -> str:
    return op.open(url, timeout=TIMEOUT).read().decode(errors="replace")


def status_of(op: urllib.request.OpenerDirector, url: str) -> int:
    try:
        return op.open(url, timeout=TIMEOUT).getcode()
    except urllib.error.HTTPError as error:
        return error.code


async def supervisor(host: str, token: str) -> tuple[str, dict]:
    """Return an ingress session token and the add-on info payload."""
    async with aiohttp.ClientSession() as session:
        socket = await session.ws_connect(f"ws://{host}{HA_WEBSOCKET_PATH}")
        await socket.receive()
        await socket.send_json({"type": "auth", "access_token": token})
        await socket.receive()

        async def call(message_id: int, message: dict) -> dict:
            message["id"] = message_id
            await socket.send_json(message)
            while True:
                reply = await socket.receive()
                if reply.type == aiohttp.WSMsgType.TEXT:
                    payload = json.loads(reply.data)
                    if payload.get("id") == message_id:
                        return payload

        session_reply = await call(
            1, {"type": SUPERVISOR_API_COMMAND, "endpoint": SUPERVISOR_INGRESS_SESSION_ENDPOINT, "method": "post", "data": {}}
        )
        info = await call(
            2, {"type": SUPERVISOR_API_COMMAND, "endpoint": SUPERVISOR_ADDON_INFO_ENDPOINT, "method": "get"}
        )
        return session_reply.get("result", {}).get("session", ""), info.get("result", {})


def ha_get(host: str, token: str, path: str) -> Any:
    request = urllib.request.Request(f"http://{host}{path}", headers={AUTHORIZATION_HEADER: f"{BEARER_PREFIX}{token}"})
    return json.loads(urllib.request.urlopen(request, timeout=TIMEOUT).read())


def response_detail(error: urllib.error.HTTPError) -> str:
    """Return Home Assistant's own error message from a failed request.

    A service call that fails answers with a body carrying the reason, for
    example "Failed to play_media: Native speaker was not found". Reporting only
    "HTTP 500" throws away the one line an operator needs to act on.
    """
    try:
        payload = json.loads(error.read().decode(errors="replace"))
    except (ValueError, OSError):
        return ""
    if not isinstance(payload, dict):
        return ""
    for key in ("message", "detail", "error"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()[:200]
    return ""


def ha_service(host: str, token: str, domain: str, service: str, payload: dict) -> str:
    request = urllib.request.Request(
        f"http://{host}{HA_SERVICE_PATH}/{domain}/{service}",
        data=json.dumps(payload).encode(),
        headers={AUTHORIZATION_HEADER: f"{BEARER_PREFIX}{token}", CONTENT_TYPE_HEADER: JSON_CONTENT_TYPE},
    )
    try:
        urllib.request.urlopen(request, timeout=SERVICE_CALL_TIMEOUT_SECONDS)
        return "ok"
    except urllib.error.HTTPError as error:
        detail = response_detail(error)
        return f"HTTP {error.code}{(': ' + detail) if detail else ''}"


def discover_entity(host: str, token: str) -> tuple[list[str], list[str]]:
    """Find the native BL-HAOS media_player from its published attributes.

    Returns the matching entity ids plus every media_player id seen, so the
    caller can report what actually exists instead of a hardcoded guess.
    """
    states = ha_get(host, token, HA_STATES_PATH)
    matches: list[str] = []
    candidates: list[str] = []
    if not isinstance(states, list):
        return matches, candidates
    for state in states:
        entity_id = state.get("entity_id")
        if not isinstance(entity_id, str) or not entity_id.startswith(ENTITY_PREFIX):
            continue
        candidates.append(entity_id)
        attributes = state.get("attributes") or {}
        if all(key in attributes for key in NATIVE_ENTITY_ATTRIBUTES):
            matches.append(entity_id)
    return sorted(matches), sorted(candidates)


def check_ui(op: urllib.request.OpenerDirector, base: str) -> None:
    print("\n[1] Ingress dashboard")
    page = fetch(op, base + "/")
    title = re.search(r"<title>(.*?)</title>", page)
    check("page title", bool(title), title.group(1) if title else "missing")
    check("root element", 'id="root"' in page)

    bundle = re.search(r"assets/(index-[A-Za-z0-9_-]+\.js)", page)
    styles = re.search(r"assets/(index-[A-Za-z0-9_-]+\.css)", page)
    if not bundle:
        check("js bundle referenced", False, "no assets/index-*.js in index.html")
        return
    check("js bundle referenced", True, bundle.group(1))
    check("css bundle referenced", bool(styles), styles.group(1) if styles else "missing")

    script = fetch(op, f"{base}/assets/{bundle.group(1)}")
    check("bundle downloaded", len(script) > 10000, f"{len(script)} bytes")
    for needle in PRESENT_IN_UI:
        check(f"UI shows {needle!r}", needle in script)
    for needle in REMOVED_FROM_UI:
        check(f"UI no longer contains {needle!r}", needle not in script)

    print("\n[2] Bridge API the UI calls")
    for path, expected in API_SURFACE:
        code = status_of(op, base + path)
        check(f"{path} -> {code}", code == expected, f"expected {expected}")
    health = json.loads(fetch(op, base + "/api/health"))
    check("bridge dbus connected", health.get("dbus_connected") is True)
    check("bridge status healthy", health.get("status") in {BRIDGE_STATUS_OK, BRIDGE_STATUS_HEALTHY}, str(health.get("status")))


def check_card(host: str, token: str, entity: str, tts_entity: str | None) -> None:
    print(f"\n[3] Home Assistant media_player card ({entity})")

    def attributes() -> dict:
        state = ha_get(host, token, f"{HA_STATES_PATH}/{entity}")
        return {"state": state["state"], **state.get("attributes", {})}

    idle = attributes()
    check("idle card has no stale title", not idle.get("media_title"), repr(idle.get("media_title")))

    # A disconnected speaker reports "off", and every command against it answers
    # "Native speaker is not trusted or not an audio sink". That is the state of
    # the hardware, not a defect in the bridge, so it must not fail an otherwise
    # healthy installation.
    if idle.get("state") == HA_STATE_OFF:
        offline = "the speaker is not connected (media_player state is 'off')"
        skip("media playback checks", offline)
        skip("text-to-speech labelling", offline)
        return

    media = os.environ.get(MEDIA_URL_ENV_VAR, "")
    if not media:
        skip("media playback checks", f"{MEDIA_URL_ENV_VAR} is not set")
    else:
        result = ha_service(
            host, token, "media_player", "play_media",
            {"entity_id": entity, "media_content_type": "music", "media_content_id": media},
        )
        check("play_media accepted", result == "ok", result)
        time.sleep(MEDIA_PROBE_SETTLE_SECONDS)  # let the background probe publish duration

        playing = attributes()
        check("state is playing", playing.get("state") == HA_STATE_PLAYING, str(playing.get("state")))
        check("card shows a title", bool(playing.get("media_title")), repr(playing.get("media_title")))
        check("card shows the duration", isinstance(playing.get("media_duration"), int),
              str(playing.get("media_duration")))
        check("card shows the position", isinstance(playing.get("media_position"), int),
              str(playing.get("media_position")))
        check("card stamps the position", bool(playing.get("media_position_updated_at")))

        ha_service(host, token, "media_player", "media_pause", {"entity_id": entity})
        paused = attributes()
        time.sleep(PAUSE_SETTLE_SECONDS)
        check("pause freezes the clock", paused.get("media_position") == attributes().get("media_position"))
        check("pause is reflected in the card", paused.get("state") == HA_STATE_PAUSED, str(paused.get("state")))

        ha_service(host, token, "media_player", "media_stop", {"entity_id": entity})
        stopped = attributes()
        check("stop clears the card", stopped.get("state") == HA_STATE_IDLE and not stopped.get("media_title"))

    print("\n[4] Text-to-speech labelling")
    if not tts_entity:
        skip("text-to-speech labelling", "no TTS entity was provided")
        return
    try:
        ha_get(host, token, f"{HA_STATES_PATH}/{tts_entity}")
    except urllib.error.HTTPError as error:
        skip("text-to-speech labelling", f"{tts_entity} is not available here (HTTP {error.code})")
        return
    tts = ha_service(
        host, token, "tts", "speak",
        {
            "entity_id": tts_entity,
            "media_player_entity_id": entity,
            "message": TTS_PROBE_MESSAGE,
        },
    )
    check("tts.speak accepted", tts == "ok", tts)
    deadline = time.time() + TTS_PROBE_TIMEOUT_SECONDS
    seen = None
    while time.time() < deadline:
        current = attributes()
        if current.get("state") == HA_STATE_PLAYING and current.get("media_title"):
            seen = current["media_title"]
            break
        time.sleep(TTS_POLL_INTERVAL_SECONDS)
    check("tts stream is labelled", seen == TTS_STREAM_TITLE, repr(seen))
    ha_service(host, token, "media_player", "media_stop", {"entity_id": entity})


def resolve_entity(host: str, token: str, requested: str) -> str:
    """Return the native media_player to check, discovering it when unspecified."""
    if requested:
        return requested
    matches, candidates = discover_entity(host, token)
    if len(matches) == 1:
        print(f"entity: {matches[0]} (discovered)")
        return matches[0]
    if matches:
        print(
            "several BL-HAOS media players are present; choose one with --entity or "
            f"{ENTITY_ENV_VAR}: {', '.join(matches)}",
            file=sys.stderr,
        )
        return ""
    print(
        f"no BL-HAOS media player (attributes: {', '.join(NATIVE_ENTITY_ATTRIBUTES)}) was found. "
        f"Pass --entity or {ENTITY_ENV_VAR}; Home Assistant reports: "
        f"{', '.join(candidates) if candidates else 'no media_player entities'}",
        file=sys.stderr,
    )
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(description="BL-HAOS UI check")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--entity", default=DEFAULT_ENTITY, help="BL-HAOS media_player id (default: discover it)")
    parser.add_argument("--tts", default=DEFAULT_TTS_ENTITY, help="TTS entity for the labelling check")
    parser.add_argument("--session", default=os.environ.get(INGRESS_SESSION_ENV_VAR, ""))
    arguments = parser.parse_args()

    token = os.environ.get(TOKEN_ENV_VAR, "").strip()
    if not token:
        print(f"{TOKEN_ENV_VAR} (long-lived Home Assistant token) is required", file=sys.stderr)
        return 2

    entity = resolve_entity(arguments.host, token, arguments.entity.strip())
    if not entity:
        return 2

    session = arguments.session
    ingress = os.environ.get(INGRESS_URL_ENV_VAR, "")
    version = "unknown"
    if not session or not ingress:
        session, info = asyncio.run(supervisor(arguments.host, token))
        ingress = ingress or str(info.get("ingress_url") or "")
        version = str(info.get("version"))
    if not ingress:
        print("could not resolve the add-on ingress URL", file=sys.stderr)
        return 2
    base = f"http://{arguments.host}{ingress.rstrip('/')}"
    print(f"add-on version: {version} | ingress: {ingress}")

    check_ui(opener(session), base)
    check_card(arguments.host, token, entity, arguments.tts.strip() or None)

    print()
    if _skipped:
        print(f"SKIPPED {len(_skipped)} check group(s):")
        for item in _skipped:
            print(f"  - {item}")
    if _failures:
        print(f"FAILED {len(_failures)} check(s):")
        for failure in _failures:
            print(f"  - {failure}")
        return 1
    print("All UI checks passed." + (" (with skips)" if _skipped else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
