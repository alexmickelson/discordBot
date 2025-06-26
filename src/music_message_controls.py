from src.models import BotResponse, BotStatus, MessageType
from src.my_voice_client import get_voice_client
from src.playback_service import (
    change_playback_position,
    get_playback_info,
    get_status,
    handle_new_song_on_queue,
    play_current_song,
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

    def get_playback_info(self):
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

    def get_all_songs(self):
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

    async def ws_message(self, data):
        if "action" not in data:
            return BotResponse(
                message_type=MessageType.ERROR,
                status=get_status(),
                error="Invalid request, action is required",
            )
        action = data["action"]
        
        if action == "seek_to_position":
            return self.seek_to_position(data)
        elif action == "play_song_by_index":
            return self.play_song_by_index(data)
        elif action == "get_playback_info":
            return self.get_playback_info()
        elif action == "get_all_songs":
            return self.get_all_songs()
        elif action == "add_song_to_queue":
            return self.add_song_to_queue(data)
        else:
            return BotResponse(
                message_type=MessageType.ERROR,
                status=get_status(),
                error=f"Unknown action: {action}",
            )
