from fastapi import WebSocket
from typing import Dict


class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        self.active_connections[user_id] = websocket
        print(f"🔗 WebSocket connected | user={user_id}")
        print("📊 Active ws users:", list(self.active_connections.keys()))

    def disconnect(self, user_id: str):
        self.active_connections.pop(user_id, None)
        print(f"❌ WebSocket disconnected | user={user_id}")

    async def send_message(self, user_id: str, message: dict):
        ws = self.active_connections.get(user_id)
        if ws:
            await ws.send_json(message)


# ✅ GLOBAL INSTANCE (IMPORTANT)
ws_manager = WebSocketManager()
