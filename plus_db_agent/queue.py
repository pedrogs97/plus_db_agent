"""Connection Manager Module"""

import asyncio
import json
import time
import uuid
from threading import Thread
from typing import List, Optional, Union

from fastapi import WebSocket
from fastapi.websockets import WebSocketDisconnect, WebSocketState
from tortoise.exceptions import OperationalError
from typing_extensions import Self

from plus_db_agent.enums import BaseMessageType
from plus_db_agent.logger import logger
from plus_db_agent.schemas import (
    BaseSchema,
    ConnectionSchema,
    CreateUUIDSchema,
    ErrorResponseSchema,
    Message,
)


class BaseClientWebSocket:
    """Custom BaseClientWebSocket"""

    token: Optional[str] = None
    clinic_id: int
    uuid: str
    user_id: Optional[int] = None
    wb: WebSocket

    def __init__(self, wb: WebSocket) -> None:
        self.wb = wb

    async def accept(
        self,
        client_id: Union[int, None] = None,
        uuid_code: Union[str, None] = None,
    ) -> None:
        """Accept connection"""
        if client_id is None or uuid_code is None:
            return await self.send_error_message("Client ID ou UUID não informado")
        self.clinic_id = client_id
        self.uuid = uuid_code
        await self.wb.accept()

    async def send_invalid_message(self) -> None:
        """Send invalid message"""
        await self.send(
            Message(messageType=BaseMessageType.INVALID, clinicId=self.clinic_id)
        )

    async def send_error_message(self, error: str) -> None:
        """Send error message"""
        await self.send(
            Message(
                messageType=BaseMessageType.ERROR,
                clinicId=self.clinic_id,
                data=ErrorResponseSchema(error=error),
            )
        )

    async def send_new_uuid(self, uuid_code: str) -> None:
        """Send new uuid"""
        await self.send(
            Message(
                messageType=BaseMessageType.CREATE_UUID,
                clinicId=self.clinic_id,
                data=CreateUUIDSchema(uuid=uuid_code),
            )
        )

    async def send(self, message: Union[Message, dict]) -> None:
        """Send message"""
        if isinstance(message, BaseSchema):
            await self.wb.send_json(message.model_dump())
        else:
            await self.wb.send_json(message)

    async def close(self) -> None:
        """Close connection"""
        if self.wb.state == WebSocketState.CONNECTED:
            await self.wb.close()


class BaseConnectionManager:
    """Class defining socket events"""

    _instance: "BaseConnectionManager" = None
    client_connections: List[BaseClientWebSocket] = []
    queue = asyncio.Queue()

    def __new__(cls) -> Self:
        """Singleton instance"""
        if cls._instance is None:
            cls._instance = super(BaseConnectionManager, cls).__new__(cls)
        return cls._instance

    async def connect(self, websocket: WebSocket, clinic_id: int):
        """Add a new client connection to the list on connect"""
        client_websocket = BaseClientWebSocket(wb=websocket)
        new_uuid = uuid.uuid4().hex
        await client_websocket.accept(client_id=clinic_id, uuid_code=new_uuid)
        await client_websocket.send_new_uuid(new_uuid)
        self.client_connections.append(client_websocket)
        await self.__listenner(client_websocket)

    async def disconnect(self, client: BaseClientWebSocket):
        """Remove a client connection from the list on disconnect"""
        if client in self.client_connections:
            self.client_connections.remove(client)
        if client.wb.state == WebSocketState.CONNECTED:
            await client.close()

    def get_all_connections(self) -> List[BaseClientWebSocket]:
        """Return all connections"""
        return self.client_connections

    def get_connection_by_uuid(
        self, uuid_code: str
    ) -> Union[BaseClientWebSocket, None]:
        """Return connection by uuid"""
        for connection in self.client_connections:
            if connection.uuid == uuid_code:
                return connection
        return None

    def get_connection_by_clinic_id(
        self, clinic_id: int
    ) -> Union[BaseClientWebSocket, None]:
        """Return connection by clinic_id"""
        for connection in self.client_connections:
            if connection.clinic_id == clinic_id:
                return connection
        return None

    async def broadcast_clinic_messages(self, clinic_id: int, message: Message) -> None:
        """Broadcast messages"""
        for client_connection in self.client_connections:
            if client_connection.clinic_id == clinic_id:
                await client_connection.send(message)

    async def __listenner(self, websocket_client: BaseClientWebSocket) -> None:
        """Listen to incoming messages"""
        try:
            while True:
                data = await websocket_client.wb.receive_json()
                try:
                    message = Message.model_validate_json(json.dumps(data))
                    await self.queue.put((websocket_client, message))
                except (ValueError, AttributeError):
                    await websocket_client.send_invalid_message()
                    continue
        except WebSocketDisconnect:
            self.disconnect(websocket_client)

    async def __process_connection(self, message: Message, client: BaseClientWebSocket):
        """Process connection"""
        try:
            if not isinstance(message.data, ConnectionSchema):
                await client.send_invalid_message()
                return
            client.token = message.data.token
            await client.send(
                Message(
                    message_type=BaseMessageType.CONNECTION,
                    clinic_id=message.clinic_id,
                )
            )
        except (OperationalError, AttributeError):
            await client.send_error_message("Erro ao validar conexão")
            time.sleep(0.1)
            await self.disconnect(client)

    async def __process_message(
        self, message: Message, client: BaseClientWebSocket
    ) -> None:
        """Process message"""
        try:
            if message.message_type == BaseMessageType.CONNECTION:
                await self.__process_connection(message, client)
            elif not client.token:
                await client.send_error_message("Token inválido")
                time.sleep(0.1)
                await self.disconnect(client)
            else:
                await client.send_invalid_message()
        except (AttributeError, OperationalError):
            await client.send_error_message("Erro ao processar a mensagem")

    async def __process_queue(self):
        while True:
            if not self.queue.empty():
                websocket, message = await self.queue.get()
                logger.info("Processing message: %s", message.message_type)
                await self.__process_message(message, websocket)
            await asyncio.sleep(1)

    def __start_queue_processor(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.__process_queue())

    def start_main_thread(self):
        """Start the main thread"""
        thread = Thread(target=self.__start_queue_processor)
        thread.start()
        logger.info("Main thread started")
