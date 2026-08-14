import json
import time

import websocket


class Action:
    def __init__(self, server: str, port: int):
        self.ws = websocket.create_connection(f"ws://{server}:{port}", timeout=5)

    def heartbeat(self, id: str):
        payload = {
            "action": "heartbeat",
            "data": {"id": id, "timestamp": int(time.time())},
        }
        self.ws.send(json.dumps(payload))
