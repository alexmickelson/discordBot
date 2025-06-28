from fastapi import APIRouter
from src.discord_utils import connect_to_channel_by_name, is_bot_connected
from src.music.music_controls import MusicControls

controls = MusicControls()

playback_router = APIRouter(prefix="/api")


@playback_router.post("/seek_to_position")
async def api_seek_to_position(position: int):
    if not is_bot_connected():
        await connect_to_channel_by_name("Absolute Sophistication")
    return controls.seek_to_position(position)


@playback_router.post("/play_song_by_index")
async def api_play_song_by_index(position: int):
    if not is_bot_connected():
        await connect_to_channel_by_name("Absolute Sophistication")
    return controls.play_song_by_index(position)


@playback_router.get("/get_playback_info")
async def api_get_playback_info():
    if not is_bot_connected():
        await connect_to_channel_by_name("Absolute Sophistication")
    return controls.get_playback_info()


@playback_router.get("/get_all_songs")
async def api_get_all_songs():
    if not is_bot_connected():
        await connect_to_channel_by_name("Absolute Sophistication")
    return controls.get_all_songs()


@playback_router.post("/add_song_to_queue")
async def api_add_song_to_queue(filename: str):
    if not is_bot_connected():
        await connect_to_channel_by_name("Absolute Sophistication")
    return controls.add_song_to_queue(filename)


@playback_router.post("/pause_song")
async def api_pause_song():
    if not is_bot_connected():
        await connect_to_channel_by_name("Absolute Sophistication")
    return controls.pause_song()


@playback_router.post("/unpause_song")
async def api_unpause_song():
    if not is_bot_connected():
        await connect_to_channel_by_name("Absolute Sophistication")
    return controls.unpause_song()


@playback_router.post("/add_to_queue")
async def api_add_to_queue(url: str):
    if not is_bot_connected():
        await connect_to_channel_by_name("Absolute Sophistication")
    return controls.add_to_queue(url)
