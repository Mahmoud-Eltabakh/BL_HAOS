"""End-to-end UI check for the BL-HAOS Ingress dashboard and HA media player.

Prints a pass/fail report for the surfaces an operator sees:

  * the Ingress page and the bundle it actually serves
  * the bridge HTTP API the UI depends on
  * the Home Assistant `media_player` attributes the Lovelace card renders

Usage:
    set HATOK=<long-lived-token>
    python ui_check.py [--host 192.168.1.21:8123] [--entity media_player.x]

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

import aiohttp

TIMEOUT = 30
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
    ("/api/health", 200),
    ("/api/adapters", 200),
    ("/api/devices?audio_only=false", 200),
    ("/api/recovery", 404),
    ("/api/support/bundle", 404),
    ("/api/diagnostics", 404),
)

_failures: list[str] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    """Record and print one assertion outcome."""
    print(f"  {'OK  ' if ok else 'FAIL'}  {label}{(' -> ' + detail) if detail else ''}")
    if not ok:
        _failures.append(label)


def opener(session: str) -> urllib.request.OpenerDirector:
    build = urllib.request.build_opener()
    build.addheaders = [("Cookie", f"ingress_session={session}")]
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
        socket = await session.ws_connect(f"ws://{host}/api/websocket")
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
            1, {"type": "supervisor/api", "endpoint": "/ingress/session", "method": "post", "data": {}}
        )
        info = await call(
            2, {"type": "supervisor/api", "endpoint": "/addons/c839f4a9_bl_haos/info", "method": "get"}
        )
        return session_reply.get("result", {}).get("session", ""), info.get("result", {})


def ha_get(host: str, token: str, path: str) -> dict:
    request = urllib.request.Request(f"http://{host}{path}", headers={"Authorization": f"Bearer {token}"})
    return json.loads(urllib.request.urlopen(request, timeout=TIMEOUT).read())


def ha_service(host: str, token: str, domain: str, service: str, payload: dict) -> str:
    request = urllib.request.Request(
        f"http://{host}/api/services/{domain}/{service}",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    try:
        urllib.request.urlopen(request, timeout=120)
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
    check("bridge status healthy", health.get("status") in {"ok", "healthy"}, str(health.get("status")))


def check_card(host: str, token: str, entity: str) -> None:
    print(f"\n[3] Home Assistant media_player card ({entity})")

    def attributes() -> dict:
        state = ha_get(host, token, f"/api/states/{entity}")
        return {"state": state["state"], **state.get("attributes", {})}

    idle = attributes()
    check("idle card has no stale title", not idle.get("media_title"), repr(idle.get("media_title")))

    media = os.environ.get(
        "BLHAOS_UI_CHECK_MEDIA",
        f"http://{host}/media/local/03.athan_fajr_Malek%20Chibat%20Al-Hamd.mp3",
    )
    result = ha_service(
        host, token, "media_player", "play_media",
        {"entity_id": entity, "media_content_type": "music", "media_content_id": media},
    )
    check("play_media accepted", result == "ok", result)
    time.sleep(6)  # let the background probe publish duration

    playing = attributes()
    check("state is playing", playing.get("state") == "playing", str(playing.get("state")))
    check("card shows a title", bool(playing.get("media_title")), repr(playing.get("media_title")))
    check("card shows the duration", isinstance(playing.get("media_duration"), int),
          str(playing.get("media_duration")))
    check("card shows the position", isinstance(playing.get("media_position"), int),
          str(playing.get("media_position")))
    check("card stamps the position", bool(playing.get("media_position_updated_at")))

    ha_service(host, token, "media_player", "media_pause", {"entity_id": entity})
    paused = attributes()
    time.sleep(2)
    check("pause freezes the clock", paused.get("media_position") == attributes().get("media_position"))
    check("pause is reflected in the card", paused.get("state") == "paused", str(paused.get("state")))

    ha_service(host, token, "media_player", "media_stop", {"entity_id": entity})
    stopped = attributes()
    check("stop clears the card", stopped.get("state") == "idle" and not stopped.get("media_title"))

    print("\n[4] Text-to-speech labelling")
    tts = ha_service(
        host, token, "tts", "speak",
        {
            "entity_id": os.environ.get("BLHAOS_UI_CHECK_TTS", "tts.google_translate_en_com"),
            "media_player_entity_id": entity,
            "message": "UI check.",
        },
    )
    check("tts.speak accepted", tts == "ok", tts)
    deadline = time.time() + 8
    seen = None
    while time.time() < deadline:
        current = attributes()
        if current.get("state") == "playing" and current.get("media_title"):
            seen = current["media_title"]
            break
        time.sleep(0.4)
    check("tts stream is labelled", seen == "Text to speech", repr(seen))
    ha_service(host, token, "media_player", "media_stop", {"entity_id": entity})


def main() -> int:
    parser = argparse.ArgumentParser(description="BL-HAOS UI check")
    parser.add_argument("--host", default=os.environ.get("BLHAOS_HOST", "192.168.1.21:8123"))
    parser.add_argument("--entity", default=os.environ.get("BLHAOS_ENTITY", "media_player.mdr_xb950n1"))
    parser.add_argument("--session", default=os.environ.get("BLHAOS_INGRESS_SESSION", ""))
    arguments = parser.parse_args()

    token = os.environ.get("HATOK", "").strip()
    if not token:
        print("HATOK (long-lived Home Assistant token) is required", file=sys.stderr)
        return 2

    session = arguments.session
    ingress = os.environ.get("BLHAOS_INGRESS_URL", "")
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
