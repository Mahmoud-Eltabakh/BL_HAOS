"""Test pairing and connecting to Logitech BT Adapter on Pi."""

import asyncio
import json
import os
import urllib.request
import websockets

HA_URL = os.environ.get("HA_URL", "http://homeassistant.local:8123")
HA_WS = os.environ.get("HA_WS", "ws://homeassistant.local:8123/api/websocket")
TOKEN = os.environ.get("HA_TOKEN", "YOUR_LONG_LIVED_ACCESS_TOKEN")
TARGET_MAC = "EC:81:93:53:A9:16"

async def run():
    async with websockets.connect(HA_WS) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": TOKEN}))
        await ws.recv()
        
        await ws.send(json.dumps({"id": 1, "type": "supervisor/api", "endpoint": "/addons/c839f4a9_bl_haos/info", "method": "get"}))
        addon_info = (json.loads(await ws.recv())).get("result", {})
        ingress_url = addon_info.get("ingress_url")
        if not ingress_url.endswith("/"):
            ingress_url += "/"
        
        await ws.send(json.dumps({"id": 2, "type": "supervisor/api", "endpoint": "/ingress/session", "method": "post"}))
        session_id = (json.loads(await ws.recv())).get("result", {}).get("session")
        
        print("1. Starting discovery scan on hci0...")
        req_start = urllib.request.Request(
            f"{HA_URL}{ingress_url}api/scan/start",
            data=json.dumps({"adapter_name": "hci0"}).encode("utf-8"),
            headers={"Cookie": f"ingress_session={session_id}", "Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req_start, timeout=5) as r:
                print("   Scan started successfully.")
        except Exception as e:
            print(f"   Scan start note: {e}")
            
        print("   Listening for Bluetooth beacons (5 seconds)...")
        await asyncio.sleep(5)
        
        req_dev = urllib.request.Request(
            f"{HA_URL}{ingress_url}api/devices",
            headers={"Cookie": f"ingress_session={session_id}"}
        )
        with urllib.request.urlopen(req_dev, timeout=5) as r:
            devices = json.loads(r.read().decode("utf-8"))
            print(f"2. Found {len(devices)} discovered devices over the air:")
            for d in devices:
                name = d.get("name") or d.get("alias") or "(Unknown)"
                addr = d.get("address")
                rssi = d.get("rssi")
                sink = d.get("is_audio_sink")
                print(f"   - {name} [{addr}] RSSI={rssi}dBm AudioSink={sink}")
                
        print(f"3. Attempting to Pair & Connect with {TARGET_MAC}...")
        req_pair = urllib.request.Request(
            f"{HA_URL}{ingress_url}api/devices/pair",
            data=json.dumps({"address": TARGET_MAC}).encode("utf-8"),
            headers={"Cookie": f"ingress_session={session_id}", "Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req_pair, timeout=25) as r:
                print(f"   PAIR RESULT: HTTP {r.status} {r.read().decode('utf-8')}")
        except urllib.error.HTTPError as e:
            print(f"   PAIR HTTP Error {e.code}: {e.read().decode('utf-8')}")
        except Exception as e:
            print(f"   PAIR General Error: {e}")

if __name__ == "__main__":
    asyncio.run(run())
