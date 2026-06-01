from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.security import decode_access_token
from app.services.websocket_manager import ws_manager

# ✅ THIS WAS MISSING / WRONG EARLIER
router = APIRouter()

print("🚀 WebSocket router initialized")


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=1008)
        return

    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Invalid token payload")
    except Exception:
        await websocket.close(code=1008)
        return

    await websocket.accept()
    await ws_manager.connect(user_id, websocket)

    try:
        while True:
            await websocket.receive_text()  # keep connection alive
    except WebSocketDisconnect:
        ws_manager.disconnect(user_id)
