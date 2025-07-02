import discord
from discord.ext import commands
from dotenv import load_dotenv
from src.music.my_voice_client import set_voice_client, stop_playback_and_disconnect
from src.music.song_queue import add_url_to_queue, handle_new_song_on_queue, pause_song

load_dotenv()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Bot is ready")


@bot.command(name="play", pass_context=True)
async def play(ctx: commands.Context, url: str):
    print("playing", url)
    if not isinstance(ctx.author, discord.Member) or ctx.author.voice is None:
        await ctx.send("You are not connected to a voice channel.")
        return
    channel = ctx.author.voice.channel
    print("connecting to channel", channel)

    if channel is None:
        await ctx.send("Could not find your voice channel.")
        return

    if ctx.voice_client is None:
        set_voice_client(await channel.connect())
    add_url_to_queue(url)
    print(f"added {url} to queue")

    handle_new_song_on_queue()


@bot.command(name="url")
async def url(ctx: commands.Context):
    await ctx.send("http://server.alexmickelson.guru:5677/")


@bot.command(pass_context=True)
async def stop(ctx: commands.Context):
    print("stopping playing")
    await stop_playback_and_disconnect()
    await ctx.send("Stopped playing")


@bot.command(pass_context=True)
async def pause(ctx: commands.Context):
    print("pausing playing")
    pause_song()
