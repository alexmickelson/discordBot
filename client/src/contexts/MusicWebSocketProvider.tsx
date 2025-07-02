import { FC, ReactNode, useEffect } from "react";
import { BotResponse } from "../models";
import { useWebSocketConnection } from "./useWebSocket";
import { MusicWebSocketContext } from "./useMusicWebSocketContexts";
import { useQueryClient } from "@tanstack/react-query";
import { playbackKeys } from "../features/playbackHooks";

export const MusicWebSocketProvider: FC<{ children: ReactNode }> = ({
  children,
}) => {
  const queryClient = useQueryClient();
  const { ws } = useWebSocketConnection();

  useEffect(() => {
    if (!ws) return;
    ws.onopen = () => {};
    ws.onmessage = (event) => {
      const response: BotResponse = JSON.parse(event.data);

      if (
        response.song_queue &&
        response.playback_information &&
        response.all_songs_list
      ) {
        queryClient.setQueryData(
          playbackKeys.playbackInfo,
          response.playback_information
        );
        queryClient.setQueryData(playbackKeys.songQueue, response.song_queue);
        queryClient.setQueryData(
          playbackKeys.allSongs,
          response.all_songs_list
        );
      }
    };
    ws.onclose = () => {};
  }, [queryClient, ws]);

  return (
    <MusicWebSocketContext.Provider value={{}}>
      {children}
    </MusicWebSocketContext.Provider>
  );
};
