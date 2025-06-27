import { FC, ReactNode, useState, useEffect } from "react";
import {
  PlaybackInfoData,
  SongQueue,
  SongMetadata,
  BotResponse,
} from "../models";
import { useWebSocketConnection } from "./useWebSocket";
import { MusicWebSocketContext } from "./useMusicWebSocketContexts";

// MusicWebSocketProvider: manages music messaging state and logic

export const MusicWebSocketProvider: FC<{ children: ReactNode }> = ({
  children,
}) => {
  const { ws } = useWebSocketConnection();
  const [playbackInfo, setPlaybackInfo] = useState<
    PlaybackInfoData | undefined
  >();
  const [songQueue, setSongQueue] = useState<SongQueue | undefined>();
  const [error, setError] = useState<string>("");
  const [message, setMessage] = useState("");
  const [botStatus, setBotStatus] = useState<string | undefined>();
  const [allSongsList, setAllSongsList] = useState<SongMetadata[]>([]);

  useEffect(() => {
    if (!ws) return;
    ws.onopen = () => {
      ws.send(JSON.stringify({ action: "get_playback_info" }));
      ws.send(JSON.stringify({ action: "get_all_songs" }));
    };
    ws.onmessage = (event) => {
      const response: BotResponse = JSON.parse(event.data);
      setBotStatus(response.status);
      if (response.message_type === "ERROR") setError(response.error ?? "");
      if (response.message_type === "MESSAGE")
        setMessage(response.message ?? "");
      if (response.message_type === "PLAYBACK_INFORMATION") {
        setPlaybackInfo(response.playback_information);
        setSongQueue(response.song_queue);
      }
      if (response.message_type === "ALL_SONGS_LIST") {
        setAllSongsList(response.all_songs_list ?? []);
      }
    };
    ws.onerror = () => setError("WebSocket error occurred.");
    ws.onclose = () => {};
    // No cleanup here; connection is managed by WebSocketConnectionProvider
  }, [ws]);

  const sendMessage = (message: unknown) => {
    if (ws) ws.send(JSON.stringify(message));
  };

  return (
    <MusicWebSocketContext.Provider
      value={{
        error,
        message,
        botStatus,
        playbackInfo,
        songQueue,
        sendMessage,
        allSongsList,
      }}
    >
      {children}
    </MusicWebSocketContext.Provider>
  );
};
