import json
import threading

import streamlit as st
import websocket

from utils.notifications import push_reminder


class ReminderSocket:

    def __init__(self, token):
        self.token = token

    def on_message(self, ws, message):
        data = json.loads(message)
        if data.get("type") == "reminder":
            push_reminder(data)

    def on_error(self, ws, error):
        print("WEBSOCKET ERROR:", error)

    def on_close(self, ws, close_status_code, close_msg):
        print("WEBSOCKET CLOSED")

    def on_open(self, ws):
        print("WEBSOCKET CONNECTED")

    def start(self):
        ws = websocket.WebSocketApp(
            f"ws://127.0.0.1:8000/api/v1/ws?token={self.token}",
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )

        thread = threading.Thread(target=ws.run_forever, daemon=True)
        thread.start()