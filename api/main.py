import inspect
import json
import os
from typing import Set, Dict, Any
from dotenv import load_dotenv
from fastapi.concurrency import asynccontextmanager
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from src.discord_utils import connect_to_channel_by_name, is_bot_connected
from src.models import BotResponse, MessageType, BotStatus
from fastapi.staticfiles import StaticFiles
from src.mcp_server import discord_mcp
from src.music.music_controls import MusicControls, get_music_controls
from src.playback_router import playback_router
from src.discord_bot import bot

load_dotenv()


@asynccontextmanager
async def lifespan(app):
    discord_secret = os.getenv("DISCORD_SECRET")
    if not discord_secret:
        raise RuntimeError("DISCORD_SECRET environment variable is not set.")
    discord_task = asyncio.create_task(bot.start(discord_secret))
    mcp_task = asyncio.create_task(
        discord_mcp.run_async(transport="http", port=5678, host="0.0.0.0")
    )
    yield
    discord_task.cancel()
    mcp_task.cancel()


app = FastAPI(lifespan=lifespan)

controls = get_music_controls()


async def send_response_message(websocket: WebSocket, response: BotResponse):
    await websocket.send_text(response.model_dump_json())


async def websocket_handler(websocket: WebSocket):
    try:
        while True:
            # Broadcast PLAYBACK_INFORMATION to all clients 3 times a second
            info = controls.get_playback_info()
            response = BotResponse(
                message_type=MessageType.PLAYBACK_INFORMATION,
                status=(BotStatus.PLAYING if info else BotStatus.IDLE),
                playback_information=info,
                song_queue=controls.get_queue_status(),
                all_songs_list=controls.get_all_songs(),
            )
            await websocket.send_text(response.model_dump_json())
            await asyncio.sleep(1 / 3)  # 3 times a second
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise e
    finally:
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
