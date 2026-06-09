from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict

app = FastAPI()

# قاموس لتخزين الاتصالات النشطة لكل مستخدم
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        # إرسال رسالة ترحيب
        await manager.broadcast(f"نظام: انضم {user_id} إلى المحادثة")
        
        while True:
            # انتظار استقبال الرسائل من العميل
            data = await websocket.receive_text()
            # إعادة إرسال الرسالة للجميع
            await manager.broadcast(f"{user_id}: {data}")
            
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        await manager.broadcast(f"نظام: غادر {user_id} المحادثة")
