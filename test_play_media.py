import asyncio
import json
import os
import urllib.request
import websockets

HA_URL = os.environ.get("HA_URL", "http://192.168.1.21:8123")
HA_WS = os.environ.get("HA_WS", "ws://192.168.1.21:8123/api/websocket")
TOKEN = os.environ.get("HA_TOKEN", "")
TARGET_MAC = "EC:81:93:53:A9:16"
ENTITY_ID = "media_player.logitech_bt_adapter_logitech_bt_adapter"
MEDIA_URL = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"

async def main():
    async with websockets.connect(HA_WS) as ws:
        await ws.recv() # Wait for auth_required
        await ws.send(json.dumps({"type": "auth", "access_token": TOKEN}))
        auth = json.loads(await ws.recv())
        if auth.get("type") != "auth_ok":
            print("[-] Authentication failed")
            return
            
        # 1. Get ingress session to call API directly
        await ws.send(json.dumps({"id": 1, "type": "supervisor/api", "endpoint": "/addons/c839f4a9_bl_haos/info", "method": "get"}))
        addon_info = (json.loads(await ws.recv())).get("result", {})
        ingress_url = addon_info.get("ingress_url", "")
        
        await ws.send(json.dumps({"id": 2, "type": "supervisor/api", "endpoint": "/ingress/session", "method": "post"}))
        sess_resp = json.loads(await ws.recv())
        session_id = sess_resp.get("result", {}).get("session")
        headers = {"Cookie": f"ingress_session={session_id}", "Content-Type": "application/json"}
        
        # 2. Connect the Bluetooth Device Explicitly
        print(f"[*] Sending explicit connect command to {TARGET_MAC}...")
        req = urllib.request.Request(
            f"{HA_URL}{ingress_url}api/devices/{TARGET_MAC}/connect",
            data=b"{}", headers=headers, method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                print(f"    - Connect response: {r.status} {r.read().decode('utf-8')}")
        except Exception as e:
            print(f"    - Connect error: {e}")
            
        print("[*] Waiting 5 seconds for PipeWire A2DP profile to negotiate...")
        await asyncio.sleep(5)
        
        # 3. Start playback via Native Transport
        print(f"[*] Sending play_media command to {ENTITY_ID}...")
        await ws.send(json.dumps({
            "id": 3,
            "type": "call_service",
            "domain": "media_player",
            "service": "play_media",
            "target": {"entity_id": ENTITY_ID},
            "service_data": {
                "media_content_id": MEDIA_URL,
                "media_content_type": "music"
            }
        }))
        res = json.loads(await ws.recv())
        print(f"    - Response: {res}")
        
        # Wait to let it play a bit
        print("[*] Waiting 10 seconds for playback...")
        await asyncio.sleep(10)
        
        # Stop
        print(f"[*] Sending stop command to {ENTITY_ID}...")
        await ws.send(json.dumps({
            "id": 4,
            "type": "call_service",
            "domain": "media_player",
            "service": "media_stop",
            "target": {"entity_id": ENTITY_ID}
        }))
        res = json.loads(await ws.recv())
        print(f"    - Response: {res}")

if __name__ == "__main__":
    asyncio.run(main())
