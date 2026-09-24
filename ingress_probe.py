import asyncio
import json
import os

import aiohttp

TOK = os.environ["TOK"]
BASE = "192.168.1.21"


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        ws = await session.ws_connect(f"ws://{BASE}:8123/api/websocket")
        hello = await ws.receive_json()
        if hello.get("type") != "auth_required":
            print("websocket_handshake:", hello.get("type"))
            return
        await ws.send_json({"type": "auth", "access_token": TOK})
        while True:
            data = await ws.receive_json()
            if data.get("type") in ("auth_ok", "auth_invalid"):
                print("auth:", data.get("type"))
                if data.get("type") == "auth_invalid":
                    return
                break
        await ws.send_json({"id": 2, "type": "ingress/list"})
        while True:
            data = await ws.receive_json()
            if data.get("id") == 2:
                if data.get("success"):
                    print("ingress:", json.dumps(data.get("result"), indent=2))
                else:
                    print("ingress_error:", data.get("error"))
                break


if __name__ == "__main__":
    asyncio.run(main())
