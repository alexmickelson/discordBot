import discord
from src.music.my_voice_client import set_voice_client
from src.discord_bot import bot


async def connect_to_channel_by_name(channel_name: str):
    for guild in bot.guilds:
        channel = discord.utils.get(guild.voice_channels, name=channel_name)
        if channel is not None:
            voice_client = guild.voice_client
            if (
                isinstance(voice_client, discord.VoiceClient)
                and voice_client.is_connected()
            ):
                if voice_client.channel == channel:
                    print(f"Already connected to the requested channel: {channel}")
                    set_voice_client(voice_client)
                    return voice_client
                else:
                    print(f"Moving to channel: {channel}")
                    await voice_client.move_to(channel)
                    set_voice_client(voice_client)
                    return voice_client
            try:
                voice_client = await channel.connect()
            except discord.errors.ClientException as e:
                if str(e) == "Already connected to a voice channel.":
                    print(f"Already connected to a voice channel, ignoring: {e}")
                    return guild.voice_client
                else:
                    raise
            set_voice_client(voice_client)
            print(f"Connected to channel: {channel}")
            return voice_client
    print(f"Channel '{channel_name}' not found in any guild.")
    return None


def is_bot_connected():
    for guild in bot.guilds:
        if (
            isinstance(guild.voice_client, discord.VoiceClient)
            and guild.voice_client.is_connected()
        ):
            return True
    return False
