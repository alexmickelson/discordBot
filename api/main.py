import json
import os
from typing import Set
from dotenv import load_dotenv
from fastapi.concurrency import asynccontextmanager
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from src.discord_bot import bot, connect_to_channel_by_name, is_bot_connected
from src.models import BotResponse
from fastapi.staticfiles import StaticFiles
from api.src.mcp_server import start_mcp_server
from api.src.music_controls import MusicControlsControls

load_dotenv()


@asynccontextmanager
async def lifespan(app):
    asyncio.create_task(bot.start(os.getenv("DISCORD_SECRET")))
    # Start MCP server in background
    start_mcp_server()
    yield


app = FastAPI(lifespan=lifespan)

connected_clients: Set[WebSocket] = set()
controls = MusicControlsControls()

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
            
            response = await controls.ws_message(data_json)
            await send_response_message(websocket, response)
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise e
    finally:
        connected_clients.remove(websocket)
        print("WebSocket connection closed")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    if not is_bot_connected():
        await connect_to_channel_by_name("Absolute Sophistication")
    await websocket_handler(websocket)


app.mount("/", StaticFiles(directory="/app/client-dist", html=True), name="client-dist")