import asyncio
import time
import discord
from src.models import BotStatus, PlaybackInformation
from src.my_voice_client import get_voice_client
from src.song_queue import (
    get_current_metadata,
    handle_song_end,
    has_current_song,
    move_to_last_song_in_queue,
    set_current_song_start_time,
)

pause_offset = -1


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
