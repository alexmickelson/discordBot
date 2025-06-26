import os
from dotenv import load_dotenv
from fastapi.concurrency import asynccontextmanager
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
import uvicorn
from src.discord_bot import bot, connect_to_channel_by_name, is_bot_connected
from src.websocket_server import websocket_handler

load_dotenv()


@asynccontextmanager
async def lifespan(app):
    asyncio.create_task(bot.start(os.getenv("DISCORD_SECRET")))
    yield


app = FastAPI(lifespan=lifespan)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    if not is_bot_connected():
        await connect_to_channel_by_name("Absolute Sophistication")
    await websocket_handler(websocket)
