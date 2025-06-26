import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from src.my_voice_client import get_voice_client, set_voice_client
from src.playback_service import (
    handle_new_song_on_queue,
    pause_song,
)
from src.song_queue import add_to_queue

load_dotenv()

_bot_instance = None


def get_bot():
    global _bot_instance
    if _bot_instance is None:
        _bot_instance = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        register_bot_commands(_bot_instance)
    return _bot_instance


def register_bot_commands(bot):
    @bot.event
    async def on_ready():
        print("Bot is ready")

    @bot.command(name="play", pass_context=True)
    async def play(ctx: commands.Context, url: str):
        print("playing", url)
        channel = ctx.message.author.voice.channel
        print("connecting to channel", channel)
        if ctx.voice_client is None:
            set_voice_client(await channel.connect())
        add_to_queue(url)
        handle_new_song_on_queue()

    @bot.command(name="url")
    async def url(ctx: commands.Context):
        await ctx.send("http://server.alexmickelson.guru:5677/")

    @bot.command(pass_context=True)
    async def stop(ctx: commands.Context):
        print("stopping playing")
        voice_client = get_voice_client()
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await voice_client.disconnect()
            await ctx.send("Stopped playing")

    @bot.command(pass_context=True)
    async def pause(ctx: commands.Context):
        print("pausing playing")
        pause_song()
