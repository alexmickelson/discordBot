import { FC, ReactNode, useState, useEffect } from "react";
import {
  BotResponse,
} from "../models";
import { useWebSocketConnection } from "./useWebSocket";
import { MusicWebSocketContext } from "./useMusicWebSocketContexts";
import { useQueryClient } from "@tanstack/react-query";
import { playbackKeys } from "../features/playbackHooks";

export const MusicWebSocketProvider: FC<{ children: ReactNode }> = ({
  children,
}) => {
  const queryClient = useQueryClient();
  const { ws } = useWebSocketConnection();
  const [error, setError] = useState<string>("");
  const [message, setMessage] = useState("");
  const [botStatus, setBotStatus] = useState<string | undefined>();

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

      if (
        response.message_type === "PLAYBACK_INFORMATION" &&
        response.song_queue &&
        response.playback_information
      ) {
        queryClient.setQueryData(
          playbackKeys.playbackInfo,
          response.playback_information
        );
        queryClient.setQueryData(playbackKeys.songQueue, response.song_queue);
      }
      
      if (
        response.message_type === "ALL_SONGS_LIST" &&
        response.all_songs_list
      ) {
        queryClient.setQueryData(
          playbackKeys.allSongs,
          response.all_songs_list
        );
      }
    };
    ws.onerror = () => setError("WebSocket error occurred.");
    ws.onclose = () => {};
  }, [queryClient, ws]);

  return (
    <MusicWebSocketContext.Provider
      value={{
        error,
        message,
        botStatus,
      }}
    >
      {children}
    </MusicWebSocketContext.Provider>
  );
};
