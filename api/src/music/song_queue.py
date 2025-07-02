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
from pydantic import BaseModel
from src.music.my_voice_client import get_is_paused_from_voice_client, get_voice_client
from src.music.song_filesystem_service import (
    handle_metadata,
    download_url,
    get_all_songs,
)

DATA_PATH = "/tmp/songs"


class PlaybackState(BaseModel):
    is_paused: bool = False
    start_time: float = 0
    pause_offset: float = -1
    duration: int = 0

    def set_playing(self, duration: int):
        self.is_playing = True
        self.is_paused = False
        self.start_time = time.time()
        self.duration = duration
        self.pause_offset = -1

    def pause(self):
        if not self.is_paused:
            self.is_paused = True
            self.pause_offset = time.time() - self.start_time

    def resume(self):
        if self.is_paused:
            self.is_paused = False
            self.start_time = time.time() - self.pause_offset
            self.pause_offset = -1


class QueueState(BaseModel):
    song_file_list: list = []
    current_position: int = -1
    playback_state: PlaybackState | None = None

    def current_song(self):
        if self.has_current_song():
            return self.song_file_list[self.current_position]
        return None

    def has_current_song(self):
        if not self.song_file_list:
            return False
        if self.current_position == -1:
            return False
        if self.current_position >= len(self.song_file_list):
            return False
        return True

    def get_current_metadata(self):
        if not self.has_current_song():
            print("cannot request metadata when no current song")
            return None
        song = self.song_file_list[self.current_position]
        start_time = self.playback_state.start_time if self.playback_state else 0
        return (
            song.filename,
            song.duration,
            start_time,
        )

    def move_to_last_song_in_queue(self):
        self.current_position = len(self.song_file_list) - 1

    def set_queue_position(self, position: int):
        self.current_position = position

    def reset(self):
        self.song_file_list = []
        self.current_position = -1
        self.playback_state = PlaybackState()


queue_state: QueueState | None = None


def get_queue_state() -> QueueState:
    global queue_state
    if queue_state is None:
        queue_state = QueueState()
    return queue_state


def add_url_to_queue(url: str):
    filename, duration = download_url(url)
    song = SongItem(filename=filename, duration=duration)
    get_queue_state().song_file_list.append(song)


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
            get_queue_state().song_file_list.append(song)
            return True
    except Exception as e:
        print(f"Failed to add song from metadata {json_path}: {e}")
        return False


def handle_song_end():
    queue = get_queue_state()
    print(
        "handling song end ",
        queue.current_position,
        len(queue.song_file_list),
    )
    if queue.current_position == -1:
        return
    if queue.current_position == (len(queue.song_file_list) - 1):
        print("last song ended, resetting position to start and pausing")
        queue.current_position = 0
        pause_song()
        return
    print("song ended, moving to next song")
    queue.current_position += 1


def get_queue_status():
    is_paused = get_is_paused_from_voice_client()
    return SongQueueStatus(
        song_file_list=get_queue_state().song_file_list,
        position=get_queue_state().current_position,
        is_paused=is_paused,
    )


def set_queue_position(position: int):
    get_queue_state().set_queue_position(position)


def after_playing(error):
    if error:
        print(f"Error during playback: {error}")
    queue = get_queue_state()
    metadata = queue.get_current_metadata()
    if not metadata:
        print("No current metadata available.")
        return
    fileName, duration, start_time = metadata
    print(f"Finished playing {fileName}")

    metadata = queue.get_current_metadata()
    if not metadata:
        print("No current metadata available.")
        return
    fileName, duration, start_time = metadata
    current_playing_time = time.time() - start_time

    if current_playing_time > (duration - 1):
        # song ended
        handle_song_end()
        if queue.has_current_song():
            print("start next song")
            play_current_song()
        else:
            print("end of queue")
    else:
        print("not changing song because it is still playing")


def change_playback_position(position: int):
    queue = get_queue_state()
    metadata = queue.get_current_metadata()
    if not metadata:
        print("No current metadata available.")
        return None
    fileName, duration, start_time = metadata
    voice_client = get_voice_client()
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        audio = discord.FFmpegPCMAudio(
            source=fileName, before_options=f"-ss {position}"
        )
        voice_client.play(audio, after=after_playing)
        if queue.playback_state:
            queue.playback_state.start_time = time.time() - position
        return {"status": "Playback position changed"}
    else:
        print("cannot change position, no song playing")
        return None


def play_current_song():
    queue = get_queue_state()
    if queue.has_current_song():
        metadata = queue.get_current_metadata()
        if not metadata:
            print("No current metadata available.")
            return
        fileName, duration, start_time = metadata
        if queue.playback_state:
            queue.playback_state.start_time = time.time()
        voice_client = get_voice_client()
        if voice_client:
            voice_client.play(
                discord.FFmpegPCMAudio(source=fileName), after=after_playing
            )
        else:
            print("No voice client available to play audio.")
    else:
        print(f"cannot play current song when not selected")


def get_status():
    voice_client = get_voice_client()
    if voice_client and voice_client.is_playing():
        return BotStatus.PLAYING
    return BotStatus.IDLE


def get_playback_info():
    queue = get_queue_state()
    metadata = queue.get_current_metadata()
    if not metadata:
        return None
    fileName, duration, start_time = metadata
    voice_client = get_voice_client()
    if queue.playback_state:
        if queue.playback_state.is_paused and queue.playback_state.pause_offset > 0:
            elapsed_time = queue.playback_state.pause_offset
        else:
            elapsed_time = time.time() - start_time
    else:
        elapsed_time = 0
    if voice_client and voice_client.is_playing():
        return PlaybackInformation(
            file_name=fileName,
            current_position=elapsed_time,
            duration=duration,
        )
    else:
        return None


def handle_new_song_on_queue():
    if not get_queue_state().has_current_song():
        get_queue_state().move_to_last_song_in_queue()
        if get_queue_state().has_current_song():
            play_current_song()
            print("started playing current song")
        else:
            print("moving to the last song did not put us on a current song")
    else:
        print("not moving to new song because there is current song")


def pause_song():
    queue = get_queue_state()
    voice_client = get_voice_client()
    if voice_client and voice_client.is_playing():
        if queue.has_current_song() and queue.playback_state is not None:
            metadata = queue.get_current_metadata()
            if not metadata:
                print("No current metadata available.")
                return
            fileName, duration, start_time = metadata
            queue.playback_state.pause()
            voice_client.pause()


def unpause_song():
    queue = get_queue_state()
    voice_client = get_voice_client()
    if voice_client and voice_client.is_playing():
        if queue.playback_state is not None:
            queue.playback_state.resume()
        voice_client.resume()
    else:
        if queue.has_current_song() and queue.playback_state is not None:
            metadata = queue.get_current_metadata()
            if not metadata:
                print("No current metadata available.")
                return
            fileName, duration, start_time = metadata
            seek_time = queue.playback_state.pause_offset if queue.playback_state.pause_offset > 0 else (time.time() - start_time)
            audio = discord.FFmpegPCMAudio(
                source=fileName, before_options=f"-ss {seek_time}"
            )
            if voice_client:
                voice_client.play(audio, after=after_playing)
                queue.playback_state.start_time = time.time() - seek_time
                queue.playback_state.pause_offset = -1
                print(f"Resumed playback from {seek_time}s for {fileName}")
            else:
                print("No voice client available to play audio.")
        else:
            print("cannot unpause song, no song playing")
