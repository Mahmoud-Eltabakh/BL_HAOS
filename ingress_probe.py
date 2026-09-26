"""Probe Home Assistant for the BL-HAOS Supervisor add-on and its Ingress route.

Home Assistant no longer exposes a WebSocket command that lists Ingress panels
(``ingress/list`` and ``ingress/panels`` both answer ``unknown_command`` on
2026.9), so this probe asks Supervisor through the supported ``supervisor/api``
command instead - the same path the Home Assistant frontend uses to open an
add-on panel.

The add-on list only carries slug/version/state; the Ingress URL comes from the
per-add-on info endpoint, so the probe lists, selects, and then details.

Credentials: the Ingress *session* is reported as acquired and never printed.
The resolved Ingress URL is printed because it is needed to build requests, but
its path segment is a credential-like handle - redact it when sharing output.

Configuration comes from the environment (``HA_HOST``, ``HA_TOKEN``) or the
command line, so no LAN address, port, or credential is baked into the repo.

Usage:
    set HA_HOST=homeassistant.local:8123
    set HA_TOKEN=<long-lived-token>
    python ingress_probe.py [--slug c839f4a9_bl_haos]

Exit codes:
    0  the add-on was found and its Ingress URL plus session resolved
    1  the probe ran but could not resolve the add-on
    2  no token was supplied
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys

import aiohttp

HA_DEFAULT_PORT = 8123
HA_WEBSOCKET_PATH = "/api/websocket"
HA_HOST_ENV_VAR = "HA_HOST"
HA_TOKEN_ENV_VAR = "HA_TOKEN"
HA_AUTH_MESSAGE = "auth"
HA_AUTH_REQUIRED = "auth_required"
HA_AUTH_OK = "auth_ok"
SUPERVISOR_API_COMMAND = "supervisor/api"
ADDONS_ENDPOINT = "/addons"
INGRESS_SESSION_ENDPOINT = "/ingress/session"
ADDON_SLUG_MARKER = "bl_haos"
ADDONS_MESSAGE_ID = 1
ADDON_INFO_MESSAGE_ID = 2
SESSION_MESSAGE_ID = 3
DEFAULT_HOST = os.environ.get(HA_HOST_ENV_VAR, f"homeassistant.local:{HA_DEFAULT_PORT}")


class ProbeError(RuntimeError):
    """A probe step returned something other than a usable result."""


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Probe the BL-HAOS add-on Ingress route")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Home Assistant host[:port]")
    parser.add_argument("--token", default=os.environ.get(HA_TOKEN_ENV_VAR, ""), help="long-lived HA token")
    parser.add_argument(
        "--slug",
        default="",
        help=f"add-on slug to probe (default: the single slug containing {ADDON_SLUG_MARKER!r})",
    )
    return parser.parse_args()


async def _call(socket, message_id: int, message: dict) -> dict:
    """Send one WebSocket command and return its result, or raise ProbeError."""
    await socket.send_json({**message, "id": message_id})
    while True:
        reply = await socket.receive_json()
        if reply.get("id") != message_id:
            continue
        if not reply.get("success"):
            raise ProbeError(f"{message['type']} failed: {reply.get('error')}")
        result = reply.get("result")
        return result if isinstance(result, dict) else {"result": result}


def _select_slug(payload: dict, slug: str) -> str | None:
    """Print the add-on inventory and return the slug to detail."""
    addons = payload.get("addons")
    if not isinstance(addons, list) or not addons:
        print("supervisor returned no add-ons", file=sys.stderr)
        return None
    entries = [addon for addon in addons if isinstance(addon, dict)]
    for addon in entries:
        print(
            "addon: slug=%s version=%s state=%s"
            % (addon.get("slug"), addon.get("version"), addon.get("state"))
        )
    if slug:
        matched = [addon for addon in entries if addon.get("slug") == slug]
    else:
        matched = [addon for addon in entries if ADDON_SLUG_MARKER in str(addon.get("slug", ""))]
    if not matched:
        print(f"no add-on matched {slug or ADDON_SLUG_MARKER!r}; pass --slug", file=sys.stderr)
        return None
    if len(matched) > 1:
        print(
            f"several add-ons matched; pass --slug: {[addon.get('slug') for addon in matched]}",
            file=sys.stderr,
        )
        return None
    return str(matched[0].get("slug"))


def _describe_addon(info: dict) -> str | None:
    """Print the selected add-on and return its Ingress URL, if it has one."""
    ingress = info.get("ingress_url")
    print(
        "add-on: %s %s (state=%s, ingress_panel=%s)"
        % (info.get("name"), info.get("version"), info.get("state"), info.get("ingress_panel"))
    )
    if not ingress:
        print(f"add-on {info.get('slug')} has no Ingress panel", file=sys.stderr)
        return None
    print(f"ingress: {ingress}")
    return str(ingress)


async def main() -> int:
    arguments = _parse_args()
    token = arguments.token.strip()
    if not token:
        print(f"{HA_TOKEN_ENV_VAR} (long-lived Home Assistant token) is required", file=sys.stderr)
        return 2

    try:
        async with aiohttp.ClientSession() as session:
            socket = await session.ws_connect(f"ws://{arguments.host}{HA_WEBSOCKET_PATH}")
            async with socket:
                hello = await socket.receive_json()
                if hello.get("type") != HA_AUTH_REQUIRED:
                    print(f"unexpected websocket handshake: {hello.get('type')!r}", file=sys.stderr)
                    return 1
                await socket.send_json({"type": HA_AUTH_MESSAGE, "access_token": token})
                auth = await socket.receive_json()
                print("auth:", auth.get("type"))
                if auth.get("type") != HA_AUTH_OK:
                    return 1
                addons = await _call(
                    socket,
                    ADDONS_MESSAGE_ID,
                    {"type": SUPERVISOR_API_COMMAND, "endpoint": ADDONS_ENDPOINT, "method": "get"},
                )
                slug = _select_slug(addons, arguments.slug)
                if slug is None:
                    return 1
                info = await _call(
                    socket,
                    ADDON_INFO_MESSAGE_ID,
                    {
                        "type": SUPERVISOR_API_COMMAND,
                        "endpoint": f"{ADDONS_ENDPOINT}/{slug}/info",
                        "method": "get",
                    },
                )
                if _describe_addon(info) is None:
                    return 1
                issued = await _call(
                    socket,
                    SESSION_MESSAGE_ID,
                    {
                        "type": SUPERVISOR_API_COMMAND,
                        "endpoint": INGRESS_SESSION_ENDPOINT,
                        "method": "post",
                        "data": {},
                    },
                )
    except (aiohttp.ClientError, ProbeError) as error:
        print(f"probe failed: {error}", file=sys.stderr)
        return 1

    issued_session = str(issued.get("session") or "")
    if not issued_session:
        print("supervisor returned no Ingress session", file=sys.stderr)
        return 1
    print(f"ingress session: acquired ({len(issued_session)} chars, value never printed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
