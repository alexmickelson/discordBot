import { createContext, useContext } from "react";
import { PlaybackInfoData, SongQueue, SongMetadata } from "../models";

interface WebSocketContextType {
  ws: WebSocket | undefined;
  error: string;
  message: string;
  botStatus: string | undefined;
  playbackInfo: PlaybackInfoData | undefined;
  songQueue: SongQueue | undefined;
  sendMessage: (message: unknown) => void;
  allSongsList: SongMetadata[];
}

export const WebSocketContext = createContext<WebSocketContextType | undefined>(
  undefined
);

export const useWebSocket = () => {
  const context = useContext(WebSocketContext);
  if (!context) {
    throw new Error("useWebSocket must be used within a WebSocketProvider");
  }
  return context;
};
