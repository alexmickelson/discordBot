from src.models import BotResponse, BotStatus, MessageType
from src.my_voice_client import get_voice_client
from src.playback_service import (
    change_playback_position,
    get_playback_info,
    get_status,
    handle_new_song_on_queue,
    play_current_song,
    pause_song,  # add import
    unpause_song,  # add import
)
from src.song_queue import (
    add_existing_song_to_queue,
    get_all_songs,
    get_queue_status,
    has_current_song,
    set_queue_position,
)


class MusicMessageControls:

    def seek_to_position(self, data):
        if "position" not in data:
            return BotResponse(
                message_type=MessageType.ERROR,
                status=get_status(),
                error="Invalid request, position is required",
            )
        result = change_playback_position(data["position"])
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

    def play_song_by_index(self, data):
        if "position" not in data:
            return BotResponse(
                message_type=MessageType.ERROR,
                status=get_status(),
                error="Invalid request, position is required",
            )
        set_queue_position(data["position"])
        get_voice_client().stop()
        play_current_song()
        info = get_playback_info()
        return BotResponse(
            message_type=MessageType.PLAYBACK_INFORMATION,
            status=BotStatus.PLAYING if info else BotStatus.IDLE,
            playback_information=info,
            song_queue=get_queue_status(),
        )

    def get_playback_info(self, data):
        status = get_queue_status()
        if not has_current_song():
            return BotResponse(
                message_type=MessageType.PLAYBACK_INFORMATION,
                status=BotStatus.IDLE,
                playback_information=None,
                song_queue=status,
            )
        else:
            info = get_playback_info()
            return BotResponse(
                message_type=MessageType.PLAYBACK_INFORMATION,
                status=BotStatus.PLAYING if info else BotStatus.IDLE,
                playback_information=info,
                song_queue=status,
            )

    def get_all_songs(self, data):
        all_songs_list = get_all_songs()
        print("all_songs_list", all_songs_list)
        return BotResponse(
            message_type=MessageType.ALL_SONGS_LIST,
            status=get_status(),
            message=None,
            playback_information=None,
            song_queue=None,
            error=None,
            all_songs_list=all_songs_list,
        )

    def add_song_to_queue(self, data):
        if "filename" not in data:
            return BotResponse(
                message_type=MessageType.ERROR,
                status=get_status(),
                error="Invalid request, filename is required",
            )
        filename = data["filename"]
        success = add_existing_song_to_queue(filename)
        handle_new_song_on_queue()
        if success:
            return BotResponse(
                message_type=MessageType.ADD_SONG_TO_QUEUE,
                status=get_status(),
                message="Song added to queue",
                song_queue=get_queue_status(),
            )
        else:
            return BotResponse(
                message_type=MessageType.ERROR,
                status=get_status(),
                error="Failed to add song to queue",
            )

    def pause_song(self, data):
        pause_song()
        return BotResponse(
            message_type=MessageType.PLAYBACK_INFORMATION,
            status=get_status(),
            playback_information=get_playback_info(),
            song_queue=get_queue_status(),
        )

    def unpause_song(self, data):
        unpause_song()
        return BotResponse(
            message_type=MessageType.PLAYBACK_INFORMATION,
            status=get_status(),
            playback_information=get_playback_info(),
            song_queue=get_queue_status(),
        )

    async def ws_message(self, data):
        if "action" not in data:
            return BotResponse(
                message_type=MessageType.ERROR,
                status=get_status(),
                error="Invalid request, action is required",
            )

        # Dynamically call method based on action
        method = getattr(self, data["action"], None)
        if callable(method):
            return method(data)
        else:
            return BotResponse(
                message_type=MessageType.ERROR,
                status=get_status(),
                error=f"Unknown action: {data["action"]}",
            )
