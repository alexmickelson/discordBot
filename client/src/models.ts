export enum BotStatus {
  PLAYING = "Playing",
  Idle = "Idle",
}

export interface PlaybackInfoData {
  file_name: string;
  current_position: number;
  duration: number;
}

export interface SongQueue {
  song_file_list: {
    filename: string;
    duration: number;
  }[];
  position: number;
}

export interface SongMetadata {
  filename: string;
  duration: number;
  url: string;
}

export interface BotResponse {
  message_type: "PLAYBACK_INFORMATION" | "ERROR" | "MESSAGE" | "ALL_SONGS_LIST";
  status: BotStatus;
  error?: string;
  message?: string;
  playback_information?: PlaybackInfoData;
  song_queue?: SongQueue;
  all_songs_list?: SongMetadata[];
}
