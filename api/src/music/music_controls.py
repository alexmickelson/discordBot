import inspect
from src.models import BotResponse, BotStatus, MessageType

from typing import Any, Dict
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from src.music.my_voice_client import stop_playback
from src.music.song_queue import get_queue_state, get_all_songs


def extract_downloadable_url(url: str) -> str | None:
    """
    Extract a YouTube URL with only the 'v' query parameter, or return None if not present.
    """
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    v_param = qs.get("v")
    if not v_param:
        return None
    new_query = urlencode({"v": v_param[0]})
    return urlunparse(parsed._replace(query=new_query))


class MusicControls:
    def seek_to_position(self, position: int):
        return get_queue_state().change_playback_position(position)

    def play_song_by_index(self, position: int):
        get_queue_state().set_queue_position(position)
        stop_playback()
        get_queue_state().play_current_song()
        return get_queue_state().get_playback_info()

    def get_playback_info(self):
        return get_queue_state().get_playback_info()

    def get_all_songs(self):
        return get_all_songs()

    def add_song_to_queue(self, filename: str):
        success = get_queue_state().add_existing_song_to_queue(filename)
        get_queue_state().handle_new_song_on_queue()
        return success

    def pause_song(self):
        get_queue_state().pause_song()
        return get_queue_state().get_playback_info()

    def unpause_song(self):
        get_queue_state().unpause_song()
        return get_queue_state().get_playback_info()

    def add_to_queue(self, url: str):
        print("request to add to queue with url", url)
        downloadable_url = extract_downloadable_url(url)
        if not downloadable_url:
            return None
        print("parsed url to be", downloadable_url)
        get_queue_state().add_url_to_queue(downloadable_url)
        return get_queue_state().get_playback_info()

    def get_queue_status(self):
        return get_queue_state().get_queue_status()


controls: MusicControls | None = None


def get_music_controls() -> MusicControls:
    global controls
    if controls is None:
        controls = MusicControls()
    return controls
