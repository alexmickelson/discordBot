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
    def seek_to_position(self, position: int) -> BotResponse:
        result = get_queue_state().change_playback_position(position)
        if result:
            return BotResponse(
                message_type=MessageType.MESSAGE,
                status=get_queue_state().get_status(),
                message="position changed",
            )
        else:
            return BotResponse(
                message_type=MessageType.ERROR,
                status=get_queue_state().get_status(),
                error="unable to change position",
            )

    def play_song_by_index(self, position: int) -> BotResponse:
        get_queue_state().set_queue_position(position)
        stop_playback()
        get_queue_state().play_current_song()
        info = get_queue_state().get_playback_info()
        return BotResponse(
            message_type=MessageType.PLAYBACK_INFORMATION,
            status=BotStatus.PLAYING if info else BotStatus.IDLE,
            playback_information=info,
            song_queue=get_queue_state().get_queue_status(),
        )

    def get_playback_info(self) -> BotResponse:
        status = get_queue_state().get_queue_status()
        all_songs = get_all_songs()
        info = get_queue_state().get_playback_info()
        if not info:
            return BotResponse(
                message_type=MessageType.PLAYBACK_INFORMATION,
                status=BotStatus.IDLE,
                playback_information=None,
                song_queue=status,
                all_songs_list=all_songs,
            )
        else:
            return BotResponse(
                message_type=MessageType.PLAYBACK_INFORMATION,
                status=BotStatus.PLAYING,
                playback_information=info,
                song_queue=status,
                all_songs_list=all_songs,
            )

    def get_all_songs(self) -> BotResponse:
        all_songs_list = get_all_songs()
        print("all_songs_list", all_songs_list)
        return BotResponse(
            message_type=MessageType.ALL_SONGS_LIST,
            status=get_queue_state().get_status(),
            message=None,
            playback_information=None,
            song_queue=get_queue_state().get_queue_status(),
            error=None,
            all_songs_list=all_songs_list,
        )

    def add_song_to_queue(self, filename: str) -> BotResponse:
        success = get_queue_state().add_existing_song_to_queue(filename)
        get_queue_state().handle_new_song_on_queue()
        all_songs = get_all_songs()
        if success:
            return BotResponse(
                message_type=MessageType.ADD_SONG_TO_QUEUE,
                status=get_queue_state().get_status(),
                message="Song added to queue",
                song_queue=get_queue_state().get_queue_status(),
                all_songs_list=all_songs,
            )
        else:
            return BotResponse(
                message_type=MessageType.ERROR,
                status=get_queue_state().get_status(),
                error="Failed to add song to queue",
            )

    def pause_song(self) -> BotResponse:
        get_queue_state().pause_song()
        return BotResponse(
            message_type=MessageType.PLAYBACK_INFORMATION,
            status=get_queue_state().get_status(),
            playback_information=get_queue_state().get_playback_info(),
            song_queue=get_queue_state().get_queue_status(),
        )

    def unpause_song(self) -> BotResponse:
        get_queue_state().unpause_song()
        return BotResponse(
            message_type=MessageType.PLAYBACK_INFORMATION,
            status=get_queue_state().get_status(),
            playback_information=get_queue_state().get_playback_info(),
            song_queue=get_queue_state().get_queue_status(),
        )

    def add_to_queue(self, url: str) -> BotResponse:
        print("request to add to queue with url", url)
        downloadable_url = extract_downloadable_url(url)
        if not downloadable_url:
            return BotResponse(
                message_type=MessageType.ERROR,
                status=get_queue_state().get_status(),
                error="URL must contain a 'v' query parameter, e.g. https://youtube.com/watch?v=VIDEO_ID",
            )
        print("parsed url to be", downloadable_url)
        get_queue_state().add_url_to_queue(downloadable_url)
        return BotResponse(
            message_type=MessageType.ADD_SONG_TO_QUEUE,
            status=get_queue_state().get_status(),
            message="Song added to queue from URL",
            song_queue=get_queue_state().get_queue_status(),
        )

    def get_queue_status(self):
        status = get_queue_state().get_queue_status()
        return BotResponse(
            message_type=MessageType.PLAYBACK_INFORMATION,
            status=get_queue_state().get_status(),
            song_queue=status,
            playback_information=get_queue_state().get_playback_info(),
        )


controls: MusicControls | None = None


def get_music_controls() -> MusicControls:
    global controls
    if controls is None:
        controls = MusicControls()
    return controls
