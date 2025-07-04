from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class BotStatus(str, Enum):
    PLAYING = "Playing"
    IDLE = "Idle"


class MessageType(str, Enum):
    PLAYBACK_INFORMATION = "PLAYBACK_INFORMATION"
    ERROR = "ERROR"
    MESSAGE = "MESSAGE"
    ALL_SONGS_LIST = "ALL_SONGS_LIST"
    ADD_SONG_TO_QUEUE = "ADD_SONG_TO_QUEUE"  # new action


class SongItem(BaseModel):
    filename: str
    duration: int


class SongMetadata(BaseModel):
    filename: str
    duration: int
    url: str
    thumbnail: str


class SongQueueStatus(BaseModel):
    song_file_list: list[SongItem]
    position: int
    is_paused: bool


class PlaybackInformation(BaseModel):
    file_name: str
    current_position: float
    duration: float


class BotResponse(BaseModel):
    message_type: MessageType
    status: BotStatus
    error: Optional[str] = None
    message: Optional[str] = None
    playback_information: Optional[PlaybackInformation] = None
    song_queue: Optional[SongQueueStatus] = None
    all_songs_list: Optional[List[SongMetadata]] = None
