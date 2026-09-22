"""Inspect complete BlueZ D-Bus Object hierarchy on the Raspberry Pi."""

import asyncio
import json
import os
import urllib.request
import websockets

HA_URL = os.environ.get("HA_URL", "http://homeassistant.local:8123")
HA_WS = os.environ.get("HA_WS", "ws://homeassistant.local:8123/api/websocket")
TOKEN = os.environ.get("HA_TOKEN", "YOUR_LONG_LIVED_ACCESS_TOKEN")

async def main():
    async with websockets.connect(HA_WS) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": TOKEN}))
        await ws.recv()
        
        await ws.send(json.dumps({"id": 1, "type": "supervisor/api", "endpoint": "/ingress/session", "method": "post"}))
        session_id = (json.loads(await ws.recv())).get("result", {}).get("session")
        ingress_url = "/api/hassio_ingress/iLVjC7IzpodIae1Oqa20mkdgflEPEJsr7sL7LA4wD-8/"
        
        req = urllib.request.Request(
            f"{HA_URL}{ingress_url}api/devices?audio_only=false",
            headers={"Cookie": f"ingress_session={session_id}"}
        )
        with urllib.request.urlopen(req, timeout=5) as r:
            devices = json.loads(r.read().decode("utf-8"))
            
        print(f"Total devices currently tracked: {len(devices)}")
        for d in devices:
            print("---")
            print(f"MAC: {d.get('address')}")
            print(f"Name: {d.get('name')}")
            print(f"Alias: {d.get('alias')}")
            print(f"Class of Device: {d.get('class_of_device')}")
            print(f"UUIDs: {d.get('uuids')}")
            print(f"Paired: {d.get('paired')}, Trusted: {d.get('trusted')}, Connected: {d.get('connected')}")
            print(f"RSSI: {d.get('rssi')}")

if __name__ == "__main__":
    asyncio.run(main())
