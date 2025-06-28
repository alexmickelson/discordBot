import inspect
from src.models import BotResponse, BotStatus, MessageType

from typing import Any, Dict
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from src.music.my_voice_client import stop_playback
from src.music.song_queue import (
    add_existing_song_to_queue,
    add_to_queue,
    change_playback_position,
    get_all_songs,
    get_playback_info,
    get_queue_status,
    get_status,
    handle_new_song_on_queue,
    has_current_song,
    pause_song,
    play_current_song,
    set_queue_position,
    unpause_song,
)


class MusicControls:
    def seek_to_position(self, position: int) -> BotResponse:
        result = change_playback_position(position)
        if result:
            return BotResponse(
                message_type=MessageType.MESSAGE,
                status=get_status(),
                message="position changed",
            )
        else:
            return BotResponse(
                message_type=MessageType.ERROR,
                status=get_status(),
                error="unable to change position",
            )

    def play_song_by_index(self, position: int) -> BotResponse:
        set_queue_position(position)
        stop_playback()
        play_current_song()
        info = get_playback_info()
        return BotResponse(
            message_type=MessageType.PLAYBACK_INFORMATION,
            status=BotStatus.PLAYING if info else BotStatus.IDLE,
            playback_information=info,
            song_queue=get_queue_status(),
        )

    def get_playback_info(self) -> BotResponse:
        status = get_queue_status()
        all_songs = get_all_songs()
        if not has_current_song():
            return BotResponse(
                message_type=MessageType.PLAYBACK_INFORMATION,
                status=BotStatus.IDLE,
                playback_information=None,
                song_queue=status,
                all_songs_list=all_songs,
            )
        else:
            info = get_playback_info()
            return BotResponse(
                message_type=MessageType.PLAYBACK_INFORMATION,
                status=BotStatus.PLAYING if info else BotStatus.IDLE,
                playback_information=info,
                song_queue=status,
                all_songs_list=all_songs,
            )

    def get_all_songs(self) -> BotResponse:
        all_songs_list = get_all_songs()
        print("all_songs_list", all_songs_list)
        return BotResponse(
            message_type=MessageType.ALL_SONGS_LIST,
            status=get_status(),  # Added required status field
            message=None,
            playback_information=None,
            song_queue=get_queue_status(),
            error=None,
            all_songs_list=all_songs_list,
        )

    def add_song_to_queue(self, filename: str) -> BotResponse:
        success = add_existing_song_to_queue(filename)
        handle_new_song_on_queue()
        all_songs = get_all_songs()
        if success:
            return BotResponse(
                message_type=MessageType.ADD_SONG_TO_QUEUE,
                status=get_status(),
                message="Song added to queue",
                song_queue=get_queue_status(),
                all_songs_list=all_songs,
            )
        else:
            return BotResponse(
                message_type=MessageType.ERROR,
                status=get_status(),
                error="Failed to add song to queue",
            )

    def pause_song(self) -> BotResponse:
        pause_song()
        return BotResponse(
            message_type=MessageType.PLAYBACK_INFORMATION,
            status=get_status(),
            playback_information=get_playback_info(),
            song_queue=get_queue_status(),
        )

    def unpause_song(self) -> BotResponse:
        unpause_song()
        return BotResponse(
            message_type=MessageType.PLAYBACK_INFORMATION,
            status=get_status(),
            playback_information=get_playback_info(),
            song_queue=get_queue_status(),
        )

    def add_to_queue(self, url: str) -> BotResponse:
        print("request to add to queue with url", url)
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        v_param = qs.get("v")
        if not v_param:
            return BotResponse(
                message_type=MessageType.ERROR,
                status=get_status(),
                error="URL must contain a 'v' query parameter, e.g. https://youtube.com/watch?v=VIDEO_ID",
            )
        new_query = urlencode({"v": v_param[0]})
        updated = urlunparse(parsed._replace(query=new_query))
        print("parsed url to be", updated)
        add_to_queue(updated)
        return BotResponse(
            message_type=MessageType.ADD_SONG_TO_QUEUE,
            status=get_status(),
            message="Song added to queue from URL",
            song_queue=get_queue_status(),
        )
