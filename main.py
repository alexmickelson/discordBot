import os
from dotenv import load_dotenv
from fastapi.concurrency import asynccontextmanager
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from src.discord_bot import bot
from src.websocket_server import websocket_handler

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async def start_bot():
        await bot.start(os.getenv("DISCORD_SECRET"))

    app.state.bot_task = asyncio.create_task(start_bot())
    yield
    app.state.bot_task.cancel()
    await asyncio.gather(app.state.bot_task, return_exceptions=True)


app = FastAPI(lifespan=lifespan)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket_handler(websocket)


# app.mount("/", StaticFiles(directory="./client", html=True), name="static")
