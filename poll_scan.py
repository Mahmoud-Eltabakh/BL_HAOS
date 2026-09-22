"""Poll Bluetooth devices in real time."""

import asyncio
import json
import os
import urllib.request
import websockets

HA_URL = os.environ.get("HA_URL", "http://homeassistant.local:8123")
HA_WS = os.environ.get("HA_WS", "ws://homeassistant.local:8123/api/websocket")
TOKEN = os.environ.get("HA_TOKEN", "YOUR_LONG_LIVED_ACCESS_TOKEN")

async def run():
    async with websockets.connect(HA_WS) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": TOKEN}))
        await ws.recv()
        
        await ws.send(json.dumps({"id": 1, "type": "supervisor/api", "endpoint": "/ingress/session", "method": "post"}))
        session_id = (json.loads(await ws.recv())).get("result", {}).get("session")
        ingress_url = "/api/hassio_ingress/iLVjC7IzpodIae1Oqa20mkdgflEPEJsr7sL7LA4wD-8/"
        
        print("Starting Bluetooth discovery scan on Raspberry Pi...")
        req_start = urllib.request.Request(
            f"{HA_URL}{ingress_url}api/scan/start",
            data=json.dumps({"adapter_name": "hci0"}).encode("utf-8"),
            headers={"Cookie": f"ingress_session={session_id}", "Content-Type": "application/json"},
            method="POST"
        )
        try:
            urllib.request.urlopen(req_start, timeout=5)
        except Exception:
            pass
            
        for i in range(5):
            await asyncio.sleep(3)
            req_dev = urllib.request.Request(
                f"{HA_URL}{ingress_url}api/devices",
                headers={"Cookie": f"ingress_session={session_id}"}
            )
            with urllib.request.urlopen(req_dev, timeout=5) as r:
                devs = json.loads(r.read().decode("utf-8"))
                print(f"Poll {i+1} (t={(i+1)*3}s): Found {len(devs)} Bluetooth devices in range")
                for d in devs:
                    name = d.get("name") or d.get("alias") or "(Unknown)"
                    print(f"   -> {name} [{d.get('address')}] RSSI={d.get('rssi')} AudioSink={d.get('is_audio_sink')}")

if __name__ == "__main__":
    asyncio.run(run())
