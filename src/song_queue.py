import os
from typing import List
from pydantic import BaseModel
import yt_dlp
import logging
import json
import glob
from src.models import SongItem, SongQueueStatus, SongMetadata
from src.my_voice_client import get_voice_client

DATA_PATH = "/tmp/songs"

song_file_list: List[SongItem] = []
current_position = -1
current_song_start_time = 0


def __handle_metadata(filename: str, song_duration: int, url: str):
    from src.models import SongMetadata

    json_path = filename.rsplit(".", 1)[0] + ".json"
    song_metadata = SongMetadata(filename=filename, duration=song_duration, url=url)
    with open(json_path, "w") as f:
        f.write(song_metadata.model_dump_json())


def __download_url(url: str):
    print("in download url")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{DATA_PATH}/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
        "nooverwrites": False,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            res = ydl.extract_info(url)
            filename = ydl.prepare_filename(res).rsplit(".", 1)[0] + ".mp3"
            song_duration = res["duration"]
            print(f"got file {filename} {song_duration}")
            __handle_metadata(filename, song_duration, url)
            return filename, song_duration
    except Exception as e:
        print(f"Error in download: {e}")
        raise


def get_all_songs():
    all_songs_list = []
    for json_path in glob.glob(f"{DATA_PATH}/*.json"):
        print(f"checking {json_path}")
        try:
            with open(json_path, "r") as f:
                data = f.read()
                song_metadata = SongMetadata.model_validate_json(data)
                all_songs_list.append(song_metadata)
        except Exception as e:
            print(f"Failed to load {json_path}: {e}")
    return all_songs_list


def add_to_queue(url: str):
    global current_song_start_time, song_file_list, current_position
    filename, duration = __download_url(url)
    song = SongItem(filename=filename, duration=duration)
    song_file_list.append(song)


def add_existing_song_to_queue(filename: str):
    """
    Add a song to the queue by its filename (must be present in DATA_PATH and have a .json metadata file).
    """
    json_path = filename.rsplit(".", 1)[0] + ".json"
    if not os.path.exists(json_path):
        print(f"Metadata file {json_path} not found for song {filename}")
        return False
    try:
        with open(json_path, "r") as f:
            data = f.read()

            song_metadata = SongMetadata.model_validate_json(data)
            song = SongItem(
                filename=song_metadata.filename, duration=song_metadata.duration
            )
            song_file_list.append(song)
            return True
    except Exception as e:
        print(f"Failed to add song from metadata {json_path}: {e}")
        return False


def has_current_song():
    global current_song_start_time, song_file_list, current_position
    if not song_file_list:
        return False
    if len(song_file_list) == current_position:
        return False
    if current_position == -1:
        return False
    return True


def get_current_metadata():
    global current_song_start_time, song_file_list, current_position
    if not has_current_song():
        print("cannot request metadata when no current song")
        return None

    return (
        song_file_list[current_position].filename,
        song_file_list[current_position].duration,
        current_song_start_time,
    )


def set_current_song_start_time(start_time: float):
    global current_song_start_time, song_file_list, current_position
    current_song_start_time = start_time


def handle_song_end():
    global current_song_start_time, song_file_list, current_position
    print("handling song end ", current_position, len(song_file_list))
    if current_position == -1:
        return
    if current_position == (len(song_file_list) - 1):
        print("last song ended, reseting position")
        current_position = -1
        return
    print("song ended, moving to next song")
    current_position += 1


def move_to_last_song_in_queue():
    global current_song_start_time, song_file_list, current_position
    current_position = len(song_file_list) - 1


def get_queue_status():
    global current_song_start_time, song_file_list, current_position

    voice_client = get_voice_client()
    is_paused = False
    if voice_client is not None:
        is_paused = not voice_client.is_playing() and voice_client.is_connected()
    return SongQueueStatus(
        song_file_list=song_file_list, position=current_position, is_paused=is_paused
    )


def set_queue_position(position: int):
    global current_song_start_time, song_file_list, current_position
    current_position = position
