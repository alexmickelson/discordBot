import asyncio
import json
from typing import Set
from fastapi import WebSocket, WebSocketDisconnect

from src.models import BotResponse
from src.playback_service import handle_message


connected_clients: Set[WebSocket] = set()


async def broadcast_bot_response(response: BotResponse):
    if connected_clients:
        await asyncio.gather(
            *[
                client.send_text(response.model_dump_json())
                for client in connected_clients
            ],
            return_exceptions=True,
        )
    else:
        raise TypeError("No connected clients to broadcast to.")


async def send_response_message(websocket: WebSocket, response: BotResponse):
    await websocket.send_text(response.model_dump_json())


async def websocket_handler(websocket: WebSocket):
    connected_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data_json = json.loads(data)

            response = await handle_message(data_json)
            await send_response_message(websocket, response)
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise e
    finally:
        connected_clients.remove(websocket)
        print("WebSocket connection closed")
