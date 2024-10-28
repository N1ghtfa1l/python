import json
from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from sqlalchemy import insert, select
from src.database import async_session_maker
from src.model.core import Messages

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_text(json.dumps(message))

    async def broadcast(self, message: dict, add_to_db: bool):
        if add_to_db:
            # Извлечение сообщения из dict
            await self.add_messages_to_database(message['message'], message['name'])
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))

    @staticmethod
    async def add_messages_to_database(message: str, name: str):
        async with async_session_maker() as session:
            stmt = insert(Messages).values(
                message=message,
                user=name
            )
            await session.execute(stmt)
            await session.commit()


manager = ConnectionManager()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            message = {
                "client_id": client_id,
                "message": message_data['message'],
                "name": message_data['name']
            }
            await manager.broadcast(message, add_to_db=True)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.get("/messages")
async def get_messages():
    async with async_session_maker() as session:
        result = await session.execute(select(Messages).order_by(Messages.id))
        messages = result.scalars().all()
        return [{"id": msg.id, "message": msg.message, "user": msg.user} for msg in messages]
