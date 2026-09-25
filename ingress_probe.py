"""Probe the Home Assistant WebSocket and list the Ingress panel registry.

Configuration comes from the environment (``HA_HOST``, ``HA_TOKEN``) or the
command line, so no LAN address, port, or credential is baked into the repo.

Usage:
    set HA_HOST=homeassistant.local:8123
    set HA_TOKEN=<long-lived-token>
    python ingress_probe.py
"""

from __future__ import annotations

import argparse
import asyncio
import json
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
HA_AUTH_INVALID = "auth_invalid"
HA_INGRESS_LIST_COMMAND = "ingress/list"
PROBE_MESSAGE_ID = 2
DEFAULT_HOST = os.environ.get(HA_HOST_ENV_VAR, f"homeassistant.local:{HA_DEFAULT_PORT}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Probe the Home Assistant WebSocket ingress registry")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Home Assistant host[:port]")
    parser.add_argument("--token", default=os.environ.get(HA_TOKEN_ENV_VAR, ""), help="long-lived HA token")
    return parser.parse_args()


async def main() -> int:
    arguments = _parse_args()
    if not arguments.token:
        print(f"{HA_TOKEN_ENV_VAR} (long-lived Home Assistant token) is required", file=sys.stderr)
        return 2
    async with aiohttp.ClientSession() as session:
        ws = await session.ws_connect(f"ws://{arguments.host}{HA_WEBSOCKET_PATH}")
        hello = await ws.receive_json()
        if hello.get("type") != HA_AUTH_REQUIRED:
            print("websocket_handshake:", hello.get("type"))
            return 1
        await ws.send_json({"type": HA_AUTH_MESSAGE, "access_token": arguments.token})
        while True:
            data = await ws.receive_json()
            if data.get("type") in (HA_AUTH_OK, HA_AUTH_INVALID):
                print("auth:", data.get("type"))
                if data.get("type") == HA_AUTH_INVALID:
                    return 1
                break
        await ws.send_json({"id": PROBE_MESSAGE_ID, "type": HA_INGRESS_LIST_COMMAND})
        while True:
            data = await ws.receive_json()
            if data.get("id") == PROBE_MESSAGE_ID:
                if data.get("success"):
                    print("ingress:", json.dumps(data.get("result"), indent=2))
                else:
                    print("ingress_error:", data.get("error"))
                break
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
