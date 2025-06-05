from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.views import router as frontend_router

app = FastAPI()
app.include_router(frontend_router)

# ---------- WebSocket Connection Manager ----------

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                self.disconnect(connection)  # Remove broken connection

manager = ConnectionManager()

# ---------- WebSocket Endpoint ----------

@app.websocket("/ws/inventory/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # No-op; keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# ---------- Notifier Function (used by backend) ----------

async def notify_inventory_update(message: str):
    await manager.broadcast(message)
