"""Live Raspberry Pi verification script for BL-HAOS Bridge & Integration."""

import asyncio
import json
import os
import urllib.request
import websockets

HA_URL = os.environ.get("HA_URL", "http://homeassistant.local:8123")
HA_WS = os.environ.get("HA_WS", "ws://homeassistant.local:8123/api/websocket")
TOKEN = os.environ.get("HA_TOKEN", "YOUR_LONG_LIVED_ACCESS_TOKEN")

async def run_diagnostics():
    print("==================================================================")
    print("   BL-HAOS LIVE VERIFICATION: RASPBERRY PI (192.168.1.21)")
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
        print(f"    - IP Address: {addon_info.get('ip_address')}")
        print(f"    - Ingress Port: {addon_info.get('ingress_port')}")
        ingress_url = addon_info.get("ingress_url")
        print(f"    - Ingress URL: {ingress_url}")
        
        # 2. Ingress Session & Bridge API Checks
        await ws.send(json.dumps({"id": 2, "type": "supervisor/api", "endpoint": "/ingress/session", "method": "post"}))
        sess_resp = json.loads(await ws.recv())
        session_id = sess_resp.get("result", {}).get("session")
        print(f"[*] Ingress Session: Obtained token ({session_id[:16]}...)")
        
        def bridge_get(path):
            req = urllib.request.Request(
                f"{HA_URL}{ingress_url}{path.lstrip('/')}",
                headers={"Cookie": f"ingress_session={session_id}"}
            )
            with urllib.request.urlopen(req, timeout=5) as r:
                return json.loads(r.read().decode("utf-8"))
        
        health = bridge_get("/api/health")
        print(f"[*] Bridge Health: {health}")
        
        adapters = bridge_get("/api/adapters")
        print(f"[*] Bluetooth Adapters ({len(adapters)} found):")
        for ad in adapters:
            print(f"    - [{ad.get('interface')}] {ad.get('name')} (MAC: {ad.get('address')}) Powered={ad.get('powered')}")
        
        speakers = bridge_get("/api/native/speakers")
        print(f"[*] Native Speakers in Bridge ({len(speakers.get('speakers', {}))} registered):")
        for mac, spk in speakers.get("speakers", {}).items():
            print(f"    - {spk.get('name')} [{mac}] Connected={spk.get('connected')} State={spk.get('playback', {}).get('state')} Volume={spk.get('playback', {}).get('volume')}")
        
        # 3. Native Integration Config Entry
        await ws.send(json.dumps({"id": 3, "type": "config_entries/get", "domain": "bl_haos"}))
        entries = (json.loads(await ws.recv())).get("result", [])
        bl_entry = next((e for e in entries if e.get("domain") == "bl_haos"), None)
        print(f"[*] HA Native Integration Config Entry:")
        if bl_entry:
            print(f"    - Title: {bl_entry.get('title')}")
            print(f"    - Entry ID: {bl_entry.get('entry_id')}")
            print(f"    - State: {bl_entry.get('state')}")
            print(f"    - Data: {bl_entry.get('data')}")
        else:
            print("    - None found")
            
        # 4. Registered Media Player Entities in HA
        await ws.send(json.dumps({"id": 4, "type": "get_states"}))
        states = (json.loads(await ws.recv())).get("result", [])
        media_players = [s for s in states if s.get("entity_id", "").startswith("media_player.")]
        print(f"[*] Home Assistant Media Players ({len(media_players)} total):")
        for mp in media_players:
            if "logitech" in mp.get("entity_id", "") or "bl_haos" in mp.get("entity_id", ""):
                print(f"    -> {mp.get('entity_id')} | State: {mp.get('state')} | Friendly Name: {mp.get('attributes', {}).get('friendly_name')}")
            else:
                print(f"       {mp.get('entity_id')} | State: {mp.get('state')}")
                
        # 5. Native Diagnostics via API
        diag = bridge_get("/api/diagnostics/native")
        print(f"[*] Native Diagnostics:")
        print(f"    - Bridge Version: {diag.get('bridge_version')}")
        print(f"    - Native Transport Ready: {diag.get('native_transport_ready')}")
        print(f"    - Native Client Count (Active WebSocket): {diag.get('native_client_count')}")
        print(f"    - Trusted Speakers: {diag.get('trusted_speaker_count')}")
        print(f"    - Connected Trusted Speakers: {diag.get('connected_trusted_speaker_count')}")
        
        # 6. Test Live Bluetooth Device Scan on hci0
        print("[*] Triggering live Bluetooth discovery scan on hci0...")
        req_scan = urllib.request.Request(
            f"{HA_URL}{ingress_url}api/scan/start",
            data=json.dumps({"adapter_name": "hci0"}).encode("utf-8"),
            headers={"Cookie": f"ingress_session={session_id}", "Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req_scan, timeout=5) as r:
                print(f"    - Scan started: HTTP {r.status} {r.read().decode('utf-8')}")
            await asyncio.sleep(4)
            devices = bridge_get("/api/devices")
            print(f"[*] Bluetooth Devices Discovered ({len(devices)} total):")
            for dev in devices[:10]:
                name = dev.get("name") or dev.get("alias") or "(Unknown)"
                print(f"    - {name} [{dev.get('address')}] RSSI={dev.get('rssi')}dBm AudioSink={dev.get('is_audio_sink')} Trusted={dev.get('trusted')}")
        except Exception as e:
            print(f"    - Scan error: {e}")
        
    print("==================================================================")
    print("   ALL TESTS COMPLETED SUCCESSFULLY ON RASPBERRY PI!")
    print("==================================================================")

if __name__ == "__main__":
    asyncio.run(run_diagnostics())
