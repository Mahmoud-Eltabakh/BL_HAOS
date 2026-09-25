"""End-to-end UI check for the BL-HAOS Ingress dashboard and HA media player.

Prints a pass/fail report for the surfaces an operator sees:

  * the Ingress page and the bundle it actually serves
  * the bridge HTTP API the UI depends on
  * the Home Assistant `media_player` attributes the Lovelace card renders

Usage:
    set HATOK=<long-lived-token>
    python ui_check.py [--host homeassistant.local:8123] [--entity media_player.your_speaker]

Host, entity, token, ingress session/URL, and the probe media URL come from
arguments or environment variables; see the *_ENV_VAR constants below. The
media-playback section is skipped, and says so, when the probe URL is unset.

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
DEFAULT_ENTITY = os.environ.get(ENTITY_ENV_VAR, "media_player.bl_haos_speaker")
DEFAULT_TTS_ENTITY = os.environ.get(TTS_ENTITY_ENV_VAR, "tts.google_translate_en_com")
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


def check(label: str, ok: bool, detail: str = "") -> None:
    """Record and print one assertion outcome."""
    print(f"  {'OK  ' if ok else 'FAIL'}  {label}{(' -> ' + detail) if detail else ''}")
    if not ok:
        _failures.append(label)


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


def ha_get(host: str, token: str, path: str) -> dict:
    request = urllib.request.Request(f"http://{host}{path}", headers={AUTHORIZATION_HEADER: f"{BEARER_PREFIX}{token}"})
    return json.loads(urllib.request.urlopen(request, timeout=TIMEOUT).read())


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
        return f"HTTP {error.code}"


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


def check_card(host: str, token: str, entity: str) -> None:
    print(f"\n[3] Home Assistant media_player card ({entity})")

    def attributes() -> dict:
        state = ha_get(host, token, f"{HA_STATES_PATH}/{entity}")
        return {"state": state["state"], **state.get("attributes", {})}

    idle = attributes()
    check("idle card has no stale title", not idle.get("media_title"), repr(idle.get("media_title")))

    media = os.environ.get(MEDIA_URL_ENV_VAR, "")
    if not media:
        print(f"  SKIP  media playback checks ({MEDIA_URL_ENV_VAR} is not set)")
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
    tts = ha_service(
        host, token, "tts", "speak",
        {
            "entity_id": DEFAULT_TTS_ENTITY,
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


def main() -> int:
    parser = argparse.ArgumentParser(description="BL-HAOS UI check")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--entity", default=DEFAULT_ENTITY)
    parser.add_argument("--session", default=os.environ.get(INGRESS_SESSION_ENV_VAR, ""))
    arguments = parser.parse_args()

    token = os.environ.get(TOKEN_ENV_VAR, "").strip()
    if not token:
        print(f"{TOKEN_ENV_VAR} (long-lived Home Assistant token) is required", file=sys.stderr)
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
    check_card(arguments.host, token, arguments.entity)

    print()
    if _failures:
        print(f"FAILED {len(_failures)} check(s):")
        for failure in _failures:
            print(f"  - {failure}")
        return 1
    print("All UI checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
