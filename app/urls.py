
from fastapi import FastAPI
from app.views import router as frontend_router

app = FastAPI()

app.include_router(frontend_router)


from fastapi import WebSocket
from fastapi import WebSocketDisconnect

connections = []

@app.websocket("/ws/inventory/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # No-op, we only push data from server
    except WebSocketDisconnect:
        connections.remove(websocket)

async def notify_inventory_update(message: str):
    for conn in connections:
        await conn.send_text(message)