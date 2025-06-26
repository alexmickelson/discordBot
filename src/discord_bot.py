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
import asyncio

load_dotenv()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


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
    print(f"added {url} to queue")

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


async def connect_to_channel_by_name(channel_name: str):
    """
    Connect the bot to a voice channel by name in any available guild.
    Only connect if not already connected to a voice channel in that guild.
    """
    for guild in bot.guilds:
        channel = discord.utils.get(guild.voice_channels, name=channel_name)
        if channel is not None:
            voice_client = await channel.connect()
            set_voice_client(voice_client)
            print(f"Connected to channel: {channel}")
            return voice_client
    print(f"Channel '{channel_name}' not found in any guild.")
    return None


def is_bot_connected():
    """
    Returns True if the bot is currently connected to a voice channel in any guild, False otherwise.
    """
    for guild in bot.guilds:
        if guild.voice_client and guild.voice_client.is_connected():
            return True
    return False
