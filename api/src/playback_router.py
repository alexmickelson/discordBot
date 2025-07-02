from fastapi import APIRouter
from src.discord_utils import connect_to_channel_by_name, is_bot_connected
from src.music.music_controls import MusicControls, get_music_controls
from src.models import BotResponse, BotStatus, MessageType
from fastapi.responses import FileResponse
import os
from src.music.song_queue import DATA_PATH

controls = get_music_controls()

playback_router = APIRouter(prefix="/api")


@playback_router.post("/seek_to_position")
async def api_seek_to_position(position: int):
    if not is_bot_connected():
        await connect_to_channel_by_name("Absolute Sophistication")
    result = controls.seek_to_position(position)
    if result:
        return BotResponse(
            message_type=MessageType.MESSAGE,
            status=controls.get_queue_status().is_paused and BotStatus.IDLE or BotStatus.PLAYING,
            message="position changed",
        )
    else:
        return BotResponse(
            message_type=MessageType.ERROR,
            status=controls.get_queue_status().is_paused and BotStatus.IDLE or BotStatus.PLAYING,
            error="unable to change position",
        )


@playback_router.post("/play_song_by_index")
async def api_play_song_by_index(position: int):
    if not is_bot_connected():
        await connect_to_channel_by_name("Absolute Sophistication")
    info = controls.play_song_by_index(position)
    return BotResponse(
        message_type=MessageType.PLAYBACK_INFORMATION,
        status=BotStatus.PLAYING if info else BotStatus.IDLE,
        playback_information=info,
        song_queue=controls.get_queue_status(),
    )


@playback_router.get("/get_playback_info")
async def api_get_playback_info():
    if not is_bot_connected():
        await connect_to_channel_by_name("Absolute Sophistication")
    info = controls.get_playback_info()
    return info


@playback_router.get("/get_all_songs")
async def api_get_all_songs():
    if not is_bot_connected():
        await connect_to_channel_by_name("Absolute Sophistication")
    all_songs = controls.get_all_songs()
    return all_songs


@playback_router.post("/add_song_to_queue")
async def api_add_song_to_queue(filename: str):
    if not is_bot_connected():
        await connect_to_channel_by_name("Absolute Sophistication")
    success = controls.add_song_to_queue(filename)
    if success:
        return BotResponse(
            message_type=MessageType.ADD_SONG_TO_QUEUE,
            status=controls.get_queue_status().is_paused and BotStatus.IDLE or BotStatus.PLAYING,
            message="Song added to queue",
            song_queue=controls.get_queue_status(),
        )
    else:
        return BotResponse(
            message_type=MessageType.ERROR,
            status=controls.get_queue_status().is_paused and BotStatus.IDLE or BotStatus.PLAYING,
            error="Failed to add song to queue",
        )


@playback_router.post("/pause_song")
async def api_pause_song():
    if not is_bot_connected():
        await connect_to_channel_by_name("Absolute Sophistication")
    info = controls.pause_song()
    return BotResponse(
        message_type=MessageType.PLAYBACK_INFORMATION,
        status=BotStatus.IDLE,
        playback_information=info,
        song_queue=controls.get_queue_status(),
    )


@playback_router.post("/unpause_song")
async def api_unpause_song():
    if not is_bot_connected():
        await connect_to_channel_by_name("Absolute Sophistication")
    info = controls.unpause_song()
    return BotResponse(
        message_type=MessageType.PLAYBACK_INFORMATION,
        status=BotStatus.PLAYING,
        playback_information=info,
        song_queue=controls.get_queue_status(),
    )


@playback_router.post("/add_to_queue")
async def api_add_to_queue(url: str):
    if not is_bot_connected():
        await connect_to_channel_by_name("Absolute Sophistication")
    info = controls.add_to_queue(url)
    if info:
        return BotResponse(
            message_type=MessageType.ADD_SONG_TO_QUEUE,
            status=BotStatus.PLAYING,
            message="Song added to queue from URL",
            song_queue=controls.get_queue_status(),
        )
    else:
        return BotResponse(
            message_type=MessageType.ERROR,
            status=BotStatus.IDLE,
            error="URL must contain a 'v' query parameter, e.g. https://youtube.com/watch?v=VIDEO_ID",
        )


@playback_router.get("/get_song_thumbnail")
def api_get_song_thumbnail(thumbnail: str):
    print(f"Requested thumbnail: {thumbnail}")
    path = os.path.join(DATA_PATH, thumbnail)
    if not os.path.isfile(path):
        raise FileNotFoundError("Thumbnail not found: " + path)
    return FileResponse(path)


@playback_router.get("/get_song_queue")
async def api_get_song_queue():
    if not is_bot_connected():
        await connect_to_channel_by_name("Absolute Sophistication")
    queue_status = controls.get_queue_status()
    return queue_status
