"""List all Bluetooth MAC addresses and device names on Raspberry Pi."""

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
        
        # 1. Trigger fresh scan to update RSSI / discover nearby
        print("[*] Performing 8-second Bluetooth scan to discover all active devices...")
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
            
        await asyncio.sleep(8)
        
        # 2. Query all devices with audio_only=false
        req = urllib.request.Request(
            f"{HA_URL}{ingress_url}api/devices?audio_only=false",
            headers={"Cookie": f"ingress_session={session_id}"}
        )
        with urllib.request.urlopen(req, timeout=5) as r:
            devices = json.loads(r.read().decode("utf-8"))
            
        print(f"\n[*] Found {len(devices)} Bluetooth Devices in BlueZ:")
        print(f"{'MAC Address':<20} | {'Device Name':<32} | {'Type':<12} | {'Paired':<8} | {'RSSI'}")
        print("-" * 85)
        for d in sorted(devices, key=lambda x: (not x.get("is_audio_sink"), x.get("name") is None)):
            mac = d.get("address")
            name = d.get("name") or d.get("alias") or "(No Name / Unresolved)"
            sink = "Audio Sink" if d.get("is_audio_sink") else "BLE/Other"
            paired = "Yes" if d.get("paired") else "No"
            rssi = f"{d.get('rssi')} dBm" if d.get("rssi") is not None else "N/A"
            print(f"{mac:<20} | {name:<32} | {sink:<12} | {paired:<8} | {rssi}")
        print("-" * 85)

if __name__ == "__main__":
    asyncio.run(main())
