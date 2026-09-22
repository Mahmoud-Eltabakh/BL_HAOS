"""Full live validation on Raspberry Pi."""

import asyncio
import json
import os
import urllib.request
import websockets

HA_URL = os.environ.get("HA_URL", "http://192.168.1.21:8123")
HA_WS = os.environ.get("HA_WS", "ws://192.168.1.21:8123/api/websocket")
TOKEN = os.environ.get("HA_TOKEN", "")
TARGET_MAC = "EC:81:93:53:A9:16"

async def main():
    print("==================================================================")
    print("   BL-HAOS COMPLETE SYSTEM VERIFICATION: RASPBERRY PI")
    print("==================================================================")
    
    async with websockets.connect(HA_WS) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": TOKEN}))
        auth = json.loads(await ws.recv())
        print(f"[*] Home Assistant Core: Authenticated OK (v{auth.get('ha_version')})")
        
        # 1. Add-on Status
        await ws.send(json.dumps({"id": 1, "type": "supervisor/api", "endpoint": "/addons/c839f4a9_bl_haos/info", "method": "get"}))
        addon_info = (json.loads(await ws.recv())).get("result", {})
        print(f"[*] Bridge Add-on: {addon_info.get('name')} v{addon_info.get('version')} (State: {addon_info.get('state')})")
        ingress_url = addon_info.get("ingress_url")
        if not ingress_url.endswith("/"):
            ingress_url += "/"
            
        # 2. Ingress Session
        await ws.send(json.dumps({"id": 2, "type": "supervisor/api", "endpoint": "/ingress/session", "method": "post"}))
        sess_resp = json.loads(await ws.recv())
        session_id = sess_resp.get("result", {}).get("session")
        headers = {"Cookie": f"ingress_session={session_id}", "Content-Type": "application/json"}
        
        # 3. Health & Adapters
        def bridge_get(path):
            req = urllib.request.Request(f"{HA_URL}{ingress_url}{path.lstrip('/')}", headers=headers)
            with urllib.request.urlopen(req, timeout=10) as r:
                return json.loads(r.read().decode("utf-8"))
                
        health = bridge_get("/api/health")
        print(f"[*] Bridge Health: {health}")
        
        adapters = bridge_get("/api/adapters")
        print(f"[*] Bluetooth Adapters: {adapters}")
        
        # 4. Start Scan
        print("[*] Starting Bluetooth discovery scan on hci0...")
        req_start = urllib.request.Request(
            f"{HA_URL}{ingress_url}api/scan/start",
            data=json.dumps({"adapter_name": "hci0"}).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        try:
            with urllib.request.urlopen(req_start, timeout=10) as r:
                print(f"    - Scan start response: {r.read().decode('utf-8')}")
        except Exception as e:
            print(f"    - Scan start note: {e}")
            
        print("[*] Listening for Bluetooth beacons (6 seconds)...")
        await asyncio.sleep(6)
        
        # 5. List Discovered Devices
        devices = bridge_get("/api/devices?audio_only=false")
        print(f"[*] Discovered Bluetooth Devices ({len(devices)} total):")
        for d in devices:
            name = d.get("name") or d.get("alias") or "(Unknown)"
            addr = d.get("address")
            sink = d.get("is_audio_sink")
            rssi = d.get("rssi")
            print(f"    - {name} [{addr}] AudioSink={sink} RSSI={rssi}dBm")
            
        # 6. Pair & Trust Logitech BT Adapter
        print(f"[*] Pairing & Trusting {TARGET_MAC}...")
        req_pair = urllib.request.Request(
            f"{HA_URL}{ingress_url}api/devices/pair",
            data=json.dumps({"address": TARGET_MAC, "pin": "0000"}).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        try:
            with urllib.request.urlopen(req_pair, timeout=25) as r:
                pair_res = json.loads(r.read().decode("utf-8"))
                print(f"    - Pair result: {pair_res}")
        except urllib.error.HTTPError as e:
            print(f"    - Pair HTTP {e.code}: {e.read().decode('utf-8')}")
        except Exception as e:
            print(f"    - Pair general error: {e}")
            
        # 7. Check Registered Native Speakers
        speakers = bridge_get("/api/native/speakers")
        print(f"[*] Registered Native Speakers in Bridge: {json.dumps(speakers, indent=2)}")
        
        # 8. Check Config Entries and Media Players in Home Assistant
        await ws.send(json.dumps({"id": 3, "type": "config_entries/get", "domain": "bl_haos"}))
        entries = (json.loads(await ws.recv())).get("result", [])
        print(f"[*] BL-HAOS Integration Config Entries: {len(entries)}")
        
        await ws.send(json.dumps({"id": 4, "type": "get_states"}))
        states = (json.loads(await ws.recv())).get("result", [])
        media_players = [s for s in states if s.get("entity_id", "").startswith("media_player.")]
        print(f"[*] Home Assistant Media Players ({len(media_players)} total):")
        for mp in media_players:
            print(f"    -> {mp.get('entity_id')} | State: {mp.get('state')} | Name: {mp.get('attributes', {}).get('friendly_name')}")

if __name__ == "__main__":
    asyncio.run(main())
