import os
import time
from typing import List
import discord
import yt_dlp
import glob
from src.models import (
    BotStatus,
    PlaybackInformation,
    SongItem,
    SongQueueStatus,
    SongMetadata,
)
from src.music.my_voice_client import get_is_paused_from_voice_client, get_voice_client

DATA_PATH = "/tmp/songs"

song_file_list: List[SongItem] = []
current_position = -1
current_song_start_time = 0
pause_offset = -1


def __handle_metadata(filename: str, song_duration: int, url: str):
    json_path = filename.rsplit(".", 1)[0] + ".json"
    thumbnail_path = filename.rsplit(".", 1)[0] + ".jpg"
    thumbnail_filename = os.path.basename(thumbnail_path)
    song_metadata = SongMetadata(
        filename=filename,
        duration=song_duration,
        url=url,
        thumbnail=thumbnail_filename,
    )
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
        "writethumbnail": True,  # Download thumbnail as well
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            },
            {"key": "FFmpegThumbnailsConvertor", "format": "jpg"},
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
        # print(f"checking {json_path}")
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
    is_paused = get_is_paused_from_voice_client()
    return SongQueueStatus(
        song_file_list=song_file_list, position=current_position, is_paused=is_paused
    )


def set_queue_position(position: int):
    global current_song_start_time, song_file_list, current_position
    current_position = position


def after_playing(error):
    if error:
        print(f"Error during playback: {error}")
    fileName, duration, start_time = get_current_metadata()
    print(f"Finished playing {fileName}")

    fileName, duration, start_time = get_current_metadata()
    current_playing_time = time.time() - start_time

    if current_playing_time > (duration - 1):
        # song ended
        handle_song_end()
        if has_current_song():
            print("start next song")
            play_current_song()
        else:
            print("end of queue")
    else:
        print("not changing song because it is still playing")


def change_playback_position(position: int):
    fileName, duration, start_time = get_current_metadata()
    voice_client = get_voice_client()
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        audio = discord.FFmpegPCMAudio(
            source=fileName, before_options=f"-ss {position}"
        )
        voice_client.play(audio, after=after_playing)
        set_current_song_start_time(time.time() - position)
        return {"status": "Playback position changed"}
    else:
        print("cannot change position, no song playing")
        return None


def play_current_song():
    if has_current_song():
        fileName, duration, start_time = get_current_metadata()
        start_time_now()
        get_voice_client().play(
            discord.FFmpegPCMAudio(source=fileName), after=after_playing
        )
    else:
        print(f"cannot play current song when not selected")


def get_status():
    voice_client = get_voice_client()
    if voice_client and voice_client.is_playing():
        return BotStatus.PLAYING
    return BotStatus.IDLE


def get_playback_info():
    fileName, duration, start_time = get_current_metadata()
    voice_client = get_voice_client()
    if voice_client and voice_client.is_playing():
        elapsed_time = time.time() - start_time

        return PlaybackInformation(
            file_name=fileName,
            current_position=elapsed_time,
            duration=duration,
        )
    else:
        return None


def get_filename_and_starttime():
    fileName, duration, start_time = get_current_metadata()
    return fileName, start_time


def start_time_now():
    set_current_song_start_time(time.time())


def handle_new_song_on_queue():
    if not has_current_song():
        move_to_last_song_in_queue()
        if has_current_song():
            play_current_song()
            print("started playing current song")
        else:
            print("moving to the last song did not put us on a current song")
    else:
        print("not moving to new song because there is current song")


def pause_song():
    global pause_offset
    voice_client = get_voice_client()
    if voice_client and voice_client.is_playing():
        fileName, duration, start_time = get_current_metadata()
        pause_offset = time.time() - start_time
        voice_client.pause()


def unpause_song():
    global pause_offset
    voice_client = get_voice_client()
    if voice_client and voice_client.is_playing():
        voice_client.resume()
        set_current_song_start_time(time.time() - pause_offset)
        pause_offset = -1
    else:
        if has_current_song():
            fileName, duration, start_time = get_current_metadata()
            seek_time = pause_offset if pause_offset > 0 else (time.time() - start_time)
            audio = discord.FFmpegPCMAudio(
                source=fileName, before_options=f"-ss {seek_time}"
            )
            voice_client.play(audio, after=after_playing)
            set_current_song_start_time(time.time() - seek_time)
            pause_offset = -1
            print(f"Resumed playback from {seek_time}s for {fileName}")
        else:
            print("cannot unpause song, no song playing")
