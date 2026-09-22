"""Guarded, local-only Home Assistant verification utility for BL-HAOS."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from itertools import count
from typing import Any
from urllib.parse import urlsplit, urlunsplit
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def get_environment() -> tuple[str, str]:
    """Load runtime-only credentials without logging their values."""
    url = os.environ.get("HA_URL", "").rstrip("/")
    token = os.environ.get("HA_TOKEN", "")
    parsed = urlsplit(url)
    if not token or parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.username or parsed.password:
        raise ValueError("HA_URL and HA_TOKEN must be set in the local process environment")
    return url, token


def websocket_url(ha_url: str) -> str:
    parsed = urlsplit(ha_url)
    return urlunsplit(("wss" if parsed.scheme == "https" else "ws", parsed.netloc, "/api/websocket", "", ""))


def config_flow_url(ha_url: str, flow_id: str | None = None) -> str:
    """Return the Home Assistant REST endpoint for a config-entry flow."""
    suffix = "/api/config/config_entries/flow"
    return f"{ha_url}{suffix if flow_id is None else f'{suffix}/{flow_id}'}"


def config_flow_handlers_url(ha_url: str) -> str:
    """Return the read-only Home Assistant config-flow handler endpoint."""
    return f"{ha_url}/api/config/config_entries/flow_handlers"


def post_config_flow(ha_url: str, token: str, payload: dict[str, Any], flow_id: str | None = None) -> dict[str, Any]:
    """Submit a local config flow without logging credentials or response bodies."""
    request = Request(
        config_flow_url(ha_url, flow_id),
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        raise RuntimeError(f"Home Assistant config flow returned HTTP {error.code}") from error
    except (URLError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError("Home Assistant config flow did not return valid JSON") from error


def get_config_flow_handlers(ha_url: str, token: str) -> list[str] | None:
    """List Core-supported config flows without exposing credentials or response bodies."""
    request = Request(
        config_flow_handlers_url(ha_url),
        headers={"Authorization": f"Bearer {token}"},
        method="GET",
    )
    try:
        with urlopen(request, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, list) and all(isinstance(item, str) for item in payload) else None


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify the BL-HAOS native integration without exposing credentials.")
    parser.add_argument("command", choices=("preflight", "store-reload", "addon-rebuild", "addon-start", "addon-stop", "addon-restart", "native-setup", "play-media"), nargs="?", default="preflight")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--entity-id")
    parser.add_argument("--media-id")
    parser.add_argument("--media-type")
    return parser.parse_args(argv)


async def async_request(websocket: Any, request_id: int, message_type: str, **payload: Any) -> Any:
    """Await the correlated HA response and ignore unrelated events."""
    await websocket.send(json.dumps({"id": request_id, "type": message_type, **payload}))
    while True:
        response = json.loads(await websocket.recv())
        if response.get("id") == request_id:
            if not response.get("success", True):
                error = response.get("error", {})
                code = error.get("code", "unknown_error") if isinstance(error, dict) else "unknown_error"
                raise RuntimeError(f"Home Assistant rejected {message_type} ({code})")
            return response.get("result", {})


def addon_slug(metadata: Any) -> str:
    addons = metadata.get("addons", metadata.get("data", {}).get("addons", [])) if isinstance(metadata, dict) else []
    for addon in addons:
        slug = str(addon.get("slug", ""))
        if slug == "bl_haos" or slug.endswith("_bl_haos"):
            return slug
    raise RuntimeError("BL-HAOS add-on was not found in Supervisor metadata")


async def resolve_addon_slug(websocket: Any, request_ids: count) -> str:
    return addon_slug(await async_request(websocket, next(request_ids), "supervisor/api", endpoint="/addons", method="get"))


async def preflight(websocket: Any, request_ids: count, ha_url: str, token: str) -> dict[str, Any]:
    """Use only authenticated read-only requests to inspect the native integration."""
    slug = await resolve_addon_slug(websocket, request_ids)
    addon = await async_request(websocket, next(request_ids), "supervisor/api", endpoint=f"/addons/{slug}/info", method="get")
    entries = await async_request(websocket, next(request_ids), "config_entries/get")
    registry = await async_request(websocket, next(request_ids), "config/entity_registry/list")
    states = await async_request(websocket, next(request_ids), "get_states")
    flow_handlers = await asyncio.to_thread(get_config_flow_handlers, ha_url, token)
    native_ids = {item.get("entity_id") for item in registry if item.get("entity_id", "").startswith("media_player.") and item.get("platform") == "bl_haos"}
    return {
        "addon": {"slug": slug, "state": addon.get("state")},
        "native_config_entry_count": sum(entry.get("domain") == "bl_haos" for entry in entries),
        "native_flow_available": flow_handlers is not None and "bl_haos" in flow_handlers,
        "config_flow_api_available": flow_handlers is not None,
        "native_media_players": [{"entity_id": state.get("entity_id"), "state": state.get("state")} for state in states if state.get("entity_id") in native_ids],
    }


async def run_mutation(websocket: Any, request_ids: count, args: argparse.Namespace, ha_url: str = "", token: str = "") -> dict[str, Any]:
    if not args.apply:
        raise ValueError("--apply is required for lifecycle and playback operations")
    if args.command == "store-reload":
        return await async_request(websocket, next(request_ids), "supervisor/api", endpoint="/store/reload", method="post")
    if args.command.startswith("addon-"):
        slug = await resolve_addon_slug(websocket, request_ids)
        return await async_request(websocket, next(request_ids), "supervisor/api", endpoint=f"/addons/{slug}/{args.command.removeprefix('addon-')}", method="post")
    if args.command == "native-setup":
        slug = await resolve_addon_slug(websocket, request_ids)
        addon = await async_request(websocket, next(request_ids), "supervisor/api", endpoint=f"/addons/{slug}/info", method="get")
        host = addon.get("ip_address")
        if not host:
            raise RuntimeError("Supervisor did not provide a private add-on address")
        flow = await asyncio.to_thread(post_config_flow, ha_url, token, {"handler": "bl_haos"})
        if flow.get("type") == "create_entry":
            return {"configured": True}
        flow_id = flow.get("flow_id")
        if flow.get("type") != "form" or not flow_id:
            raise RuntimeError("Home Assistant did not offer the BL-HAOS setup flow")
        result = await asyncio.to_thread(
            post_config_flow, ha_url, token, {"endpoint": f"http://{host}:8099"}, flow_id
        )
        if result.get("type") != "create_entry":
            raise RuntimeError("Home Assistant rejected the BL-HAOS endpoint")
        return {"configured": True}
    if args.command == "play-media":
        if not args.entity_id or not args.entity_id.startswith("media_player.") or not args.media_id or not args.media_type:
            raise ValueError("play-media requires --entity-id, --media-id, and --media-type")
        await async_request(websocket, next(request_ids), "call_service", domain="media_player", service="play_media", target={"entity_id": args.entity_id}, service_data={"media_content_id": args.media_id, "media_content_type": args.media_type})
        for _ in range(3):
            states = await async_request(websocket, next(request_ids), "get_states")
            matching = next((state for state in states if state.get("entity_id") == args.entity_id), None)
            if matching:
                return {"entity_id": args.entity_id, "state": matching.get("state")}
            await asyncio.sleep(1)
        raise RuntimeError("No bounded state acknowledgement was returned")
    raise ValueError("Unsupported operation")


async def async_main(args: argparse.Namespace) -> dict[str, Any]:
    url, token = get_environment()
    import websockets

    async with websockets.connect(websocket_url(url)) as websocket:
        await websocket.recv()
        await websocket.send(json.dumps({"type": "auth", "access_token": token}))
        if json.loads(await websocket.recv()).get("type") != "auth_ok":
            raise RuntimeError("Home Assistant authentication failed")
        request_ids = count(1)
        return await preflight(websocket, request_ids, url, token) if args.command == "preflight" else await run_mutation(websocket, request_ids, args, url, token)


def main(argv: list[str] | None = None) -> int:
    try:
        result = asyncio.run(async_main(parse_args(argv)))
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as error:
        print(f"BL-HAOS verification did not complete: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
