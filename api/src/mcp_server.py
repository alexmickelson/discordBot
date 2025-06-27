from fastmcp import FastMCP
from src.discord_bot import connect_to_channel_by_name, is_bot_connected
from src.music_controls import MusicControls

discord_mcp = FastMCP("Discord Music MCP")
controls = MusicControls()


async def ensure_bot_connected():
    if not is_bot_connected():
        await connect_to_channel_by_name("Absolute Sophistication")
@discord_mcp.tool
async def seek_to_position(position: int):
    await ensure_bot_connected()
    return controls.seek_to_position(position)


@discord_mcp.tool
async def play_song_by_index(position: int):
    await ensure_bot_connected()
    return controls.play_song_by_index(position)


@discord_mcp.tool
async def get_playback_info():
    await ensure_bot_connected()
    return controls.get_playback_info()


@discord_mcp.tool
async def get_all_songs():
    await ensure_bot_connected()
    return controls.get_all_songs()


@discord_mcp.tool
async def add_song_to_queue(filename: str):
    await ensure_bot_connected()
    return controls.add_song_to_queue(filename)


@discord_mcp.tool
async def pause_song():
    await ensure_bot_connected()
    return controls.pause_song()


@discord_mcp.tool
async def unpause_song():
    await ensure_bot_connected()
    return controls.unpause_song()


@discord_mcp.tool
async def add_to_queue(url: str):
    await ensure_bot_connected()
    return controls.add_to_queue(url)
