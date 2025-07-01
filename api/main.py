import inspect
import json
import os
from typing import Set, Dict, Any
from dotenv import load_dotenv
from fastapi.concurrency import asynccontextmanager
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from src.discord_utils import connect_to_channel_by_name, is_bot_connected
from src.models import BotResponse, MessageType
from fastapi.staticfiles import StaticFiles
from src.mcp_server import discord_mcp
from src.music.music_controls import MusicControls, get_music_controls
from src.music.song_queue import get_status
from src.playback_router import playback_router
from src.discord_bot import bot

load_dotenv()


@asynccontextmanager
async def lifespan(app):
    discord_task = asyncio.create_task(bot.start(os.getenv("DISCORD_SECRET")))
    mcp_task = asyncio.create_task(
        discord_mcp.run_async(transport="http", port=5678, host="0.0.0.0")
    )
    # mcp_task_sse = asyncio.create_task(
    #     discord_mcp.run_async(transport="sse", port=5676, host="0.0.0.0")
    # )
    yield
    discord_task.cancel()
    mcp_task.cancel()
    # mcp_task_sse.cancel()


app = FastAPI(lifespan=lifespan)

connected_clients: Set[WebSocket] = set()
controls = get_music_controls()


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


async def ws_message(data: Dict[str, Any]) -> BotResponse:
    if "action" not in data:
        return BotResponse(
            message_type=MessageType.ERROR,
            status=get_status(),
            error="Invalid request, action is required",
        )
    method = getattr(controls, data["action"], None)
    if callable(method):
        sig = inspect.signature(method)
        params = {k: data[k] for k in sig.parameters if k in data}
        return method(**params)
    else:
        return BotResponse(
            message_type=MessageType.ERROR,
            status=get_status(),
            error=f"Unknown action: {data['action']}",
        )


async def websocket_handler(websocket: WebSocket):
    connected_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data_json = json.loads(data)

            response = await ws_message(data_json)
            await send_response_message(websocket, response)
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise e
    finally:
        connected_clients.remove(websocket)
        print("WebSocket connection closed")


@app.websocket("/discord_ws")
async def websocket_endpoint(websocket: WebSocket):
    print("received websocket connection")

    await websocket.accept()

    if not is_bot_connected():
        await connect_to_channel_by_name("Absolute Sophistication")
    await websocket_handler(websocket)


@app.get("/health")
async def health(request: Request):
    # Disable logging for this endpoint
    request.scope["fastapi.logger"] = None
    return {"status": "ok"}


app.include_router(playback_router)

os.makedirs("/app/client-dist", exist_ok=True)
app.mount("/", StaticFiles(directory="/app/client-dist", html=True), name="client-dist")
