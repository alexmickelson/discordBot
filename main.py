import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from fastapi.concurrency import asynccontextmanager
import asyncio
from src.my_voice_client import get_voice_client, set_voice_client
from src.playback_service import (
    handle_message,
    handle_new_song_on_queue,
    pause_song,
)
from src.song_queue import add_to_queue
from src.websocket_server import websocket_handler

load_dotenv()

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Bot is ready")


@bot.command(name="play", pass_context=True)
async def play(ctx: commands.Context, url: str):
    print("playing", url)
    channel = ctx.message.author.voice.channel

    if ctx.voice_client is None:
        set_voice_client(await channel.connect())
    add_to_queue(url)
    handle_new_song_on_queue()


@bot.command(name="url")
async def url(ctx: commands.Context):
    await ctx.send("http://server.alexmickelson.guru:5677/")


@bot.command(pass_context=True)
async def stop(ctx: commands.Context):
    voice_client = get_voice_client()
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await voice_client.disconnect()
        await ctx.send("Stopped playing")


@bot.command(pass_context=True)
async def pause(ctx: commands.Context):
    pause_song()


@asynccontextmanager
async def lifespan(app: FastAPI):
    bot_task = asyncio.create_task(bot.start(os.getenv("DISCORD_SECRET")))
    app.state.bot_task = bot_task

    yield

    app.state.bot_task.cancel()
    await asyncio.gather(app.state.bot_task, return_exceptions=True)


app = FastAPI(lifespan=lifespan)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
#     allow_headers=["*"],  # Allow all headers
# )


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket_handler(websocket)


app.mount("/", StaticFiles(directory="./client", html=True), name="static")
